import os
from .config import config

TEMPLATE = '''"""
Migration {migration_id}: {description}
"""
from pymongo_migration.types import Database

def upgrade(db: Database) -> None:
    # Write your upgrade logic here
    pass

def downgrade(db: Database) -> None:
    # Write your downgrade logic here
    pass
'''

def create_migration_file(migration_id: str, description: str):
    filename = f'{migration_id}_{description.replace(" ", "_").lower()}.py'
    filepath = os.path.join(config.migrations_dir, filename)

    if not os.path.exists(config.migrations_dir):
        os.makedirs(config.migrations_dir)

    content = TEMPLATE.format(
        migration_id=migration_id,
        description=description,
    )

    with open(filepath, 'w') as f:
        f.write(content)

    return filename