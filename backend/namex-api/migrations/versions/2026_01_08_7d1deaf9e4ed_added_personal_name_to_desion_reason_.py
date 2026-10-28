"""Added-Personal-Name-to-Desion-Reason-Table

Revision ID: 7d1deaf9e4ed
Revises: 799297eb2af2
Create Date: 2026-01-08 17:10:15.886524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d1deaf9e4ed'
down_revision = '799297eb2af2'
branch_labels = None
depends_on = None


def upgrade():
    # Get reference to the decision_reason table
    decision_reason_table = sa.table('decision_reason',
                                     sa.column('id', sa.Integer),
                                     sa.column('name', sa.String),
                                     sa.column('reason', sa.String)
                                     )

    # Insert the new entry
    op.bulk_insert(
        decision_reason_table,
        [
            {'id': 53, 'name': 'Personal Name', 'reason': 'Personal names cannot be used on their own; an additional word or alphanumeric element must be included.'},
        ]
    )


def downgrade():
    # Remove the entry if rolling back
    op.execute("DELETE FROM decision_reason WHERE id = 53")
