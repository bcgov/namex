"""index-by-idp-guid

Revision ID: 7d31f01702d1
Revises: 4cd0a149e021
Create Date: 2022-12-13 00:11:24.201850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d31f01702d1'
down_revision = '4cd0a149e021'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_user_idp_userid'), 'users', ['idp_userid'], unique=True)
    op.create_unique_constraint('users_idp_userid_key', 'users', ['idp_userid'])


def downgrade():
    op.drop_index(op.f('ix_user_idp_userid'), table_name='users')
    op.drop_constraint('users_idp_userid_key', 'users', ['idp_userid'])
