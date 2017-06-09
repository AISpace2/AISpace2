var _ = require('underscore');
var Backbone = require('backbone');

var handler = {
    get: function(target: any, name: string) {
        if (!(name in target)) {
            target[name] = _.extend({}, Backbone.Events);
        }
        
        return target[name];
    }
};

export let eventBus = new Proxy({}, handler);