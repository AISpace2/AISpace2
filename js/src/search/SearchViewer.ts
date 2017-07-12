import * as widgets from "jupyter-js-widgets";
import Vue from "vue";
import CSPViewer from "../csp/CSPViewer";
import { IEvent, isOutputEvent } from "../Events";
import { Graph } from "../Graph";
import { d3ForceLayoutEngine } from "../GraphLayout";
import * as StepEvents from "../StepEvents";
import SearchVisualizer from "./components/SearchVisualizer.vue";
import { isHighlightPathEvent } from "./SearchViewerEvents";
import SearchViewerModel from "./SearchViewerModel";

export default class SearchViewer extends widgets.DOMWidgetView {
    public model: SearchViewerModel;
    private graph: Graph;
    private vue: any;

    public initialize(opts: any) {
        super.initialize(opts);
        this.graph = Graph.fromJSON(this.model.graphJSON);
        this.listenTo(this.model, "view:msg", (event: IEvent) => {
            if (isOutputEvent(event)) {
                this.vue.output = event.text;
            } else if (isHighlightPathEvent(event)) {
                for (const edge of this.graph.edges) {
                    if (event.path.includes(edge.id)) {
                        Vue.set(edge.styles, "stroke", "pink");
                    } else {
                        Vue.set(edge.styles, "stroke", "black");
                    }
                }
            }
        });
    }

    public render() {
        d3ForceLayoutEngine.setup(this.graph, { width: 800, height: 500 });

        const that = this;
        const App = Vue.extend({
            components: { SearchVisualizer },
            template: `
                <div id="app">
                    <SearchVisualizer :graph="graph" :output="output"
                        @click:auto-step="autostep"
                        @click:step="step"
                        @click:fine-step="finestep">
                    </SearchVisualizer>
                </div>`,
            data() {
                return {
                    graph: that.graph,
                    output: null,
                };
            },
            methods: {
                autostep() {
                    that.send({event: StepEvents.AUTO_STEP_CLICK});
                },
                finestep() {
                    that.send({event: StepEvents.FINE_STEP_CLICK});
                },
                step() {
                    that.send({event: StepEvents.STEP_CLICK});
                },
            },
        });

        this.vue = new App().$mount();
        this.el.appendChild(this.vue.$el);
    }
}
