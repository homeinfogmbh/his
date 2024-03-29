"""Error messages and error handlers."""

from argon2.exceptions import VerifyMismatchError
from peewee import IntegrityError

from peeweeplus import FieldNotNullable
from peeweeplus import FieldValueError
from peeweeplus import InvalidKeys
from peeweeplus import MissingKeyError
from peeweeplus import NonUniqueValue
from peeweeplus import PasswordTooShort
from recaptcha import VerificationError
from wsgilib import InvalidData, JSONMessage

from his.exceptions import AccountLimitReached
from his.exceptions import AccountLocked
from his.exceptions import InvalidCredentials
from his.exceptions import NoSessionSpecified
from his.exceptions import NotAuthorized
from his.exceptions import RecaptchaNotConfigured
from his.exceptions import SessionExpired
from his.orm.account import Account
from his.orm.account_service import AccountService
from his.orm.customer_service import CustomerService
from his.orm.customer_settings import CustomerSettings
from his.orm.pwreset import PasswordResetToken
from his.orm.service import Service
from his.orm.service_dependency import ServiceDependency
from his.orm.session import Session


__all__ = ["ERRORS"]


FIELD_NOT_NULLABLE = JSONMessage("Field cannot be NULL.", status=422)
FIELD_VALUE_ERROR = JSONMessage("Invalid value for field.", status=422)
INVALID_CREDENTIALS = JSONMessage("Invalid credentials.", 400)
INVALID_KEYS = JSONMessage("Invalid keys for model.", status=422)
KEY_ERROR = JSONMessage("Missing JSON key.", status=400)
MISSING_KEY_ERROR = JSONMessage("Missing key for field.", status=422)
NON_UNIQUE_VALUE = JSONMessage("Value for field is not unique.", status=422)
NOT_AUTHORIZED = JSONMessage("Not authorized.", status=403)
PASSWORD_TOO_SHORT = JSONMessage("Password too short.", status=415)


ERRORS = {
    Account.DoesNotExist: lambda _: JSONMessage("No such account.", status=404),
    AccountLimitReached: lambda _: JSONMessage("Account limit reached.", status=403),
    AccountLocked: lambda _: JSONMessage("Account locked.", status=423),
    AccountService.DoesNotExist: lambda _: JSONMessage(
        "No such account service.", status=404
    ),
    CustomerService.DoesNotExist: lambda _: JSONMessage(
        "No such customer service.", status=404
    ),
    CustomerSettings.DoesNotExist: lambda _: JSONMessage(
        "No configuration for customer.", status=404
    ),
    FieldNotNullable: lambda error: FIELD_NOT_NULLABLE.update(
        model=error.model.__name__,
        field=type(error.field).__name__,
        attribute=error.attribute,
        column=error.field.column_name,
        key=error.key,
    ),
    FieldValueError: lambda error: FIELD_VALUE_ERROR.update(
        model=error.model.__name__,
        field=type(error.field).__name__,
        attribute=error.attribute,
        column=error.field.column_name,
        key=error.key,
        value=str(error.value),
        type=type(error.value).__name__,
    ),
    IntegrityError: lambda error: JSONMessage(str(error), status=409),
    InvalidCredentials: lambda _: INVALID_CREDENTIALS,
    InvalidData: lambda error: JSONMessage(str(error), status=400),
    InvalidKeys: lambda error: INVALID_KEYS.update(keys=error.invalid_keys),
    MissingKeyError: lambda error: MISSING_KEY_ERROR.update(
        model=error.model.__name__,
        field=type(error.field).__name__,
        attribute=error.attribute,
        column=error.field.column_name,
        key=error.key,
    ),
    NonUniqueValue: lambda error: NON_UNIQUE_VALUE.update(
        key=error.key, value=error.value
    ),
    NoSessionSpecified: lambda _: JSONMessage("No session specified.", status=401),
    NotAuthorized: lambda error: NOT_AUTHORIZED.update(reasons=error.args),
    PasswordResetToken.DoesNotExist: lambda _: JSONMessage("Invalid token.", 400),
    PasswordTooShort: lambda error: PASSWORD_TOO_SHORT.update(minlen=error.minlen),
    RecaptchaNotConfigured: lambda _: JSONMessage(
        "No ReCAPTCHA configured.", status=500
    ),
    Service.DoesNotExist: lambda _: JSONMessage("No such service.", status=404),
    ServiceDependency.DoesNotExist: lambda _: JSONMessage(
        "No such service dependency.", status=404
    ),
    Session.DoesNotExist: lambda _: JSONMessage("No such session.", status=404),
    SessionExpired: lambda _: JSONMessage("Session expired.", status=401),
    VerificationError: lambda _: JSONMessage("ReCAPTCHA challenge failed.", status=400),
    VerifyMismatchError: lambda _: INVALID_CREDENTIALS,
}
