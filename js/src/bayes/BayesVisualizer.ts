import { DOMWidgetView } from "@jupyter-widgets/base";
import { timeout } from "d3";
import * as Events from "./BayesVisualizerEvents";
import BayesVisualizerModel from "./BayesVisualizerModel";
import BayesNetInteractor from "./components/BayesVisualizer.vue";
import { IObservation, ObservationManager } from "./Observation";

import { cloneDeep } from "lodash";
import * as Analytics from "../Analytics";
import { IBayesGraphNode } from "../Graph";
import { d3ForcePlusRelativeLayout, GraphLayout, relativeLayout } from "../GraphLayout";
import * as labelDict from "../labelDictionary";
import * as StepEvents from "../StepEvents";

export default class BayesVisualizer extends DOMWidgetView {
  public model: BayesVisualizerModel;
  private vue: any;
  private manager: ObservationManager;

  public initialize(opts: any) {
    super.initialize(opts);
    this.manager = new ObservationManager();
    this.manager.reset();

    // Receive message from backend
    this.listenTo(this.model, "view:msg", (event: Events.Events) => {
      switch (event.action) {
        case "observe":
          this.manager.add(event.name, event.value);
          break;
        case "query":
          this.parseQueryResult(event);
          break;
        case "showPositions":
          this.vue.positions = this.vue.positions && event.positions == this.vue.positions ? "" : event.positions
          break;
      }
    });
  }

  public render() {
    timeout(() => {
      this.vue = new BayesNetInteractor({
        data: {
          graph: this.model.graph,
          iniGraph: cloneDeep(this.model.graph),
          output: null,
          warningMessage: null,
          positions: null,
          // Layout object that controls where nodes are drawn
          layout: new GraphLayout(d3ForcePlusRelativeLayout(), relativeLayout()),
          textSize: this.model.textSize,
          lineWidth: this.model.lineWidth,
          detailLevel: this.model.detailLevel,
          isQuerying: false,
          decimalPlace: this.model.decimalPlace
        }
      }).$mount(this.el);

      this.vue.$on(StepEvents.PRINT_POSITIONS, () => {
        this.send({
          event: StepEvents.PRINT_POSITIONS,
          nodes: this.vue.graph.nodes
        });
      });

      this.vue.$on("click:submit", () => {
        Analytics.trackEvent("Bayes Visualizer", "Observe Node");
        this.chooseObservation();

        this.model.graph.nodes.map((variableNode: IBayesGraphNode) => {
          this.vue.$emit("click:query-node", variableNode);
          this.vue.$set(variableNode.styles, "strokeWidth", 0);
        });
      });

      this.vue.$on("click:query-node", (node: IBayesGraphNode) => {
        Analytics.trackEvent("Bayes Visualizer", "Query Node");

        const dumpData: IObservation[] = this.manager.dump();

        this.send({
          event: "node:query",
          name: node.name,
          evidences: dumpData.map((n: IObservation) => {
            return { "name": n.name, "value": n.value };
          })
        });
      });

      this.vue.$on('reset', () => {
        this.manager.reset();
        this.vue.graph.should_relayout = false;
        this.model.graph = cloneDeep(this.vue.iniGraph);
        this.vue.graph = this.model.graph;
        this.model.graph.nodes.map((variableNode: IBayesGraphNode) => {
          this.vue.$set(variableNode, "prob", undefined);
          this.vue.$set(variableNode, "observed", undefined);
          this.vue.$set(variableNode, "displaying", undefined);
          this.vue.$set(variableNode.styles, "strokeWidth", 0);
          this.vue.FocusNode.domain = [];
        });
      });

      if (!this.model.previouslyRendered) {
        this.send({ event: "initial_render" });
        this.vue.iniGraph = cloneDeep(this.model.graph);
      }
    });
  }

  private parseQueryResult(event: Events.IBayesQueryEvent) {
    const nodes = this.model.graph.nodes.filter(node => node.name === event.name);
    if (nodes.length === 0) {
      return;
    } else {
      const variableNode = nodes[0] as IBayesGraphNode;
      variableNode.prob = event.prob;
      if (variableNode.displaying) {
        this.vue.$set(variableNode.styles, "strokeWidth", 2);
      }
    }
  }

  private chooseObservation() {
    if (this.vue.FocusNode.checkedNames === '') {
      this.vue.warningMessage = "Choose one value to observe.";
      return;
    }
    const nodes = this.model.graph.nodes.filter(node => node.name === this.vue.FocusNode.nodeName);
    const variableNode = nodes[0] as IBayesGraphNode;
    let value: null | string = this.vue.FocusNode.checkedNames;
    this.manager.add(variableNode.name, value);
    this.vue.$set(variableNode, "observed", value.toString());
    this.vue.FocusNode.domain = [];
    this.vue.warningMessage = null;
  }
}
