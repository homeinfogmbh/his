"""User accounts."""

from __future__ import annotations
from datetime import datetime
from email.utils import parseaddr
from typing import Union

from argon2.exceptions import VerifyMismatchError
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import ModelSelect

from mdb import Company, Customer
from peeweeplus import InvalidKeys, Argon2Field

from his.exceptions import AccountExistsError
from his.messages.account import ACCOUNT_LOCKED
from his.messages.session import INVALID_CREDENTIALS
from his.orm.common import HISModel


__all__ = ['Account']


MAX_FAILED_LOGINS = 5


class Account(HISModel):    # pylint: disable=R0902
    """A HIS account."""

    customer = ForeignKeyField(
        Customer, column_name='customer', backref='accounts', lazy_load=False)
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
            root: bool = False) -> Account:
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
    def admins(cls, customer: Union[Customer, int] = None) -> ModelSelect:
        """Yields administrators."""
        condition = cls.admin == 1

        if customer is not None:
            condition &= cls.customer == customer

        select = cls.select(cls, Customer, Company)
        select = select.join(Customer).join(Company)
        return select.where(condition)

    @classmethod
    def find(cls, id_or_name: Union[int, str],
             customer: Union[Customer, int, None] = None) -> Account:
        """Find account by primary key or login name."""
        condition = True if customer is None else cls.customer == customer

        try:
            ident = int(id_or_name)
        except ValueError:
            condition &= cls.name == id_or_name
        else:
            condition &= cls.id == ident

        select = cls.select(cls, Customer, Company)
        select = select.join(Customer).join(Company)
        return select.where(condition).get()

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
    def subjects(self) -> ModelSelect:
        """Yields accounts this account can manage."""
        cls = type(self)
        condition = cls.customer == self.customer
        select = cls.select(cls, Customer, Company)
        select = select.join(Customer).join(Company)

        if self.root:
            return select.where(True)

        if not self.admin:
            condition &= cls.id == self.id

        return select.where(condition)

    @property
    def info(self) -> dict:
        """Returns brief account information."""
        return {'id': self.id, 'email': self.email}

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

    def patch_json(self, json: dict, allow: set = (), **kwargs) -> None:
        """Patches the account with fields limited to allow."""
        invalid = {key for key in json if key not in allow} if allow else None

        if invalid:
            raise InvalidKeys(invalid)

        return super().patch_json(json, **kwargs)
