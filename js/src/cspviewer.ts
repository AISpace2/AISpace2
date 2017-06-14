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
var CSPViewerModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
        _model_name: 'CSPViewerModel',
        _view_name: 'CSPViewer',
        _model_module: 'aispace',
        _view_module: 'aispace',
        _model_module_version: '0.1.0',
        _view_module_version: '0.1.0',
        line_width: 2.0
    })
});

// Custom View. Renders the widget model.
var CSPViewer = widgets.DOMWidgetView.extend({
    initialize: function () {
        widgets.DOMWidgetView.prototype.initialize.apply(this, arguments);
        this.eventBus = _.extend({}, Backbone.Events);
        this.visualizer = new CSPGraphInteractor(this.eventBus);
        this.eventBus.listenTo(this.eventBus, 'arc:click', (d: any) => {
            this.send({ event: 'arc:click', constId: d.constId, varId: d.varId });
        });

        this.model.listenTo(this.model, 'msg:custom', (event: Event) => {
            console.log(event);

            if (isHighlightArcEvent(event)) {
                this.visualizer.highlightArc(event.arcId, event.style, event.colour);
            } else if (isSetDomainEvent(event)) {
                this.visualizer.setDomain(event.nodeId, event.domain);
            } else if (isOutputEvent(event)) {
                this.$('#output').text(event.result);
            } else if (isRerenderEvent(event)) {
                this.draw();
                this.model.trigger('msg:custom', { action: 'highlightArc', arcId: null, style: 'normal', colour: 'blue' });
            }
        });
    },
    render: function () {
        this.$el.html('<div id="container"><div id="svg"></div><span id="output"></span></div>');

        // Ensure the DOM element exists (with appropriate sizing) before rendering
        d3.timeout(() => this.model.trigger('msg:custom', {
            action: 'rerender'
        }));

        return this;
    },

    draw: function () {
        this.visualizer.lineWidth = this.model.get('line_width');
        this.visualizer.render(this.model.get('graphJSON'), this.$('#svg')[0]);
    }
});

interface Event {
    action: string;
}

interface CSPHighlightArcEvent extends Event {
    arcId: string;
    style: 'normal' | 'bold';
    colour: string;
}

interface CSPSetDomainEvent extends Event {
    nodeId: string;
    domain: string[];
}

interface OutputEvent extends Event {
    result: string;
}

interface RerenderEvent extends Event {
    result: 'rerender';
}

function isHighlightArcEvent(event: Event): event is CSPHighlightArcEvent {
    return event.action === 'highlightArc';
}

function isSetDomainEvent(event: Event): event is CSPSetDomainEvent {
    return event.action === 'setDomain';
}

function isOutputEvent(event: Event): event is OutputEvent {
    return event.action === 'output';
}

function isRerenderEvent(event: Event): event is RerenderEvent {
    return event.action === 'rerender';
}

module.exports = {
    CSPViewerModel: CSPViewerModel,
    CSPViewer: CSPViewer
};