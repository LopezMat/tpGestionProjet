"""T-011 : schéma, salles et démarrage tolérant, sur un vrai PostgreSQL 16 (jamais SQLite).

Les tests d'intégration sont ignorés sans TEST_DATABASE_URL (voir README) ; ils créent
et suppriment un schéma de base jetable et n'utilisent que la base de test.
"""

import logging
import os

import pytest
from alembic import command
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

from reservation import demarrer, migrer

URL_TEST = os.environ.get("TEST_DATABASE_URL")
integration = pytest.mark.skipif(not URL_TEST, reason="TEST_DATABASE_URL non renseignée")


def _vider(moteur):
    with moteur.begin() as c:
        c.execute(text("DROP SCHEMA public CASCADE"))
        c.execute(text("CREATE SCHEMA public"))


@pytest.fixture
def base(monkeypatch):
    from reservation import config
    url = config.convertir_url_base(URL_TEST)
    monkeypatch.setenv("DATABASE_URL", URL_TEST)
    moteur = create_engine(url)
    _vider(moteur)
    yield moteur
    _vider(moteur)
    moteur.dispose()


@pytest.fixture
def migree(base):
    assert migrer.appliquer() is True
    return base


def _exec(moteur, sql, **p):
    with moteur.begin() as c:
        return c.execute(text(sql), p)


def _utilisateur(moteur, email="a@b.fr"):
    return _exec(moteur, "INSERT INTO utilisateur (nom,email,mot_de_passe_hash,role) "
                 "VALUES ('A',:e,'h','membre') RETURNING id", e=email).scalar()


@integration
def test_tables_et_colonnes(migree):
    cols = {}
    with migree.connect() as c:
        for t, col in c.execute(text(
                "SELECT table_name, column_name FROM information_schema.columns "
                "WHERE table_schema='public'")):
            cols.setdefault(t, set()).add(col)
    assert cols["utilisateur"] >= {"id", "nom", "email", "mot_de_passe_hash", "role",
                                   "doit_changer_mdp", "cree_le", "mdp_change_le"}
    assert cols["salle"] >= {"id", "nom", "capacite", "equipements", "ordre"}
    assert cols["reservation"] >= {"id", "salle_id", "utilisateur_id", "date_creneau",
                                   "heure_debut", "cree_le"}
    assert cols["session"] >= {"jeton_hash", "utilisateur_id", "cree_le",
                               "derniere_activite", "expire_le"}


@integration
def test_email_unique_et_role_controle(migree):
    _utilisateur(migree)
    with pytest.raises(IntegrityError):
        _utilisateur(migree)
    with pytest.raises(IntegrityError):
        _exec(migree, "INSERT INTO utilisateur (nom,email,mot_de_passe_hash,role) "
              "VALUES ('A','x@y.fr','h','admin')")


@integration
def test_contraintes_de_reservation(migree):
    u = _utilisateur(migree)
    ins = ("INSERT INTO reservation (salle_id,utilisateur_id,date_creneau,heure_debut) "
           "VALUES (1,:u,:d,:h)")
    _exec(migree, ins, u=u, d="2026-12-01", h=8)          # mardi
    _exec(migree, ins, u=u, d="2026-12-01", h=19)
    with pytest.raises(IntegrityError):                   # doublon de créneau
        _exec(migree, ins, u=u, d="2026-12-01", h=8)
    for h in (7, 20):
        with pytest.raises(IntegrityError):
            _exec(migree, ins, u=u, d="2026-12-02", h=h)
    for d in ("2026-12-05", "2026-12-06"):                # samedi, dimanche
        with pytest.raises(IntegrityError):
            _exec(migree, ins, u=u, d=d, h=9)
    _exec(migree, ins, u=u, d="2026-12-04", h=9)          # vendredi


@integration
def test_suppression_utilisateur_en_cascade(migree):
    u = _utilisateur(migree)
    _exec(migree, "INSERT INTO reservation (salle_id,utilisateur_id,date_creneau,heure_debut)"
          " VALUES (1,:u,'2026-12-01',9)", u=u)
    _exec(migree, "INSERT INTO session (jeton_hash,utilisateur_id,expire_le) "
          "VALUES (:j,:u,now())", j=b"\x01" * 32, u=u)
    _exec(migree, "DELETE FROM utilisateur WHERE id=:u", u=u)
    assert _exec(migree, "SELECT count(*) FROM reservation").scalar() == 0
    assert _exec(migree, "SELECT count(*) FROM session").scalar() == 0


