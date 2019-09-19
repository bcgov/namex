'use strict';

var _client = require('../client');

var util = require('util');

var events = require('events');

function WaitForXHR() {
    // $FlowFixMe
    events.EventEmitter.call(this);
}

util.inherits(WaitForXHR, events.EventEmitter);

WaitForXHR.prototype.command = function () {
    var urlPattern = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '';
    var delay = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 1000;
    var trigger = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : function () {};
    var callback = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : function () {};

    var command = this;
    var api = this.api;

    this.callback = callback;
    this.urlPattern = urlPattern;

    // console.log('Verifying request ...');
    if (typeof urlPattern === 'string') {
        // throw new Error('urlPattern should be empty, string or regular expression');
    }
    if (typeof trigger !== 'function') {
        throw new Error('trigger should be a function');
    }
    if (typeof callback !== 'function') {
        throw new Error('callback should be a function');
    }

    // console.log('Setting up listening...');
    api.execute(_client.clientListen, [], function (res) {
        // console.warn('Listening XHR requests');
    });

    // console.log('Setting up timeout...');
    this.timeout = setTimeout(function () {
        command.api.execute(_client.clientPoll, [], function (_ref) {
            var xhrs = _ref.value;

            //console.log('xhrss', xhrs);
            var matchingXhrs = xhrs ? xhrs.filter(function (xhr) {
                return xhr.url.match(command.urlPattern);
            }) : [];
            if (matchingXhrs) command.callback(matchingXhrs);else command.client.assertion(false, 'Nothing heard', 'XHR Request', 'No XHR opened with pattern ' + urlPattern + ' !');
            command.emit('complete');
        });
    }, delay);

    // console.log('Handling trigger ...');
    if (trigger) {
        if (typeof trigger === "function") trigger();else if (typeof trigger === "string") api.click(trigger);
    }
    // console.log('Done');
    return this;
};

module.exports = WaitForXHR;