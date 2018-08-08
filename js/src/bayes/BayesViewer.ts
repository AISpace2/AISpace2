import { DOMWidgetView } from "@jupyter-widgets/base";
import { timeout } from "d3";
import { Events } from "./BayesEvents";
import BayesViewerModel from "./BayesViewerModel";
import BayesNetInteractor from "./components/BayesNetVisualizer.vue";
import * as Analytics from "../Analytics";
import {IBayesGraphNode} from "../Graph";
import { d3ForceLayout, GraphLayout, relativeLayout } from "../GraphLayout";
import * as labelDict from "../labelDictionary";
import * as StepEvents from "../StepEvents";

export default class BayesViewer extends DOMWidgetView {
  public model: BayesViewerModel;
  private vue: any;

  public initialize(opts: any) {
    super.initialize(opts);

    // Receive message from backend
    this.listenTo(this.model, "view:msg", (event: Events) => {
      switch (event.action) {
        case "highlightArcs":
          return "function";
      }

      return "";
    });
  }

  public render() {
    console.log("graph", this.model.graph);
    timeout(() => {
      this.vue = new BayesNetInteractor({
        data: {
          graph: this.model.graph,
          output: null,
          /** Layout object that controls where nodes are drawn. */
          layout: new GraphLayout(d3ForceLayout(), relativeLayout()),
          textSize: this.model.textSize,
          detailLevel: this.model.detailLevel,
          legendText: labelDict.bayesLabelText,
          legendColor: labelDict.bayesLabelColor,
          isQuerying: true
        }
      }).$mount(this.el);

      this.vue.$on(StepEvents.PRINT_POSITIONS, () => {
        this.send({
          event: StepEvents.PRINT_POSITIONS,
          nodes: this.vue.graph.nodes
        });
      });

      this.vue.$on("click:observe-node", (node: IBayesGraphNode) => {
        Analytics.trackEvent("Bayes Visualizer", "Observe Node");
        this.send({
          event: "node:observe",
          varName: node.name
        });
      });

      this.vue.$on("click:query-node", (node: IBayesGraphNode) => {
        Analytics.trackEvent("Bayes Visualizer", "Query Node");
        this.send({
          event: "node:query",
          varName: node.name
        });
      });

      if (!this.model.previouslyRendered) {
        this.send({ event: "initial_render" });
      }
    });
  }
}
