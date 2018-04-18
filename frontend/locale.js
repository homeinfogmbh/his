/*
  locale.js - HOMEINFO Integrated Services locale library.

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
*/
"use strict";

/*
  HIS core namespace.
*/
var his = his || {};


/*
  Locale namespace.
*/
his.locale = his.locale || {};


/*
  Default locale.
*/
his.locale.DEFAULT = 'de_DE';


/*
  Sets the current locale.
*/
his.locale.set = function (locale) {
  localStorage.setItem('his.locale', locale);
}


/*
  Sets the current locale.
*/
his.locale.get = function (locale) {
  var locale = localStorage.getItem('his.locale');

  if (locale == null) {
    return his.locale.DEFAULT;
  }

  return locale;
}


/*
  Deletes the current locale.
*/
his.locale.delete = function (locale) {
  localStorage.removeItem('his.locale');
}
