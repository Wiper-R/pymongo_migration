import os
import click, dotenv


MONGO_URI = dotenv.get_key(".env", "MONGO_CONNECTION_URI")
DATABASE_NAME = dotenv.get_key(".env", "DATABASE_NAME")

@click.group("main")
def main() -> None:
    pass

@main.command()
@click.argument("description")
def create(description: str):
    from datetime import datetime, UTC
    from .create_migration import create_migration_file

    migration_id = datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")
    filename = create_migration_file(migration_id, description)
    click.echo(f"Migration {filename} created successfully")

@main.command()
def migrate() -> None:
    import pymongo
    from .migration_manager import MigrationManager
    db = pymongo.MongoClient(MONGO_URI)[DATABASE_NAME]
    MigrationManager(db).upgrade()
    click.echo("Applied migrations successfully")

@main.command()
def downgrade() -> None:
    import pymongo
    from .migration_manager import MigrationManager
    db = pymongo.MongoClient(MONGO_URI)[DATABASE_NAME]
    MigrationManager(db).downgrade()
    click.echo("Downgraded migrations successfully")

main()