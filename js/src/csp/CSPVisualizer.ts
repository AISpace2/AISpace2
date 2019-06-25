import * as widgets from "@jupyter-widgets/base";
import { timeout } from "d3";
import * as Analytics from "../Analytics";
import { ICSPGraphNode, IGraphEdge } from "../Graph";
import { d3ForceLayout, GraphLayout, relativeLayout } from "../GraphLayout";
import * as labelDict from "../labelDictionary";
import * as StepEvents from "../StepEvents";
import CSPGraphVisualizer from "./components/CSPVisualizer.vue";
import * as CSPEvents from "./CSPVisualizerEvents";
import CSPViewerModel from "./CSPVisualizerModel";

/**
 * Creates a CSP visualization and handles events received from the backend.
 *
 * See the accompanying backend file: `aispace2/jupyter/csp/csp.py`
 */
export default class CSPViewer extends widgets.DOMWidgetView {
  private static readonly ARC_CLICK = "arc:click";
  private static readonly VAR_CLICK = "var:click";

  public model: CSPViewerModel;
  private vue: any;

  public initialize(opts: any) {
    super.initialize(opts);

    this.listenTo(this.model, "view:msg", (event: CSPEvents.Events) => {
      // tslint:disable-next-line:no-console
      console.log(event);

      switch (event.action) {
        case "highlightArcs":
          return this.highlightArcs(event);
        case "setDomains":
          return this.setDomains(event);
        case "highlightNodes":
          return this.highlightNodes(event);
        case "chooseDomainSplit":
          return this.chooseDomainSplit(event);
        case "chooseDomainSplitBeforeAC":
          return this.chooseDomainSplitBeforeAC(event);
        case "setSolution":
          this.vue.pre_solution += "\n        " + event.solution;
          break;
        case "output":
          this.vue.output = event.text;
          break;
        case "showPositions":
          this.vue.positions = this.vue.positions ? "" : event.positions
          break;
      }
    });
  }

  public render() {
    timeout(() => {
      this.vue = new CSPGraphVisualizer({
        data: {
          graph: this.model.graph,
          layout: new GraphLayout(d3ForceLayout(), relativeLayout()),
          width: 0,
          height: 0,
          output: null,
          pre_solution: "",
          positions: null,
          textSize: this.model.textSize,
          detailLevel: this.model.detailLevel,
          legendText: labelDict.cspLabelText,
          legendColor: labelDict.cspLabelColor,
          needACButton: this.model.needACButton
        }
      }).$mount(this.el);

      this.vue.$on(StepEvents.FINE_STEP_CLICK, () => {
        Analytics.trackEvent("CSP Visualizer", "Fine Step");
        this.send({ event: StepEvents.FINE_STEP_CLICK });
      });

      this.vue.$on(StepEvents.STEP_CLICK, () => {
        Analytics.trackEvent("CSP Visualizer", "Step");
        this.send({ event: StepEvents.STEP_CLICK });
      });

      this.vue.$on(StepEvents.AUTO_ARC_CONSISTENCY_CLICK, () => {
        Analytics.trackEvent("CSP Visualizer", "Auto Arc Consistency");
        this.send({ event: StepEvents.AUTO_ARC_CONSISTENCY_CLICK });
      });

      this.vue.$on(StepEvents.AUTO_SOLVE_CLICK, () => {
        Analytics.trackEvent("CSP Visualizer", "Auto Solve");
        this.send({ event: StepEvents.AUTO_SOLVE_CLICK });
      });

      this.vue.$on(StepEvents.PAUSE_CLICK, () => {
        Analytics.trackEvent("CSP Visualizer", "Pause");
        this.send({ event: StepEvents.PAUSE_CLICK });
      });

      this.vue.$on(StepEvents.PRINT_POSITIONS, () => {
        this.send({
          event: StepEvents.PRINT_POSITIONS,
          nodes: this.vue.graph.nodes
        });
      });

      this.vue.$on("click:edge", (edge: IGraphEdge) => {
        Analytics.trackEvent("CSP Visualizer", "Edge Clicked");
        this.send({
          constId: edge.target.idx,
          event: CSPViewer.ARC_CLICK,
          varName: edge.source.name
        });
      });

      this.vue.$on("click:node", (node: ICSPGraphNode) => {
        Analytics.trackEvent("CSP Visualizer", "Node Clicked");
        this.send({
          event: CSPViewer.VAR_CLICK,
          varName: node.name,
          varType: node.type
        });
      });

      // Functions called on the Python backend are queued until first render
      if (!this.model.previouslyRendered && this.model.waitForRender) {
        this.send({ event: "initial_render" });
        this.highlightArcs({
          action: "highlightArcs",
          arcIds: null,
          colour: "blue",
          style: "normal"
        });
      }
    });

    return this;
  }

  public remove() {
    if (this.vue != null) {
      this.vue.$destroy();
    }
  }

  /**
   * Highlights an arc (or all arcs), as described by the event object.
   */
  private highlightArcs(event: CSPEvents.ICSPHighlightArcsEvent) {
    const strokeWidth =
      event.style === "bold" ? this.model.lineWidth + 3 : this.model.lineWidth;

    if (event.arcIds == null) {
      for (const edge of this.model.graph.edges) {
        const stroke = event.colour ? event.colour : edge.styles.stroke;
        this.vue.$set(edge.styles, "stroke", stroke);
        this.vue.$set(edge.styles, "strokeWidth", strokeWidth);
      }
    } else {
      for (const arcId of event.arcIds) {
        const stroke = event.colour ? event.colour : this.model.graph.idMap[arcId].styles.stroke;
        this.vue.$set(this.model.graph.idMap[arcId].styles, "stroke", stroke);
        this.vue.$set(
          this.model.graph.idMap[arcId].styles,
          "strokeWidth",
          strokeWidth
        );
      }
    }
  }

  /**
   * Sets the domain of a variable node, as described by the event object.
   */
  private setDomains(event: CSPEvents.ICSPSetDomainsEvent) {
    for (let i = 0; i < event.nodeIds.length; i++) {
      const variableNode = this.model.graph.idMap[event.nodeIds[i]] as ICSPGraphNode;
      variableNode.domain = event.domains[i];
    }
  }

  /**
   * Highlights nodes, as described by the event object.
   */
  private highlightNodes(event: CSPEvents.ICSPHighlightNodesEvent) {
    for (const nodeId of event.nodeIds) {
      this.vue.$set(
        this.model.graph.idMap[nodeId].styles,
        "stroke",
        event.colour
      );
      this.vue.$set(this.model.graph.idMap[nodeId].styles, "strokeWidth", 2);
    }
  }

  /**
   * Requests the user choose a domain for one side of the split.
   */
  private chooseDomainSplit(event: CSPEvents.ICSPChooseDomainSplitEvent) {
    const domainString = window.prompt(
      "Choose domain for first split for variable " + event.var + ". Cancel to choose a default split.",
      event.domain.join()
    );
    const newDomain = domainString != null ? domainString.split(",").filter(d => d) : null;
    this.send({ event: "domain_split", domain: newDomain });
  }

  /**
   * Prompt the user that the AC needs to be finished before the domain can be split.
   */
  private chooseDomainSplitBeforeAC(event: CSPEvents.ICSPChooseDomainSplitBeforeACEvent) {
    window.alert("Arc consistency needs to be finished before the domain can be split.");
  }
}
