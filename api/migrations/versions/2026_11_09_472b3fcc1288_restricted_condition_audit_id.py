"""restricted condition audit id

Revision ID: 472b3fcc1288
Revises: 4c33aac6da67
Create Date: 2026-11-09 22:51:00.105602

"""
from serial_id import upgrade_serial_id


revision = '472b3fcc1288'
down_revision = '4c33aac6da67'
branch_labels = None
depends_on = None


TABLE_NAME = 'restricted_condition_audit'
COLUMN_NAME = 'id'
SEQUENCE_NAME = 'restricted_condition_audit_id_seq'
PK_NAME = 'restricted_condition_audit_pkey'


def upgrade():
    upgrade_serial_id(TABLE_NAME, COLUMN_NAME, SEQUENCE_NAME, PK_NAME)


def downgrade():
    # Test and prod already had this sequence and primary key. Dropping them
    # would stop audit rows there, so this revision leaves them in place.
    pass
