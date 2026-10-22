"""increase size of fields for restricted words

Revision ID: e6a452dcc698
Revises: add_restricted_word_tables
Create Date: 2018-07-11 13:20:18.476790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6a452dcc698'
down_revision = 'add_restricted_word_tables'
branch_labels = None
depends_on = None


def upgrade():

    # increase size of text fields to 1000
    op.alter_column('restricted_condition', 'cnd_text', type_=sa.String(length=1000))
    op.alter_column('restricted_condition', 'instructions', type_=sa.String(length=1000))



def downgrade():
    pass
