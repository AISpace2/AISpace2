import { timeout } from "d3";
import * as widgets from "jupyter-js-widgets";
import { debounce } from "underscore";
import Vue from "vue";
import { IEvent, isOutputEvent } from "../Events";
import { Graph, ICSPGraphNode } from "../Graph";
import { d3ForceLayoutEngine } from "../GraphLayout";
import * as StepEvents from "../StepEvents";
import CSPGraphInteractor from "./components/CSPGraphInteractor.vue";
import * as Events from "./CSPViewerEvents";
import CSPViewerModel from "./CSPViewerModel";

export default class CSPViewer extends widgets.DOMWidgetView {
  private static readonly ARC_CLICK = "arc:click";
  private static readonly VAR_CLICK = "var:click";

  public model: CSPViewerModel;

  private vue: any;
  private graph: Graph<ICSPGraphNode>;

  public initialize(opts: any) {
    super.initialize(opts);

    this.graph = Graph.fromJSON(this.model.graphJSON) as Graph<ICSPGraphNode>;

    // Functions called on the Python backend are queued until first render
    if (this.model.initial_render) {
      this.send({ event: "initial_render" });
      this.highlightArcs({
        action: "highlightArcs",
        arcIds: null,
        colour: "blue",
        style: "normal"
      });
    }

    this.listenTo(this.model, "view:msg", (event: IEvent) => {
      // tslint:disable-next-line:no-console
      console.log(event);

      if (Events.isHighlightArcsEvent(event)) {
        this.highlightArcs(event);
      } else if (Events.isSetDomainEvent(event)) {
        this.setDomain(event);
      } else if (Events.isHighlightNodesEvent(event)) {
        this.highlightNodes(event);
      } else if (isOutputEvent(event)) {
        this.vue.output = event.text;
      }
    });

    $(window).resize(() => {
      this.handleResize();
    });
  }

  public render() {
    timeout(() => {
      // Workaround: Since nodes need some position before rendering, assign 0
      this.graph.nodes.forEach(node => {
        node.x = 0;
        node.y = 0;
      });

      this.vue = new CSPGraphInteractor({
        data: {
          graph: this.graph,
          width: 0,
          height: 0,
          output: null
        }
      }).$mount();

      this.vue.$on("click:fine-step", () =>
        this.send({ event: StepEvents.FINE_STEP_CLICK })
      );
      this.vue.$on("click:step", () =>
        this.send({ event: StepEvents.STEP_CLICK })
      );
      this.vue.$on("click:auto-step", () =>
        this.send({ event: StepEvents.AUTO_STEP_CLICK })
      );

      // We debounce after our intial resize, since the first "resize" is when the cell is first executed
      // We don't want to delay for no reason in that case
      this.handleResize();
      this.handleResize = debounce(this.handleResize, 300);
      this.el.appendChild(this.vue.$el);
    });

    return this;
  }

  /**
   * Highlights an arc (or all arcs), as described by the event object.
   */
  private highlightArcs(event: Events.ICSPHighlightArcsEvent) {
    const strokeWidth = event.style === "bold" ? 7 : 4;

    if (event.arcIds == null) {
      for (const edge of this.graph.edges) {
        const stroke = event.colour ? event.colour : edge.styles.stroke;
        this.vue.$set(edge.styles, "stroke", stroke);
        this.vue.$set(edge.styles, "strokeWidth", strokeWidth);
      }
    } else {
      for (const arcId of event.arcIds) {
        const stroke = event.colour
          ? event.colour
          : this.graph.idMap[arcId].styles.stroke;
        this.vue.$set(this.graph.idMap[arcId].styles, "stroke", stroke);
        this.vue.$set(
          this.graph.idMap[arcId].styles,
          "strokeWidth",
          strokeWidth
        );
      }
    }
  }

  /**
   * Sets the domain of a variable node, as described by the event object.
   */
  private setDomain(event: Events.ICSPSetDomainEvent) {
    const variableNode = this.graph.idMap[event.nodeId] as ICSPGraphNode;
    variableNode.domain = event.domain;
  }

  /**
   * Highlights nodes, as described by the event object.
   */
  private highlightNodes(event: Events.ICSPHighlightNodesEvent) {
    for (const nodeId of event.nodeIds) {
      this.vue.$set(this.graph.idMap[nodeId].styles, "stroke", event.colour);
      this.vue.$set(this.graph.idMap[nodeId].styles, "strokeWidth", 2);
    }
  }

  /** Resize the width and height of the graph. */
  private handleResize() {
    const width = this.$el.width();
    const height = width / 1.6;

    if (this.vue != null) {
      d3ForceLayoutEngine.setup(this.graph, { width, height });
      this.vue.width = width;
      this.vue.height = height;
    }
  }
}
