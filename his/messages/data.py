"""Data errors."""

from his.messages.common import Message

__all__ = [
    'DataError',
    'NoDataProvided',
    'MissingData',
    'IncompleteData',
    'InvalidData',
    'NotAnInteger',
    'InvalidUTF8Data',
    'InvalidJSON',
    'InvalidCustomerID']


class DataError(Message):
    """Indicates errors in sent data."""

    STATUS = 422


class NoDataProvided(DataError):
    """Indicates missing data."""

    pass


class MissingData(DataError):
    """Indicates missing data."""

    pass


class IncompleteData(DataError):
    """Indicates incomplete data."""

    pass


class InvalidData(DataError):
    """Indicates missing data."""

    pass


class NotAnInteger(InvalidData):
    """Indicates missing credentials."""

    pass


class InvalidUTF8Data(InvalidData):
    """Indicates that the data provided was not UTF-8 text."""

    pass


class InvalidJSON(InvalidData):
    """Indicates that the JSON data is invalid."""

    pass


class InvalidCustomerID(InvalidData):
    """Indicates that an invalid customer ID was specified."""

    pass
