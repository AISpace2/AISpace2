import * as widgets from "@jupyter-widgets/base";
import { timeout } from "d3";
import Vue from "vue";
import { IEvent } from "../Events";
import { Graph, ICSPGraphNode } from "../Graph";
import { d3ForceLayout, GraphLayout, relativeLayout } from "../GraphLayout";
import CSPGraphBuilder from "./components/CSPBuilder.vue";
import CSPBuilderModel from "./CSPBuilderModel";
declare let Jupyter: any;

export default class CSPBuilder extends widgets.DOMWidgetView {
  private static readonly SHOW_PYTHON_CODE = "python-code";

  public model: CSPBuilderModel;
  public graph: Graph<ICSPGraphNode>;
  public vue: any;

  public initialize(opts: any) {
    super.initialize(opts);

    this.graph = Graph.fromJSON(this.model.graphJSON) as Graph<ICSPGraphNode>;
    this.listenTo(this.model, "view:msg", (event: IEvent) => {
      if (event.action === CSPBuilder.SHOW_PYTHON_CODE) {
        // Replace cell contents with the code
        Jupyter.notebook.insert_cell_below().set_text((event as any).code);
      }
    });
  }

  public render() {
    timeout(() => {
      this.vue = new CSPGraphBuilder({
        data: {
          graph: this.graph,
          layout: new GraphLayout(d3ForceLayout(), relativeLayout())
        },
        watch: {
          graph: {
            handler: (val, oldVal) => {
              const cspCopy = JSON.parse(JSON.stringify(this.graph));
              this.model.graphJSON = cspCopy;
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
