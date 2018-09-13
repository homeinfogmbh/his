import unittest

from peewee import CharField, BooleanField
from his import orm


class TestService(unittest.TestCase):

    def test_fields(self):
        self.asserIsInstance(orm.Service.name, CharField)
        self.asserIsInstance(orm.Service.description, CharField)
        self.asserIsInstance(orm.Service.description, BooleanField)


if __name__ == '__main__':
    unittest.main()
