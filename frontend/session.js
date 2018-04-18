/*
  his.js - HOMEINFO Integrated Services session library.

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
    * his.js
*/
"use strict";

/*
  HIS core namespace.
*/
var his = his || {};


/*
  HIS session API.
*/
his.session = his.session || {};


/*
  Returns a URL for session queries.
*/
his.session.getUrl = function (sessionToken) {
  var url = his.BASE_URL + '/session';

  if (sessionToken != null) {
    url += '/' + sessionToken;
  }

  return url;
}


/*
  Opens a session.
*/
his.session.login = function (userName, passwd, args) {
  var url = his.session.getUrl();
  var credentials = {'account': userName, 'passwd': passwd};
  var data = JSON.stringify(credentials);
  var promise = his.post(url, data, args);
  return promise.then(his.setSession);
}


/*
  Lists active sessions.
*/
his.session.list = function (args) {
  var url = his.session.getUrl();
  return his.get(url, args);
}


/*
  Gets session data.
*/
his.session.get = function (token, args) {
  var sessionToken = token || his.getSessionToken();
  var url = his.session.getUrl(sessionToken);
  return his.get(url, args);
}


/*
  Refreshes a session.
*/
his.session.refresh = function (args) {
  var sessionToken = his.getSessionToken();
  var url = his.session.getUrl(sessionToken);
  var promise = his.put(url, null, args);
  return promise.then(his.setSession);
}


/*
  Ends a session.
*/
his.session.close = function (args) {
  var sessionToken = his.getSessionToken();
  var url = his.session.getUrl(sessionToken);
  var promise = his.delete(url, args);
  return promise.then(his.terminateSession);
}
