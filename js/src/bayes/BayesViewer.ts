import { DOMWidgetView } from "@jupyter-widgets/base";
import BayesViewerModel from "./BayesViewerModel";
import { timeout } from "d3";
import { BayesNetInteractor } from "./components/BayesNetVisualizer.vue";
import * as labelDict from "../labelDictionary";
import * as StepEvents from "../StepEvents";
import * as Analytics from "../Analytics";

export default class BayesViewer extends DOMWidgetView {
  public model: BayesViewerModel;
  private vue: any;

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
    timeout(() => {
      this.vue = new BayesNetInteractor({
        data: {
          graph: this.model.graph,
          showEdgeCosts: this.model.showEdgeCosts,
          showNodeHeuristics: this.model.showNodeHeuristics,
          output: null,
          textSize: this.model.textSize,
          detailLevel: this.model.detailLevel,
          legendText: labelDict.searchLabelText,
          legendColor: labelDict.searchLabelColor,
          frontier: []
        }
      }).$mount(this.el);

      this.vue.$on(StepEvents.FINE_STEP_CLICK, () => {
        Analytics.trackEvent("Search Visualizer", "Fine Step");
        this.send({ event: StepEvents.FINE_STEP_CLICK });
      });

      this.vue.$on(StepEvents.STEP_CLICK, () => {
        Analytics.trackEvent("Search Visualizer", "Step");
        this.send({ event: StepEvents.STEP_CLICK });
      });

      this.vue.$on(StepEvents.AUTO_SOLVE_CLICK, () => {
        Analytics.trackEvent("Search Visualizer", "Auto Solve");
        this.send({ event: StepEvents.AUTO_SOLVE_CLICK });
      });

      this.vue.$on(StepEvents.PAUSE_CLICK, () => {
        Analytics.trackEvent("Search Visualizer", "Pause");
        this.send({ event: StepEvents.PAUSE_CLICK });
      });

      this.vue.$on(StepEvents.PRINT_POSITIONS, () => {
        this.send({
          event: StepEvents.PRINT_POSITIONS,
          nodes: this.vue.graph.nodes
        });
      });

      this.vue.$on("toggle:showFullDomain", () => {
        this.showFullDomainFlag = !this.showFullDomainFlag;
        // Nodes/edges have been added to the graph from the backend.
        this.model.graph.mergeStylesFrom(this.model.previous("graph"));

        this.vue.graph = this.showFullDomainFlag
          ? this.model.graph
          : this.trimGraph();
      });

      if (!this.model.previouslyRendered) {
        this.send({ event: "initial_render" });
      }
    });
  }
}
