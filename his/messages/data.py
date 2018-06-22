"""Data errors."""

from his.messages.api import HISMessage

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


class DataError(HISMessage):
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

    def __init__(self, *args, **kwargs):
        """Debug arguments."""
        for index, arg in enumerate(args):
            print('arg{}:'.format(index), arg, '({})'.format(type(arg)),
                  flush=True)

        for keyword, value in kwargs.items():
            print('{}:'.format(keyword), value, '({})'.format(type(value)),
                  flush=True)

        super().__init__(*args, **kwargs)

    @classmethod
    def from_field_not_nullable(cls, error):
        """Initializes from a FieldNotNullable error."""
        return cls(
            model=error.model.__name__, key=error.field.column_name,
            field=error.field.__class__)

    @classmethod
    def from_field_value_error(cls, error):
        """Initializes from a FieldNotNullable error."""
        return cls(
            model=error.model.__name__, key=error.field.column_name,
            field=error.field.__class__, value=error.value)

    @classmethod
    def from_invalid_keys(cls, error):
        """Initializes from a FieldNotNullable error."""
        return cls(keys=error.invalid_keys)


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
