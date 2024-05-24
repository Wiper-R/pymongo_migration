import os
from importlib.machinery import SourceFileLoader

from .config import config
from .migration_state import MigrationState
from .types import Database


class MigrationManager:
    def __init__(self, db: Database) -> None:
        self.migration_state = MigrationState(db)
        self.db = db

    def _load_migration(self, migration: str):
        return SourceFileLoader(
            migration, f"{config.migrations_dir}/{migration}.py"
        ).load_module()

    def upgrade(self, target: str | None = None):
        applied_migrations = self.migration_state.get_applied_migrations()
        migrations = sorted(
            f[:-3]
            for f in os.listdir(config.migrations_dir)
            if f.endswith(".py") and not f.startswith("_")
        )

        for migration in migrations:
            if migration not in applied_migrations:
                module = self._load_migration(migration)
                module.upgrade(self.db)
                self.migration_state.add_migration(migration)

                if target and migration == target:
                    break

    def downgrade(self, target: str | None = None):
        applied_migrations = self.migration_state.get_applied_migrations()
        applied_migrations.reverse()

        for migration in applied_migrations:
            module = self._load_migration(migration)
            module.downgrade(self.db)
            self.migration_state.remove_migration(migration)
            if target and migration == target:
                break
