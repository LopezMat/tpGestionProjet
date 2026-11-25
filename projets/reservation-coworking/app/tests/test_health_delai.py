"""Critère 1 de T-010 et T-056 : /health répond 503 en environ 1 s quand la base se tait.

Trois façons de se taire sont simulées sans Docker, avec une fausse base locale :
- elle accepte la connexion TCP et n'envoie rien (base gelée, coupure réseau) ;
- elle termine la connexion (handshake) puis ne répond jamais aux requêtes (connexion
  déjà ouverte, gelée ensuite) ;
- le nom de la base n'est plus résolu (conteneur arrêté).
Le contrôle doit aussi laisser la boucle d'événements libre.
"""

import asyncio
import socket
import struct
import threading
import time

import httpx
import pytest
from fastapi.testclient import TestClient

from reservation import bdd
from reservation.app import creer_app

LIMITE_S = 2.0  # exigence T-056 ; la borne de conception est bdd.DELAI_BASE_S (1 s)


class FausseBase:
    """Serveur TCP local qui n'implémente que ce qu'il faut du protocole PostgreSQL."""

    def __init__(self, handshake: bool):
        self.handshake = handshake
        self._ecoute = socket.socket()
        self._ecoute.bind(("127.0.0.1", 0))
        self._ecoute.listen(16)
        self._connexions: list[socket.socket] = []
        self._ferme = False
        self.port = self._ecoute.getsockname()[1]
        threading.Thread(target=self._boucle, daemon=True).start()

    def _boucle(self):
        while not self._ferme:
            try:
                connexion, _ = self._ecoute.accept()
            except OSError:
                return
            self._connexions.append(connexion)
            if self.handshake:
                threading.Thread(target=self._servir, args=(connexion,), daemon=True).start()
            # sinon : on garde la connexion ouverte sans jamais rien lire ni écrire

    @staticmethod
    def _lire(connexion: socket.socket, n: int) -> bytes:
        tampon = b""
        while len(tampon) < n:
            morceau = connexion.recv(n - len(tampon))
            if not morceau:
                raise OSError("fermé")
            tampon += morceau
        return tampon

    def _servir(self, connexion: socket.socket):
        try:
            while True:  # SSLRequest / GSSENCRequest : refusés ; puis StartupMessage
                longueur, code = struct.unpack("!ii", self._lire(connexion, 8))
                if code in (80877103, 80877104):
                    connexion.sendall(b"N")
                    continue
                self._lire(connexion, longueur - 8)
                break
            connexion.sendall(b"R" + struct.pack("!ii", 8, 0))  # AuthenticationOk
            connexion.sendall(b"Z" + struct.pack("!i", 5) + b"I")  # ReadyForQuery
            while connexion.recv(4096):  # les requêtes suivantes restent sans réponse
                pass
        except OSError:
            pass

    @property
    def url(self) -> str:
        return f"postgresql://esn:secret-de-test@127.0.0.1:{self.port}/app"

    def fermer(self):
        self._ferme = True
        # shutdown() avant close() : sous Linux, close() seul ne réveille pas un recv()
        # ou un accept() bloqué dans un autre fil, et la connexion resterait ouverte.
        for prise in [self._ecoute, *self._connexions]:
            try:
                prise.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            prise.close()


def _attendre_places_libres(delai_s: float = 20):
    """Les sondes d'un test précédent (résolution DNS lente, par exemple) doivent être
    terminées, sinon elles fausseraient le test suivant (réponse immédiate « faux »)."""
    fin = time.monotonic() + delai_s
    while bdd._places._value < bdd._MAX_CONTROLES:  # noqa: SLF001
        assert time.monotonic() < fin, "des sondes de la base sont restées bloquées"
        time.sleep(0.05)


@pytest.fixture(autouse=True)
def _sondes_terminees():
    _attendre_places_libres()
    yield
    _attendre_places_libres()


@pytest.fixture
def fausse_base(request):
    base = FausseBase(handshake=request.param)
    yield base
    base.fermer()


@pytest.fixture
def sonde_bloquee(monkeypatch):
    """Remplace la sonde par une sonde qui ne revient jamais (jusqu'à la fin du test)."""
    liberer = threading.Event()
    monkeypatch.setattr(bdd, "_sonder", lambda: liberer.wait(30))
    yield
    liberer.set()


def _health(monkeypatch, url: str) -> tuple[int, float]:
    monkeypatch.setenv("DATABASE_URL", url)
    monkeypatch.setenv("GIT_COMMIT", "a" * 40)
    debut = time.monotonic()
    reponse = TestClient(creer_app()).get("/health")
    duree = time.monotonic() - debut
    assert reponse.json() == {"status": "ko", "commit": "a" * 40}
    return reponse.status_code, duree


@pytest.mark.parametrize("fausse_base", [False, True], ids=["tcp_muet", "handshake_puis_muet"], indirect=True)
def test_health_503_rapide_quand_la_base_accepte_la_connexion_sans_repondre(fausse_base, monkeypatch):
    statut, duree = _health(monkeypatch, fausse_base.url)
    assert statut == 503
    assert duree < LIMITE_S


def test_health_503_rapide_quand_le_nom_de_la_base_n_est_pas_resolu(monkeypatch):
    statut, duree = _health(monkeypatch, "postgresql://esn:secret-de-test@base-absente.invalid:5432/app")
    assert statut == 503
    assert duree < LIMITE_S


def test_health_503_rapide_quand_le_controle_ne_revient_jamais(sonde_bloquee, monkeypatch):
    """Indépendant du pilote : même une sonde qui ne rend jamais la main est bornée."""
    statut, duree = _health(monkeypatch, "postgresql://u:p@127.0.0.1:1/app")
    assert statut == 503
    assert bdd.DELAI_BASE_S <= duree < LIMITE_S


def test_health_ne_bloque_pas_les_autres_requetes(sonde_bloquee, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@127.0.0.1:1/app")

    async def scenario():
        transport = httpx.ASGITransport(app=creer_app())
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            sante = asyncio.create_task(client.get("/health"))
            await asyncio.sleep(0.1)  # /health est en attente de la base
            debut = time.monotonic()
            accueil = await client.get("/")
            duree_accueil = time.monotonic() - debut
            return (await sante).status_code, accueil.status_code, duree_accueil

    sante, accueil, duree_accueil = asyncio.run(scenario())
    assert sante == 503
    assert accueil == 200
    assert duree_accueil < 0.5


def test_sondes_bloquees_ne_s_empilent_pas(sonde_bloquee, monkeypatch):
    """Toutes les places prises (base gelée) : réponse immédiate, aucun fil de plus."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@127.0.0.1:1/app")
    for _ in range(bdd._MAX_CONTROLES):
        assert bdd.base_repond(delai_s=0.05) is False  # chaque sonde reste bloquée
    debut = time.monotonic()
    assert bdd.base_repond(delai_s=5) is False
    assert time.monotonic() - debut < 0.5


@pytest.mark.parametrize("fausse_base", [True], ids=["handshake_puis_muet"], indirect=True)
def test_base_repond_bloquant_est_aussi_borne(fausse_base, monkeypatch):
    """Version utilisée par l'attente au démarrage."""
    monkeypatch.setenv("DATABASE_URL", fausse_base.url)
    debut = time.monotonic()
    assert bdd.base_repond() is False
    assert time.monotonic() - debut < LIMITE_S
