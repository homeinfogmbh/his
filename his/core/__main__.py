"""
CREAM's main handler
"""
class Cream():
    """
    Common real estate advanced manager
    """
    __customer = None
    __REQ_INIT = '?'    # Request initialization separator
    __REQ_SEP = '&'     # Request element separator
    __REQ_ASS = '='     # Request assignment separator
    __LIST_SEP = ','    # List element separator
    
    def __init__(self, customer):
        """
        Create a new instance of cream for a certain customer
        """
        self.__customer = customer
        
    def terminate(self):
        """
        Terminate the given instance
        """
        self = None # XXX: Is this really what we want?
        return True
        
    @property
    def customer(self):
        """
        Returns the customer
        """
        return self.__customer
    
    def handle(self, environ, start_response):
        """
        Handle a request for WSGI application-like arguments
        """
        headers, bodies, status = self.__handle(environ)
        start_response(status, headers)
        return bodies
    
    def __handle(self, environ):
        """
        Handle CGI-like environment dictionary
        """
        headers = []
        bodies = []
        status = '200 OK'
        method = environ['REQUEST_METHOD']
        path, request = self.__parse(environ['REQUEST_URI'])
        # TODO: implement
        return headers, bodies, status
    
    def __parse(self, request_uri):
        """
        Parses a request URI into a dictionary
        """
        request = {}
        try:
            path, req = self.__REQ_INIT.join(request_uri.split(self.__REQ_INIT))
        except:
            print('Invalid request: ' + str(request_uri))
        else:
            req_ass = req.split(self.__REQ_SEP)
            for r in req_ass:
                try:
                    field, raw_value = r.split(self.__REQ_ASS)
                except:
                    print('Invalid reuest assignment: ' + str(r))
                else:
                    val_list = raw_value.split(self.__LIST_SEP)
                    if len(val_list) > 1:
                        value = [e for e in val_list if e != '']
                    else:
                        value = raw_value
                    request[field] = value
        return path, request