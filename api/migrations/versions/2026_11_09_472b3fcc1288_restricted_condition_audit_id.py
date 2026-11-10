"""restricted condition audit id

Revision ID: 472b3fcc1288
Revises: 4c33aac6da67
Create Date: 2026-11-09 22:51:00.105602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '472b3fcc1288'
down_revision = '4c33aac6da67'
branch_labels = None
depends_on = None


TABLE_NAME = 'restricted_condition_audit'
COLUMN_NAME = 'id'
SEQUENCE_NAME = 'restricted_condition_audit_id_seq'
PK_NAME = 'restricted_condition_audit_pkey'
GRANT_ROLES = (
    'readwrite',
    'sa-api@a083gt-dev.iam',
    'sa-api@a083gt-test.iam',
    'sa-api@a083gt-prod.iam',
)


def _sequence_exists():
    return op.get_bind().execute(
        sa.text(
            """
            SELECT 1
            FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE n.nspname = 'public'
              AND c.relname = :sequence_name
              AND c.relkind = 'S'
            """
        ),
        {'sequence_name': SEQUENCE_NAME},
    ).scalar() is not None


def _column_default():
    return op.get_bind().execute(
        sa.text(
            """
            SELECT pg_get_expr(ad.adbin, ad.adrelid)
            FROM pg_attribute a
            JOIN pg_class c ON c.oid = a.attrelid
            JOIN pg_namespace n ON n.oid = c.relnamespace
            LEFT JOIN pg_attrdef ad ON ad.adrelid = c.oid AND ad.adnum = a.attnum
            WHERE n.nspname = 'public'
              AND c.relname = :table_name
              AND a.attname = :column_name
              AND NOT a.attisdropped
            """
        ),
        {'table_name': TABLE_NAME, 'column_name': COLUMN_NAME},
    ).scalar()


def _is_nullable():
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
        {'table_name': TABLE_NAME, 'column_name': COLUMN_NAME},
    ).scalar()


def _has_primary_key():
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
        {'table_name': TABLE_NAME},
    ).scalar() is not None


def _require_unique_ids():
    connection = op.get_bind()
    null_ids = connection.execute(
        sa.text(f'SELECT count(*) FROM {TABLE_NAME} WHERE {COLUMN_NAME} IS NULL')
    ).scalar()
    if null_ids:
        raise RuntimeError(
            f'{TABLE_NAME} has {null_ids} null {COLUMN_NAME} values'
        )
    duplicate_ids = connection.execute(
        sa.text(
            f"""
            SELECT count(*) FROM (
                SELECT {COLUMN_NAME}
                FROM {TABLE_NAME}
                GROUP BY {COLUMN_NAME}
                HAVING count(*) > 1
            ) duplicate_ids
            """
        )
    ).scalar()
    if duplicate_ids:
        raise RuntimeError(
            f'{TABLE_NAME} has {duplicate_ids} duplicate {COLUMN_NAME} values'
        )


def _create_sequence():
    op.execute(
        f"""
        CREATE SEQUENCE {SEQUENCE_NAME}
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1
        """
    )
    op.get_bind().execute(
        sa.text(
            f"""
            SELECT setval(
                '{SEQUENCE_NAME}',
                COALESCE((SELECT MAX({COLUMN_NAME}) FROM {TABLE_NAME}), 1),
                (SELECT MAX({COLUMN_NAME}) FROM {TABLE_NAME}) IS NOT NULL
            )
            """
        )
    )
    op.execute(
        f'ALTER SEQUENCE {SEQUENCE_NAME} OWNED BY {TABLE_NAME}.{COLUMN_NAME}'
    )
    connection = op.get_bind()
    for role_name in GRANT_ROLES:
        exists = connection.execute(
            sa.text('SELECT 1 FROM pg_roles WHERE rolname = :role_name'),
            {'role_name': role_name},
        ).scalar()
        if exists is None:
            continue
        quoted_role = '"' + role_name.replace('"', '""') + '"'
        op.execute(
            f'GRANT USAGE, SELECT ON SEQUENCE {SEQUENCE_NAME} TO {quoted_role}'
        )


def upgrade():
    if not _sequence_exists():
        _create_sequence()
    if _column_default() is None:
        op.execute(
            f"ALTER TABLE {TABLE_NAME} ALTER COLUMN {COLUMN_NAME} "
            f"SET DEFAULT nextval('{SEQUENCE_NAME}'::regclass)"
        )
    if _is_nullable():
        _require_unique_ids()
        op.execute(
            f'ALTER TABLE {TABLE_NAME} ALTER COLUMN {COLUMN_NAME} SET NOT NULL'
        )
    if not _has_primary_key():
        _require_unique_ids()
        op.execute(
            f'ALTER TABLE {TABLE_NAME} ADD CONSTRAINT {PK_NAME} '
            f'PRIMARY KEY ({COLUMN_NAME})'
        )


def downgrade():
    # Test and prod already had this sequence and primary key. Dropping them
    # would stop audit rows there, so this revision leaves them in place.
    pass
