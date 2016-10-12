"""HIS meta services"""

from logging import getLogger

from peewee import DoesNotExist

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import Error, OK, JSON

from his.api.errors import MissingCredentials, NoSuchAccount, \
    NoSessionSpecified, NoSuchSession, SessionExpired, NoServiceSpecified, \
    NoSuchService, InvalidCustomerID, NoSuchCustomer, NotAuthorized
from his.api.handlers import HISService, AuthenticatedService
from his.orm import InconsistencyError, Service, \
    CustomerService, Account, Session

__all__ = [
    'Session',
    'ServicePermissions',
    'install']


logger = getLogger(__file__)


class Session(HISService):
    """Session handling service"""

    NODE = 'session'
    NAME = 'sessions manager'
    DESCRIPTION = 'Manages account sessions'
    PROMOTE = False
    PARAMETER_ERROR = Error(
        'Must specify either account name or session token',
        status=400)

    def get(self):
        """Lists session information"""
        if not self.resource:
            # List all sessions iff specified session is root
            try:
                session = self.params['session']
            except KeyError:
                raise NoSessionSpecified()
            else:
                try:
                    session = Session.get(Session.token == session)
                except DoesNotExist:
                    raise NoSuchSession()
                else:
                    if session.alive:
                        if session.account.root:
                            sessions = {}

                            for session in Session:
                                sessions[session.token] = session.todict()

                            return JSON(sessions)
                        else:
                            raise NotAuthorized()
                    else:
                        raise SessionExpired()
        else:
            # List specific session information
            try:
                session = Session.get(Session.token == self.resource)
            except DoesNotExist:
                raise NoSuchSession()
            else:
                if session.alive:
                    return JSON(session.todict())
                else:
                    raise SessionExpired()

    def post(self):
        """Handles account login requests"""
        if self.resource is not None:
            raise Error('Sub-sessions are not supported')

        # XXX: Currently ignores posted data
        try:
            account = self.params['account']
            passwd = self.params['passwd']
        except KeyError:
            raise MissingCredentials()
        else:
            try:
                account = Account.get(Account.name == account)
            except DoesNotExist:
                raise NoSuchAccount()
            else:
                session = account.login(passwd)
                return JSON(session.todict())

    def put(self):
        """Tries to keep a session alive"""
        if not self.resource:
            raise NoSessionSpecified()

        try:
            session = Session.get(Session.token == self.resource)
        except DoesNotExist:
            raise NoSuchSession()
        else:
            if session.alive:
                if session.renew():
                    return JSON(session.todict())
                else:
                    raise SessionExpired()
            else:
                raise SessionExpired()

    def delete(self):
        """Tries to close a specific session identified by its token or
        all sessions for a certain account specified by its name
        """
        if not self.resource:
            raise NoSessionSpecified()

        try:
            session = Session.get(Session.token == self.resource)
        except DoesNotExist:
            raise NoSuchSession()
        else:
            session.close()
            return JSON({'closed': [session.token]})


class ServicePermissions(AuthenticatedService):
    """Handles service permissions"""

    NODE = 'services'
    NAME = 'services manager'
    DESCRIPTION = 'Manages services permissions'
    PROMOTE = False

    def post(self):
        """Allows services"""
        session = self.session

        try:
            service = Service.get(Service.name == self.params['service'])
        except KeyError:
            raise NoServiceSpecified() from None
        except DoesNotExist:
            raise NoSuchService() from None
        else:
            account = session.account
            customer_id = self.params.get('customer')
            account_name = self.params.get('account')

            if customer_id is not None and account_name is not None:
                return Error('Must specify either customer or accout.',
                             status=400)
            elif customer_id is not None:
                if account.root:
                    try:
                        cid = int(customer_id)
                    except ValueError:
                        raise InvalidCustomerID() from None

                    try:
                        customer = Customer.get(Customer.id == cid)
                    except DoesNotExist:
                        raise NoSuchCustomer() from None

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
                            raise Error('Could not add service.',
                                        status=500)
                    else:
                        return OK('Service already enabled.')
                else:
                    raise Error('You are not a root user.', status=400)
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


install = [Session, ServicePermissions]
