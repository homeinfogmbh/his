"""Common ORM constants, functions and models."""

from peeweeplus import JSONModel, MySQLDatabaseProxy

from his.config import CONFIG_FILE


__all__ = ["DATABASE", "HISModel"]


DATABASE = MySQLDatabaseProxy("his", CONFIG_FILE)


class HISModel(JSONModel):
    """Generic HIS database model."""

    class Meta:
        database = DATABASE
        schema = database.database
