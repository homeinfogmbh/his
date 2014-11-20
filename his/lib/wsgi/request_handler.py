"""
Handles the request_uri from the environ dictionary
"""
from string import printable

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '25.09.2014'
__all__ = ['InvalidURI', 'RequestHandler']


class InvalidURI(Exception):
    """
    Indicate an invalid URI
    """
    pass


class RequestHandler():
    """
    Handles requests
    """
    __PATH_SEP = '/'
    __REQ_SEP = '?'
    __PARAM_SEP = '&'
    __ASS_SEP = '='
    __LIST_SEP = ','

    def __init__(self, request_uri,
                 min_path_len=None, max_path_len=None,
                 min_argc=None, max_argc=None,
                 min_list_len=None, max_list_len=None,
                 valid_chars=None, invalid_chars=None):
        """Initializes with a request URI to process"""
        self.__request_uri = request_uri
        self.extensive_validate(request_uri,
                                min_path_len=min_path_len,
                                max_path_len=max_path_len,
                                min_argc=min_argc,
                                max_argc=max_argc,
                                min_list_len=min_list_len,
                                max_list_len=max_list_len,
                                valid_chars=valid_chars,
                                invalid_chars=invalid_chars)

    def validate(self, request_uri):
        """Validate a request_uri"""
        return self.__validate(request_uri)

    def extensive_validate(self, request_uri,
                           min_path_len=None, max_path_len=None,
                           min_argc=None, max_argc=None,
                           min_list_len=None, max_list_len=None,
                           valid_chars=None, invalid_chars=None):
        """validate a request URI more thoroughly"""
        return self.validate(request_uri) \
            and self.__extensive_validate(request_uri,
                                          min_path_len=min_path_len,
                                          max_path_len=max_path_len,
                                          min_argc=min_argc,
                                          max_argc=max_argc,
                                          min_list_len=min_list_len,
                                          max_list_len=max_list_len,
                                          valid_chars=valid_chars,
                                          invalid_chars=invalid_chars)

    @property
    def PATH_SEP(self):
        """Returns the path separator"""
        return self.__PATH_SEP

    @property
    def REQ_SEP(self):
        """Returns the request separator"""
        return self.__REQ_SEP

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
    def request_uri(self):
        """Returns the request_uri"""
        return self.__request_uri

    @property
    def path_req(self):
        """Returns a list of [path, requests]"""
        return self.request_uri.split(self.REQ_SEP)

    @property
    def path(self):
        """Returns the path of the request_uri"""
        return self.path_req[0].split(self.PATH_SEP)

    @property
    def request(self):
        """Returns the request of the request_uri"""
        return self.path_req[1]

    @property
    def paramlist(self):
        """Returns a list of parameter assignments"""
        return self.request.split(self.PARAM_SEP)

    @property
    def params(self):
        """Returns a dictionary of {parameter: value}"""
        return {self._key(p): self._val(p) for p in self.paramlist}

    @property
    def valid_chars(self):
        """Returns a string of valid characters"""
        return printable.strip()    # @UndefinedVariable

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
        """Generate a list from a string if it \
        contains the predefined list separator"""
        l = s.split(self.LIST_SEP)
        if len(l) > 1:
            return l
        else:
            return s

    def __validate(self, request_uri):
        """Actually validates a request URI"""
        # Checks for invalid characters
        remainder = request_uri
        for c in self.valid_chars:
            remainder = remainder.replace(c, '')
        if remainder != '':
            raise InvalidURI('Request contains invalid characters: '
                             + remainder)
        else:
            # Checks for correct structure
            l = request_uri.split(self.REQ_SEP)
            if len(l) > 2:
                raise InvalidURI('Request URI contains more than one '
                                 + self.REQ_SEP)
            else:
                return True

    def __extensive_validate(self, request_uri,
                             min_path_len=None, max_path_len=None,
                             min_argc=None, max_argc=None,
                             min_list_len=None, max_list_len=None,
                             valid_chars=None, invalid_chars=None):
        """Perform extensive request validation"""
        # Checks for valid characters
        if valid_chars is not None:
            remainder = request_uri
            for v in self.valid_chars:
                remainder = remainder.replace(v, '')
            if remainder != '':
                raise InvalidURI('Request contains invalid characters: '
                                 + remainder)
        # Check for invalid characters
        if invalid_chars is not None:
            for i in invalid_chars:
                if i in request_uri:
                    raise InvalidURI('Request contains invalid character: '
                                     + i)
        l = request_uri.split(self.REQ_SEP)
        uri = l[0]
        path = uri.split(self.PATH_SEP)
        # Checks minimal path length
        if min_path_len is not None:
            if len(path) < min_path_len:
                raise InvalidURI('Request URI path is too short: '
                                 + str(len(path)) + '/' + str(min_path_len))
        # Checks maximum path length
        if max_path_len is not None:
            if len(path) > max_path_len:
                raise InvalidURI('Request URI path is too long: '
                                 + str(len(path)) + '/' + str(max_path_len))
        if len(l) > 1:
            params = self.REQ_SEP.join(l[1:]).split(self.PARAM_SEP)
            # Checks minimal argument count
            if min_argc is not None:
                if len(params) < min_argc:
                    raise InvalidURI('Request URI has too few arguments: '
                                     + str(len(params)) + '/' + str(min_argc))
            # Checks maximum argument count
            if max_argc is not None:
                if len(params) > max_argc:
                    raise InvalidURI('Request URI has too much arguments: '
                                     + str(len(params)) + '/' + str(max_argc))
            for p in params:
                ass = p.split(self.ASS_SEP)
                val = self.ASS_SEP.join(ass[1:]) if len(ass) > 1 else None
                if val is not None:
                    lst = val.split(self.LIST_SEP)
                    # Checks minimal list length
                    if min_list_len is not None:
                        if len(lst) < min_list_len:
                            raise InvalidURI('Request URI parameter contains '
                                             'a too short list: '
                                             + str(len(lst)) + '/'
                                             + str(min_list_len))
                    # Checks maximum list length
                    if max_list_len is not None:
                        if len(lst) > max_list_len:
                            raise InvalidURI('Request URI parameter contains '
                                             'a too long list: '
                                             + str(len(lst)) + '/'
                                             + str(max_list_len))
        return True


class LoginHandler():
    """
    Handles user logins
    """
    def __init__(self, requests):
        """Initializes with a request dictionary"""
        self.__user_name = requests.get('user_name', None)
        self.__password = requests.get('passwd', None)
