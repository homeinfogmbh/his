"""Data errors."""

from his.messages.facility import HIS_MESSAGE


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
    'non_unique_value',
    'invalid_enum_value']


MISSING_DATA = HIS_MESSAGE('The request is missing data.', status=422)
INCOMPLETE_DATA = HIS_MESSAGE(
    'The data sent in the request is incomplete.', status=422)
INVALID_DATA = HIS_MESSAGE(
    'The data sent in the request is invalid.', status=422)
AMBIGUOUS_DATA = HIS_MESSAGE('Data is ambiguous.', status=422)
NOT_AN_INTEGER = HIS_MESSAGE(
    'The provided value is not an integer.', status=422)
INVALID_CUSTOMER_ID = HIS_MESSAGE(
    'The provided value is not a valid customer ID.', status=422)
FIELD_VALUE_ERROR = HIS_MESSAGE('Invalid value for field.', status=422)
FIELD_NOT_NULLABLE = HIS_MESSAGE('Field cannot be NULL.', status=422)
MISSING_KEY_ERROR = HIS_MESSAGE('Missing key for field.', status=422)
INVALID_KEYS = HIS_MESSAGE('Invalid keys for model.', status=422)
NON_UNIQUE_VALUE = HIS_MESSAGE('Value for field is not unique.', status=422)
INVALID_ENUM_VALUE = HIS_MESSAGE(
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


def invalid_enum_value(iev):
    """Creates a message from a peeweeplus.InvalidEnumerationValue."""

    return INVALID_ENUM_VALUE.update(
        value=iev.value, enum=[value.value for value in iev.enum])
