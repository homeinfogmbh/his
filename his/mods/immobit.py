"""A real estate data manipulation library"""

from peewee import DoesNotExist

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import Error, OK, XML, JSON

from openimmo.factories import openimmo, uebertragung, anbieter
from openimmo.openimmo import Umfang

from openimmodb3.db import Immobilie

from his.api.handlers import CheckedAccountService
from his.crypto import load
from his.orm import InconsistencyError, AlreadyLoggedIn, Service, \
    CustomerService, Account, Session


class ImmobitHandler(CheckedAccountService):
    """Handles requests for ImmoBit"""

    PATH = 'immobit'
    NAME = 'ImmoBit'
    DESCRIPTION = 'Immobiliendatenverwaltung'
    PROMOTE = True

    @property
    def filters(self):
        """Returns filters"""
        try:
            filter_str = self.query_dict['filter']
        except KeyError:
            filters = []
        else:
            filters = [f for f in filter_str.split(',') if f]

    def get(self):
        """Handles GET requests"""
        # TODO: Handle filters
        uebertragung_dom = uebertragung(
            self.__class__.NAME,
            'latest',
            'info@homeinfo.de',
            umfang=Umfang.VOLL)
        anbieter_dom = anbieter(repr(self.customer), str(self.customer))

        for immobilie in Immobilie.by_cid(self.customer):
            anbieter_dom.immobilie.append(immobilie.dom)

        return XML(anbieter_dom)
