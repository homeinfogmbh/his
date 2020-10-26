/*
    account.js - HOMEINFO Integrated Services account library.

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


function getURL (accountName) {
    const url = BASE_URL + '/account';

    if (accountName == null)
        return url;

    return url + '/' + accountName;
}


/*
    Constructor for a new account object.
*/
export class Account {
    constructor (customer, name, email, passwd = null, user = null) {
        if (customer == null)
            throw 'No customer specified.';

        this.customer = customer;

        if (name == null)
            throw 'No name specified.';

        this.name = name;

        if (email == null)
            throw 'No email address specified.';

        this.email = email;

        if (passwd != null)
            this.passwd = passwd;

        if (user != null)
            this.user = user;
    }
}


/*
    Constructor for an account patch object.
*/
export class AccountPatch {
    constructor (email, passwd, name = null, admin = null, customer = null, user = null, failedLogins = null,
        lockedUntil = null, disabled = null) {
        if (email != null)
            this.email = email;

        if (passwd != null)
            this.passwd = passwd;

        if (name != null)
            this.name = name;

        if (admin != null)
            this.admin = admin;

        if (customer != null)
            this.customer = customer;

        if (user != null)
            this.user = user;

        if (failedLogins != null)
            this.failedLogins = failedLogins;

        if (lockedUntil != null)
            this.lockedUntil = lockedUntil;

        if (disabled != null)
            this.disabled = disabled;
    }
}


/*
    Lists available accounts.
*/
export function list (args) {
    return request.get(getURL(), args);
}


/*
    Gets the specified account.
*/
export function get (name, args) {
    name = name || '!';
    return request.get(getURL(name), args);
};


/*
    Adds an account.
*/
export function add (account, args) {
    return request.post(getURL(), args, account);
};


/*
    Adds an account.
*/
export function patch (name, args, accountPatch) {
    name = name || '!';
    return request.patch(getURL(name), args, accountPatch);
};
