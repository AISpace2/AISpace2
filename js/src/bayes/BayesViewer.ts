import { DOMWidgetView } from "@jupyter-widgets/base";
import BayesViewerModel from "./BayesViewerModel";

export default class BayesViewer extends DOMWidgetView {
  public model: BayesViewerModel;

  public initialize(opts: any) {
    super.initialize(opts);

    // Receive message from backend
    this.listenTo(this.model, "view:msg", (event: object) => {
      // switch (event.action) {
      //   case "highlightPath":
      //     return "function";
      // }

      return "";
    });
  }

  public render() {
    this.$el.html("Bayes");
  }
}
