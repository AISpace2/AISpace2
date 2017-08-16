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
      layout_method: "force",
      _layout_root_id: null,
      _previously_rendered: false      
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

  /** True if this model has not been rendered in any cell yet.
   *
   * This is used to work around timing issues: when the model is initialized,
   * the views may not be created, so sending a re-render message (to trigger the initial state)
   * doesn't work. Neither does sending a message from Python, for the same reason.
   * Instead, check if a view has rendered this model yet. If not, render the initial state.
   */
  get previouslyRendered(): boolean {
    return this.get("_previously_rendered");
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

  /** Controls the layout engine used. */
  get layoutMethod(): "force" | "tree" {
    return this.get("layout_method");
  }

  /**
   * The ID of the node to be used as the root of the tree.
   * Only applicable when using tree layout. Set automatically to the problem's start node.
   */
  get layoutRootId(): string {
    return this.get("_layout_root_id");
  }
}
