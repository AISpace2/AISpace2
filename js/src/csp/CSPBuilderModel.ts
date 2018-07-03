import * as widgets from "@jupyter-widgets/base";
import { IEvent } from "../Events";
import {
  deserializeGraph,
  Graph,
  ICSPGraphNode,
  IGraphJSON,
  serializeGraph
} from "../Graph";

import * as packageJSON from "../../package.json"
const EXTENSION_SPEC_VERSION = (packageJSON as any).version;

/**
 * The model that receives messages and synced traitlets from the backend.
 * See the accompanying backend file: `aispace2/jupyter/csp/cspbuilder.py`
 */
export default class CSPBuilderModel extends widgets.DOMWidgetModel {
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
      _model_name: "CSPBuilderModel",
      _view_module: "aispace2",
      _view_module_version: EXTENSION_SPEC_VERSION,
      _view_name: "CSPBuilder"
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

  /** The JSON representing the CSP graph. */
  get graph(): Graph<ICSPGraphNode> {
    return this.get("graph");
  }

  set graph(val: Graph<ICSPGraphNode>) {
    this.set("graph", val);
  }

  get textSize(): number {
    return this.get("text_size");
  }
}
