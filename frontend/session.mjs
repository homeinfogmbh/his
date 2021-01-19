/*
    session.js - HOMEINFO Integrated Services session library.

    (C) 2017-2020 HOMEINFO - Digitale Informationssysteme GmbH

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
*/
'use strict';


import { BASE_URL, request } from './his.mjs';


function getURL (token) {
    const url = BASE_URL + '/session';

    if (token == null)
        return url;

    return url + '/' + token;
}


export function login (userName, passwd, args, headers = {}) {
    const url = getURL();
    const data = {'account': userName, 'passwd': passwd};
    return request.post(url, data, args, headers);
}

/*
    Lists active sessions.
*/
export function list (args, headers = {}) {
    const url = getURL();
    return request.get(url, args, headers);
}

/*
    Gets session data.
*/
export function get (token, args, headers = {}) {
    token = token || '!';
    const url = getURL(token);
    return request.get(url, args, headers);
}

/*
    Refreshes a session.
*/
export function refresh (token, args, headers = {}) {
    token = token || '!';
    const url = getURL(token);
    return request.put(url, null, args, headers);
}

/*
    Ends a session.
*/
export function close (token, args, headers = {}) {
    token = token || '!';
    const url = getURL(token);
    return request.delete(url, args, headers);
}
