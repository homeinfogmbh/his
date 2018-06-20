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

    @classmethod
    def from_field_not_nullable(cls, error):
        """Initializes from a FieldNotNullable error."""
        return cls(model=error.model, attr=error.attr, field=error.field)

    @classmethod
    def from_field_value_error(cls, error):
        """Initializes from a FieldNotNullable error."""
        return cls(
            model=error.model, attr=error.attr, field=error.field,
            value=error.value)

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
