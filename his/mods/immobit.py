"""A real estate data manipulation library"""
from peewee import DoesNotExist
from pyxb.exceptions_ import PyXBException

from homeinfo.crm import Customer
from homeinfo.lib.wsgi import Error, InternalServerError, OK, XML, JSON

from filedb.http import FileError, File

from openimmo import openimmo, factories
from openimmo.openimmo import Umfang

from openimmodb3.db import Immobilie

from his.locale import Language
from his.api.errors import HISMessage
from his.api.handlers import AuthorizedService
from his.orm import InconsistencyError, AlreadyLoggedIn, Service, \
    CustomerService, Account, Session

file_manager = File(KEY)


class InvalidOpenimmoData(HISMessage):
    """Indicates invalid OpenImmo XML data"""

    STATUS = 400
    LOCALE = {
        Language.DE_DE: 'Ungültige OpenImmo Daten.',
        Language.EN_US: 'Invalid OpenImmo data.'}

    def __init__(self, stacktrace, charset='utf-8', cors=None):
        data = {'stacktrace': stacktrace}
        super().__init__(charset=charset, cors=cors, data=data)


class InvalidDOM(HISMessage):
    """Indicates an invalid DOM"""

    STATUS = 400
    LOCALE = {
        Language.DE_DE: 'Ungültiges Dokument-Objekt-Modell.',
        Language.EN_US: 'Invalid document object model.'}


class NoSuchRealEstate(HISMessage):
    """Indicates that the requested real estate does not exist"""

    STATUS = 400
    LOCALE = {
        Language.DE_DE: 'Keine solche Immobilie.',
        Language.EN_US: 'No such real estate.'}

    def __init__(self, objektnr_extern, charset='utf-8', cors=None):
        data = {'objektnr_extern': objektnr_extern}
        super().__init__(charset=charset, cors=cors, data=data)


class RealEstatedAdded(HISMessage):
    """Indicates that a file was successfully added"""

    STATUS = 200
    LOCALE = {
        Language.DE_DE: 'Immobilie erstellt.',
        Language.EN_US: 'Real estate added.'}


class CannotAddRealEstate(HISMessage):
    """Indicates that the respective real estate could not be added"""

    STATUS = 500
    LOCALE = {
        Language.DE_DE: 'Immobilie konnte nicht gespeichert werden.',
        Language.EN_US: 'Could not add real estate.'}


class NoRealEstateSpecified(HISMessage):
    """Indicates that no real estate was specified"""

    STATUS = 400
    LOCALE = {
        Language.DE_DE: 'Keine Immobilie angegeben.',
        Language.EN_US: 'No real estate specified.'}


class CannotDeleteRealEstate(HISMessage):
    """Indicates that the respective real estate could not be deleted"""

    STATUS = 500
    LOCALE = {
        Language.DE_DE: 'Immobilie konnte nicht gelöscht werden.',
        Language.EN_US: 'Could not delete real estate.'}


class RealEstateUpdated(HISMessage):
    """Indicates that the real estate has been updated"""

    STATUS = 200
    LOCALE = {
        Language.DE_DE: 'Immobilie aktualisiert.',
        Language.EN_US: 'Real estate updated.'}


class RealEstateDeleted(HISMessage):
    """Indicates that the real estate has been deleted"""

    STATUS = 200
    LOCALE = {
        Language.DE_DE: 'Immobilie gelöscht.',
        Language.EN_US: 'Real estate deleted.'}


class ImmoBit(AuthorizedService):
    """Handles requests for ImmoBit"""

    NODE = 'immobit'
    NAME = 'ImmoBit'
    DESCRIPTION = 'Immobiliendatenverwaltung'
    PROMOTE = True

    def _validate(self, dom, reference):
        """Validates a DOM against a reference"""
        return isinstance(dom, reference().__class__)

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
            raise InternalServerError() from None
        else:
            try:
                return openimmo.CreateFromDocument(data)
            except PyXBException:
                raise InvalidOpenimmoData(format_exc()) from None

    def post(self):
        """Posts real estate data"""
        dom = self.dom

        # Verify DOM as openimmo.immobilie
        if isinstance(dom, openimmo.immobilie().__class__):
            ident = Immobilie.add(self.customer, dom)

            if ident:
                return RealEstatedAdded()
            else:
                raise CannotAddRealEstate()
        else:
            raise InvalidDOM()

    def get(self):
        """Handles GET requests"""
        if self.resource is None:
            anbieter = factories.anbieter(
                repr(self.customer), str(self.customer))

            for immobilie in Immobilie.by_cid(self.customer):
                anbieter.immobilie.append(immobilie.dom)

            return XML(anbieter)
        else:
            try:
                immobilie = Immobilie.get(
                    (Immobilie.customer == self.customer) &
                    (Immobilie.objektnr_extern == self.resource))
            except DoesNotExist:
                raise NoSuchRealEstate(self.resource) from None
            else:
                return XML(immobilie)

    def put(self):
        """Updates real estates"""
        if self.resource is None:
            raise NoRealEstateSpecified()
        else:
            dom = self.dom

            try:
                immobilie = Immobilie.get(
                    (Immobilie.customer == self.customer) &
                    (Immobilie.objektnr_extern == self.resource))
            except DoesNotExist:
                raise NoSuchRealEstate(self.resource) from None
            else:
                xml_data = immobilie.toxml(encoding='utf-8')

                try:
                    file_id = file_manager.add(xml_data)
                except FileError:
                    raise CannotAddRealEstate() from None
                else:
                    try:
                        file_manager.delete(immobilie.file)
                    except FileError:
                        raise CannotDeleteRealEstate() from None
                    else:
                        immobilie.file= file_id
                        immobilie.save()
                        return RealEstateUpdated()

    def delete(self):
        """Removes real estates"""
        if self.resource is None:
            raise NoRealEstateSpecified()
        else:
            try:
                immobilie = Immobilie.get(
                    (Immobilie.customer == self.customer) &
                    (Immobilie.objektnr_extern == self.resource))
            except DoesNotExist:
                raise NoSuchRealEstate(self.resource) from None
            else:
                try:
                    result = immobilie.remove(portals=True)
                except Exception:
                    result = False

                if result:
                    return RealEstateDeleted()
                else:
                    raise CannotDeleteRealEstate() from None
