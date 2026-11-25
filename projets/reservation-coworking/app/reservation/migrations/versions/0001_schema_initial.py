"""Schéma initial : utilisateur, salle, reservation, session + les 3 salles (H-20).

Migration additive uniquement (architecture.md § 4 et § 8) : aucune fonction `downgrade`,
aucune migration descendante n'est lancée automatiquement.

Les 3 salles sont une donnée de référence, sans lien avec l'authentification (DEC-011).
L'insertion est idempotente (clé primaire fixe + ON CONFLICT DO NOTHING).
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "utilisateur",
        sa.Column("id", sa.BigInteger, sa.Identity(), primary_key=True),
        sa.Column("nom", sa.String(100), nullable=False),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("mot_de_passe_hash", sa.Text, nullable=False),
        sa.Column("role", sa.Text, nullable=False),
        sa.Column("doit_changer_mdp", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("cree_le", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("mdp_change_le", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("email", name="uq_utilisateur_email"),
        sa.CheckConstraint("role IN ('membre', 'accueil')", name="ck_utilisateur_role"),
    )
    op.create_table(
        "salle",
        sa.Column("id", sa.SmallInteger, primary_key=True, autoincrement=False),
        sa.Column("nom", sa.String(100), nullable=False),
        sa.Column("capacite", sa.Integer, nullable=True),
        sa.Column("equipements", sa.Text, nullable=True),
        sa.Column("ordre", sa.Integer, nullable=False),
    )
    op.create_table(
        "reservation",
        sa.Column("id", sa.BigInteger, sa.Identity(), primary_key=True),
        sa.Column("salle_id", sa.SmallInteger, sa.ForeignKey("salle.id"), nullable=False),
        sa.Column("utilisateur_id", sa.BigInteger,
                  sa.ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False),
        sa.Column("date_creneau", sa.Date, nullable=False),
        sa.Column("heure_debut", sa.SmallInteger, nullable=False),
        sa.Column("cree_le", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.UniqueConstraint("salle_id", "date_creneau", "heure_debut",
                            name="uq_reservation_creneau"),
        sa.CheckConstraint("heure_debut BETWEEN 8 AND 19", name="ck_reservation_heure"),
        sa.CheckConstraint("EXTRACT(ISODOW FROM date_creneau) <= 5",
                           name="ck_reservation_jour_ouvre"),
    )
    op.create_index("ix_reservation_utilisateur_date", "reservation",
                    ["utilisateur_id", "date_creneau"])
    op.create_index("ix_reservation_date", "reservation", ["date_creneau"])
    op.create_table(
        "session",
        sa.Column("jeton_hash", sa.LargeBinary, primary_key=True),
        sa.Column("utilisateur_id", sa.BigInteger,
                  sa.ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cree_le", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("derniere_activite", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.func.now()),
        sa.Column("expire_le", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_session_utilisateur", "session", ["utilisateur_id"])

    op.execute(
        "INSERT INTO salle (id, nom, ordre) VALUES "
        "(1, 'Salle 1', 1), (2, 'Salle 2', 2), (3, 'Salle 3', 3) "
        "ON CONFLICT (id) DO NOTHING"
    )
