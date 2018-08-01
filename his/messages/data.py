"""Data errors."""

from his.messages.api import HISMessage

__all__ = [
    'DataError',
    'MissingData',
    'IncompleteData',
    'InvalidData',
    'FieldValueError',
    'FieldNotNullable',
    'MissingKeyError',
    'InvalidKeys',
    'InvalidEnumerationValue',
    'NotAnInteger',
    'InvalidCustomerID']


class DataError(HISMessage):
    """Indicates errors in sent data."""

    STATUS = 422


class MissingData(DataError):
    """Indicates missing data."""

    pass


class IncompleteData(DataError):
    """Indicates incomplete data."""

    pass


class InvalidData(DataError):
    """Indicates missing data."""

    @classmethod
    def from_error(cls, error):
        """Initializes from a peeweeplus.FieldNotNullable error."""
        return cls(**error.to_dict())


class FieldValueError(InvalidData):
    """Indicates that the value for the field is not valid."""

    pass


class FieldNotNullable(InvalidData):
    """Indicates that the field is not nullable."""

    pass


class MissingKeyError(InvalidData):
    """Indicates a missing key for the respective model."""

    pass


class InvalidKeys(InvalidData):
    """Indicates that invalid keys were passed."""

    pass


class InvalidEnumerationValue(InvalidData):
    """Indicates that an invalid enumeration value was passed."""

    pass


class NotAnInteger(InvalidData):
    """Indicates missing credentials."""

    pass


class InvalidCustomerID(InvalidData):
    """Indicates that an invalid customer ID was specified."""

    pass
