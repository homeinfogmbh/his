"""HIS messages."""

__all__ = [
    'HISServerError',
    'IncompleteImplementationError',

    'ServiceError',
    'ServiceNotRegistered',
    'NoServiceSpecified',
    'NoSuchService',
    'ServiceAdded',

    'HISDataError',
    'NoDataProvided',
    'NotAnInteger',
    'InvalidData',
    'InvalidUTF8Data',
    'InvalidJSON',
    'InvalidCustomerID',

    'HISAPIError',
    'NotAuthorized',
    'LoginError',
    'MissingCredentials',
    'InvalidCredentials',
    'AccountLocked',
    'AlreadyLoggedIn',

    'SessionError',
    'NoSessionSpecified',
    'NoSuchSession',
    'SessionExpired',

    'CustomerError',
    'NoCustomerSpecified',
    'NoSuchCustomer',

    'AccountError',
    'NoAccountSpecified',
    'NoSuchAccount',
    'AccountPatched',

    'BoundaryError',
    'DurationOutOfBounds',

    'AmbiguousTarget',

    'CustomerUnconfigured',
    'InvalidOperation']
