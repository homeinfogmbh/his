"""Account management"""

from json import loads

from peewee import DoesNotExist

from homeinfo.lib.wsgi import Error, OK, JSON, InternalServerError

from his.api.errors import NoDataProvided, InvalidJSON, NoAccountSpecified, \
    NoSuchAccount, InvalidUTF8Data, NotAuthorized
from his.api.handlers import AuthenticatedService
from his.orm import AccountExists, Account, CustomerSettings


CURRENT_ACCOUNT_SELECTOR = '!'


class AccountService(AuthenticatedService):
    """Service that handles accounts"""

    @property
    def _selected_account(self):
        """Returns the target account"""
        if self.resource is None:
            raise NoAccountSpecified() from None
        else:
            try:
                return Account.get(
                    (Account.name == self.resource) &
                    (Account.customer == self.customer))
            except DoesNotExist:
                raise NoSuchAccount() from None

    @property
    def _json(self):
        """Returns provided JSON data"""
        if self.data is None:
            raise NoDataProvided() from None
        else:
            try:
                text = self.data.decode()
            except ValueError:
                raise InvalidUTF8Data() from None
            else:
                try:
                    return loads(text)
                except AttributeError:
                    raise InvalidJSON() from None

    def _add_account(self, customer):
        """Adds an account for the respective customer"""
        json = self._json

        try:
            name = json['name']
        except KeyError:
            raise Error('No name specified')

        try:
            email = json['email']
        except KeyError:
            raise Error('No email specified')

        try:
            account = Account.add(
                customer, name, email,
                passwd=json.get('passwd'),
                disabled=json.get('disabled'),
                admin=json.get('admin'))
        except ValueError:
            raise InternalServerError('Value error.') from None
        except AccountExists as e:
            raise Error('Account already exists for {}.'.format(e.field),
                        status=409) from None
        else:
            account.save()
            return OK(status=201)

    def _change_account(self, target_account):
        """Change account data"""
        json = self._json

        if self.account.root:
            target_account.patch(json, root=True)
            target_account.save()
            return OK()
        elif self.account.admin:
            if self.account.customer == target_account.customer:
                target_account.patch(json, admin=True)
                target_account.save()
                return OK()
            else:
                raise NotAuthorized()
        else:
            if self.account == target_account:
                target_account.patch(self._json)
                target_account.save()
                return OK()
            else:
                raise NotAuthorized()

    def get(self):
        """List one or many accounts"""
        account = self.account

        if self.resource is None:
            if account.root:
                if self.query.get('customer') is None:
                    return JSON([a.to_dict() for a in Account])
                else:
                    return JSON([a.to_dict() for a in Account.select().where(
                        Account.customer == self.customer)])
            elif account.admin:
                return JSON([a.to_dict() for a in Account.select().where(
                    Account.customer == self.customer)])
            else:
                raise NotAuthorized() from None
        elif self.resource == CURRENT_ACCOUNT_SELECTOR:
            # Account of used session
            return JSON(account.to_dict())
        else:
            selected_account = self._selected_account

            if account.root:
                return JSON(selected_account.to_dict())
            elif account.admin:
                if account.customer == selected_account.customer:
                    return JSON(selected_account.to_dict())
                else:
                    raise NotAuthorized() from None
            elif account == selected_account:
                return JSON(selected_account.to_dict())
            else:
                raise NotAuthorized() from None

    def post(self):
        """Create a new account"""
        account = self.account

        if account.root:
            return self._add_account(self.customer)
        elif account.admin:
            settings = CustomerSettings.of(account.customer)

            if settings.max_accounts is None:
                return self._add_account(self.customer)
            else:
                accounts = len(list(Account.of(account.customer)))

                if accounts < settings.max_accounts:
                    return self._add_account(self.customer)
                else:
                    raise Error('Accounts exhausted.', status=403)
        else:
            raise NotAuthorized() from None

    def patch(self):
        """Modifies an account"""
        if self.resource is None:
            raise NoAccountSpecified() from None
        elif self.resource == CURRENT_ACCOUNT_SELECTOR:
            return self._change_account(self.session.account)
        else:
            return self._change_account(self._selected_account)
