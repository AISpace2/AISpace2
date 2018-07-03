import * as widgets from "@jupyter-widgets/base";
import { timeout } from "d3";
import { IEvent } from "../Events";
import { Graph, ICSPGraphNode } from "../Graph";
import { d3ForceLayout, GraphLayout, relativeLayout } from "../GraphLayout";
import CSPGraphBuilder from "./components/CSPBuilder.vue";
import CSPBuilderModel from "./CSPBuilderModel";
declare let Jupyter: any;

/**
 * Creates a view to construct a CSP. Interfaces with Jupyter backend.
 * 
 * See the accompanying backend file: `aispace2/jupyter/csp/cspbuilder.py`.
 */
export default class CSPBuilder extends widgets.DOMWidgetView {
  private static readonly SHOW_PYTHON_CODE = "python-code";

  public model: CSPBuilderModel;
  public vue: any;

  public initialize(opts: any) {
    super.initialize(opts);

    this.listenTo(this.model, "view:msg", (event: IEvent) => {
      if (event.action === CSPBuilder.SHOW_PYTHON_CODE) {
        // Replace cell contents with the code
        Jupyter.notebook.insert_cell_below().set_text((event as any).code);
      }
    });
  }

  public render() {
    const initialGraph = this.model.graph;

    timeout(() => {
      this.vue = new CSPGraphBuilder({
        data: {
          graph: initialGraph,
          textSize: this.model.textSize,
          layout: new GraphLayout(d3ForceLayout(), relativeLayout())
        },
        watch: {
          graph: {
            handler: (val: Graph, oldVal: Graph) => {
              // Creating a copy is necessary as changes are detected by reference by traitlets
              this.model.graph = Graph.fromJSON(oldVal.toJSON()) as Graph<
                ICSPGraphNode
              >;
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
