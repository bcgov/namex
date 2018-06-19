"""empty message

Revision ID: 8a9044342457
Revises: 69b15a47f334
Create Date: 2018-06-13 12:56:08.768984

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_two_decision_reasons'
down_revision = '8a9044342457'
branch_labels = None
depends_on = None


def upgrade():
    decision_reason_table= sa.table("decision_reason",
         sa.column("id"),
         sa.column("name"),
         sa.column("reason"),
         )

    op.execute(
        decision_reason_table.insert().values({'id': 1, 'name':op.inline_literal('Distinctive'),
            'reason': op.inline_literal("Require distinctive, nondescriptive first word or prefix * E.G. Person's name, initials, geographic location, etc.")})
    )
    op.execute(
        decision_reason_table.insert().values({'id': 2, 'name':op.inline_literal('Descriptive'),
            'reason': op.inline_literal('Require descriptive second word or phrase * E.G. Construction, Gardening, Investments, Holdings, Etc.')})
    )
