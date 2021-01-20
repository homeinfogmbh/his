"""Service dependencies."""

from typing import Iterator, Union

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

    @classmethod
    def tree(cls, service: Union[Service, int]) -> Iterator[Service]:
        """Yields all dependencies of a service recursively."""
        yield service
        dependency = Service.alias()
        condition = cls.service == service
        select = cls.select(cls, Service).join(Service).join_from(
            Service, dependency, on=Service.dependency == dependency.id)

        for service_dependency in select.where(condition):
            yield service_dependency.service
            yield from cls.tree(service_dependency.service)
