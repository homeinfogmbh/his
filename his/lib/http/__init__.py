"""
OAuth provider implementation
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '08.10.2014'

from html import escape

class HTTPResponse():
    """
    Generates an HTTP response
    """
    __HTML_TRANS = {}
    __content_type = {}
    __charset = ''
    __content = ''
    
    def __init__(self, content_type='text/html', charset='UTF-8'):
        """
        Create a new HTTP response
        """
        self.__content_type = content_type
        self.__charset = charset
        
    @property
    def content_type(self):
        """
        Returns the content type with character set
        """
        return {'Content-Type': self._raw_content_type 
                + '; charset=' + self.charset}
    
    @property
    def charset(self):
        """
        Returns the character set
        """
        return self.__charset
    
    @property
    def content(self):
        """
        Returns the content
        """
        return self.__content
    
    @content.setter
    def content(self, content):
        """
        Sets the content
        """
        self.__content = content
        
    @property
    def body(self):
        """
        Returns the body
        """
        if self.content_type in ['text/html']:
            begin = '<!DOCTYPE html>\n<html>\n\t<body>'
            end = '\n\t</body>\n</html>'
            return begin + self._htmlcontent + end
    
    #===========================================================================
    # Protected methods
    #===========================================================================        
    @property
    def _raw_content_type(self):
        """
        Returns the content type
        """
        return self.__content_type
    
    @property
    def _content_len(self):
        """
        Determines the length of the effective content (body)
        """
        return {'Content-Length': str(len(self.body))}
    
    @property
    def _headers(self):
        """
        Returns the headers
        """
        return self.content_type.update(self._content_len)
    
    @property
    def _htmlcontent(self):
        """
        Returns the content formatted as HTML
        """
        return escape(self.content).encode('utf-8', 'xmlcharrefreplace')