"""empty message

Revision ID: 894aa7756f5b
Revises: b29e6d35146f
Create Date: 2018-05-17 09:30:09.996841

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '894aa7756f5b'
down_revision = 'b29e6d35146f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('requests', sa.Column('furnished', sa.String(length=1), nullable=True))
    op.drop_column('requests', 'nro_updated')


def downgrade():
    op.add_column('requests', sa.Column('nro_updated', sa.VARCHAR(length=1), autoincrement=False, nullable=True))
    op.drop_column('requests', 'furnished')
