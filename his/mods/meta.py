"""HIS meta services"""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import Error, OK, JSON

from his.api import HISService
from his.crypto import load
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
            return Error('No credentials specified.', status=400)
        else:
            try:
                account = Account.get(Account.name == account_name)
            except DoesNotExist:
                return Error('No such account.', status=400)
            else:
                # Verify credentials
                pwmgr = load()

                if pwmgr.verify(passwd, account.pwhash, account.salt):
                    try:
                        session = Session.open(account)
                    except AlreadyLoggedIn:
                        return Error('Already logged in.', status=400)
                    else:
                        return JSON(session.todict())
                else:
                    return Error('Invalid credentials.', status=400)


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
            return Error('No session token specified.', status=400)
        else:
            try:
                session = Session.get(Session.token == session_token)
            except DoesNotExist:
                return Error('No such session.', status=400)
            else:
                if session.active:
                    if session.renew():
                        return JSON(session.todict())
                    else:
                        return Error('Could not renew session.', status=500)
                else:
                    return Error('Session has already expired.', status=400)


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
                return Error('No such session.', status=400)
            else:
                session.close()
                return JSON({'closed': [session.token]})
        elif account_name is not None:
            try:
                account = Account.get(Account.name == account_name)
            except DoesNotExist:
                return Error('No such account.', status=400)
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
            return Error('No session specified.', status=400)
        except DoesNotExist:
            return Error('No such session.', status=400)

        try:
            service_name = self.query_dict['service']
            service = Service.get(Service.name == service_name)
        except KeyError:
            return Error('No service specified.', status=400)
        except DoesNotExist:
            return Error('No such service.', status=400)
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
                            return Error('Invalid customer ID.',
                                         status=400)

                        try:
                            customer = Customer.get(Customer.id == cid)
                        except DoesNotExist:
                            return Error('No such customer.', status=400)

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
                        return Error('You are not an admin.', status=400)
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
