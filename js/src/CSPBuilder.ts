import * as Backbone from "backbone";
import * as d3 from "d3";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";
import Vue from "vue";
import * as template from "./cspbuilder.template.html";
import CSPBuilderModel from "./CSPBuilderModel";
import { IEvent } from "./CSPViewerEvents";
import { Graph, ICSPGraphNode } from "./Graph";
declare let Jupyter: any;
import CSPGraphBuilder from "./CSPGraphBuilder.vue";
import { d3ForceLayoutEngine } from "./GraphLayout";
import NodeLink from "./NodeLink.vue";
export default class CSPBuilder extends widgets.DOMWidgetView {
    private static readonly SHOW_PYTHON_CODE = "python-code";

    public model: CSPBuilderModel;
    public graph: Graph<ICSPGraphNode>;

    public initialize(opts: any) {
        super.initialize(opts);

        this.graph = Graph.fromJSON(this.model.graphJSON) as Graph<ICSPGraphNode>;
        this.listenTo(this.model, "view:msg", (event: IEvent) => {
            if (event.action === CSPBuilder.SHOW_PYTHON_CODE) {
                // Replace cell contents with the code
                Jupyter.notebook.get_selected_cell().set_text((event as any).code);
            }
        });
    }

    public render() {
        d3ForceLayoutEngine.setup(this.graph, { width: 800, height: 600 });

        const that = this;
        const App = Vue.extend({
            components: { CSPGraphBuilder },
            template: '<div id="app"><CSPGraphBuilder :graph="graph"></CSPGraphBuilder></div>',
            watch: {
                graph: {
                    handler(val, oldVal) {
                        const cspCopy = JSON.parse(JSON.stringify(that.graph));
                        that.model.graphJSON = cspCopy;
                        that.touch();
                    },
                    deep: true,
                },
            },
            data() {
                return {
                    graph: that.graph,
                };
            },
        });

        const app = new App().$mount();
        this.el.appendChild(app.$el);

        return this;
    }
}
