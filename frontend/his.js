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


his.BASE_URL = 'https://backend.homeinfo.de/his'


/*
  Converts a base URL and optional arguments
  into a full-featured HIS URL.

  The base URL itself must not contain any arguments.
  The args parameter is expected to be a JSON object.
*/
his.getUrl = function (baseUrl, args) {
  if (args != null) {
    argsList = []

    for (arg in args) {
      if (args.hasOwnProperty(arg)) {
        if (args[arg] == null) {
          argsList.push(arg)
        } else {
          argsList.push(arg + '=' +  args[arg]);
        }
      }
    }

    if (argsList.length > 0) {
      return baseUrl + '&' + argsList.join('&');
    }
  }

  return baseUrl
}


/*
  Contructor for an AJAX query.
*/
his.makeQuery = function (method, url, args, data) {
  var query = {
    'type': method,
    'url': his.getUrl(url, args)
  }

  if (data != null) {
    query.data = data;
  }

  console.log('Generated query: ' + JSON.stringify(query));
  return query;
}


/*
  Makes an AJAX call to the respective HIS backend.
*/
his.query = function (method, url, data, args) {
  var ajaxQuery = his.makeQuery(method, url, args, data);
  return $.ajax(ajaxQuery);
}


/*
  Updates a request's arguments to make the request authorized.
  I.e. include the session token.
*/
his.authorized = function (args) {
  if (args != null) {
    if (! args.hasOwnProperty('session')) {
      args.session = his.getSession().token;
    }
  } else {
    args = {'session': his.getSession().token};
  }

  return args;
}


/*
  Makes an GET request to the respective HIS backend.
*/
his.get = function (url, args) {
  return his.query('GET', url, null, args);
}


/*
  Makes an POST request to the respective HIS backend.
*/
his.post = function (url, data, args) {
  return his.query('POST', url, data, args);
}


/*
  Makes an PATCH request to the respective HIS backend.
*/
his.patch = function (url, data, args) {
  return his.query('PATCH', url, data, args);
}


/*
  Makes an PUT request to the respective HIS backend.
*/
his.put = function (url, data, args) {
  return his.query('PUT', url, data, args);
}


/*
  Makes an DELETE request to the respective HIS backend.
*/
his.delete = function (url, args) {
  return his.query('DELETE', url, null, args);
}


/*
  Retrieves the session from local storage.
*/
his.getSession = function () {
  return JSON.parse(localStorage.getItem('his.session'));
}


/*
  Writes the session to local storage.
*/
his.setSession = function (session) {
  localStorage.setItem('his.session', JSON.stringify(session));
}


/*
  Clears the session from the local storage.
*/
his.terminateSession = function () {
  localStorage.removeItem('his.session');
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
