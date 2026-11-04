"""add NROUPDATE state

Revision ID: 31043289e39a
Revises: 7588fb9a61d9
Create Date: 2018-08-08 11:22:38.932420

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String



# revision identifiers, used by Alembic.
revision = '31043289e39a'
down_revision = '7588fb9a61d9'
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
            {'cd': 'NRO_UPDATING',  'description': 'NRO_UPDATING - internal state used when updating records from NRO'}
        ]
    )


def downgrade():
    pass
