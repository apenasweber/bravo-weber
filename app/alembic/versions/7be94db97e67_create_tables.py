"""create tables

Revision ID: 7be94db97e67
Revises: 
Create Date: 2022-12-08 23:25:09.203621

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7be94db97e67"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "fictitious_currencies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("currency_code", sa.String(), nullable=False),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.Column("backed_by", sa.String(), server_default="USD", nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        # insert column currency_type
        sa.Column(
            "currency_type", sa.String(), server_default="fictitious", nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_fictitious_currencies_currency_code"),
        "fictitious_currencies",
        ["currency_code"],
        unique=True,
    )

    op.create_table(
        "coinbase_currencies_public_api",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("currency_code", sa.String(), nullable=False),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.Column("backed_by", sa.String(), server_default="USD", nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "currency_type", sa.String(), server_default="coinbase", nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_coinbase_currencies_public_api_currency_code"),
        "coinbase_currencies_public_api",
        ["currency_code"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_coinbase_currencies_public_api_currency_code"),
        table_name="coinbase_currencies_public_api",
    )
    op.drop_table("coinbase_currencies_public_api")
    op.drop_index(
        op.f("ix_fictitious_currencies_currency_code"),
        table_name="fictitious_currencies",
    )
    op.drop_table("fictitious_currencies")
