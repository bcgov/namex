"""empty message

Revision ID: 4a317ebb47be
Revises: 84ea2594fc08
Create Date: 2019-01-04 15:18:28.860142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a317ebb47be'
down_revision = '84ea2594fc08'
branch_labels = None
depends_on = None


def upgrade():

    op.alter_column(
        table_name='comments',
        column_name='timestamp',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="(timestamp::timestamp || 'UTC')::timestamptz"
    )

    op.alter_column(
        table_name='events',
        column_name='event_dt',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="(event_dt::timestamp || 'UTC')::timestamptz"
    )

    op.alter_column(
        table_name='requests',
        column_name='last_update',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="(last_update::timestamp || 'UTC')::timestamptz"
    )

    op.alter_column(
        table_name='requests',
        column_name='priority_date',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="(priority_date::timestamp || 'UTC')::timestamptz"
    )

    op.alter_column(
        table_name='users',
        column_name='creationDate',
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="(\"creationDate\"::timestamp || 'UTC')::timestamptz"
    )


def downgrade():
    pass
