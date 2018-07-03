import * as widgets from "@jupyter-widgets/base";
import { IEvent } from "../Events";
import {
  deserializeGraph,
  Graph,
  IGraphJSON,
  ISearchGraphEdge,
  ISearchGraphNode,
  serializeGraph
} from "../Graph";

import * as packageJSON from "../../package.json"
const EXTENSION_SPEC_VERSION = (packageJSON as any).version;

/**
 * The model that receives messages and synced traitlets from the backend.
 * See the accompanying backend file: `aispace2/jupyter/search/searchbuilder.py`
 */
export default class SearchBuilderModel extends widgets.DOMWidgetModel {
  public static serializers = Object.assign(
    {
      graph: {
        serialize: serializeGraph,
        deserialize: deserializeGraph
      }
    },
    widgets.DOMWidgetModel.serializers
  );

  public defaults() {
    return {
      ...super.defaults(),
      _model_module: "aispace2",
      _model_module_version: EXTENSION_SPEC_VERSION,
      _model_name: "SearchBuilderModel",
      _view_module: "aispace2",
      _view_module_version: EXTENSION_SPEC_VERSION,
      _view_name: "SearchBuilderModel",
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

  /** The Graph representing the search problem. */
  get graph(): Graph<ISearchGraphNode, ISearchGraphEdge> {
    return this.get("graph");
  }

  set graph(val: Graph<ISearchGraphNode, ISearchGraphEdge>) {
    this.set("graph", val);
  }

  get textSize(): number {
    return this.get("text_size");
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
