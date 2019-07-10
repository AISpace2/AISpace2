import * as widgets from "@jupyter-widgets/base";
import { IEvent } from "../Events";
import {
  deserializeGraph,
  Graph,
  IBayesGraphNode,
  IGraphJSON,
  serializeGraph
} from "../Graph";

import * as packageJSON from "../../package.json";
const EXTENSION_SPEC_VERSION = (packageJSON as any).version;

/**
 * The model that receives messages and synced traitlets from the backend.
 * See the accompanying backend file: `aispace2/jupyter/bayes/bayesbuilder.py`
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
      _model_name: "BayesBuilderModel",
      _view_module: "aispace2",
      _view_module_version: EXTENSION_SPEC_VERSION,
      _view_name: "BayesBuilder",
      decimal_place: 2
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

  // The JSON representing the Belief Network graph
  get graph(): Graph<IBayesGraphNode> {
    return this.get("graph");
  }

  set graph(val: Graph<IBayesGraphNode>) {
    this.set("graph", val);
  }

  get textSize(): number {
    return this.get("text_size");
  }

  get detailLevel(): number {
    return this.get("detail_level");
  }

  // return the decimal place in the query result
  get decimalPlace(): number {
    return this.get("decimal_place");
  }
}
