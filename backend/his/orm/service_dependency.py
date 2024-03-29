"""Service dependencies."""

from typing import Iterator, Union

from peewee import ForeignKeyField

from his.orm.common import HISModel
from his.orm.service import Service


__all__ = ["ServiceDependency"]


class ServiceDependency(HISModel):
    """Maps service dependencies."""

    class Meta:
        table_name = "service_dependency"

    service = ForeignKeyField(
        Service,
        column_name="service",
        backref="service_dependencies",
        on_delete="CASCADE",
        lazy_load=False,
    )
    dependency = ForeignKeyField(
        Service, column_name="dependency", on_delete="CASCADE", lazy_load=False
    )

    @classmethod
    def deps(cls, service: Union[Service, int]) -> Iterator[Service]:
        """Yields all dependencies of a service recursively."""
        dependency = Service.alias()
        select = (
            cls.select(cls, Service, dependency)
            .join(Service, on=cls.service == Service.id)
            .join_from(cls, dependency, on=cls.dependency == dependency.id)
        )

        for service_dependency in select.where(cls.service == service):
            yield service_dependency.dependency
            yield from cls.deps(service_dependency.dependency)
