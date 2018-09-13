import unittest

from peewee import AutoField, CharField, BooleanField, ForeignKeyField, \
    DateTimeField, IntegerField

from his.orm import HISModel, Service, Account
from peeweeplus import Argon2Field


class TestService(unittest.TestCase):

    def test_fields(self):
        self.assertIsInstance(Service.id, AutoField)
        self.assertIsInstance(Service.name, CharField)
        self.assertIsInstance(Service.description, CharField)
        self.assertIsInstance(Service.promote, BooleanField)


class TestAccount(unittest.TestCase):

    def test_fields(self):
        self.assertIsInstance(Account.id, AutoField)
        self.assertIsInstance(Account.customer, ForeignKeyField)
        self.assertIsInstance(Account.name, CharField)
        self.assertIsInstance(Account.passwd, Argon2Field)
        self.assertIsInstance(Account.email, CharField)
        self.assertIsInstance(Account.created, DateTimeField)
        self.assertIsInstance(Account.deleted, DateTimeField)
        self.assertIsInstance(Account.last_login, DateTimeField)
        self.assertIsInstance(Account.failed_logins, IntegerField)
        self.assertIsInstance(Account.locked_until, DateTimeField)
        self.assertIsInstance(Account.disabled, BooleanField)
        self.assertIsInstance(Account.admin, BooleanField)
        self.assertIsInstance(Account.root, BooleanField)


if __name__ == '__main__':
    unittest.main()
