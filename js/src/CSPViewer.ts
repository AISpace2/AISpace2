import * as Backbone from "backbone";
import * as d3 from "d3";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";

import CSPGraphInteractor from "./CSPGraphInteractor";
import { IGraphJSON } from "./Graph";

import * as template from "./cspviewer.template.html";
import {
    IEvent,
    isBeginFuncEvent,
    isHighlightArcEvent,
    isOutputEvent,
    isRerenderEvent,
    isSetDomainEvent,
} from "./CSPViewerEvents";
import CSPViewerModel from "./CSPViewerModel";

export default class CSPViewer extends widgets.DOMWidgetView {
    private static readonly ARC_CLICK = "arc:click";
    private static readonly FINE_STEP_CLICK = "fine-step:click";
    private static readonly STEP_CLICK = "step:click";
    private static readonly AUTO_STEP_CLICK = "auto-step:click";
    private static readonly BACKTRACK_CLICK = "backtrack:click";

    public model: CSPViewerModel;
    protected visualization: CSPGraphInteractor;

    public initialize(opts: any) {
        super.initialize(opts);

        if (this.model.initial_render) {
            this.send({ event: "initial_render" });
        }

        this.visualization = new CSPGraphInteractor();
        this.visualization.onArcClicked = (varId, constId) => {
            this.send({ event: CSPViewer.ARC_CLICK, constId, varId });
        };

        this.listenTo(this.model, "view:msg", (event: IEvent) => {
            // tslint:disable-next-line:no-console
            console.log(event);

            if (isHighlightArcEvent(event)) {
                this.visualization.highlightArc(event.arcId, event.style, event.colour);
            } else if (isSetDomainEvent(event)) {
                this.visualization.setDomain(event.nodeId, event.domain);
            } else if (isOutputEvent(event)) {
                this.$("#output").text(event.result);
            } else if (isRerenderEvent(event)) {
                this.draw();
                this.model.trigger("msg:custom",
                    { action: "highlightArc", arcId: null, style: "normal", colour: "blue" });
            } else if (isBeginFuncEvent(event)) {
                this.$("#controls").show();
            }
        });
    }

    public events(): Backbone.EventsHash {
        return {
            "click #auto-step": (e) => this.send({ event: CSPViewer.AUTO_STEP_CLICK }),
            "click #fine-step": (e) => this.send({ event: CSPViewer.FINE_STEP_CLICK }),
            "click #step": (e) => this.send({ event: CSPViewer.STEP_CLICK }),

        };
    }

    public render() {
        this.$el.html(template);

        // Ensure the DOM element has been created and sized
        d3.timeout(() => {
            if (this.model.initial_render) {
                this.model.initial_render = false;
                this.model.trigger("msg:custom", { action: "rerender" });
            } else {
                this.draw();
            }
        });

        return this;
    }

    private draw() {
        this.visualization.lineWidth = this.model.lineWidth;
        this.visualization.render(this.model.graphJSON, this.$("#svg")[0]);
    }
}
