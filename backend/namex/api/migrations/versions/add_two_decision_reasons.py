"""empty message

Revision ID: add_two_decision_reasons
Revises: a6af81f3d416
Create Date: 2018-06-19 (manually created by KBM)

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_two_decision_reasons'
down_revision = 'a6af81f3d416'
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
