/*
    account.js - HOMEINFO Integrated Services account library.

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
    HIS account API.
*/
his.account = his.account || {};


/*
    Returns the respective account URL.
*/
his.account._getUrl = function (accountName) {
    var url = his.BASE_URL + '/account';

    if (accountName != null) {
        url += '/' + accountName;
    }

    return url;
};


/*
    Lists available accounts.
*/
his.account.list = function (args) {
    var url = his.account._getUrl();
    return his.auth.get(url, args);
};


/*
    Gets the specified account.
*/
his.account.get = function (name, args) {
    name = name || '!';
    var url = his.account._getUrl(name);
    return his.auth.get(url, args);
};


/*
    Adds an account.
*/
his.account.add = function (account, args) {
    var url = his.account._getUrl();
    var data = JSON.stringify(account);
    return his.auth.post(url, data, args);
};


/*
    Adds an account.
*/
his.account.patch = function (name, args, accountPatch) {
    name = name || '!';
    var url = his.account._getUrl(name);
    var data = JSON.stringify(accountPatch);
    return his.auth.patch(url, data, args);
};


/*
    Constructor for a new account object.
*/
his.account.Account = function (customer, name, email, passwd=null, user=null) {
    if (customer == null) {
        throw 'No customer specified.';
    } else {
        this.customer = customer;
    }

    if (name == null) {
        throw 'No name specified.';
    } else {
        this.name = name;
    }

    if (email == null) {
        throw 'No email address specified.';
    } else {
        this.email = email;
    }

    if (passwd != null) {
        this.passwd = passwd;
    }

    if (user != null) {
        this.user = user;
    }
};


/*
    Constructor for an account patch object.
*/
his.account.AccountPatch = function (email, passwd, name=null, admin=null, customer=null, user=null, failedLogins=null,
    lockedUntil=null, disabled=null) {
    if (email != null) {
        this.email = email;
    }

    if (passwd != null) {
        this.passwd = passwd;
    }

    if (name != null) {
        this.name = name;
    }

    if (admin != null) {
        this.admin = admin;
    }

    if (customer != null) {
        this.customer = customer;
    }

    if (user != null) {
        this.user = user;
    }

    if (failedLogins != null) {
        this.failedLogins = failedLogins;
    }

    if (lockedUntil != null) {
        this.lockedUntil = lockedUntil;
    }

    if (disabled != null) {
        this.disabled = disabled;
    }
};