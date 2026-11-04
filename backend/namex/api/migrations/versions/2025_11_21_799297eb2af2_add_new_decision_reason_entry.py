"""add new decision reason entry

Revision ID: 799297eb2af2
Revises: 179a7b0089ce
Create Date: 2025-11-21 10:59:02.782992
Update Date: 2025-12-03 12:42:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799297eb2af2'
down_revision = '179a7b0089ce'
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
            {'id': 52, 'name': 'Outside Canada LP', 'reason': 'A Current Certificate Of Status from the Home Jurisdiction must be submitted to the Corporate Registry by email to bcregistries@gov.bc.ca You must include the Name Reservation Number on your correspondence.'},
        ]
    )


def downgrade():
    # Remove the entry if rolling back
    op.execute("DELETE FROM decision_reason WHERE id = 52")
