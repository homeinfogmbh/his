"""HIS messages."""

from his.messages.account import NoAccountSpecified, NoSuchAccount, \
    AccountLocked, AccountCreated, AccountDeleted, AccountPatched, \
    NotAuthorized, AccountExists, AccountsExhausted
from his.messages.api import MessageNotFound, LanguageNotFound, Message
from his.messages.customer import NoCustomerSpecified, NoSuchCustomer, \
    CustomerUnconfigured
from his.messages.data import DataError, MissingData, IncompleteData, \
    InvalidData, NotAnInteger, InvalidCustomerID, InvalidUUID
from his.messages.service import NoServiceSpecified, NoSuchService, \
    ServiceAdded, ServiceAlreadyEnabled, AmbiguousServiceTarget, \
    MissingServiceTarget
from his.messages.session import MissingCredentials, InvalidCredentials, \
    NoSessionSpecified, NoSuchSession, SessionExpired, DurationOutOfBounds

__all__ = [
    'MessageNotFound',
    'LanguageNotFound',
    'Message',
    # Account messages.
    'NoAccountSpecified',
    'NoSuchAccount',
    'AccountLocked',
    'AccountCreated',
    'AccountDeleted',
    'AccountPatched',
    'NotAuthorized',
    'AccountExists',
    'AccountsExhausted',
    # Customer messages.
    'InvalidCustomerID',
    'NoCustomerSpecified',
    'NoSuchCustomer',
    'CustomerUnconfigured',
    # Data messages.
    'DataError',
    'MissingData',
    'IncompleteData',
    'InvalidData',
    'NotAnInteger',
    'InvalidCustomerID',
    'InvalidUUID',
    # Service messages.
    'NoServiceSpecified',
    'NoSuchService',
    'ServiceAdded',
    'ServiceAlreadyEnabled',
    'AmbiguousServiceTarget',
    'MissingServiceTarget',
    # Session messages.
    'MissingCredentials',
    'InvalidCredentials',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',
    'DurationOutOfBounds']
