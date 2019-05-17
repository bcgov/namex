var util = require('util');
var events = require('events');
var request = require('request');

function apiPost() {
    events.EventEmitter.call(this);
}

util.inherits(apiPost, events.EventEmitter);

apiPost.prototype.command = function (options, callback) {
    var self = this;
    this.api.perform(function () {
        setTimeout(function () {

        request(options, function (error, response) {
            if (error) {
                console.error(error);
                return;
            }
            if (callback) {
                callback(response);
            }
        });
            self.emit('complete');
        }, 10);
    });
    return this;
};

module.exports = apiPost;