"""Service dependencies."""

from peewee import ForeignKeyField

from his.orm.common import HISModel
from his.orm.service import Service


__all__ = ['ServiceDependency']


class ServiceDependency(HISModel):
    """Maps service dependencies."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'service_dependency'

    service = ForeignKeyField(
        Service, column_name='service', backref='service_dependencies',
        on_delete='CASCADE')
    dependency = ForeignKeyField(
        Service, column_name='dependency', on_delete='CASCADE')
