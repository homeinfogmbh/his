"""HIS services."""

from __future__ import annotations

from peewee import BooleanField
from peewee import CharField

from his.exceptions import ServiceExistsError
from his.orm.common import HISModel


__all__ = ["Service"]


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
    def add(cls, name: str, description: str = None, promote: bool = True) -> Service:
        """Adds a new service."""
        try:
            cls.get(cls.name == name)
        except cls.DoesNotExist:
            service = cls(name=name, description=description, promote=promote)
            service.save()
            return service

        raise ServiceExistsError()
