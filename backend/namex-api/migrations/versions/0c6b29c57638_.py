"""empty message

Revision ID: 0c6b29c57638
Revises: 229257754f99
Create Date: 2019-07-31 13:31:54.648911

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0c6b29c57638'
down_revision = '229257754f99'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('events', sa.Column('event_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True))

def downgrade():
    op.drop_column('events', 'event_json')

