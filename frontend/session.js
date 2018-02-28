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
    * jquery.js
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
  var data = {'user_name': userName, 'passwd': passwd};
  var promise = his.post(his.session.getUrl(), JSON.stringify(data), args, ajaxQuery);
  promise.then(his.setSession);
  return promise;
}


/*
  Lists active sessions.
*/
his.session.get = function (args, ajaxQuery) {
  return his.get(his.session.getUrl(), args, ajaxQuery);
}


/*
  Gets session data.
*/
his.session.get = function (args, ajaxQuery) {
  var sessionToken = his.getSession().token;
  return his.post(his.session.getUrl(sessionToken), null, args, ajaxQuery);
}


/*
  Refreshes a session.
*/
his.session.refresh = function (args, ajaxQuery) {
  var sessionToken = his.getSession().token;
  return his.put(his.session.getUrl(sessionToken), null, args, ajaxQuery);
}


/*
  Ends a session.
*/
his.session.close = function (args, ajaxQuery) {
  var sessionToken = his.getSession().token;
  var promise = his.delete(his.session.getUrl(sessionToken), args, ajaxQuery);
  promise.then(his.terminateSession);
  return promise;
}
