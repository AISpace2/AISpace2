import {DOMWidgetView} from "@jupyter-widgets/base";
import BayesViewerModel from "./BayesViewerModel";
import * as SearchEvents from "../search/SearchVisualizerEvents";

export default class BayesViewer extends DOMWidgetView {
  public model: BayesViewerModel;

  public initialize(opts: any) {
    super.initialize(opts);

    // Receive message from backend
    this.listenTo(this.model, "view:msg", (event: object) => {
      switch (event.action) {
        case "highlightPath":
          return "function";
      }
    });
  }

  public render() {
    this.$el.html("Bayes");
  }

}
