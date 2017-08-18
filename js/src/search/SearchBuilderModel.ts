import * as widgets from "@jupyter-widgets/base";
import { IEvent } from "../Events";
import { IGraphJSON } from "../Graph";

export default class SearchBuilderModel extends widgets.DOMWidgetModel {
  public defaults() {
    return {
      ...super.defaults(),
      _model_module: "aispace2",
      _model_module_version: "0.1.0",
      _model_name: "SearchBuilderModel",
      _view_module: "aispace2",
      _view_module_version: "0.1.0",
      _view_name: "SearchBuilderModel",
      graph_json: {} as IGraphJSON,
      show_edge_costs: true,
      show_node_heuristics: false
    };
  }

  public initialize(attrs: any, opts: any) {
    super.initialize(attrs, opts);

    this.listenTo(this, "msg:custom", (event: IEvent) => {
      this.trigger("view:msg", event);
    });
  }

  /** The JSON representation of the search graph. */
  get graphJSON(): IGraphJSON {
    return this.get("graph_json");
  }

  set graphJSON(val) {
    this.set("graph_json", val);
  }

  /** True if the visualization should show edge costs. */
  get showEdgeCosts(): boolean {
    return this.get("show_edge_costs");
  }

  /** True if a node's heuristic value should be shown. */
  get showNodeHeuristics(): boolean {
    return this.get("show_node_heuristics");
  }
}
