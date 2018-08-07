"""adding states

Revision ID: 7588fb9a61d9
Revises: b36c2a0baff8
Create Date: 2018-08-07 13:22:54.561910

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String

# revision identifiers, used by Alembic.
revision = '7588fb9a61d9'
down_revision = 'b36c2a0baff8'
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
            {'cd': 'EXPIRED',  'description': 'EXPIRED - LEGACY state for expired NRs from NRO'}
        ]
    )


def downgrade():
    pass
