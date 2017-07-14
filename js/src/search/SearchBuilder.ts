import * as d3 from "d3";
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
    this.listenTo(this.model, "view:msg", (event: IEvent) => {});
  }

  public render() {
    d3ForceLayoutEngine.setup(this.graph, { width: 800, height: 600 });

    const that = this;
    const App = Vue.extend({
      components: { SearchGraphBuilder },
      template:
        '<div id="app"><SearchGraphBuilder :graph="graph"></SearchGraphBuilder></div>',
      data() {
        return {
          graph: that.graph
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
      }
    });

    d3.timeout(() => {
      const app = new App().$mount();
      this.el.appendChild(app.$el);
    });

    return this;
  }
}
