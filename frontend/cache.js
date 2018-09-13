/*
    cache.js - HOMEINFO Integrated Services caching library.

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
        * jquery.js
*/
'use strict';

var his = his || {};
his.cache = his.cache || {};


his.cache.strf = function(template, ...args) {
    for (var i = 0; i < args.length; i++) {
        console.log('Arg #' + i + ': ' + args[i]);
    }

    return template.replace(/{(\d+)}/g, function(match, index) {
        return args[index] != null ? args[index] : match;
    });
};


/*
    Callback generator to store the respective
    value using the provided instance and keys.
*/
his.cache.cache = function (instance, ...keys) {
    return function(json) {
        instance.cache(json, ...keys);
        return json;
    };
};


/*
    A cache entry.
*/
his.cache.CacheEntry = function (cached, lifetime, value) {
    this.cached = cached;       // Timestamp when the entry was cached.
    this.lifetime = lifetime;   // Lifetime in milliseconds.
    this.value = value;         // Cached JSON value.

    this.isValid = function () {
        var now = (new Date()).getTime();
        return this.cached + this.lifetime <= now;
    };
};


/*
    Cache prototype.
    Takes a local storarge slot key, a URL template
    and an optional cache lifetime in seconds.
*/
his.cache.CachedEndPoint = function (slot, urlTemplate, lifetime) {
    this.slot = slot;
    this.urlTemplate = urlTemplate;

    if (lifetime == null) {
        lifetime = 30 * 60 * 1000;  // 30 minutes in milliseconds.
    }

    this.lifetime = lifetime * 1000;  // Convert to milliseconds.
    this.dirty = false;

    /*
        Returns the key path for localStorage.
    */
    this._getKey = function (...keys) {
        var key;

        if (keys.length > 1) {
            key = '(' + keys.join(',') + ')';
        } else {
            key = keys[0];
        }

        return this.slot + '.' + key;
    };

    /*
        Returns the cached value for the provided keys.
    */
    this._getCached = function (...keys) {
        var raw = localStorage.getItem(this._getKey(...keys));

        if (raw == null) {
            return null;
        }

        var json = JSON.parse(raw);

        if (json == null) {
            return null;
        }

        return his.cache.CacheEntry(json.cached, json.lifetime, json.value);
    };

    /*
        Calls the respective endpoint.
    */
    this._getHttp = function(...keys) {
        var url = his.cache.strf(this.urlTemplate, ...keys);
        return jQuery.ajax({url: url, method: 'GET', dataType: 'json'});
    };

    /*
        Caches the provided JSON data using the respective keys.
    */
    this.cache = function (json, ...keys) {
        var lifetime = this.lifetime;
        var record = {
            cached: (new Date()).getTime(),
            lifetime: lifetime,
            value: json
        };

        var string = JSON.stringify(record);
        var key = this._getKey(...keys);
        localStorage.setItem(key, string);
    };

    /*
        Returns a promise providing the API response for the provided keys.
        If the value is cached and the cache has not timed out,
        it will return the cached value.
        Otherwise it will query the HTTP API and update the cache
        with the value returned by the API.
    */
    this.get = function (...keys) {
        var cacheEntry = this._getCached(...keys);

        if (cacheEntry.isValid() & ! this.needsRefresh()) {
            return Promise.resolve(cacheEntry.value);
        }

        return this._getHttp(...keys).then(his.cache.cache(this, ...keys));
    };
};