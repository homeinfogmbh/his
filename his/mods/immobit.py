"""A real estate data manipulation library"""
from peewee import DoesNotExist
from pyxb.exceptions_ import PyXBException

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import Error, OK, XML, JSON

from openimmo import openimmo
from openimmo.factories import anbieter
from openimmo.openimmo import Umfang

from openimmodb3.db import Immobilie

from his.api.handlers import AuthorizedService
from his.orm import InconsistencyError, AlreadyLoggedIn, Service, \
    CustomerService, Account, Session


class ImmoBit(AuthorizedService):
    """Handles requests for ImmoBit"""

    NODE = 'immobit'
    NAME = 'ImmoBit'
    DESCRIPTION = 'Immobiliendatenverwaltung'
    PROMOTE = True

    @property
    def filters(self):
        """Returns filters"""
        try:
            filter_str = self.query_dict['filter']
        except KeyError:
            return []
        else:
            return [f for f in filter_str.split(',') if f]

    @property
    def dom(self):
        """Returns the posted openimmo-compliant DOM"""
        try:
            data = self.file.read()
        except MemoryError:
            # TODO: handle
            pass
        else:
            try:
                return openimmo.CreateFromDocument(data)
            except PyXBException:
                # TODO: Handle
                pass

    def get(self):
        """Handles GET requests"""
        # TODO: Handle filters
        anbieter_dom = anbieter(repr(self.customer), str(self.customer))

        for immobilie in Immobilie.by_cid(self.customer):
            anbieter_dom.immobilie.append(immobilie.dom)

        return XML(anbieter_dom)

    def post(self):
        """Posts real estate data"""
        dom = self.dom

        # TODO: implement DOM validation
        if self.validate(dom, openimmo.immobilie):
            ident = Immobilie.add(self.customer, immobilie)

            if ident:
                return OK(ident)
            else:
                # TODO: handle
                pass
        else:
            # TODO: Raise InvalidDOM()
            pass
