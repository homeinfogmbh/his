'use strict';

var slot = 'his.session';
var urlTemplate = 'https://his.homeinfo.de/session/{0}';
var lifetime = 15;
var cache = new his.cache.CachedEndPoint(slot, urlTemplate, undefined, lifetime);
his.DEBUG = true;

function login () {
    var userName = document.getElementById('userName').value;
    var passwd = document.getElementById('passwd').value;
    return his.session.login(userName, passwd);
}

function queryEndPoint () {
    cache.get('!').then(printEndPoint);
}

function printEndPoint (json) {
    var container = document.getElementById('output');
    container.textContent = JSON.stringify(json, null, 2);
}

function clearCache () {
    cache.clear();
}
