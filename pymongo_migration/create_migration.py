import os


MIGRATIONS_DIR = 'migrations'

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
    filepath = os.path.join(MIGRATIONS_DIR, filename)

    if not os.path.exists(MIGRATIONS_DIR):
        os.makedirs(MIGRATIONS_DIR)

    content = TEMPLATE.format(
        migration_id=migration_id,
        description=description,
    )

    with open(filepath, 'w') as f:
        f.write(content)

    return filename