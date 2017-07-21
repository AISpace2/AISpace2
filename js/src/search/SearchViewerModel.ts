import * as widgets from "jupyter-js-widgets";
import { IEvent } from "../Events";
import { IGraphJSON } from "../Graph";

export default class SearchViewerModel extends widgets.DOMWidgetModel {
  public defaults() {
    return {
      ...super.defaults(),
      _model_module: "aispace2",
      _model_module_version: "0.1.0",
      _model_name: "SearchViewerModel",
      _view_module: "aispace2",
      _view_module_version: "0.1.0",
      _view_name: "SearchViewer",
      graph_json: {} as IGraphJSON,
      show_edge_costs: true,
      show_node_heuristics: false,
      layout_method: "force"
    };
  }

  public initialize(attrs: any, opts: any) {
    super.initialize(attrs, opts);

    // Forward message to views
    this.listenTo(this, "msg:custom", (event: IEvent) => {
      // We don't register a listener for Python messages (which go to the model) in the view,
      // because each new view would attach a new listener.
      // Instead, we register it once here, and broadcast it to views.
      this.trigger("view:msg", event);
    });
  }

  get graphJSON(): IGraphJSON {
    return this.get("graph_json");
  }

  set graphJSON(val) {
    this.set("graph_json", val);
  }

  get showEdgeCosts(): boolean {
    return this.get("show_edge_costs");
  }

  get showNodeHeuristics(): boolean {
    return this.get("show_node_heuristics");
  }

  get layoutMethod(): "force" | "tree" {
    return this.get("layout_method");
  }
}
