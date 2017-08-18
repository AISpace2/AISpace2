import * as widgets from "@jupyter-widgets/base";
import { IEvent } from "../Events";
import { IGraphJSON } from "../Graph";

export default class CSPBuilderModel extends widgets.DOMWidgetModel {
  public defaults() {
    return {
      ...super.defaults(),
      _model_module: "aispace2",
      _model_module_version: "0.1.0",
      _model_name: "CSPBuilderModel",
      _view_module: "aispace2",
      _view_module_version: "0.1.0",
      _view_name: "CSPBuilder",
      graph_json: {} as IGraphJSON
    };
  }

  public initialize(attrs: any, opts: any) {
    super.initialize(attrs, opts);

    this.listenTo(this, "msg:custom", (event: IEvent) => {
      this.trigger("view:msg", event);
    });
  }

  /** The JSON representing the CSP graph. */
  get graphJSON(): IGraphJSON {
    return this.get("graph_json");
  }

  set graphJSON(val) {
    this.set("graph_json", val);
  }
}
