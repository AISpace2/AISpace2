import { timeout } from "d3";
import * as widgets from "jupyter-js-widgets";
import Vue from "vue";
import { IEvent } from "../Events";
import { Graph, ICSPGraphNode } from "../Graph";
import { d3ForceLayoutEngine } from "../GraphLayout";
import CSPGraphBuilder from "./components/CSPBuilder.vue";
import CSPBuilderModel from "./CSPBuilderModel";
declare let Jupyter: any;

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
        Jupyter.notebook.insert_cell_below().set_text((event as any).code);
      }
    });
  }

  public render() {
    d3ForceLayoutEngine.setup(this.graph, { width: 800, height: 600 });

    timeout(() => {
      const width = this.$el.width();
      const height = width / 1.6;
      d3ForceLayoutEngine.setup(this.graph, { width, height });

      const vue = new CSPGraphBuilder({
        data: {
          graph: this.graph,
          width,
          height
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
      }).$mount();

      this.el.appendChild(vue.$el);
    });

    return this;
  }
}
