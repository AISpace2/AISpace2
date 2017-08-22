import * as widgets from "@jupyter-widgets/base";
import { extend } from "underscore";
import { IEvent } from "../Events";
import {
  deserializeGraph,
  Graph,
  ICSPGraphNode,
  IGraphJSON,
  serializeGraph
} from "../Graph";

export default class CSPBuilderModel extends widgets.DOMWidgetModel {
  public static serializers = extend(
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
      _model_module_version: "0.1.0",
      _model_name: "CSPBuilderModel",
      _view_module: "aispace2",
      _view_module_version: "0.1.0",
      _view_name: "CSPBuilder"
    };
  }

  public initialize(attrs: any, opts: any) {
    super.initialize(attrs, opts);

    this.listenTo(this, "msg:custom", (event: IEvent) => {
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
}
