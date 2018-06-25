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
his._debug = function (message) {
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
        for (var attribute in object) {
            if (object.hasOwnProperty(attribute)) {
                this[attribute] = object[attribute];
            }
        }
    }

    this.toString = function () {
        var args = [];

        for (var attribute in this) {
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

        if (args.length > 0) {
            return args.join('&');
        }

        return '';
    };
};


/*
    Prototype for an AJAX query.
*/
his._AjaxQuery = function (method, url, args, data) {
    this.type = method;
    var requestArgs = his._RequestArgs(args).toString();

    if (requestArgs) {
        this.url = url + '?' + requestArgs;
    } else {
        this.url = url;
    }

    if (data != null) {
        if (typeof data === 'string') {
            this.data = data;
        } else {
            this.data = JSON.stringify(data);
        }
    }

    this.toString = function () {
        return JSON.stringify(this);
    };
};


/*
    Makes an AJAX call to the respective HIS backend.
*/
his._query = function (method, url, data, args) {
    var ajaxQuery = new his._AjaxQuery(method, url, args, data);
    his._debug('Performing ajax query.');
    his._debug(ajaxQuery);
    return jQuery.ajax(ajaxQuery);
};


/*
    Updates a request's arguments to make the request authorized.
    I.e. include the session token.
*/
his._authorized = function (args) {
    if (args == null) {
        return {'session': his.getSessionToken()};
    }

    if (! args.hasOwnProperty('session')) {
        args.session = his.getSessionToken();
    }

    return args;
};


/*
    Makes a GET request to the respective HIS backend.
*/
his.get = function (url, args) {
    return his._query('GET', url, null, args);
};


/*
    Makes a POST request to the respective HIS backend.
*/
his.post = function (url, data, args) {
    return his._query('POST', url, data, args);
};


/*
    Makes a PATCH request to the respective HIS backend.
*/
his.patch = function (url, data, args) {
    return his._query('PATCH', url, data, args);
};


/*
    Makes a PUT request to the respective HIS backend.
*/
his.put = function (url, data, args) {
    return his._query('PUT', url, data, args);
};


/*
    Makes an DELETE request to the respective HIS backend.
*/
his.delete = function (url, args) {
    return his._query('DELETE', url, null, args);
};


/*
    Retrieves the session from local storage.
*/
his.getSession = function () {
    var sessionString = sessionStorage.getItem(his.SESSION_KEY);

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


/*
    Authorized requests (with session).
*/
his.auth = his.auth || {};


/*
    Performs an authorized GET request.
*/
his.auth.get = function (url, args) {
    return his.get(url, his._authorized(args));
};


/*
    Performs an authorized POST request.
*/
his.auth.post = function (url, data, args) {
    return his.post(url, data, his._authorized(args));
};


/*
    Performs an authorized PATCH request.
*/
his.auth.patch = function (url, data, args) {
    return his.patch(url, data, his._authorized(args));
};


/*
    Performs an authorized PUT request.
*/
his.auth.put = function (url, data, args) {
    return his.put(url, data, his._authorized(args));
};


/*
    Performs an authorized DELETE request.
*/
his.auth.delete = function (url, args) {
    return his.delete(url, his._authorized(args));
};