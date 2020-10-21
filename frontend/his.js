/*
    his.mjs - HOMEINFO Integrated Services API library.

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

    Requires:
        * jquery.js
*/
'use strict';

import { json } from 'https://javascript.homeinfo.de/requests.js';


export const BASE_URL = 'https://his.homeinfo.de';


/*
    Extends a URL with args from an object representing key / value pairs.
*/
function urljoin (url, args) {
    if (args == null)
        return url;

    const parsedArgs = [];

    for (let attribute in args) {
        if (Object.prototype.hasOwnProperty.call(args, attribute)) {
            if (typeof args[attribute] === 'function')
                continue;
            else if (args[attribute] == null)
                parsedArgs.push(attribute);
            else
                parsedArgs.push(attribute + '=' + args[attribute]);
        }
    }

    const string = parsedArgs.join('&');

    if (string)
        return url + '?' + string;

    return url;
}


/*
    Makes an AJAX call to the respective HIS backend.
*/
export const request = {
    get: function (url, args, headers = {}) {
        return json.get(urljoin(url, args), headers);
    },
    post: function (url, data, args, headers = {}) {
        return json.post(urljoin(url, args), data, headers);
    },
    put: function (url, data, args, headers = {}) {
        return json.put(urljoin(url, args), data, headers);
    },
    patch: function (url, data, args, headers = {}) {
        return json.patch(urljoin(url, args), headers);
    },
    delete: function (url, args, headers = {}) {
        return json.delete(urljoin(url, args), headers);
    }
};
