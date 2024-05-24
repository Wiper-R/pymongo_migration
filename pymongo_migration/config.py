import os

import msgspec
import toml


class EnvLookup(msgspec.Struct):
    db_uri: str = "DATABASE_URI"
    db_name: str = "DATABASE_NAME"


class Config(msgspec.Struct):
    migrations_dir: str = "migrations"
    migrations_collection: str = "migrations_state"
    env_lookup: EnvLookup = msgspec.field(default_factory=EnvLookup)


def load_config() -> Config:
    if os.path.isfile("pyproject.toml"):
        with open("pyproject.toml") as f:
            _toml = toml.load(f)

        return msgspec.toml._convert(
            _toml.get("tool", {}).get("pymongo_migration", {}), Config
        )

    return Config()


config = load_config()
