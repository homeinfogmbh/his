"""
Handles the request_uri from the environ dictionary
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['QueryHandler']


class QueryHandler():
    """
    Handles queries
    """
    __PARAM_SEP = '&'
    __ASS_SEP = '='
    __LIST_SEP = ','

    def __init__(self, query):
        """Initializes with a request URI to process"""
        self.__query = query

    @property
    def PARAM_SEP(self):
        """Returns the parameter (= argument) separator"""
        return self.__PARAM_SEP

    @property
    def ASS_SEP(self):
        """Returns the assignment separator"""
        return self.__ASS_SEP

    @property
    def LIST_SEP(self):
        """Returns the list separator"""
        return self.__LIST_SEP

    @property
    def query(self):
        """Returns the request_uri"""
        return self.__query

    @property
    def paramlist(self):
        """Returns a list of parameter assignments"""
        return self.query.split(self.PARAM_SEP)

    @property
    def params(self):
        """Returns a dictionary of {parameter: value}"""
        return {self._key(p): self._val(p) for p in self.paramlist}

    def _key(self, param):
        """Extracts the key of a parameter"""
        return param.split(self.ASS_SEP)[0]

    def _val(self, param):
        """Extracts the value of a parameter"""
        l = param.split(self.ASS_SEP)
        if len(l) > 1:
            return self.__genlist(self.ASS_SEP.join([l[1:]]))
        else:
            return True

    def __genlist(self, s):
        """Generate a list from a string if it
        contains the predefined list separator"""
        l = s.split(self.LIST_SEP)
        if len(l) > 1:
            return l
        else:
            return s
