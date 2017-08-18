import { timeout } from "d3";
import * as widgets from "@jupyter-widgets/base";
import Vue from "vue";
import { IEvent } from "../Events";
import { Graph } from "../Graph";
import { d3ForceLayout, GraphLayout, relativeLayout } from "../GraphLayout";
import SearchGraphBuilder from "./components/SearchBuilder.vue";
import SearchBuilderModel from "./SearchBuilderModel";
declare let Jupyter: any;

export default class SearchBuilder extends widgets.DOMWidgetView {
  private static readonly SHOW_PYTHON_CODE = "python-code";

  public model: SearchBuilderModel;
  public graph: Graph;
  public vue: any;

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
    timeout(() => {
      this.vue = new SearchGraphBuilder({
        data: {
          graph: this.graph,
          showEdgeCosts: this.model.showEdgeCosts,
          showNodeHeuristics: this.model.showNodeHeuristics,
          layout: new GraphLayout(d3ForceLayout(), relativeLayout())
        },
        watch: {
          graph: {
            handler: (val, oldVal) => {
              const searchProblemCopy = JSON.parse(JSON.stringify(this.graph));
              this.model.graphJSON = searchProblemCopy;
              this.touch();
            },
            deep: true
          }
        }
      }).$mount(this.el);
    });

    return this;
  }

  public remove() {
    if (this.vue != null) {
      this.vue.$destroy();
    }
  }
}
