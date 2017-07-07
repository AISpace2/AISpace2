import * as Backbone from "backbone";
import * as d3 from "d3";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";
import Vue from "vue";
import * as template from "./cspbuilder.template.html";
import CSPBuilderModel from "./CSPBuilderModel";
import { IEvent } from "./CSPViewerEvents";
import { Graph, IGraphNode } from "./Graph";
declare let Jupyter: any;
import CSPGraphBuilder from "./CSPGraphBuilder.vue";
import GraphVisualizer, { d3ForceLayoutEngine } from "./GraphVisualizer";
import NodeLink from "./NodeLink.vue";
export default class CSPBuilder extends widgets.DOMWidgetView {
    private static readonly SHOW_PYTHON_CODE = "python-code";

    public model: CSPBuilderModel;

    public initialize(opts: any) {
        super.initialize(opts);

        this.listenTo(this.model, "view:msg", (event: IEvent) => {
            if (event.action === CSPBuilder.SHOW_PYTHON_CODE) {
                // Replace cell contents with the code
                Jupyter.notebook.get_selected_cell().set_text((event as any).code);
            }
        });
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
            newGraph.links.push({ source: g.nodes[edge.source], target: g.nodes[edge.dest] });
        }

        const App = Vue.extend({
            components: { CSPGraphBuilder },
            template: '<div id="app"><CSPGraphBuilder :graph="graph"></CSPGraphBuilder></div>',
            data() {
                return {
                    graph: newGraph,
                };
            },
        });

        const app = new App().$mount();
        this.el.appendChild(app.$el);

        return this;
    }
}
