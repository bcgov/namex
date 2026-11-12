"""Give virtual_word_condition.id a sequence where the database has none.

Revision ID: 4c33aac6da67
Revises: c4e8a1b27f09
Create Date: 2026-11-09 22:12:00.000000

"""
from serial_id import upgrade_serial_id


revision = '4c33aac6da67'
down_revision = 'c4e8a1b27f09'
branch_labels = None
depends_on = None

TABLE_NAME = 'virtual_word_condition'
COLUMN_NAME = 'id'
SEQUENCE_NAME = 'virtual_word_condition_id_seq'
PK_NAME = 'virtual_word_condition_pkey'
GRANT_ROLES = (
    'readwrite',
    'sa-api@a083gt-dev.iam',
    'sa-api@a083gt-test.iam',
    'sa-api@a083gt-prod.iam',
)


def upgrade():
    upgrade_serial_id(TABLE_NAME, COLUMN_NAME, SEQUENCE_NAME, PK_NAME, GRANT_ROLES)


def downgrade():
    # Test and prod already had this sequence and primary key. Dropping them
    # would stop new screen rows there, so this revision leaves them in place.
    pass
