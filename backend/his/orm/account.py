"""User accounts."""

from __future__ import annotations
from datetime import datetime
from email.utils import parseaddr
from typing import Iterable, Iterator, Union

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField

from mdb import Customer
from peeweeplus import InvalidKeys, Argon2Field

from his.exceptions import AccountExistsError, InconsistencyError
from his.messages.account import ACCOUNT_LOCKED
from his.messages.session import INVALID_CREDENTIALS
from his.orm.common import HISModel


__all__ = ['Account']


MAX_FAILED_LOGINS = 5


class Account(HISModel):    # pylint: disable=R0902
    """A HIS account."""

    customer = ForeignKeyField(
        Customer, column_name='customer', backref='accounts')
    name = CharField(64, unique=True)   # Login name.
    full_name = CharField(255, null=True)   # Optional full user name.
    passwd = Argon2Field()
    email = CharField(64, unique=True)
    created = DateTimeField(default=datetime.now)
    deleted = DateTimeField(null=True)
    last_login = DateTimeField(null=True)
    failed_logins = IntegerField(default=0)
    locked_until = DateTimeField(null=True)
    disabled = BooleanField(default=False)
    # Flag, whether the account is an administrator of its customer (=company).
    admin = BooleanField(default=False)
    # Flag, whether the account is root.
    # Such accounts can do ANYTHING!
    root = BooleanField(default=False)

    def __int__(self):
        """Returns the account's ID."""
        return self.id

    def __str__(self):
        """Returns the login name and appropriate customer."""
        return f'{self.name}@{self.customer_id}'

    @classmethod
    def add(cls, customer: Union[Customer, int], name: str, email: str,
            passwd: str, *, full_name: str = None, admin: bool = False,
            root: bool = False):   # pylint: disable=R0913
        """Adds a new account."""
        if len(name) < 3:
            raise ValueError('Account name too short.')

        _, email = parseaddr(email)

        if len(email) < 6 or '@' not in email:
            raise ValueError('Invalid email address.')

        try:
            cls.get(cls.email == email)
        except cls.DoesNotExist:
            pass
        else:
            raise AccountExistsError('email')

        try:
            cls.get(cls.name == name)
        except cls.DoesNotExist:
            pass
        else:
            raise AccountExistsError('name')

        account = cls()
        account.customer = customer
        account.name = name
        account.full_name = full_name
        account.passwd = passwd
        account.email = email
        account.created = datetime.now()
        account.admin = admin
        account.root = root
        return account

    @classmethod
    def admins(cls, customer: Union[Customer, int] = None) -> Iterable[Account]:
        """Yields administrators."""
        if customer is None:
            return cls.select().where(cls.admin == 1)

        return cls.select().where(
            (cls.customer == customer) & (cls.admin == 1))

    @classmethod
    def find(cls, id_or_name: Union[int, str],
             customer: Union[Customer, int] = None) -> Account:
        """Find account by primary key or login name."""
        customer_expr = True if customer is None else cls.customer == customer

        try:
            ident = int(id_or_name)
        except ValueError:
            sel_expr = cls.name == id_or_name
        else:
            sel_expr = cls.id == ident

        return cls.get(customer_expr & sel_expr)

    @property
    def locked(self) -> bool:
        """Determines whether the account is locked."""
        if self.locked_until is None:
            return False

        return self.locked_until >= datetime.now()

    @property
    def unusable(self) -> bool:
        """Determines whether the account is currently unusable."""
        return self.deleted or self.disabled or self.locked

    @property
    def can_login(self) -> bool:
        """Determines whether the account can log in."""
        return not self.unusable and self.failed_logins <= MAX_FAILED_LOGINS

    @property
    def subjects(self) -> Iterator[Account]:
        """Yields accounts this account can manage."""
        cls = type(self)

        if self.root:
            yield from cls
        elif self.admin:
            for account in cls.select().where(cls.customer == self.customer):
                yield account
        else:
            yield self

    @property
    def active(self) -> bool:
        """Determines whether the account has an open session."""
        session = self.sessions.model

        for session in session.select().where(session.account == self):
            if session.alive:
                return True

        return False

    @property
    def info(self) -> dict:
        """Returns brief account information."""
        return {'id': self.id, 'email': self.email}

    @property
    def services(self) -> AccountServicesProxy:
        """Returns an account <> service mapping proxy."""
        return AccountServicesProxy(self)

    def login(self, passwd: str) -> bool:
        """Performs a login."""
        if not self.can_login:
            raise ACCOUNT_LOCKED

        try:
            self.passwd.verify(passwd)
        except VerifyMismatchError:
            self.failed_logins += 1
            self.save()
            raise INVALID_CREDENTIALS from None

        if self.passwd.needs_rehash:
            self.passwd = passwd

        self.failed_logins = 0
        self.last_login = datetime.now()
        self.save()
        return True

    def patch_json(self, json: dict, allow: set = (), **kwargs):
        """Patches the account with fields limited to allow."""
        invalid = {key for key in json if key not in allow} if allow else None

        if invalid:
            raise InvalidKeys(invalid)

        return super().patch_json(json, **kwargs)


class AccountServicesProxy:
    """Proxy to transparently handle an account's services."""

    def __init__(self, account: Account):
        """Sets the respective account."""
        self.account = account

    def __iter__(self):
        """Yields appropriate services."""
        for service in self.services:
            yield service

            for dependency in service.service_deps:
                yield dependency

    @property
    def account_service_model(self):
        """Returns the AccountService model."""
        return self.account.account_services.model

    @property
    def customer_service_model(self):
        """Returns the CustomerService model."""
        return self.account.customer.customer_services.model

    @property
    def services(self):
        """Yields directly assigned services."""
        account_service_model = self.account_service_model

        for account_service in account_service_model.select().where(
                account_service_model.account == self.account):
            yield account_service.service

    def add(self, service) -> bool:
        """Maps a service to this account."""
        account_service_model = self.account_service_model

        if service in self.services:
            return False

        if service in self.customer_service_model.services(
                self.account.customer):
            account_service = account_service_model()
            account_service.account = self.account
            account_service.service = service
            account_service.save()
            return True

        raise InconsistencyError(
            'Cannot enable service {} for account {}, because the '
            'respective customer {} is not enabled for it.'.format(
                service, self.account, self.account.customer))

    def remove(self, service):
        """Removes a service from the account's mapping."""
        account_service_model = self.account_service_model

        for account_service in account_service_model.select().where(
                (account_service_model.account == self.account) &
                (account_service_model.service == service)):
            account_service.delete_instance()
