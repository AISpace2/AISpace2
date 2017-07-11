import * as widgets from "jupyter-js-widgets";
import Vue from "vue";
import {IEvent} from "../Events";
import {Graph} from "../Graph";
import {d3ForceLayoutEngine} from "../GraphLayout";
import SearchVisualizer from "./components/SearchVisualizer.vue";
import SearchViewerModel from "./SearchViewerModel";

export default class SearchViewer extends widgets.DOMWidgetView {
    public model: SearchViewerModel;
    private graph: Graph;

    public initialize(opts: any) {
        super.initialize(opts);
        this.graph = Graph.fromJSON(this.model.graphJSON);

        this.listenTo(this.model, "view:msg", (event: IEvent) => {
        });
    }

    public render() {
        d3ForceLayoutEngine.setup(this.graph, {width: 800, height: 500});

        const that = this;
        const App = Vue.extend({
            components: {SearchVisualizer},
            template: '<div id="app"><SearchVisualizer :graph="graph"></SearchVisualizer></div>',
            data() {
                return {
                    graph: that.graph,
                };
            },
        });

        const app = new App().$mount();
        this.el.appendChild(app.$el);
    }
}
