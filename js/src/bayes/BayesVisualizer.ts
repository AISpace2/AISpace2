import { DOMWidgetView } from "@jupyter-widgets/base";
import { timeout } from "d3";
import * as Events from "./BayesVisualizerEvents";
import BayesVisualizerModel from "./BayesVisualizerModel";
import BayesNetInteractor from "./components/BayesVisualizer.vue";
import { IObservation, ObservationManager} from "./Observation";

import * as Analytics from "../Analytics";
import {IBayesGraphNode} from "../Graph";
import { d3ForceLayout, GraphLayout, relativeLayout } from "../GraphLayout";
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
          output: null,
          positions: null,
          // Layout object that controls where nodes are drawn
          layout: new GraphLayout(d3ForceLayout(), relativeLayout()),
          textSize: this.model.textSize,
          detailLevel: this.model.detailLevel,
          isQuerying: true,
          decimalPlace: this.model.decimalPlace
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
        this.chooseObservation(node);
      });

      this.vue.$on("click:query-node", (node: IBayesGraphNode) => {
        Analytics.trackEvent("Bayes Visualizer", "Query Node");

        const dumpData: IObservation[] = this.manager.dump();

        this.send({
          event: "node:query",
          name: node.name,
          evidences: dumpData.map((n: IObservation) => {
            return {"name": n.name, "value": n.value};
          })});
      });

      this.vue.$on('reset', () => {
        this.manager.reset();
        this.model.graph.nodes.map((variableNode: IBayesGraphNode) => {
          variableNode.falseProb = undefined;
          variableNode.trueProb = undefined;
          variableNode.observed = undefined;
          this.vue.$set(variableNode.styles, "strokeWidth", 0);
        });
      });

      if (!this.model.previouslyRendered) {
        this.send({ event: "initial_render" });
      }
    });
  }

  private parseQueryResult(event: Events.IBayesQueryEvent) {
    const nodes =  this.model.graph.nodes.filter(node => node.name === event.name);
    if (nodes.length === 0) {
      return;
    } else {
      const variableNode = nodes[0] as IBayesGraphNode;
      variableNode.prob = event.prob;
      this.vue.$set(variableNode.styles, "strokeWidth", 2);
    }
  }

  private chooseObservation(node: IBayesGraphNode) {
    function notProperResponse(res: string): boolean {
      const containsMultipleDomain: boolean = res.includes(', ');
      let notOneOfDomain: boolean;

      const domainString: string[] = [];

      for (let e of node.domain) {
        if(typeof(e) !== "string") {
          e = e.toString();
        }
        domainString.push(e);
      }

      notOneOfDomain = !domainString.includes(res);

      return containsMultipleDomain || notOneOfDomain || res === "";
    }

    let response: null | string;

    do {
      response = window.prompt(
        "Choose only one observation", node.domain.join(", "));
      if (response !== null) {response = response.trim();}
    } while (response !== null && notProperResponse(response));

    let value: null | string | boolean = response;

    if (value !== null && !value.includes(', ')) {
      if (value === "true") { value = true;}
      else if (value === "false") { value = false;}
	  node.observed = response;
      this.manager.add(node.name, value)
    };
  }
}
