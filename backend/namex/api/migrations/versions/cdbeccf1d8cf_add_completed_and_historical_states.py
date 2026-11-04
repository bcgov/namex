"""add COMPLETED and HISTORICAL states

Revision ID: cdbeccf1d8cf
Revises: dfcc6642758a
Create Date: 2018-07-24 21:31:57.346580

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String


# revision identifiers, used by Alembic.
revision = 'cdbeccf1d8cf'
down_revision = 'dfcc6642758a'
branch_labels = None
depends_on = None


def upgrade():
    # Create an ad-hoc table to use for the insert statement.
    states_table = table('states',
                           column('cd', String),
                           column('description', String)
                           )

    op.bulk_insert(
        states_table,
        [
            {'cd': 'HISTORICAL', 'description': 'HISTORICAL'},
            {'cd': 'COMPLETED',  'description': 'COMPLETED - LEGACY state for completed NRs from NRO'}
        ]
    )


def downgrade():
    pass
