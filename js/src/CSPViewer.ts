import * as Backbone from "backbone";
import * as d3 from "d3";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";

import CSPGraphInteractor from "./CSPGraphInteractor";
import { Graph } from "./Graph";

import * as template from "./cspviewer.template.html";
import { IEvent, isHighlightArcEvent, isOutputEvent, isRerenderEvent, isSetDomainEvent } from "./CSPViewerEvents";
import CSPViewerModel from "./CSPViewerModel";

export default class CSPViewer extends widgets.DOMWidgetView {
    private static readonly ARC_CLICK = "arc:click";
    private static readonly FINE_STEP_CLICK = "fine-step:click";
    private static readonly STEP_CLICK = "step:click";
    private static readonly AUTO_AC_CLICK = "auto-ac:click";
    private static readonly AUTO_SOLVE_CLICK = "auto-solve:click";
    private static readonly BACKTRACK_CLICK = "backtrack:click";

    public model: CSPViewerModel;
    protected visualization: CSPGraphInteractor;

    public initialize(opts: any) {
        super.initialize(opts);

        this.visualization = new CSPGraphInteractor(Graph.fromJSON(this.model.graphJSON));
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
            }
        });
    }

    public events(): Backbone.EventsHash {
        return {
            "click #auto-ac": (e) => this.send({ event: CSPViewer.AUTO_AC_CLICK }),
            "click #auto-solve": (e) => this.send({ event: CSPViewer.AUTO_SOLVE_CLICK }),
            "click #backtrack": (e) => this.send({ event: CSPViewer.BACKTRACK_CLICK }),
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
        this.visualization.render(this.$("#svg")[0]);
    }
}
