"""HIS meta services"""

from peewee import DoesNotExist
from argon2 import VerifyMismatchError, PasswordHasher

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import Error, OK, JSON

from his.api.errors import MissingCredentials, NoSuchAccount, \
    InvalidCredentials, AlreadyLoggedIn as AlreadyLoggedIn_, \
    NoSessionSpecified, NoSuchSession, SessionExpired, NoServiceSpecified, \
    NoSuchService, InvalidCustomerID, NoSuchCustomer, NotAuthorized
from his.api.handlers import HISService
from his.orm import InconsistencyError, AlreadyLoggedIn, Service, \
    CustomerService, Account, Session

__all__ = [
    'LoginHandler',
    'KeepAliveHandler',
    'LogoutHandler',
    'ServicePermissionsHandler',
    'install']


class LoginHandler(HISService):
    """Handles logins"""

    PATH = 'login'
    NAME = 'login manager'
    DESCRIPTION = 'Manages account logins'
    PROMOTE = False

    def get(self):
        """Logs in the user"""
        try:
            account_name = self.query_dict['account']
            passwd = self.query_dict['passwd']
        except KeyError:
            raise MissingCredentials()
        else:
            try:
                account = Account.get(Account.name == account_name)
            except DoesNotExist:
                raise NoSuchAccount()
            else:
                # Verify password with Argon2
                try:
                    ok = PasswordHasher.verify(account.pwhash, password)
                except VerifyMismatchError:
                    ok = False

                if ok:
                    try:
                        session = Session.open(account)
                    except AlreadyLoggedIn:
                        raise AlreadyLoggedIn_()
                    else:
                        return JSON(session.todict())
                else:
                    raise InvalidCredentials()


class KeepAliveHandler(HISService):
    """Handles keepalive requests"""

    PATH = 'keepalive'
    NAME = 'keepalive'
    DESCRIPTION = 'Keeps sessions alive'
    PROMOTE = False

    def get(self):
        """Tries to keep a session alive"""
        try:
            session_token = self.query_dict['session']
        except KeyError:
            raise NoSessionSpecified()
        else:
            try:
                session = Session.get(Session.token == session_token)
            except DoesNotExist:
                raise NoSuchSession()
            else:
                if session.active:
                    if session.renew():
                        return JSON(session.todict())
                    else:
                        raise SessionExpired()
                else:
                    raise SessionExpired()


class LogoutHandler(HISService):
    """Closes sessions"""

    PATH = 'logout'
    NAME = 'logout manager'
    DESCRIPTION = 'Manages account logouts'
    PROMOTE = False

    PARAMETER_ERROR = Error(
        'Must specify either account name or session token', status=400)

    def get(self):
        """Tries to close a specific session identified by its token or
        all sessions for a certain account specified by its name
        """

        session_token = self.query_dict.get('session')
        account_name = self.query_dict.get('account')

        if session_token is not None and account_name is not None:
            return self.PARAMETER_ERROR
        elif session_token is not None:
            try:
                session = Session.get(Session.token == session_token)
            except DoesNotExist:
                raise NoSuchSession()
            else:
                session.close()
                return JSON({'closed': [session.token]})
        elif account_name is not None:
            try:
                account = Account.get(Account.name == account_name)
            except DoesNotExist:
                raise NoSuchAccount()
            else:
                sessions_closed = []

                for session in Session.select().where(
                        Session.account == account):
                    session.close()
                    sessions_closed.append(session.token)

                return JSON({'closed': sessions_closed})
        else:
            return self.PARAMETER_ERROR


class ServicePermissionsHandler(HISService):
    """Handles service permissions"""

    PATH = 'services'
    NAME = 'services manager'
    DESCRIPTION = 'Manages services permissions'
    PROMOTE = False

    def post(self):
        """Allows services"""
        try:
            session_token = self.query_dict['session']
            session = Session.get(Session.token == session_token)
        except KeyError:
            raise NoSessionSpecified()
        except DoesNotExist:
            raise NoSuchSession()

        try:
            service_name = self.query_dict['service']
            service = Service.get(Service.name == service_name)
        except KeyError:
            raise NoServiceSpecified()
        except DoesNotExist:
            raise NoSuchService()
        else:
            if session.active:
                account = session.account
                customer_id = self.query_dict.get('customer')
                account_name = self.query_dict.get('account')

                if customer_id is not None and account_name is not None:
                    return Error('Must specify either customer or accout.',
                                 status=400)
                elif customer_id is not None:
                    if account.root:
                        try:
                            cid = int(customer_id)
                        except ValueError:
                            raise InvalidCustomerID()

                        try:
                            customer = Customer.get(Customer.id == cid)
                        except DoesNotExist:
                            raise NoSuchCustomer()

                        try:
                            CustomerService.get(
                                (CustomerService.customer == customer) &
                                (CustomerService.service == service))
                        except DoesNotExist:
                            customer_service = CustomerService()
                            customer_service.customer = customer
                            customer_service.service = service

                            if customer_service.save():
                                return OK('Service added for customer.')
                            else:
                                return Error('Could not add service.',
                                             status=500)
                        else:
                            return OK('Service already enabled.')
                    else:
                        return Error('You are not a root user.',
                                     status=400)
                elif account_name is not None:
                    if account.admin:
                        try:
                            account = Account.get(
                                Account.name == account_name)
                        except DoesNotExist:
                            return Error('No such account.', status=400)

                        try:
                            account.services.add(service)
                        except InconsistencyError as e:
                            return Error(e.msg, status=400)
                        else:
                            return OK('Service added for account.')
                    else:
                        raise NotAuthorized()
                else:
                    return Error('No customer or accout specified.',
                                 status=400)
            else:
                return Error('Not logged in.', status=400)


install = [
    LoginHandler,
    KeepAliveHandler,
    LogoutHandler,
    ServicePermissionsHandler]
