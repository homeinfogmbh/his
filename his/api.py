"""Meta-services for HIS"""

from json import dumps

from homeinfo.lib.wsgi import OK, RequestHandler

__all__ = ['HISService']


class HISService(RequestHandler):
    """A generic HIS service"""

    pass
