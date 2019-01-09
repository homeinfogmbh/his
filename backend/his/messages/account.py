"""Account related messages."""

from his.messages.api import HISMessage


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


class NoAccountSpecified(HISMessage):
    """Indicates that no account has been specified."""

    STATUS = 406


class NoSuchAccount(HISMessage):
    """Indicates that an account with the specified name does not exist."""

    STATUS = 404


class AccountLocked(HISMessage):
    """Indicates that the account is locked."""

    STATUS = 423


class AccountCreated(HISMessage):
    """Indicates that the account has been created."""

    STATUS = 201


class AccountDeleted(HISMessage):
    """Indicates that the account has been deleted."""

    STATUS = 200


class AccountPatched(HISMessage):
    """Indicates that the account has been patched."""

    STATUS = 200


class NotAuthorized(HISMessage):
    """Indicates that the an account is not
    authorized to perform the respective action.
    """

    STATUS = 403


class AccountExists(HISMessage):
    """Indicates that the respective account already exists."""

    STATUS = 409


class AccountsExhausted(HISMessage):
    """Indicates that the respective customer has
    exhauseted their respective account quota.
    """

    STATUS = 402


class PasswordTooShort(HISMessage):
    """Indicates that the provided password is too short."""

    STATUS = 415
