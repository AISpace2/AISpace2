import * as Backbone from "backbone";
import * as d3 from "d3";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";
import Vue from "vue";
import CSPGraphInteractor from "./CSPGraphInteractor.vue";
import { Graph, ICSPGraphNode } from "./Graph";
import { d3ForceLayoutEngine } from "./GraphLayout";

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
    private static readonly VAR_CLICK = "var:click";

    private static readonly FINE_STEP_CLICK = "fine-step:click";
    private static readonly STEP_CLICK = "step:click";
    private static readonly AUTO_STEP_CLICK = "auto-step:click";
    private static readonly BACKTRACK_CLICK = "backtrack:click";

    public model: CSPViewerModel;

    private app: any;
    private graph: Graph<ICSPGraphNode>;

    // protected visualization: CSPGraphInteractor;

    public initialize(opts: any) {
        super.initialize(opts);

        this.graph = Graph.fromJSON(this.model.graphJSON) as Graph<ICSPGraphNode>;

        // Functions called on the Python backend are queued until first render
        if (this.model.initial_render) {
            this.send({ event: "initial_render" });
        }

        this.listenTo(this.model, "view:msg", (event: IEvent) => {
            // tslint:disable-next-line:no-console
            console.log(event);

            if (isHighlightArcEvent(event)) {
                const i = this.graph.edges.map((a) => a.id).findIndex((a) => a === event.arcId);
                if (i !== -1) {
                    const stroke = event.colour ? event.colour : this.graph.edges[i].style.stroke;
                    const strokeWidth = event.style === "bold" ? 7 : 2;
                    Vue.set(this.graph.edges[i].style, "stroke", stroke);
                    Vue.set(this.graph.edges[i].style, "strokeWidth", strokeWidth);
                }
            } else if (isSetDomainEvent(event)) {
                const i = this.graph.nodes.map((a) => a.id).findIndex((a) => a === event.nodeId);

                if (i !== -1) {
                    this.graph.nodes[i].domain = event.domain;
                }
            } else if (isOutputEvent(event)) {
                this.app.output = event.text;
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
        d3ForceLayoutEngine.setup(this.graph, { width: 800, height: 600 });

        const that = this;

        const App = Vue.extend({
            components: { CSPGraphInteractor },
            data() {
                return {
                    graph: that.graph,
                    output: "",
                };
            },
            methods: {
                autostep() {
                    that.send({ event: CSPViewer.AUTO_STEP_CLICK });
                },
                finestep() {
                    that.send({ event: CSPViewer.FINE_STEP_CLICK});
                },
                link(l: any) {
                    that.send({ event: CSPViewer.ARC_CLICK, varId: l.source.name, constId: l.target.idx });
                },
                step() {
                    that.send({ event: CSPViewer.STEP_CLICK });
                },
            },
            template: `
                <div id="app">
                    <CSPGraphInteractor
                        :graph="graph"
                        @click:auto-step="autostep"
                        @click:step="step"
                        @fine-step="finestep"
                        @click:link="link"
                        :output="output">
                    </CSPGraphInteractor>
                </div>`,
        });

        this.app = new App().$mount();
        this.el.appendChild(this.app.$el);

        return this;
    }

    private draw() {
        // this.visualization.lineWidth = this.model.lineWidth;
        // this.visualization.render(this.$("#svg")[0]);
    }
}
