"""empty message

Revision ID: 21b953f6b653
Revises: 8a5fb0cadb6e
Create Date: 2019-02-07 20:35:14.501374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21b953f6b653'
down_revision = '8a5fb0cadb6e'
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column(
        table_name='names',
        column_name='consumption_date',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="(consumption_date::timestamp || 'PST')::timestamptz"
    )

    op.alter_column(
        table_name='partner_name_system',
        column_name='partner_name_date',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="date_trunc('day', (partner_name_date::timestamp || 'PST')::timestamptz)"
    )

    op.alter_column(
        table_name='requests',
        column_name='nro_last_update',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="(nro_last_update::timestamp || 'PST')::timestamptz"
    )

    op.alter_column(
        table_name='requests',
        column_name='submitted_date',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="date_trunc('day', (submitted_date::timestamp || 'PST')::timestamptz)"
    )


def downgrade():
    pass
