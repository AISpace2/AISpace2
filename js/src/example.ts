import {
    CSPGraphInteractor
} from "./GraphVisualizer";
var widgets = require('jupyter-js-widgets');
var _ = require('underscore');
var Backbone = require('backbone');
import {
    eventBus
} from './global';
import * as d3 from "d3";

// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var HelloModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
        _model_name: 'HelloModel',
        _view_name: 'HelloView',
        _model_module: 'aispace',
        _view_module: 'aispace',
        _model_module_version: '0.1.0',
        _view_module_version: '0.1.0',
        value: 'Hello World!!!!',
        process_id: 0
    })
});


// Custom View. Renders the widget model.
var HelloView = widgets.DOMWidgetView.extend({
    initialize: function () {
        widgets.DOMWidgetView.prototype.initialize.apply(this, arguments);
        this.eventBus = _.extend({}, Backbone.Events);
        this.visualizer = new CSPGraphInteractor(this.eventBus);
        this.eventBus.listenTo(this.eventBus, 'constraint:click', d => {
            this.send({
                event: 'constraint:click',
                constId: d.constId,
                varId: d.varId
            });
        })
        this.model.listenTo(this.model, 'msg:custom', data => {
            console.log(data)
            if (data.action === 'highlightArc') {
                this.visualizer.highlightArc(data.varName, data.consName, data.style, data.colour);
            } else if (data.action === 'reduceDomain') {
                this.visualizer.reduceDomain(data.nodeName, data.newDomain);
            } else if (data.action === 'output') {
                this.$('#output').text(data.result);
            } else if (data.action === 'rerender') {
                this.value_changed();
                this.model.trigger('msg:custom', {
                    action: 'highlightArc',
                    varName: 'all',
                    consName: 'all',
                    style: '!bold',
                    colour: 'blue'
                })
            }
        });
    },
    render: function () {
        this.model.on('change:value', this.value_changed, this);
        this.listenTo(eventBus[this.model.get('process_id')], 'action:highlightArc', data => {
            if (data.process_id === this.model.get('process_id')) {
                this.visualizer.highlightArc(data.varName, data.consName, data.style, data.colour);
            }
        });
        this.listenTo(eventBus[this.model.get('process_id')], 'action:reduceDomain', data => {
            if (data.process_id === this.model.get('process_id')) {
                this.visualizer.reduceDomain(data.nodeName, data.newDomain);
            }
        });
        this.listenTo(eventBus[this.model.get('process_id')], 'action:output', data => {
            this.$('#output').text(data.text);
        });
        this.$el.html('<div><div id="svg"></div><span id="output"></span></div>');

        d3.timeout(() => this.model.trigger('msg:custom', {
            action: 'rerender'
        }));

        return this;
    },

    value_changed: function () {
        this.visualizer.render(JSON.parse(this.model.get('jsonRepr')), this.$('#svg')[0]);
    }
});


module.exports = {
    HelloModel: HelloModel,
    HelloView: HelloView
};