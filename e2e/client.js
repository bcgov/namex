'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});
var clientListen = exports.clientListen = function clientListen() {
    var getXhr = function getXhr(id) {
        return window.xhrListen.find(function (xhr) {
            return xhr.id === id;
        });
    };
    var rand = function rand() {
        return Math.random() * 16 | 0;
    };
    var uuidV4 = function uuidV4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            return (c === 'x' ? rand() : rand() & 0x3 | 0x8).toString(16);
        });
    };

    window.xhrListen = [];

    if (!XMLHttpRequest.customized) {
        XMLHttpRequest.realSend = XMLHttpRequest.prototype.send;
        XMLHttpRequest.realOpen = XMLHttpRequest.prototype.open;

        XMLHttpRequest.prototype.open = function (method, url) {
            this.id = uuidV4();
            window.xhrListen.push({
                id: this.id,
                method: method,
                url: url,
                openedTime: Date.now()
            });
            this.onload = function () {
                if (this.readyState === XMLHttpRequest.DONE) {
                    var xhr = getXhr(this.id);
                    if (xhr) {
                        xhr.httpResponseCode = this.status;
                        xhr.responseData = this.responseText;
                        xhr.status = this.status === 200 ? 'success' : 'error';
                    }
                }
            };
            XMLHttpRequest.realOpen.apply(this, arguments);
        };
        XMLHttpRequest.prototype.send = function (data) {
            var xhr = getXhr(this.id);
            if (xhr) xhr.requestData = data;

            XMLHttpRequest.realSend.apply(this, arguments);
        };
        XMLHttpRequest.customized = true;
    }
};

var clientPoll = exports.clientPoll = function clientPoll() {
    return window.xhrListen || [];
};