import unittest

from peewee import CharField, BooleanField
from his.orm import Service


class TestService(unittest.TestCase):

    def test_fields(self):
        self.assertIsInstance(Service.name, CharField)
        self.assertIsInstance(Service.description, CharField)
        self.assertIsInstance(Service.promote, BooleanField)


if __name__ == '__main__':
    unittest.main()
