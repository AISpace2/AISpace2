import * as widgets from 'jupyter-js-widgets';
import * as _ from 'underscore';
import * as Backbone from 'backbone';
import * as d3 from "d3";

import { GraphJSON } from "./Graph";
import { CSPGraphInteractor } from "./GraphVisualizer";

export class CSPViewerModel extends widgets.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: 'CSPViewerModel',
            _view_name: 'CSPViewer',
            _model_module: 'aispace',
            _view_module: 'aispace',
            _model_module_version: '0.1.0',
            _view_module_version: '0.1.0',
        };
    }

    /** The base line width of the graph to draw. Bold arcs will be several pixels thicker than this. */
    get lineWidth(): number {
        return this.get('line_width');
    }

    /** The JSON representing the CSP graph. */
    get graphJSON(): GraphJSON {
        return this.get('graphJSON');
    }
}

export class CSPViewer extends widgets.DOMWidgetView {
    model: CSPViewerModel;
    visualizer: CSPGraphInteractor;
    eventBus: Backbone.Events;

    initialize(opts: any) {
        super.initialize(opts);

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
                this._draw();
                this.model.trigger('msg:custom', { action: 'highlightArc', arcId: null, style: 'normal', colour: 'blue' });
            }
        });
    }

    render() {
        this.$el.html('<div id="container"><div id="svg"></div><span id="output"></span></div>');

        // Ensure the DOM element exists (with appropriate sizing) before rendering
        d3.timeout(() => this.model.trigger('msg:custom', {
            action: 'rerender'
        }));

        return this;
    }

    _draw() {
        this.visualizer.lineWidth = this.model.lineWidth;
        this.visualizer.render(this.model.graphJSON, this.$('#svg')[0]);
    }
}

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