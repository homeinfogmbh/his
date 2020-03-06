"""Common ORM constants, functions and models."""

from peeweeplus import JSONModel, MySQLDatabase

from his.config import CONFIG


__all__ = ['DATABASE', 'HISModel']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class HISModel(JSONModel):
    """Generic HOMEINFO Integrated Service database model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
