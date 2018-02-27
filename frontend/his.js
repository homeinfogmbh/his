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
  var url = baseUrl + '?session=' + his.session.getToken();

  if (args != null) {
    argsList = []

    for (arg in args) {
      if (args.hasOwnProperty(arg)) {
        var value = args[arg];

        if (value == null) {
          argsList.push(arg)
        } else {
          argsList.push([arg, value].join('='));
        }
      }
    }

    if (argsList.length > 0) {
      return url + '&' + argsList.join('&');
    }
  }

  return url
}


/*
  Updates a basic AJAX query.
*/
his.updateQuery = function (query, method, url, args, data) {
  if (query == null) {
    query = {};
  }

  if (url != null) {
    query.url = his.getUrl(url, args);
  }

  if (method != null) {
    query.type = method;
  }

  if (data != null) {
    query.data = data;
  }

  return query;
}


/*
  Returns a basic AJAX query object containg
  the respective callback methods.
*/
his.makeQuery = function (success, error, statusCode) {
  var query = {};

  if (success != null) {
    query.success = success;
  }

  if (error != null) {
    query.error = error;
  }

  if (statusCode != null) {
    query.statusCode = statusCode;
  }

  return query;
}


/*
  Makes an AJAX call to the respective HIS backend.
*/
his.query = function (method, url, args, data, query) {
  $.ajax(his.updateQuery(query, method, url, args, data));
}


/*
  Makes an POST request to the respective HIS backend.
*/
his.post = function (url, args, data, query) {
  his.query('POST', url, args, data, query);
}


/*
  Makes an GET request to the respective HIS backend.
*/
his.get = function (url, args, query) {
  his.query('GET', url, args, null, query);
}


/*
  Makes an DELETE request to the respective HIS backend.
*/
his.delete = function (url, args, query) {
  his.query('DELETE', url, args, null, query);
}


/*
  Makes an PATCH request to the respective HIS backend.
*/
his.patch = function (url, args, data, query) {
  his.query('PATCH', url, args, data, query);
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
his.setSession = function () {
  localStorage.removeItem('his.session');
}


/*
  HIS session API.
*/
his.session = his.session || {};


/*
  Returns a URL for session queries.
*/
his.session.getUrl = function (endpoint) {
  var url = his.BASE_URL + '/session';

  if (endpoint != null) {
    url += '/' + endpoint;
  }

  return url;
}


/*
  Opens a session.
*/
his.session.login = function (success, error, statusCode) {
  var query = his.makeQuery(
    function (json) {
      his.setSession(json);

      if (success != null) {
        success(json);
      }
    },
    error,
    statusCode
  );
  return function (userName, passwd, args) {
    var data = {'user_name': userName, 'passwd': passwd};
    his.post(his.session.getUrl(), args, JSON.stringify(data), query);
  }
}


/*
  Gets session data.
*/
his.session.get = function (success, error, statusCode) {
  var query = his.makeQuery(success, error, statusCode);
  return function (token, args) {
    var sessionToken = token || his.getSession().token;
    his.post(his.session.getUrl(sessionToken), args, JSON.stringify(data), query);
  }
}
