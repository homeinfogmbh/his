"""HIS services."""

from peewee import BooleanField
from peewee import CharField
from peewee import ForeignKeyField

from his.exceptions import ServiceExistsError
from his.orm.common import HISModel


__all__ = ['Service', 'ServiceDependency', 'ServiceDomain']


class Service(HISModel):
    """Registers services of HIS."""

    name = CharField(32, null=True)
    description = CharField(255, null=True)
    # Flag whether the service shall be promoted.
    promote = BooleanField(default=True)
    # Flag whether the service is locked for maintenance.
    locked = BooleanField(default=False)

    def __str__(self):
        """Returns the service's name."""
        return self.name

    @classmethod
    def add(cls, name, description=None, promote=True):
        """Adds a new service."""
        try:
            cls.get(cls.name == name)
        except cls.DoesNotExist:
            service = cls()
            service.name = name
            service.description = description
            service.promote = promote
            return service

        raise ServiceExistsError()

    @property
    def service_deps(self):
        """Yields dependencies of this service."""
        for service_dependency in self._service_deps:
            dependency = service_dependency.dependency
            yield dependency
            yield from dependency.service_deps


class ServiceDependency(HISModel):
    """Maps service dependencies."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'service_dependency'

    service = ForeignKeyField(
        Service, column_name='service', backref='_service_deps',
        on_delete='CASCADE')
    dependency = ForeignKeyField(
        Service, column_name='dependency', on_delete='CASCADE')


class ServiceDomain(HISModel):
    """Domains for the respective services."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'service_domain'

    service = ForeignKeyField(
        Service, column_name='service', backref='domains', on_delete='CASCADE')
    domain = CharField(255)
