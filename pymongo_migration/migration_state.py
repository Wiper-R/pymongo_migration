from typing import Any, List

from .config import config
from .types import Database


class MigrationState:
    def __init__(self, db: Database):
        self.db = db
        self.collection = db[config.migrations_collection]

    def get_applied_migrations(self) -> List[Any]:
        return [doc["migration"] for doc in self.collection.find()]

    def add_migration(self, migration: str):
        self.collection.insert_one({"migration": migration})

    def remove_migration(self, migration: str):
        self.collection.delete_one({"migration": migration})
