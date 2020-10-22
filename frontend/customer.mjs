/*
    customer.js - HOMEINFO Integrated Services customer library.

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
        * his.js
*/
'use strict';


import { BASE_URL, request } from './his.mjs';


/*
    Returns the respective customer URL.
*/
function getURL (customerName) {
    const url = BASE_URL + '/customer';

    if (customerName == null)
        return url;

    return url + '/' + customerName;
}


/*
    Returns the respective customer.
*/
export function get (customer, args) {
    customer = customer || '!';
    return request.get(getURL(customer), args);
}


/*
    Returns the current customer's logo.
*/
export function logo (args) {
    return request.get(BASE_URL + '/customer-logo', args);
}
