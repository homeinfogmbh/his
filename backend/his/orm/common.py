"""Common ORM constants, functions and models."""

from peeweeplus import JSONModel, MySQLDatabase

from his.config import CONFIG


__all__ = ['DATABASE', 'HISModel', 'init']


DATABASE = MySQLDatabase(None)


def init():
    """Initializes the database."""

    DATABASE.init(
        CONFIG.get('db', 'db'), host=CONFIG.get('db', 'host'),
        user=CONFIG.get('db', 'user'), password=CONFIG.get('db', 'passwd'))


class HISModel(JSONModel):
    """Generic HOMEINFO Integrated Service database model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
