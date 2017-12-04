"""Account management."""

from peewee import DoesNotExist

from wsgilib import Error, OK, JSON, InternalServerError

from his.api.messages import HISDataError, InvalidData, NoAccountSpecified, \
    NoSuchAccount, NotAuthorized, AccountPatched
from his.api.handlers import AuthenticatedService
from his.orm import AccountExists, AmbiguousDataError, Account, \
    CustomerSettings


CURRENT_ACCOUNT_SELECTOR = '!'


class AccountService(AuthenticatedService):
    """Service that handles accounts."""

    @property
    def selected_account(self):
        """Returns the target account."""
        if self.resource is None:
            raise NoAccountSpecified() from None

        try:
            return Account.get(
                (Account.name == self.resource) &
                (Account.customer == self.customer))
        except DoesNotExist:
            raise NoSuchAccount() from None

    def add_account(self, customer):
        """Adds an account for the respective customer."""
        json = self.data.json

        try:
            name = json['name']
        except KeyError:
            raise Error('No name specified.')

        try:
            email = json['email']
        except KeyError:
            raise Error('No email specified.')

        try:
            account = Account.add(
                customer, name, email, passwd=json.get('passwd'))
        except ValueError:
            raise InternalServerError('Value error.') from None
        except AccountExists as error:
            raise Error('Account already exists for {}.'.format(error.field),
                        status=409) from None
        else:
            account.save()
            return OK(status=201)

    def change_account(self, target_account):
        """Change account data."""
        json = self.data.json

        if self.account.root:
            try:
                target_account.patch(json, root=True)
                target_account.save()
            except (TypeError, ValueError):
                raise InvalidData() from None
            except AmbiguousDataError as error:
                raise HISDataError(field=str(error)) from None

            return AccountPatched()
        elif self.account.admin:
            if self.account.customer == target_account.customer:
                patch_dict = {}
                invalid_keys = []

                # Filter valid options for admins
                for key, value in json.items():
                    if key in ('name', 'passwd', 'email', 'admin'):
                        patch_dict[key] = value
                    else:
                        invalid_keys.append(key)

                try:
                    target_account.patch(patch_dict, admin=True)
                    target_account.save()
                except (TypeError, ValueError):
                    raise InvalidData() from None
                except AmbiguousDataError as error:
                    raise HISDataError(field=str(error)) from None

                if invalid_keys:
                    return AccountPatched(invalid_keys=invalid_keys)

                return AccountPatched()

            raise NotAuthorized() from None
        else:
            if self.session.account == target_account:
                patch_dict = {}
                invalid_keys = []

                # Filter valid options for admins
                for key, value in json.items():
                    if key in ('passwd', 'email'):
                        patch_dict[key] = value
                    else:
                        invalid_keys.append(key)

                try:
                    target_account.patch(patch_dict, admin=True)
                    target_account.save()
                except (TypeError, ValueError):
                    raise InvalidData() from None
                except AmbiguousDataError as error:
                    raise HISDataError(field=str(error)) from None

                if invalid_keys:
                    return AccountPatched(invalid_keys=invalid_keys)

                return AccountPatched()

            raise NotAuthorized() from None

    def get(self):
        """List one or many accounts."""
        account = self.account

        if self.resource is None:
            if account.root:
                if self.query.get('customer') is None:
                    return JSON([a.to_dict() for a in Account])

                return JSON([a.to_dict() for a in Account.select().where(
                    Account.customer == self.customer)])
            elif account.admin:
                return JSON([a.to_dict() for a in Account.select().where(
                    Account.customer == self.customer)])

            raise NotAuthorized() from None
        elif self.resource == CURRENT_ACCOUNT_SELECTOR:
            # Account of used session
            return JSON(account.to_dict())

        selected_account = self.selected_account

        if account.root:
            return JSON(selected_account.to_dict())
        elif account.admin:
            if account.customer == selected_account.customer:
                return JSON(selected_account.to_dict())

            raise NotAuthorized() from None
        elif account == selected_account:
            return JSON(selected_account.to_dict())

        raise NotAuthorized() from None

    def post(self):
        """Create a new account."""
        account = self.account

        if account.root:
            return self.add_account(self.customer)
        elif account.admin:
            settings = CustomerSettings.get(
                CustomerSettings.customer == account.customer)

            if settings.max_accounts is None:
                return self.add_account(self.customer)

            accounts = Account.select().where(
                Account.customer == account.customer)
            accounts = len(tuple(accounts))

            if accounts < settings.max_accounts:
                return self.add_account(self.customer)

            raise Error('Accounts exhausted.', status=403)

        raise NotAuthorized() from None

    def patch(self):
        """Modifies an account."""
        if self.resource is None:
            raise NoAccountSpecified() from None
        elif self.resource == CURRENT_ACCOUNT_SELECTOR:
            return self.change_account(self.session.account)

        return self.change_account(self.selected_account)
