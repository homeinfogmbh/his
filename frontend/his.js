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
"use strict";

/*
  HIS core namespace.
*/
var his = his || {};


his.BASE_URL = 'https://his.homeinfo.de'
his.SESSION_KEY = 'his.session';


/*
  HIS URL arguments class.
*/
his._argsToString = function (object) {
  if (object == null) {
    return '';
  }

  var args = []

  for (var attribute in object) {
    if (object.hasOwnProperty(attribute)) {
      if (object[attribute] == null) {
        args.push(attribute)
      } else {
        args.push(attribute + '=' + object[attribute]);
      }
    }
  }

  if (args.length > 0) {
    return args.join('&');
  }

  return '';
}

/*
  Converts a base URL and optional arguments
  into a full-featured HIS URL.

  The base URL itself must not contain any arguments.
  The args parameter is expected to be a JSON object.
*/
his._getUrl = function (baseUrl, args) {
  if (args != null) {
    return baseUrl + '?' + his._argsToString(args);
  }

  return baseUrl;
}


/*
  Contructor for an AJAX query.
*/
his._AjaxQuery = function (method, url, args, data) {
  this.type = method;
  this.url = his._getUrl(url, args);

  if (data != null) {
    this.data = data;
  }
}


/*
  Makes an AJAX call to the respective HIS backend.
*/
his._query = function (method, url, data, args) {
  var ajaxQuery = new his._AjaxQuery(method, url, args, data);
  return jQuery.ajax(ajaxQuery);
}


/*
  Updates a request's arguments to make the request authorized.
  I.e. include the session token.
*/
his.authorized = function (args) {
  if (args == null) {
    return {'session': his.getSessionToken()};
  }

  if (! args.hasOwnProperty('session')) {
    args.session = his.getSessionToken();
  }

  return args;
}


/*
  Makes an GET request to the respective HIS backend.
*/
his.get = function (url, args) {
  return his._query('GET', url, null, args);
}


/*
  Makes an POST request to the respective HIS backend.
*/
his.post = function (url, data, args) {
  return his._query('POST', url, data, args);
}


/*
  Makes an PATCH request to the respective HIS backend.
*/
his.patch = function (url, data, args) {
  return his._query('PATCH', url, data, args);
}


/*
  Makes an PUT request to the respective HIS backend.
*/
his.put = function (url, data, args) {
  return his._query('PUT', url, data, args);
}


/*
  Makes an DELETE request to the respective HIS backend.
*/
his.delete = function (url, args) {
  return his._query('DELETE', url, null, args);
}


/*
  Retrieves the session from local storage.
*/
his.getSession = function () {
  var sessionString = localStorage.getItem(his.SESSION_KEY);

  if (sessionString == null) {
    throw 'Not logged in.';
  }

  return JSON.parse(sessionString);
}


/*
  Safely returns the session token.
*/
his.getSessionToken = function () {
  return his.getSession().token;
}


/*
  Authorized requests (with session).
*/
his.auth = his.auth || {};


/*
  Performs an authorized GET request.
*/
his.auth.get = function (url, args) {
  return his.get(url, his.authorized(args));
}


/*
  Performs an authorized POST request.
*/
his.auth.post = function (url, data, args) {
  return his.post(url, data, his.authorized(args));
}


/*
  Performs an authorized PATCH request.
*/
his.auth.patch = function (url, data, args) {
  return his.patch(url, data, his.authorized(args));
}


/*
  Performs an authorized PUT request.
*/
his.auth.put = function (url, data, args) {
  return his.put(url, data, his.authorized(args));
}


/*
  Performs an authorized DELETE request.
*/
his.auth.delete = function (url, args) {
  return his.delete(url, his.authorized(args));
}
