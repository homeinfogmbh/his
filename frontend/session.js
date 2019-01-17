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
    sessionStorage.setItem(his.SESSION_KEY, JSON.stringify(session));
    return session;
};


/*
    Clears the session from the local storage.
*/
his.session._remove = function () {
    const session = his.getSession();
    sessionStorage.removeItem(his.SESSION_KEY);
    return session;
};


/*
    Removes the session from sessionStorage if the session
    termination call failed only because the session has gone.
*/
his.session._handleTerminationError = function (error) {
    // Remove session if session does not exist or is gone.
    if (error.status == 404 || error.status == 410) {
        return Promise.resolve(his.session._remove());
    }

    return Promise.reject(error);
};


/*
    Returns a URL for session queries.
*/
his.session._getUrl = function (sessionToken) {
    const url = his.BASE_URL + '/session';

    if (sessionToken != null) {
        return url + '/' + sessionToken;
    }

    return url;
};


/*
    Opens a session.
*/
his.session.login = function (userName, passwd, args) {
    const url = his.session._getUrl();
    const data = {'account': userName, 'passwd': passwd};
    const promise = his.post(url, args, data);
    return promise.then(his.session._set);
};


/*
    Lists active sessions.
*/
his.session.list = function (args) {
    const url = his.session._getUrl();
    return his.get(url, args);
};


/*
    Gets session data.
*/
his.session.get = function (token, args) {
    const sessionToken = token || '!';
    const url = his.session._getUrl(sessionToken);
    return his.get(url, args);
};


/*
    Refreshes a session.
*/
his.session.refresh = function (token, args) {
    const sessionToken = token || '!';
    const url = his.session._getUrl(sessionToken);
    const promise = his.put(url, null, args);
    return promise.then(his.session._set);
};


/*
    Ends a session.
*/
his.session.close = function (token, args) {
    const sessionToken = token || '!';
    const url = his.session._getUrl(sessionToken);
    const promise = his.delete(url, args);
    return promise.then(his.session._remove, his.session._handleTerminationError);
};
