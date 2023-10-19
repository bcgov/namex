"""cobrs tables

Revision ID: e7c2ca8b223a
Revises: 7d31f01702d1
Create Date: 2023-10-18 16:16:53.119329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7c2ca8b223a'
down_revision = '7d31f01702d1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cobrs_request',
    sa.Column('RQUESTNO', sa.VARCHAR(), nullable=False),
    sa.Column('CHOICENO', sa.VARCHAR(), nullable=True),
    sa.Column('ACCREJFL', sa.VARCHAR(), nullable=True),
    sa.Column('REQTNAME', sa.VARCHAR(), nullable=True),
    sa.Column('REJ_COND', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('RQUESTNO')
    )

    op.create_table('cobrs_reqname',
    sa.Column('RQUESTNO', sa.VARCHAR(), nullable=False),
    sa.Column('REQSTATS', sa.VARCHAR(), nullable=True),
    sa.Column('PRIORQST', sa.VARCHAR(), nullable=True),
    sa.Column('JUMPQFLG', sa.VARCHAR(), nullable=True),
    sa.Column('ENTRYDAT', sa.DATE(), nullable=True),
    sa.Column('ENTRYTIM', sa.TIME(), nullable=False),
    sa.Column('ENTRYRID', sa.VARCHAR(), nullable=True),
    sa.Column('UPDATEID', sa.VARCHAR(), nullable=True),
    sa.Column('UPDATEDA', sa.DATE(), nullable=True),
    sa.Column('UPDATETI', sa.TIME(), nullable=True),
    sa.Column('EXAMINID', sa.VARCHAR(), nullable=False),
    sa.Column('EXAMINDA', sa.DATE(), nullable=True),
    sa.Column('EXAMINTI', sa.TIME(), nullable=True),
    sa.Column('RSLIPNUM', sa.Integer(), nullable=True),
    sa.Column('BCOLACCT', sa.Integer(), nullable=True),
    sa.Column('FOLIOTAG', sa.VARCHAR(), nullable=True),
    sa.Column('DATNUMBR', sa.VARCHAR(), nullable=True),
    sa.Column('RQSOURCE', sa.VARCHAR(), nullable=True),
    sa.Column('RQSTTYPE', sa.VARCHAR(), nullable=True),
    sa.Column('EXTRAPRO', sa.VARCHAR(), nullable=True),
    sa.Column('JURISDIC', sa.VARCHAR(), nullable=True),
    sa.Column('SUBPNAME', sa.VARCHAR(), nullable=True),
    sa.Column('SUBPADDR', sa.VARCHAR(), nullable=True),
    sa.Column('SUBPCITY', sa.VARCHAR(), nullable=True),
    sa.Column('SUBPPOCO', sa.VARCHAR(), nullable=True),
    sa.Column('SUBPFONE', sa.VARCHAR(), nullable=True),
    sa.Column('SUBPFAX', sa.VARCHAR(), nullable=True),
    sa.Column('SUBPCONT', sa.VARCHAR(), nullable=True),
    sa.Column('NAMETOTL', sa.VARCHAR(), nullable=True),
    sa.Column('CLINOTNO', sa.Integer(), nullable=True),
    sa.Column('ADDINFOR', sa.VARCHAR(), nullable=True),
    sa.Column('CANREASN', sa.VARCHAR(), nullable=True),
    sa.Column('EXPIDATE', sa.Integer(), nullable=True),
    sa.Column('COMPNUMB', sa.VARCHAR(), nullable=True),
    sa.Column('EXAMCOMM', sa.VARCHAR(), nullable=True),
    sa.Column('USERNOTE', sa.VARCHAR(), nullable=True),
    sa.Column('SUBPCLIE', sa.VARCHAR(), nullable=True),
    sa.Column('FINIFLAG', sa.VARCHAR(), nullable=True),
    sa.Column('LOCNCODE', sa.VARCHAR(), nullable=True),
    sa.Column('DOCUMTID', sa.VARCHAR(), nullable=True),
    sa.Column('CONSFLAG', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('RQUESTNO')
    )

def downgrade():
    op.drop_table('cobrs_request')
    op.drop_table('cobrs_reqname')
