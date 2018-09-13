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
        * his.js
*/
'use strict';

var his = his || {};
his.cache = his.cache || {};


his.cache.strf = function(template, args) {
    return template.replace(/{(\d+)}/g, function(match, index) {
        return args[index] != null ? args[index] : match;
    });
};


/*
    Callback generator to store the respective
    value using the provided instance and keys.
*/
his.cache.cache = function (cache, identifiers) {
    return function(json) {
        cache.cache(json, ...identifiers);
        return json;
    };
};


/*
    Callback to mark the respective cache as dirty.
*/
his.cache.markDirty = function (cache) {
    return function (result) {
        cache.markDirty();
        return result;
    };
};


/*
    A cache entry.
*/
his.cache.CacheEntry = function (cached, lifetime, value) {
    this.cached = cached;       // Timestamp when the entry was cached.
    this.lifetime = lifetime;   // Lifetime in milliseconds.
    this.value = value;         // Cached JSON value.

    this.getExpiration = function () {
        return this.cached + this.lifetime;
    };

    this.isValid = function () {
        var now = (new Date()).getTime();
        return this.getExpiration() >= now;
    };
};


/*
    Cache prototype.
    Takes a local storarge slot key, a URL template
    and an optional cache lifetime in seconds.
*/
his.cache.CachedEndPoint = function (slot, urlTemplate, authenticated, lifetime) {
    this._slot = slot;
    this._urlTemplate = urlTemplate;

    if (authenticated == null) {
        authenticated = true;
    }

    this._authenticated = authenticated;

    if (lifetime == null) {
        lifetime = 30 * 60;     // 30 minutes in seconds.
    }

    this._lifetime = lifetime * 1000;  // Convert to milliseconds.
    this._dirty = false;

    /*
        Returns the cache's content.
    */
    this._getCache = function () {
        var raw = localStorage.getItem(this._slot);

        if (raw == null) {
            return {};
        }

        var json = JSON.parse(raw);

        if (json == null) {
            return {};
        }

        return json;
    };

    /*
        Returns the cache entry's key.
    */
    this._getKey = function (identifiers) {
        return '[' + identifiers.join(',') + ']';
    };

    /*
        Returns the cached value for the provided keys.
    */
    this._getCacheEntry = function (identifiers) {
        var cache = this._getCache();
        his.debug('Current cache content:\n' + JSON.stringify(cache, null, 2));
        var key = this._getKey(identifiers);
        var rawEntry = cache[key];

        if (rawEntry == null) {
            return null;
        }

        return new his.cache.CacheEntry(rawEntry.cached, rawEntry.lifetime, rawEntry.value);
    };

    /*
        Returns the formatted URL template.
    */
    this._getUrl = function (identifiers) {
        return his.cache.strf(this._urlTemplate, identifiers);
    };

    /*
        Calls the respective HTTP endpoint.
    */
    this._get = function(identifiers, args) {
        var url = this._getUrl(identifiers);

        if (this._authenticated) {
            return his.auth.get(url, args);
        }

        return his.get(url, args);
    };

    /*
        Caches the provided JSON data using the respective keys.
    */
    this.cache = function (json, ...identifiers) {
        var cache = this._getCache();
        var now = (new Date()).getTime();
        var lifetime = this._lifetime;
        var key = this._getKey(identifiers);
        cache[key] = {
            cached: now,
            lifetime: lifetime,
            value: json
        };
        var string = JSON.stringify(cache);
        localStorage.setItem(this._slot, string);
        this._dirty = false;
    };

    /*
        Returns a promise providing the API response for the provided keys.
        If the value is cached and the cache has not timed out,
        it will return the cached value.
        Otherwise it will query the HTTP API and update the cache
        with the value returned by the API.
    */
    this.get = function (...identifiers) {
        var cacheEntry = this._getCacheEntry(identifiers);

        if (cacheEntry != null) {
            if (cacheEntry.isValid() & ! this._dirty) {
                return Promise.resolve(cacheEntry.value);
            }
        }

        return this._get(identifiers).then(his.cache.cache(this, identifiers));
    };

    /*
        Marks the cache as dirty.
    */
    this.markDirty = function () {
        this._dirty = true;
    };

    /*
        Removes all cached data.
    */
    this.clear = function () {
        localStorage.removeItem(this._slot);
    };
};