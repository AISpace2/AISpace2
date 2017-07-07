import * as Backbone from "backbone";
import * as d3 from "d3";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";
import Vue from "vue";
import CSPGraphInteractor from "./CSPGraphInteractor.vue";
import { Graph, IGraphNode } from "./Graph";
import GraphVisualizer, {d3ForceLayoutEngine} from "./GraphVisualizer";

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
    private app: Vue;
    private g: object;

    public model: CSPViewerModel;
    // protected visualization: CSPGraphInteractor;

    public initialize(opts: any) {
        super.initialize(opts);

        if (this.model.initial_render) {
            this.send({ event: "initial_render" });
        }

        // this.visualization = new CSPGraphInteractor(Graph.fromJSON(this.model.graphJSON));
        // this.visualization.onArcClicked = (varId, constId) => {
        //     this.send({ event: CSPViewer.ARC_CLICK, constId, varId });
        // };
        // this.visualization.onVarClicked = (varId) => {
        //     this.send({ event: CSPViewer.VAR_CLICK, varId });
        // };

        this.listenTo(this.model, "view:msg", (event: IEvent) => {
            // tslint:disable-next-line:no-console
            console.log(event);

            if (isHighlightArcEvent(event)) {
                // this.visualization.highlightArc(event.arcId, event.style, event.colour);
                const i = this.g.links.map((a) => a.id).findIndex((a) => a === event.arcId);
                if (i !== -1) {
                    const stroke = event.colour ? event.colour : this.g.links[i].style.stroke;
                    const strokeWidth = event.style === "bold" ? 7 : 2;
                    Vue.set(this.g.links[i].style, "stroke", stroke);
                    Vue.set(this.g.links[i].style, "strokeWidth", strokeWidth);
                }
            } else if (isSetDomainEvent(event)) {
                // this.visualization.setDomain(event.nodeId, event.domain);
                const i = this.g.nodes.map((a) => a.id).findIndex((a) => a === event.nodeId);

                if (i !== -1) {
                    this.g.nodes[i].domain = event.domain;
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
        const newGraph = {
            links: [] as any[],
            nodes: [] as IGraphNode[],
        };

        const g = Graph.fromJSON(this.model.graphJSON);

        d3ForceLayoutEngine.setup(g, { width: 800, height: 600 } as GraphVisualizer);

        for (const node of Object.values(g.nodes)) {
            newGraph.nodes.push(node);

            if (node.type === "csp:constraint") {
                node.constraint = "lt";
            }
        }

        for (const edge of Object.values(g.edges)) {
            // Find source
            newGraph.links.push({ id: edge.id, source: g.nodes[edge.source], target: g.nodes[edge.dest], style: {} });
        }

        this.g = newGraph;

        const that = this;

        const App = Vue.extend({
            components: { CSPGraphInteractor },
            template: '<div id="app"><CSPGraphInteractor :graph="graph" @click:auto-step="autostep" @click:step="step" @fine-step="finestep" @click:link="link" :output="output"></CSPGraphInteractor></div>',
            data() {
                return {
                    graph: newGraph,
                    output: "",
                };
            },
            methods: {
                autostep() {
                    that.send({ event: CSPViewer.AUTO_STEP_CLICK });
                },
                step() {
                    that.send({ event: CSPViewer.STEP_CLICK });
                },
                finestep() {
                    that.send({ event: CSPViewer.FINE_STEP_CLICK});
                },
                link(l: any) {
                    console.log(l.source.name, l.target.idx);
                    that.send({ event: CSPViewer.ARC_CLICK, varId: l.source.name, constId: l.target.idx });
                },
            },
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
