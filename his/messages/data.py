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

    pass


class FieldValueError(InvalidData):
    """Indicates that the value for the field is not valid."""

    @classmethod
    def from_fve(cls, fve):
        """Creates the messsage from a peeweeplus.FieldValueError."""
        return cls(model=fve.model.__name__, field=type(fve.field).__name__,
                   attribute=fve.field.name, column=fve.field.column_name,
                   key=fve.field.json_key, value=str(fve.value),
                   type=type(fve.value).__name__)


class FieldNotNullable(InvalidData):
    """Indicates that the field is not nullable."""

    @classmethod
    def from_fnn(cls, fnn):
        """Creates the message from a peeweeplus.FieldNotNullable error."""
        return cls(model=fnn.model.__name__, field=type(fnn.field).__name__,
                   attribute=fnn.field.name, column=fnn.field.column_name,
                   key=fnn.field.json_key)


class MissingKeyError(InvalidData):
    """Indicates a missing key for the respective model."""

    @classmethod
    def from_mke(cls, mke):
        """Creates the message from the peeweeplus.MissingKeyError."""
        return cls(model=mke.model.__name__, field=type(mke.field).__name__,
                   attribute=mke.field.name, column=mke.field.column_name,
                   key=mke.field.json_key)


class InvalidKeys(InvalidData):
    """Indicates that invalid keys were passed."""

    @classmethod
    def from_iks(cls, iks):
        """Creates the message from the peeweeplus.InvalidKeys error."""
        return cls(keys=iks.invalid_keys)


class InvalidEnumerationValue(InvalidData):
    """Indicates that an invalid enumeration value was passed."""

    @classmethod
    def from_iev(cls, iev):
        """Creates a message from a peeweeplus.InvalidEnumerationValue."""
        return cls(value=iev.value, enum=[value.value for value in iev.enum])


class NotAnInteger(InvalidData):
    """Indicates missing credentials."""

    pass


class InvalidCustomerID(InvalidData):
    """Indicates that an invalid customer ID was specified."""

    pass
