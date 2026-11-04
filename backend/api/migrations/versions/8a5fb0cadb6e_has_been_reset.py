"""empty message

Revision ID: 8a5fb0cadb6e
Revises: 4a317ebb47be
Create Date: 2019-01-19 17:26:39.259176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a5fb0cadb6e'
down_revision = '4a317ebb47be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('requests', sa.Column('has_been_reset', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('requests', 'has_been_reset')

