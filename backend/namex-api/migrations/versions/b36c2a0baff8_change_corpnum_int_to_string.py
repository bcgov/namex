"""empty message

Revision ID: b36c2a0baff8
Revises: cdbeccf1d8cf
Create Date: 2018-07-25 15:48:13.311747

Change the corpNum field from an Integer to an String.

[Katie] Not auto-generated, created by hand. Alembic didn't pick up field type change from Integer to String. Also had
to drop field before re-creating it, since just trying to alter the column didn't work (no error, but no change to db).

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b36c2a0baff8'
down_revision = 'cdbeccf1d8cf'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('requests', 'corp_num')
    op.add_column('requests', sa.Column('corp_num', sa.String(20), nullable=True))



def downgrade():

    op.drop_column('requests', 'corp_num')
    op.add_column('requests', sa.Column('corp_num', sa.Integer(), nullable=True))

