"""HTTP response classes"""

from html import escape

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '08.10.2014'
__all__ = ['render', 'Status', 'ContentType', 'HTTPResponse']


# TODO: Replace with homeinfolib.http

def render(renderable, json=False):
    """Renders a renderable object"""
    return renderable.__json__() if json else renderable.__xml__()


class Status():
    """
    HTTP status codes
    """
    OK = '200 OK'


class ContentType():
    """
    A content type library
    """
    TEXT_HTML = 'text/html'
    TEXT_PLAIN = 'text/plain'
    APPLICATION_XML = 'application/xml'


class HTTPResponse():
    """
    Generates an HTTP response
    """
    def __init__(self, content, content_type=ContentType.APPLICATION_XML,
                 charset='UTF-8', status=Status.OK):
        """
        Create a new HTTP response
        """
        self.__content = content
        self.__content_type = content_type
        self.__charset = charset
        self.__status = status

    @property
    def content(self):
        """Returns the content"""
        return self.__content

    @content.setter
    def content(self, content):
        """
        Sets the content
        """
        self.__content = content

    @property
    def content_type(self):
        """
        Returns the content type
        """
        return self.__content_type

    @property
    def charset(self):
        """Returns the character set"""
        return self.__charset

    @property
    def status(self):
        """The status code"""
        return self.__status

    @property
    def body(self):
        """
        Returns the body
        """
        if self.content_type in ['text/html']:
            return ''.join['<!DOCTYPE html>\n<html>\n\t<body>',
                           self._htmlcontent,
                           '\n\t</body>\n</html>']

    @property
    def length(self):
        """Determines the length of the effective content (body)"""
        return ('Content-Length', str(len(self.body)))

    @property
    def headers(self):
        """Returns the headers"""
        return [('Content-Type',
                 ''.join([self.content_type,
                          '; charset=', self.charset])),
                self.length]

    @property
    def _htmlcontent(self):
        """
        Returns the content formatted as HTML
        """
        return escape(self.content).encode('utf-8', 'xmlcharrefreplace')

    def __render__(self):
        """Render the data"""
        return self.status, self.headers, self.body
