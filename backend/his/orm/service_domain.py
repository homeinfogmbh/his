"""Service domains."""

from peewee import CharField, ForeignKeyField

from his.orm.common import HISModel
from his.orm.service import Service


__all__ = ['ServiceDomain']


class ServiceDomain(HISModel):
    """Domains for the respective services."""

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'service_domain'

    service = ForeignKeyField(
        Service, column_name='service', backref='domains', on_delete='CASCADE')
    domain = CharField(255)
