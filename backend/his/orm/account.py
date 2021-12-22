"""User accounts."""

from __future__ import annotations
from datetime import datetime
from email.utils import parseaddr
from typing import Union

from argon2.exceptions import VerifyMismatchError
from peewee import JOIN
from peewee import BooleanField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import ModelSelect

from mdb import Company, Customer, Address
from peeweeplus import InvalidKeys, Argon2Field, EMailField, UserNameField

from his.exceptions import AccountLocked
from his.orm.common import HISModel


__all__ = ['Account']


MAX_FAILED_LOGINS = 5


class Account(HISModel):    # pylint: disable=R0902
    """A HIS account."""

    customer = ForeignKeyField(
        Customer, column_name='customer', backref='accounts',
        on_delete='CASCADE', lazy_load=False)
    name = UserNameField(64, unique=True)   # Login name.
    full_name = UserNameField(255, null=True)   # Optional full user name.
    passwd = Argon2Field()
    email = EMailField(64, unique=True)
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

        account = cls(
            customer=customer, name=name, full_name=full_name, passwd=passwd,
            email=email, created=datetime.now(), admin=admin, root=root)
        account.save()
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

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects accounts."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Customer, Company, Address, *args}
        return super().select(*args, **kwargs).join(Customer).join(
            Company).join(Address, join_type=JOIN.LEFT_OUTER)

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
            raise AccountLocked()

        try:
            self.passwd.verify(passwd)
        except VerifyMismatchError:
            self.failed_logins += 1
            self.save()
            raise

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
