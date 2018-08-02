import * as widgets from "@jupyter-widgets/base";
import * as packageJSON from "../../package.json";
import { IEvent } from "../Events";

const EXTENSION_SPEC_VERSION = (packageJSON as any).version;

export default class BayesViewerModel extends widgets.DOMWidgetModel {
  public defaults() {
    return {
      ...super.defaults(),
      _model_name: "BayesViewerModel",
      _model_module: "aispace2",
      _model_module_version: EXTENSION_SPEC_VERSION,
      _view_name: "BayesViewer",
      _view_module: "aispace2",
      _view_module_version: EXTENSION_SPEC_VERSION
    };
  }

  public initialize(attrs: any, opts: any) {
    super.initialize(attrs, opts);

    this.listenTo(this, "msg:custom", (event: IEvent) => {
      this.trigger("view:msg", event);
    });
  }
}
