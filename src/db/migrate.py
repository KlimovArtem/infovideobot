from pathlib import Path

from db_adapters import postgres as db_adapter


async def create_table(connection):
    query = """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            migrated_at TIMESTAMP NOT NULL DEFAULT NOW()
        );"""
    async with db_adapter.database.pool.acquire() as connection:
        await connection.execute(query)

async def get_pending_migrations(connection):
    migrations = []
    migrations_dir = Path(__file__).parent / "migrations"
    for path in migrations_dir.iterdir():
        if not path.is_file():
            continue
        migration = {}
        migration["name"] = path.name
        migration["content"] = path.read_text()
        migration["version"] = int(path.name.split("_")[0])
        migrations.append(migration)

    query = "SELECT version from schema_migrations ORDER BY version ASC"
    records = await connection.fetch(query)
    applied_versions = [r["version"] for r in records]

    migrations = [m for m in migrations if m["version"] not in applied_versions]

    migrations = sorted(migrations, key=lambda m: m['version'])
    return migrations

async def apply_pending_migrations():
    await create_table()
    migrations = await get_pending_migrations()
    async with db_adapter.database.pool.aqcurie() as connection:
        async with connection.transaction():
            for migration in migrations:
                await connection.execute(migration["content"])
                await connection.execute("INSERT INTO schema_migrations (version, name) VALUES ($1, $2)", migration["version"], migration["name"])

