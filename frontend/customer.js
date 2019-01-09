/*
    customer.js - HOMEINFO Integrated Services customer library.

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
    HIS customer API.
*/
his.customer = his.customer || {};


/*
    Returns the respective customer URL.
*/
his.customer._getUrl = function (customerName) {
    var url = his.BASE_URL + '/customer';

    if (customerName != null) {
        url += '/' + customerName;
    }

    return url;
};


/*
    Returns the respective customer.
*/
his.customer.get = function (customer, args) {
    if (customer == null) {
        customer = '!';
    }

    var url = his.customer._getUrl(customer);
    return his.get(url, args);
};


/*
    Returns the current customer's logo.
*/
his.customer.logo = function (args) {
    var url = his.BASE_URL + '/customer-logo';
    return his.get(url, args);
};
