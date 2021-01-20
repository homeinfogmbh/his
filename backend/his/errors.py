"""Exception error handlers."""

from peeweeplus import FieldNotNullable
from peeweeplus import FieldValueError
from peeweeplus import InvalidKeys
from peeweeplus import MissingKeyError
from peeweeplus import NonUniqueValue
from wsgilib import JSONMessage

from his.exceptions import AuthenticationError
from his.exceptions import AuthorizationError
from his.exceptions import InconsistencyError
from his.exceptions import NoSessionSpecified
from his.exceptions import SessionExpired
from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.pwreset import PasswordResetToken
from his.orm.service import Service
from his.orm.service_dependency import ServiceDependency
from his.orm.service_domain import ServiceDomain
from his.orm.session import Session


__all__ = ['ERRORS']


DURATION_OUT_OF_BOUNDS = JSONMessage('Duration out of bounds.', status=400)
INVALID_CREDENTIALS = JSONMessage('Invalid credentials.', status=401)
KEY_ERROR = JSONMessage('Missing JSON key.', status=400)
MISSING_CREDENTIALS = JSONMessage('Missing credentials.', status=401)
NO_SESSION_SPECIFIED = JSONMessage('No session specified.', status=401)
NO_SUCH_ACCOUNT = JSONMessage('No such account.', status=404)
NO_SUCH_ACCOUNT_SERVICE = JSONMessage('No such account service.', status=404)
NO_SUCH_CUSTOMER_SERVICE = JSONMessage('No such customer service.', status=404)
NO_SUCH_SERVICE = JSONMessage('No such service.', status=404)
NO_SUCH_SERVICE_DEPENDENCY = JSONMessage(
    'No such service dependency.', status=404)
NO_SUCH_SESSION = JSONMessage('No such session.', status=404)
NO_SUCH_TOKEN = JSONMessage('No such token.', status=404)
NOT_AUTHENTICATED = JSONMessage('Not authenticated.', status=401)
NOT_AUTHORIZED = JSONMessage('Not authorized.', status=403)
SESSION_EXPIRED = JSONMessage('Session expired.', status=401)


def field_value_error(fve):
    """Creates a messsage from a peeweeplus.FieldValueError."""

    return FIELD_VALUE_ERROR.update(
        model=fve.model.__name__,
        field=type(fve.field).__name__,
        attribute=fve.attribute,
        column=fve.field.column_name,
        key=fve.key,
        value=str(fve.value),
        type=type(fve.value).__name__
    )


def field_not_nullable(fnn):
    """Creates the message from a peeweeplus.FieldNotNullable error."""

    return FIELD_NOT_NULLABLE.update(
        model=fnn.model.__name__,
        field=type(fnn.field).__name__,
        attribute=fnn.attribute,
        column=fnn.field.column_name,
        key=fnn.key
    )


def missing_key_error(mke):
    """Creates the message from the peeweeplus.MissingKeyError."""

    return MISSING_KEY_ERROR.update(
        model=mke.model.__name__,
        field=type(mke.field).__name__,
        attribute=mke.attribute,
        column=mke.field.column_name,
        key=mke.key
    )


def invalid_keys(iks):
    """Creates the message from the peeweeplus.InvalidKeys error."""

    return INVALID_KEYS.update(keys=iks.invalid_keys)


def non_unique_value(nuv):
    """Creates the message from the peeweeplus.NonUniqueValue error."""

    return NON_UNIQUE_VALUE.update(key=nuv.key, value=nuv.value)


ERRORS = {
    KeyError: lambda error: KEY_ERROR.update(key=str(error)),
    Account.DoesNotExist: lambda _: NO_SUCH_ACCOUNT,
    AccountService.DoesNotExist: lambda _: NO_SUCH_ACCOUNT_SERVICE,
    AuthenticationError: lambda _: NOT_AUTHENTICATED,
    AuthorizationError: lambda _: NOT_AUTHORIZED,
    CustomerService.DoesNotExist: lambda _: NO_SUCH_CUSTOMER_SERVICE,
    FieldNotNullable: field_not_nullable,
    FieldValueError: field_value_error,
    InconsistencyError: lambda _: NOT_AUTHORIZED,
    InvalidKeys: invalid_keys,
    MissingKeyError: missing_key_error,
    NonUniqueValue: non_unique_value,
    NoSessionSpecified: lambda _: NO_SESSION_SPECIFIED,
    PasswordResetToken.DoesNotExist: lambda _: NO_SUCH_TOKEN,
    Service.DoesNotExist: lambda _: NO_SUCH_SERVICE,
    ServiceDependency.DoesNotExist: lambda _: NO_SUCH_SERVICE_DEPENDENCY,
    SessionExpired: lambda _: SESSION_EXPIRED,
}
