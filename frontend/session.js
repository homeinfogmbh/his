/*
    session.js - HOMEINFO Integrated Services session library.

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
'use strict';

/*
    HIS core namespace.
*/
var his = his || {};


/*
    HIS session API.
*/
his.session = his.session || {};


/*
    Writes the session to local storage.
*/
his.session._set = function (session) {
    localStorage.setItem(his.SESSION_KEY, JSON.stringify(session));
    return session;
};


/*
    Clears the session from the local storage.
*/
his.session._remove = function () {
    var session = his.getSession();
    localStorage.removeItem(his.SESSION_KEY);
    return session;
};


/*
    Removes the session from localStorage if the session
    termination call failed only because the session has gone.
*/
his.session._handleTerminationError = function (error) {
    // Remove session of session does not exist or is gone.
    if (error.status == 404 || error.status == 404) {
        return Promise.resolve(his.session._remove());
    }

    return Promise.reject(error);
};


/*
    Returns a URL for session queries.
*/
his.session._getUrl = function (sessionToken) {
    var url = his.BASE_URL + '/session';

    if (sessionToken != null) {
        url += '/' + sessionToken;
    }

    return url;
};


/*
    Opens a session.
*/
his.session.login = function (userName, passwd, args) {
    var url = his.session._getUrl();
    var credentials = {'account': userName, 'passwd': passwd};
    var data = JSON.stringify(credentials);
    var promise = his.post(url, data, args);
    return promise.then(his.session._set);
};


/*
    Lists active sessions.
*/
his.session.list = function (args) {
    var url = his.session._getUrl();
    return his.get(url, args);
};


/*
    Gets session data.
*/
his.session.get = function (token, args) {
    var sessionToken = token || his.getSessionToken();
    var url = his.session._getUrl(sessionToken);
    return his.get(url, args);
};


/*
    Refreshes a session.
*/
his.session.refresh = function (args) {
    try {
        var sessionToken = his.getSessionToken();
    } catch (error) {
        return Promise.reject(error);
    }

    var url = his.session._getUrl(sessionToken);
    var promise = his.put(url, null, args);
    return promise.then(his.session._set);
};


/*
    Ends a session.
*/
his.session.close = function (args) {
    try {
        var sessionToken = his.getSessionToken();
    } catch (error) {
        return Promise.reject(error);
    }

    var url = his.session._getUrl(sessionToken);
    var promise = his.delete(url, args);
    return promise.then(his.session._remove, his.session._handleTerminationError);
};
