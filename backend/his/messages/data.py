"""Data errors."""

from wsgilib import JSONMessage


__all__ = [
    'MISSING_DATA',
    'INCOMPLETE_DATA',
    'INVALID_DATA',
    'AMBIGUOUS_DATA',
    'NOT_AN_INTEGER',
    'INVALID_CUSTOMER_ID',
    'FIELD_VALUE_ERROR',
    'FIELD_NOT_NULLABLE',
    'MISSING_KEY_ERROR',
    'INVALID_KEYS',
    'NON_UNIQUE_VALUE',
    'INVALID_ENUM_VALUE',
    'field_value_error',
    'field_not_nullable',
    'missing_key_error',
    'invalid_keys',
    'non_unique_value']


MISSING_DATA = JSONMessage('The request is missing data.', status=422)
INCOMPLETE_DATA = JSONMessage(
    'The data sent in the request is incomplete.', status=422)
INVALID_DATA = JSONMessage(
    'The data sent in the request is invalid.', status=422)
AMBIGUOUS_DATA = JSONMessage('Data is ambiguous.', status=422)
NOT_AN_INTEGER = JSONMessage(
    'The provided value is not an integer.', status=422)
INVALID_CUSTOMER_ID = JSONMessage(
    'The provided value is not a valid customer ID.', status=422)
FIELD_VALUE_ERROR = JSONMessage('Invalid value for field.', status=422)
FIELD_NOT_NULLABLE = JSONMessage('Field cannot be NULL.', status=422)
MISSING_KEY_ERROR = JSONMessage('Missing key for field.', status=422)
INVALID_KEYS = JSONMessage('Invalid keys for model.', status=422)
NON_UNIQUE_VALUE = JSONMessage('Value for field is not unique.', status=422)
INVALID_ENUM_VALUE = JSONMessage(
    'Invalid value for enumeration contraint.', status=422)


def field_value_error(fve):
    """Creates a messsage from a peeweeplus.FieldValueError."""

    return FIELD_VALUE_ERROR.update(
        model=fve.model.__name__, field=type(fve.field).__name__,
        attribute=fve.attribute, column=fve.field.column_name, key=fve.key,
        value=str(fve.value), type=type(fve.value).__name__)


def field_not_nullable(fnn):
    """Creates the message from a peeweeplus.FieldNotNullable error."""

    return FIELD_NOT_NULLABLE.update(
        model=fnn.model.__name__, field=type(fnn.field).__name__,
        attribute=fnn.attribute, column=fnn.field.column_name, key=fnn.key)


def missing_key_error(mke):
    """Creates the message from the peeweeplus.MissingKeyError."""

    return MISSING_KEY_ERROR.update(
        model=mke.model.__name__, field=type(mke.field).__name__,
        attribute=mke.attribute, column=mke.field.column_name, key=mke.key)


def invalid_keys(iks):
    """Creates the message from the peeweeplus.InvalidKeys error."""

    return INVALID_KEYS.update(keys=iks.invalid_keys)


def non_unique_value(nuv):
    """Creates the message from the peeweeplus.NonUniqueValue error."""

    return NON_UNIQUE_VALUE.update(key=nuv.key, value=nuv.value)
