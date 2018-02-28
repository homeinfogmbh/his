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
    * jquery.js
*/
"use strict";

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
his.account.getUrl = function (accountName) {
  var url = his.BASE_URL + '/session';

  if (accountName != null) {
    url += '/' + accountName;
  }

  return url;
}


/*
  Lists available accounts.
*/
his.account.list = function (args, ajaxQuery) {
  his.auth.get(his.account.getUrl(), args, ajaxQuery);
}


/*
  Gets the specified account.
*/
his.account.get = function (name, args, ajaxQuery) {
  his.auth.get(his.account.getUrl(name), args, ajaxQuery);
}


/*
  Adds an account.
*/
his.account.add = function (account, args, ajaxQuery) {
  his.auth.post(his.account.getUrl(), JSON.stringify(account), args, ajaxQuery);
}


/*
  Adds an account.
*/
his.account.patch = function (name, account, args, ajaxQuery) {
  his.auth.patch(his.account.getUrl(name), JSON.stringify(account), args, ajaxQuery);
}


/*
  Constructor for a new account object.
*/
his.account.Account = function (customer, name, email, /**/ passwd, user) {
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
}


/*
  Constructor for an account patch object.
*/
his.account.AccountPatch = function (
    /* Allowed by all accounts. */
    email, passwd,
    /* Additionally allowed by admins. */
    name, admin,
    /* Allowed by root users only.*/
    customer, user, failedLogins, lockedUntil, disabled) {
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
}
