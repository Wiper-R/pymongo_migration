from typing import Any, Mapping

from pymongo import database

Database = database.Database[Mapping[str, Any]]