@integration
def test_index_attendus(migree):
    defs = " ".join(r[0] for r in _exec(
        migree, "SELECT indexdef FROM pg_indexes WHERE schemaname='public' "
        "AND tablename='reservation'"))
    assert "(utilisateur_id, date_creneau)" in defs
    assert "(date_creneau)" in defs


@integration
def test_trois_salles_sur_base_vide_sans_compte(base):
    """DEC-011 : `alembic upgrade head` seul suffit, sans compte ni script ; sans doublon."""
    migrer.appliquer()
    migrer.appliquer()  # relance : aucun doublon
    noms = [r[0] for r in _exec(base, "SELECT nom FROM salle ORDER BY ordre")]
    assert noms == ["Salle 1", "Salle 2", "Salle 3"]
    assert _exec(base, "SELECT count(*) FROM utilisateur").scalar() == 0
    assert _exec(base, "SELECT count(*) FROM reservation").scalar() == 0


@integration
def test_upgrade_head_direct_donne_les_salles(base):
    command.upgrade(migrer._configuration(migrer.config.url_base()), "head")
    assert _exec(base, "SELECT count(*) FROM salle").scalar() == 3


@integration
def test_migrer_est_appele_au_demarrage_et_applique_la_tete(base, monkeypatch):
    monkeypatch.setattr(demarrer, "attendre_base", lambda: True)
    monkeypatch.setattr(demarrer.uvicorn, "run", lambda *a, **kw: None)
    assert demarrer.main() == 0
    assert _exec(base, "SELECT count(*) FROM salle").scalar() == 3


@integration
def test_base_en_avance_avertit_et_ne_migre_pas(base, caplog):
    _exec(base, "CREATE TABLE alembic_version (version_num varchar(32) PRIMARY KEY)")
    _exec(base, "INSERT INTO alembic_version VALUES ('9999_future')")
    with caplog.at_level(logging.WARNING, logger="reservation.migrer"):
        assert migrer.appliquer() is False
    assert "plus récente" in caplog.text
    assert _exec(base, "SELECT to_regclass('public.salle')").scalar() is None
    assert _exec(base, "SELECT version_num FROM alembic_version").scalar() == "9999_future"


@integration
def test_demarrage_avec_base_en_avance_demarre(base, monkeypatch):
    _exec(base, "CREATE TABLE alembic_version (version_num varchar(32) PRIMARY KEY)")
    _exec(base, "INSERT INTO alembic_version VALUES ('9999_future')")
    monkeypatch.setattr(demarrer, "attendre_base", lambda: True)
    monkeypatch.setattr(demarrer.uvicorn, "run", lambda *a, **kw: None)
    assert demarrer.main() == 0


# --- Sans base : politique « additive uniquement » ---------------------------------------

def test_aucune_migration_descendante():
    from reservation.migrer import DOSSIER
    for fichier in (DOSSIER / "versions").glob("*.py"):
        assert "def downgrade" not in fichier.read_text(encoding="utf-8"), fichier.name
        assert "drop_" not in fichier.read_text(encoding="utf-8"), fichier.name


def test_demarrage_n_appelle_que_upgrade_head():
    import inspect
    source = inspect.getsource(migrer.appliquer)
    assert 'command.upgrade(cfg, "head")' in source
    assert "downgrade" not in source


def test_echec_de_migration_arrete_le_demarrage_sans_fuite(monkeypatch, caplog):
    def echec():
        raise RuntimeError("postgresql://esn:SECRET@db/app")
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@db/app")
    monkeypatch.setattr(demarrer, "attendre_base", lambda: True)
    monkeypatch.setattr(demarrer.migrer, "appliquer", echec)
    assert demarrer.main() == 1
    assert "SECRET" not in caplog.text


def test_moteurs_distincts():
    from reservation import bdd
    assert bdd._moteur_sonde is not bdd.moteur_applicatif
    assert not hasattr(bdd, "_moteur")


@integration
def test_moteur_applicatif_a_un_pool_et_sert_les_requetes(migree):
    from reservation import bdd
    bdd.moteur_applicatif.cache_clear()
    moteur = bdd.moteur_applicatif()
    assert moteur.pool.__class__.__name__ == "QueuePool"
    with moteur.connect() as c:
        assert c.execute(text("SELECT count(*) FROM salle")).scalar() == 3
    bdd.moteur_applicatif.cache_clear()
