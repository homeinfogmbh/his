"""Account related messages."""

from his.messages.common import Message

__all__ = [
    'NoAccountSpecified',
    'NoSuchAccount',
    'AccountLocked',
    'AccountCreated',
    'AccountDeleted',
    'AccountPatched',
    'NotAuthorized',
    'AccountExists',
    'AccountsExhausted',
    'PasswordTooShort']


class _AccountMessage(Message):
    """Abstract common account message."""

    LOCALES = '/etc/his.d/locale/his/account.ini'


class NoAccountSpecified(_AccountMessage):
    """Indicates that no account has been specified."""

    STATUS = 406


class NoSuchAccount(_AccountMessage):
    """Indicates that an account with the specified name does not exist."""

    STATUS = 404


class AccountLocked(_AccountMessage):
    """Indicates that the account is locked."""

    STATUS = 423


class AccountCreated(_AccountMessage):
    """Indicates that the account has been created."""

    STATUS = 201


class AccountDeleted(_AccountMessage):
    """Indicates that the account has been deleted."""

    STATUS = 200


class AccountPatched(_AccountMessage):
    """Indicates that the account has been patched."""

    STATUS = 200


class NotAuthorized(_AccountMessage):
    """Indicates that the an account is not
    authorized to perform the respective action.
    """

    STATUS = 403


class AccountExists(_AccountMessage):
    """Indicates that the respective account already exists."""

    STATUS = 409


class AccountsExhausted(_AccountMessage):
    """Indicates that the respective customer has
    exhauseted their respective account quota.
    """

    STATUS = 402


class PasswordTooShort(_AccountMessage):
    """Indicates that the provided password is too short."""

    STATUS = 415
