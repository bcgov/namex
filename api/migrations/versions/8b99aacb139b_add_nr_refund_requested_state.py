"""add nr refund requested state

Revision ID: 8b99aacb139b
Revises: 07563e18d763
Create Date: 2020-11-30 10:43:13.218082

"""
from alembic import op
from sqlalchemy import MetaData, Table

# revision identifiers, used by Alembic.
revision = '8b99aacb139b'
down_revision = '07563e18d763'
branch_labels = None
depends_on = None


def upgrade():
    # Get metadata from current connection
    meta = MetaData()

    # Pass in tuple with tables we want to reflect, otherwise whole database will get reflected
    meta.reflect(bind=op.get_bind(), only=('states',))

    # Define table representation
    states_tbl = Table('states', meta)

    op.bulk_insert(
        states_tbl,
        [{'cd': 'REFUND_REQUESTED', 'description': 'The request is cancelled and a refund for all payments has been requested'}]
    )


def downgrade():
    op.execute("DELETE FROM states WHERE cd = 'REFUND_REQUESTED';")
