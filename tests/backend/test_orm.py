import unittest

from peewee import CharField, BooleanField
from his import orm


class TestService(unittest.TestCase):

    def test_fields(self):
        self.assertIsInstance(orm.Service.name, CharField)
        self.assertIsInstance(orm.Service.description, CharField)
        self.assertIsInstance(orm.Service.description, BooleanField)


if __name__ == '__main__':
    unittest.main()
