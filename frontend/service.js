/*
  service.js - HOMEINFO Integrated Services service library.

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
"use strict";

/*
  HIS core namespace.
*/
var his = his || {};


/*
  HIS service API.
*/
his.service = his.service || {};


/*
  Returns the respective service URL.
*/
his.service.getUrl = function (endpoint) {
  var url = his.BASE_URL + '/service';

  if (endpoint != null) {
    url += '/' + endpoint;
  }

  return url;
}


/*
  Lists available services.
*/
his.service.list = function (service, args) {
  var url = his.service.getUrl();
  return his.auth.get(url, args);
}


/*
  Lists customer services.
*/
his.service.listAccountServices = function (service, args) {
  var url = his.service.getUrl('customer');
  return his.auth.get(url, args);
}


/*
  Lists account services.
*/
his.service.listAccountServices = function (service, args) {
  var url = his.service.getUrl('account');
  return his.auth.get(url, args);
}


/*
  Adds a customer or account services.
*/
his.service.add = function (service, args) {
  var url;

  if (service.hasOwnProperty('customer')) {
    url = his.service.getUrl('customer');
  } else if (service.hasOwnProperty('account')) {
    url = his.service.getUrl('account');
  }

  return his.auth.post(url, data, args);
}
