from pymongo.database import Database
from .config import config

class MigrationState:
    def __init__(self, db: Database):
        self.db = db
        self.collection = db[config.migrations_collection]

    def get_applied_migrations(self):
        return [doc['migration'] for doc in self.collection.find()]
    
    def add_migration(self, migration):
        # FIXME: Add type
        self.collection.insert_one({'migration': migration})

    def remove_migration(self, migration):
        self.collection.delete_one({"migration": migration})