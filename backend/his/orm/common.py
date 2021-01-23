"""Common ORM constants, functions and models."""

from peeweeplus import JSONModel

from his.config import DATABASE


__all__ = ['DATABASE', 'HISModel']


class HISModel(JSONModel):
    """Generic HOMEINFO Integrated Service database model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
