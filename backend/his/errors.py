"""Exception / error handlers."""

from peewee import IntegrityError

from peeweeplus import FieldNotNullable
from peeweeplus import FieldValueError
from peeweeplus import InvalidKeys
from peeweeplus import MissingKeyError
from peeweeplus import NonUniqueValue
from peeweeplus import PasswordTooShortError
from wsgilib import JSONMessage

from his.exceptions import AccountLimitReached
from his.exceptions import AccountLocked
from his.exceptions import AuthenticationError
from his.exceptions import AuthorizationError
from his.exceptions import InconsistencyError
from his.exceptions import InvalidData
from his.exceptions import NoSessionSpecified
from his.exceptions import NotAuthorized
from his.exceptions import SessionExpired
from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.customer_settings import CustomerSettings
from his.orm.pwreset import PasswordResetToken
from his.orm.service import Service
from his.orm.service_dependency import ServiceDependency
from his.orm.session import Session


__all__ = ['ERRORS']


ACCOUNT_LIMIT_REACHED = JSONMessage('Account limit reached.', status=403)
ACCOUNT_LOCKED = JSONMessage('Account locked.', status=423)
CUSTOMER_NOT_CONFIGURED = JSONMessage(
    'No configuration for customer.', status=404)
DURATION_OUT_OF_BOUNDS = JSONMessage('Duration out of bounds.', status=400)
FIELD_NOT_NULLABLE = JSONMessage('Field cannot be NULL.', status=422)
FIELD_VALUE_ERROR = JSONMessage('Invalid value for field.', status=422)
INVALID_CREDENTIALS = JSONMessage('Invalid credentials.', status=401)
INVALID_KEYS = JSONMessage('Invalid keys for model.', status=422)
KEY_ERROR = JSONMessage('Missing JSON key.', status=400)
MISSING_CREDENTIALS = JSONMessage('Missing credentials.', status=401)
MISSING_KEY_ERROR = JSONMessage('Missing key for field.', status=422)
NO_SESSION_SPECIFIED = JSONMessage('No session specified.', status=401)
NO_SUCH_ACCOUNT = JSONMessage('No such account.', status=404)
NO_SUCH_ACCOUNT_SERVICE = JSONMessage('No such account service.', status=404)
NO_SUCH_CUSTOMER_SERVICE = JSONMessage('No such customer service.', status=404)
NO_SUCH_SERVICE = JSONMessage('No such service.', status=404)
NO_SUCH_SERVICE_DEPENDENCY = JSONMessage(
    'No such service dependency.', status=404)
NO_SUCH_SESSION = JSONMessage('No such session.', status=404)
NO_SUCH_TOKEN = JSONMessage('No such token.', status=404)
NON_UNIQUE_VALUE = JSONMessage('Value for field is not unique.', status=422)
NOT_AUTHENTICATED = JSONMessage('Not authenticated.', status=401)
NOT_AUTHORIZED = JSONMessage('Not authorized.', status=403)
PASSWORD_TOO_SHORT = JSONMessage('Password too short.', status=415)
SESSION_EXPIRED = JSONMessage('Session expired.', status=401)


ERRORS = {
    KeyError: lambda error: KEY_ERROR.update(key=str(error)),
    Account.DoesNotExist: lambda _: NO_SUCH_ACCOUNT,
    AccountLimitReached: lambda _: ACCOUNT_LIMIT_REACHED,
    AccountLocked: lambda _: ACCOUNT_LOCKED,
    AccountService.DoesNotExist: lambda _: NO_SUCH_ACCOUNT_SERVICE,
    AuthenticationError: lambda _: NOT_AUTHENTICATED,
    AuthorizationError: lambda _: NOT_AUTHORIZED,
    CustomerService.DoesNotExist: lambda _: NO_SUCH_CUSTOMER_SERVICE,
    CustomerSettings.DoesNotExist: lambda _: CUSTOMER_NOT_CONFIGURED,
    FieldNotNullable: lambda error: FIELD_NOT_NULLABLE.update(
        model=error.model.__name__,
        field=type(error.field).__name__,
        attribute=error.attribute,
        column=error.field.column_name,
        key=error.key
    ),
    FieldValueError: lambda error: FIELD_VALUE_ERROR.update(
        model=error.model.__name__,
        field=type(error.field).__name__,
        attribute=error.attribute,
        column=error.field.column_name,
        key=error.key,
        value=str(error.value),
        type=type(error.value).__name__
    ),
    InconsistencyError: lambda _: NOT_AUTHORIZED,
    IntegrityError: lambda error: JSONMessage(str(error), status=409),
    InvalidData: lambda error: JSONMessage(str(error), status=400),
    InvalidKeys: lambda error: INVALID_KEYS.update(keys=error.invalid_keys),
    MissingKeyError: lambda error: MISSING_KEY_ERROR.update(
        model=error.model.__name__,
        field=type(error.field).__name__,
        attribute=error.attribute,
        column=error.field.column_name,
        key=error.key
    ),
    NonUniqueValue: lambda error: NON_UNIQUE_VALUE.update(
        key=error.key, value=error.value),
    NoSessionSpecified: lambda _: NO_SESSION_SPECIFIED,
    NotAuthorized: lambda _: NOT_AUTHORIZED,
    PasswordResetToken.DoesNotExist: lambda _: NO_SUCH_TOKEN,
    PasswordTooShortError: lambda error: PASSWORD_TOO_SHORT.update(
        minlen=error.minlen),
    Service.DoesNotExist: lambda _: NO_SUCH_SERVICE,
    ServiceDependency.DoesNotExist: lambda _: NO_SUCH_SERVICE_DEPENDENCY,
    Session.DoesNotExist: lambda _: NO_SUCH_SESSION,
    SessionExpired: lambda _: SESSION_EXPIRED,
}
