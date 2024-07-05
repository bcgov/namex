"""Add nr_num_lifespan and nr_num_exclude tables

Revision ID: 6be595afb9ba
Revises: e7c2ca8b223a
Create Date: 2024-07-03 14:09:17.896835

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6be595afb9ba'
down_revision = 'e7c2ca8b223a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('nr_number_exclude',
    sa.Column('nr_num', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('nr_num')
    )
    op.create_table('nr_number_lifespan',
    sa.Column('nr_num', sa.String(length=10), nullable=False),
    sa.Column('nr_timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('nr_num')
    )


def downgrade():
    op.drop_table('nr_number_lifespan')
    op.drop_table('nr_number_exclude')
