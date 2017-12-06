"""Account related messages."""

from his.messages.common import Message

__all__ = [
    'NoAccountSpecified',
    'NoSuchAccount',
    'AccountLocked',
    'AccountCreated',
    'AccountDeleted',
    'AccountPatched',
    'NotAuthorized']


class NoAccountSpecified(Message):
    """Indicates that no account has been specified."""

    STATUS = 406


class NoSuchAccount(Message):
    """Indicates that an account with the specified name does not exist."""

    STATUS = 404


class AccountLocked(Message):
    """Indicates that the account is locked."""

    STATUS = 423


class AccountCreated(Message):
    """Indicates that the account has been created."""

    STATUS = 201


class AccountDeleted(Message):
    """Indicates that the account has been deleted."""

    STATUS = 200


class AccountPatched(Message):
    """Indicates that the account has been patched."""

    STATUS = 200


class NotAuthorized(Message):
    """Indicates that the an account is not
    authorized to perform the respective action.
    """

    STATUS = 403
