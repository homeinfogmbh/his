/*
    his.js - HOMEINFO Integrated Services API library.

    (C) 2017 HOMEINFO - Digitale Informationssysteme GmbH

    This library is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this library.  If not, see <http://www.gnu.org/licenses/>.

    Maintainer: Richard Neumann <r dot neumann at homeinfo period de>

    Requires:
        * jquery.js
*/
'use strict';

/*
    HIS core namespace.
*/
var his = his || {};


his.BASE_URL = 'https://his.homeinfo.de';
his.SESSION_KEY = 'his.session';
his.DEBUG = false;


/*
    Logs debug messages.
*/
his.debug = function (message) {
    if (his.DEBUG) {
        /* eslint-disable no-console */
        console.log('[DEBUG] his: ' + message);
        /* eslint-enable no-console */
    }
};


/*
    Prototype for request arguments.
*/
his._RequestArgs = function (object) {
    if (object != null) {
        for (let attribute in object) {
            if (object.hasOwnProperty(attribute)) {
                this[attribute] = object[attribute];
            }
        }
    }

    this.toString = function () {
        const args = [];

        for (let attribute in this) {
            if (this.hasOwnProperty(attribute)) {
                if (typeof this[attribute] === 'function') {
                    continue;
                } else if (this[attribute] == null) {
                    args.push(attribute);
                } else {
                    args.push(attribute + '=' + this[attribute]);
                }
            }
        }

        const string = args.join('&');

        if (string) {
            return '?' + string;
        }

        return '';
    };
};


/*
    Determines the content type from the given data.
*/
his._getContentType = function (data) {
    if (data instanceof FormData) {
        return 'multipart/form-data';
    } else if (data instanceof File) {
        return 'multipart/form-data';
    } else if (data instanceof Blob) {
        return 'application/octet-stream';
    } else if (typeof data === 'string' || data instanceof String) {
        return 'text/plain';
    } else if (data instanceof Element) {
        return 'text/html';
    } else if (data instanceof Object) {
        return 'application/json';
    }

    return null;
};


/*
    Prototype for an AJAX query.
*/
his._AjaxQuery = function (method, url, args, data, contentType) {
    this.type = method;
    const requestArgs = new his._RequestArgs(args);
    this.url = url + requestArgs;

    if (data != null) {
        this.data = data;

        if (contentType == null) {
            contentType = his._getContentType(data);
        }

        if (contentType == 'application/json' && data instanceof Object) {
            this.data = JSON.stringify(data);
        }
    }

    this.contentType = contentType;
    this.xhrFields = {withCredentials: true};

    this.toString = function () {
        return JSON.stringify(this);
    };
};


/*
    Makes an AJAX call to the respective HIS backend.
*/
his._query = function (method, url, args, data, contentType) {
    const ajaxQuery = new his._AjaxQuery(method, url, args, data, contentType);
    his.debug('Performing ajax query.');
    his.debug(JSON.stringify(ajaxQuery, null, 2));
    return jQuery.ajax(ajaxQuery);
};


/*
    Makes a GET request to the respective HIS backend.
*/
his.get = function (url, args) {
    return his._query('GET', url, args);
};


/*
    Makes a POST request to the respective HIS backend.
*/
his.post = function (url, args, data, contentType) {
    return his._query('POST', url, args, data, contentType);
};


/*
    Makes a PATCH request to the respective HIS backend.
*/
his.patch = function (url, args, data, contentType) {
    return his._query('PATCH', url, args, data, contentType);
};


/*
    Makes a PUT request to the respective HIS backend.
*/
his.put = function (url, args, data, contentType) {
    return his._query('PUT', url, args, data, contentType);
};


/*
    Makes an DELETE request to the respective HIS backend.
*/
his.delete = function (url, args) {
    return his._query('DELETE', url, args);
};


/*
    Retrieves the session from local storage.
*/
his.getSession = function () {
    const sessionString = sessionStorage.getItem(his.SESSION_KEY);

    if (sessionString == null) {
        throw 'Not logged in.';
    }

    return JSON.parse(sessionString);
};


/*
    Safely returns the session token.
*/
his.getSessionToken = function () {
    return his.getSession().token;
};
