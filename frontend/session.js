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
    Returns a URL for session queries.
*/
his.session._getUrl = function (token) {
    const url = his.BASE_URL + '/session';

    if (token != null) {
        return url + '/' + token;
    }

    return url;
};


/*
    Opens a session.
*/
his.session.login = function (userName, passwd, args) {
    const url = his.session._getUrl();
    const data = {'account': userName, 'passwd': passwd};
    return his.post(url, args, data);
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
    token = token || '!';
    const url = his.session._getUrl(token);
    return his.get(url, args);
};


/*
    Refreshes a session.
*/
his.session.refresh = function (token, args) {
    token = token || '!';
    const url = his.session._getUrl(token);
    return his.put(url, null, args);
};


/*
    Ends a session.
*/
his.session.close = function (token, args) {
    token = token || '!';
    const url = his.session._getUrl(token);
    return his.delete(url, args);
};
