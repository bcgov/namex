"""Create restricted-word scratch tables and repair missing primary keys.

Revision ID: c4e8a1b27f09
Revises: 7d1deaf9e4ed
Create Date: 2026-11-09 21:28:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c4e8a1b27f09'
down_revision = '7d1deaf9e4ed'
branch_labels = None
depends_on = None

WORD_SEQUENCE = 'restricted_word_word_id_seq'
CONDITION_SEQUENCE = 'restricted_condition_cnd_id_seq'
GRANT_ROLES = (
    'readwrite',
    'sa-api@a083gt-dev.iam',
    'sa-api@a083gt-test.iam',
    'sa-api@a083gt-prod.iam',
)
SCRATCH_TABLES = (
    'restricted_word_tmp',
    'restricted_condition_tmp',
    'restricted_word_condition_tmp',
)


def _has_primary_key(table_name):
    return op.get_bind().execute(
        sa.text(
            """
            SELECT 1
            FROM pg_constraint con
            JOIN pg_class c ON c.oid = con.conrelid
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = 'public'
              AND c.relname = :table_name
              AND con.contype = 'p'
            """
        ),
        {'table_name': table_name},
    ).scalar() is not None


def _is_nullable(table_name, column_name):
    return op.get_bind().execute(
        sa.text(
            """
            SELECT NOT a.attnotnull
            FROM pg_attribute a
            JOIN pg_class c ON c.oid = a.attrelid
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = 'public'
              AND c.relname = :table_name
              AND a.attname = :column_name
              AND NOT a.attisdropped
            """
        ),
        {'table_name': table_name, 'column_name': column_name},
    ).scalar()


def _repair_id_column(table_name, column_name, sequence_name, pk_name):
    op.execute(
        f"ALTER TABLE {table_name} "
        f"ALTER COLUMN {column_name} SET DEFAULT nextval('{sequence_name}'::regclass)"
    )
    if _is_nullable(table_name, column_name):
        op.execute(f'ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL')
    if not _has_primary_key(table_name):
        op.execute(
            f'ALTER TABLE {table_name} ADD CONSTRAINT {pk_name} PRIMARY KEY ({column_name})'
        )


def _repair_link(table_name, pk_name):
    if _is_nullable(table_name, 'cnd_id') or _is_nullable(table_name, 'word_id'):
        op.execute(
            f'DELETE FROM {table_name} WHERE cnd_id IS NULL OR word_id IS NULL'
        )
        if _is_nullable(table_name, 'cnd_id'):
            op.execute(f'ALTER TABLE {table_name} ALTER COLUMN cnd_id SET NOT NULL')
        if _is_nullable(table_name, 'word_id'):
            op.execute(f'ALTER TABLE {table_name} ALTER COLUMN word_id SET NOT NULL')
    if not _has_primary_key(table_name):
        op.execute(
            f'ALTER TABLE {table_name} '
            f'ADD CONSTRAINT {pk_name} PRIMARY KEY (cnd_id, word_id)'
        )


def _recreate_scratch_tables():
    op.execute('DROP TABLE IF EXISTS restricted_word_condition_tmp')
    op.execute('DROP TABLE IF EXISTS restricted_condition_tmp')
    op.execute('DROP TABLE IF EXISTS restricted_word_tmp')
    op.execute(
        f"""
        CREATE TABLE restricted_word_tmp (
            word_id integer NOT NULL DEFAULT nextval('{WORD_SEQUENCE}'::regclass),
            word_phrase character varying(60),
            CONSTRAINT restricted_word_tmp_pkey PRIMARY KEY (word_id)
        )
        """
    )
    op.execute(
        f"""
        CREATE TABLE restricted_condition_tmp (
            cnd_id integer NOT NULL DEFAULT nextval('{CONDITION_SEQUENCE}'::regclass),
            cnd_text character varying(1000),
            allow_use character varying(1),
            consent_required character varying(1),
            consenting_body character varying(195),
            instructions character varying(1000),
            CONSTRAINT restricted_condition_tmp_pkey PRIMARY KEY (cnd_id)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE restricted_word_condition_tmp (
            cnd_id integer NOT NULL,
            word_id integer NOT NULL,
            CONSTRAINT restricted_word_condition_tmp_pkey PRIMARY KEY (cnd_id, word_id)
        )
        """
    )


def _grant_scratch_tables():
    connection = op.get_bind()
    for role_name in GRANT_ROLES:
        exists = connection.execute(
            sa.text('SELECT 1 FROM pg_roles WHERE rolname = :role_name'),
            {'role_name': role_name},
        ).scalar()
        if exists is None:
            continue
        quoted_role = '"' + role_name.replace('"', '""') + '"'
        for table_name in SCRATCH_TABLES:
            op.execute(
                f'GRANT SELECT, INSERT, DELETE, TRUNCATE ON {table_name} TO {quoted_role}'
            )
        op.execute(
            f'GRANT USAGE, SELECT ON SEQUENCE {WORD_SEQUENCE} TO {quoted_role}'
        )
        op.execute(
            f'GRANT USAGE, SELECT ON SEQUENCE {CONDITION_SEQUENCE} TO {quoted_role}'
        )


def upgrade():
    _repair_link('restricted_word_condition', 'rest_word_condition_pkey')
    _repair_id_column(
        'restricted_condition', 'cnd_id', CONDITION_SEQUENCE, 'rest_condition_pkey'
    )
    _repair_id_column(
        'restricted_word', 'word_id', WORD_SEQUENCE, 'rest_word_pkey'
    )
    op.execute(
        f'ALTER SEQUENCE {WORD_SEQUENCE} OWNED BY restricted_word.word_id'
    )
    op.execute(
        f'ALTER SEQUENCE {CONDITION_SEQUENCE} OWNED BY restricted_condition.cnd_id'
    )
    _recreate_scratch_tables()
    _grant_scratch_tables()


def downgrade():
    op.execute('DROP TABLE IF EXISTS restricted_word_condition_tmp')
    op.execute('DROP TABLE IF EXISTS restricted_condition_tmp')
    op.execute('DROP TABLE IF EXISTS restricted_word_tmp')
