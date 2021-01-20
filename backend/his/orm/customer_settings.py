"""Customer settings."""

from peewee import ForeignKeyField, IntegerField

from filedb import File
from mdb import Customer

from his.orm.common import HISModel


__all__ = ['CustomerSettings']


class CustomerSettings(HISModel):
    """Settings for a certain customer."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'customer_settings'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE',
        lazy_load=False)
    max_accounts = IntegerField(null=True, default=10)
    logo = ForeignKeyField(File, column_name='logo', null=True)
