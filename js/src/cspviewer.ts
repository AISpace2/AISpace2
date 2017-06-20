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
            initial_render: true,
            graphJSON: {}
        };
    }

    initialize(attrs: any, opts: any) {
        super.initialize(attrs, opts);

        // Forward message to views
        this.listenTo(this, 'msg:custom', (event: Event) => {
            // We don't register a listener for Python messages (which go to the model) in the view,
            // because each new view would attach a new listener. Instead, we register it once here, and broadcast it to views.
            this.trigger('view:msg', event);
        });
    }

    /** True if this model has not been rendered in any cell yet.
     * 
     * This is used to work around timing issues: when the model is initialized,
     * the views may not be created, so sending a re-render message (to trigger the initial state)
     * doesn't work. Neither does sending a message from Python, for the same reason.
     * Instead, check if a view has rendered this model yet. If not, render the initial state.
     */
    get initial_render(): boolean {
        return this.get('initial_render');
    }

    set initial_render(val: boolean) {
        this.set('initial_render', val);
    }

    /** The base line width of the graph to draw. Bold arcs will be several pixels thicker than this. */
    get lineWidth(): number {
        return this.get('line_width');
    }

    /** The JSON representing the CSP graph. */
    get graphJSON(): GraphJSON {
        return this.get('graphJSON');
    }

    set graphJSON(graph) {
        this.set('graphJSON', graph);
    }
}

export class CSPViewer extends widgets.DOMWidgetView {
    private static readonly ARC_CLICK = 'arc:click';

    model: CSPViewerModel;
    visualization: CSPGraphInteractor;

    initialize(opts: any) {
        super.initialize(opts);

        this.visualization = new CSPGraphInteractor();
        this.visualization.onArcClicked = (varId, constId) => {
            this.send({ event: CSPViewer.ARC_CLICK, constId, varId });
        }

        this.listenTo(this.model, 'view:msg', (event: Event) => {
            console.log(event);

            if (isHighlightArcEvent(event)) {
                this.visualization.highlightArc(event.arcId, event.style, event.colour);
            } else if (isSetDomainEvent(event)) {
                this.visualization.setDomain(event.nodeId, event.domain);
            } else if (isOutputEvent(event)) {
                this.$('#output').text(event.result);
            } else if (isRerenderEvent(event)) {
                this.model.graphJSON = event.graph || this.model.graphJSON;
                this.draw();
                this.model.trigger('msg:custom', { action: 'highlightArc', arcId: null, style: 'normal', colour: 'blue' });
            }
        });
    }

    render() {
        this.$el.html('<div id="container"><div id="svg"></div><span id="output"></span></div>');

        // Ensure the DOM element has been created and sized
        d3.timeout(() => {
            if (this.model.initial_render) {
                this.model.initial_render = false;
                this.model.trigger('msg:custom', { action: 'rerender' });
            } else {
                this.draw();
            }
        });

        return this;
    }

    private draw() {
        this.visualization.lineWidth = this.model.lineWidth;
        this.visualization.render(this.model.graphJSON, this.$('#svg')[0]);
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
    graph?: GraphJSON;
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