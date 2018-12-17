"""empty message

Revision ID: 84ea2594fc08
Revises: 75b6e6ecfde9
Create Date: 2018-12-17 10:05:35.807701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84ea2594fc08'
down_revision = '75b6e6ecfde9'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name='requests',
        column_name='expiration_date',
        type_=sa.TIMESTAMP(timezone=True)
    )

def downgrade():
    pass
