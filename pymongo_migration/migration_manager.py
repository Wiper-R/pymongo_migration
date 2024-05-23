import importlib
from os import PathLike
import os
from pymongo.database import Database

from .migration_state import MigrationState


class MigrationManager:
    def __init__(self, db: Database, migration_dir: PathLike = "migrations") -> None:
        self.migration_state = MigrationState(db)
        self.migration_dir = migration_dir
        self.db = db

    def _load_migration(self, migration):
        return importlib.import_module(f"{self.migration_dir}.{migration}")

    def upgrade(self, target=None):
        applied_migrations = self.migration_state.get_applied_migrations()
        migrations = sorted(
            f[:-3]
            for f in os.listdir(self.migration_dir)
            if f.endswith(".py") and not f.startswith("_")
        )

        for migration in migrations:
            if migration not in applied_migrations:
                module = self._load_migration(migration)
                module.upgrade(self.db)
                self.migration_state.add_migration(migration)

                if target and migration == target:
                    break

    def downgrade(self, target=None):
        applied_migrations = self.migration_state.get_applied_migrations()
        applied_migrations.reverse()

        for migration in applied_migrations:
            module = self._load_migration(migration)
            module.downgrade(self.db)
            self.migration_state.remove_migration(migration)
            if target and migration == target:
                break
