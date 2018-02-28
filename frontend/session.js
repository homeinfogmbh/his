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
his.session.login = function (userName, passwd, args, ajaxQuery) {
  var originalSuccessFunction = ajaxQuery.success;

  function wrappedSuccessFunction (json) {
    his.setSession(json);

    if (originalSuccessFunction != null) {
        originalSuccessFunction(json);
    }
  };

  ajaxQuery.success = wrappedSuccessFunction;
  var data = {'user_name': userName, 'passwd': passwd};
  his.post(his.session.getUrl(), JSON.stringify(data), args, ajaxQuery);
}


/*
  Lists active sessions.
*/
his.session.get = function (args, ajaxQuery) {
  his.get(his.session.getUrl(), args, ajaxQuery);
}


/*
  Gets session data.
*/
his.session.get = function (token, args, ajaxQuery) {
  var sessionToken = token || his.getSession().token;
  his.post(his.session.getUrl(sessionToken), null, args, ajaxQuery);
}


/*
  Refreshes a session.
*/
his.session.refresh = function (token, duration, args, ajaxQuery) {
  var sessionToken = token || his.getSession().token;

  if (duration != null) {
    if (args != null) {
      args.duration = duration;
    } else {
      args = {'duration': duration};
    }
  }

  his.put(his.session.getUrl(sessionToken), null, args, ajaxQuery);
}


/*
  Ends a session.
*/
his.session.close = function (args, ajaxQuery) {
  var originalSuccessFunction = ajaxQuery.success;

  function wrappedSuccessFunction (json) {
    his.terminateSession();

    if (originalSuccessFunction != null) {
        originalSuccessFunction(json);
    }
  };

  ajaxQuery.success = wrappedSuccessFunction;
  var sessionToken = his.getSession().token
  his.delete(his.session.getUrl(sessionToken), args, ajaxQuery);
}
