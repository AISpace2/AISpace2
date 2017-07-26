import { timeout } from "d3";
import * as widgets from "jupyter-js-widgets";
import Vue from "vue";
import { IEvent } from "../Events";
import { Graph } from "../Graph";
import { d3ForceLayoutEngine } from "../GraphLayout";
import SearchGraphBuilder from "./components/SearchGraphBuilder.vue";
import SearchBuilderModel from "./SearchBuilderModel";
declare let Jupyter: any;

export default class SearchBuilder extends widgets.DOMWidgetView {
  private static readonly SHOW_PYTHON_CODE = "python-code";

  public model: SearchBuilderModel;
  public graph: Graph;

  public initialize(opts: any) {
    super.initialize(opts);

    this.graph = Graph.fromJSON(this.model.graphJSON) as Graph;
    this.listenTo(this.model, "view:msg", (event: IEvent) => {
      if (event.action === SearchBuilder.SHOW_PYTHON_CODE) {
        // Replace cell contents with the code
        Jupyter.notebook.insert_cell_below().set_text((event as any).code);
      }
    });
  }

  public render() {
    d3ForceLayoutEngine.setup(this.graph, { width: 800, height: 600 });

    const that = this;
    const App = Vue.extend({
      components: { SearchGraphBuilder },
      data() {
        return {
          graph: that.graph,
          showEdgeCosts: that.model.showEdgeCosts,
          showNodeHeuristics: that.model.showNodeHeuristics,
          width: 0,
          height: 0
        };
      },
      watch: {
        graph: {
          handler(val, oldVal) {
            const searchProblemCopy = JSON.parse(JSON.stringify(that.graph));
            that.model.graphJSON = searchProblemCopy;
            that.touch();
          },
          deep: true
        }
      },
      render(createElement: Vue.CreateElement) {
        return createElement(SearchGraphBuilder, {
          props: {
            graph: this.graph,
            width: this.width,
            height: this.height,
            showEdgeCosts: this.showEdgeCosts,
            showNodeHeuristics: this.showNodeHeuristics
          }
        });
      }
    });

    timeout(() => {
      const width = this.$el.width();
      const height = width / 1.6;
      d3ForceLayoutEngine.setup(this.graph, { width, height });
      const app = new App().$mount();
      (app.$data as any).width = width;
      (app.$data as any).height = height;
      this.el.appendChild(app.$el);
    });

    return this;
  }
}
