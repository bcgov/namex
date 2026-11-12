from alembic import op
import sqlalchemy as sa


def _sequence_exists(sequence_name):
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
        {'sequence_name': sequence_name},
    ).scalar() is not None


def _column_default(table_name, column_name):
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
        {'table_name': table_name, 'column_name': column_name},
    ).scalar()


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


def _require_unique_ids(table_name, column_name):
    connection = op.get_bind()
    null_ids = connection.execute(
        sa.text(f'SELECT count(*) FROM {table_name} WHERE {column_name} IS NULL')
    ).scalar()
    if null_ids:
        raise RuntimeError(
            f'{table_name} has {null_ids} null {column_name} values'
        )
    duplicate_ids = connection.execute(
        sa.text(
            f"""
            SELECT count(*) FROM (
                SELECT {column_name}
                FROM {table_name}
                GROUP BY {column_name}
                HAVING count(*) > 1
            ) duplicate_ids
            """
        )
    ).scalar()
    if duplicate_ids:
        raise RuntimeError(
            f'{table_name} has {duplicate_ids} duplicate {column_name} values'
        )


def _create_sequence(table_name, column_name, sequence_name, grant_roles):
    op.execute(
        f"""
        CREATE SEQUENCE {sequence_name}
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
                '{sequence_name}',
                COALESCE((SELECT MAX({column_name}) FROM {table_name}), 1),
                (SELECT MAX({column_name}) FROM {table_name}) IS NOT NULL
            )
            """
        )
    )
    op.execute(
        f'ALTER SEQUENCE {sequence_name} OWNED BY {table_name}.{column_name}'
    )
    connection = op.get_bind()
    for role_name in grant_roles:
        exists = connection.execute(
            sa.text('SELECT 1 FROM pg_roles WHERE rolname = :role_name'),
            {'role_name': role_name},
        ).scalar()
        if exists is None:
            continue
        quoted_role = '"' + role_name.replace('"', '""') + '"'
        op.execute(
            f'GRANT USAGE, SELECT ON SEQUENCE {sequence_name} TO {quoted_role}'
        )


def upgrade_serial_id(table_name, column_name, sequence_name, pk_name, grant_roles):
    if not _sequence_exists(sequence_name):
        _create_sequence(table_name, column_name, sequence_name, grant_roles)
    if _column_default(table_name, column_name) is None:
        op.execute(
            f"ALTER TABLE {table_name} ALTER COLUMN {column_name} "
            f"SET DEFAULT nextval('{sequence_name}'::regclass)"
        )
    if _is_nullable(table_name, column_name):
        _require_unique_ids(table_name, column_name)
        op.execute(
            f'ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL'
        )
    if not _has_primary_key(table_name):
        _require_unique_ids(table_name, column_name)
        op.execute(
            f'ALTER TABLE {table_name} ADD CONSTRAINT {pk_name} '
            f'PRIMARY KEY ({column_name})'
        )
