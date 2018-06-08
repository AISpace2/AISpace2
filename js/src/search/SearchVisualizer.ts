import * as widgets from "@jupyter-widgets/base";
import { timeout } from "d3";
import { without } from "underscore";
import Vue from "vue";
import * as Analytics from "../Analytics";
import { Graph, ISearchGraphEdge, ISearchGraphNode } from "../Graph";
import { d3ForceLayout, d3TreeLayout, GraphLayout } from "../GraphLayout";
import * as StepEvents from "../StepEvents";
import SearchVisualizer from "./components/SearchVisualizer.vue";
import * as SearchEvents from "./SearchVisualizerEvents";
import SearchViewerModel from "./SearchVisualizerModel";
import * as labelDict from "../labelDictionary";
/**
 * Creates a Search visualization and handles events received from the backend.
 * 
 * See the accompanying backend file: `aispace2/jupyter/search/search.py`
 */
export default class SearchViewer extends widgets.DOMWidgetView {
  public model: SearchViewerModel;
  private vue: any;

  public initialize(opts: any) {
    super.initialize(opts);

    this.listenTo(this.model, "view:msg", (event: SearchEvents.Events) => {
      switch (event.action) {
        case "highlightPath":
          return this.highlightPath(event);
        case "highlightNodes":
          return this.highlightNodes(event);
        case "clear":
          return this.clearStyling();
        case "setFrontier":
          this.vue.frontier = event.frontier;
          return;
        case "output":
          this.vue.output = event.text;
          return;
      }
    });

    this.listenTo(this.model, "change:graph", () => {
      // Nodes/edges have been added to the graph from the backend.
      this.model.graph.mergeStylesFrom(this.model.previous("graph"));
      this.vue.graph = this.model.showFullDomain
        ? this.model.graph
        : this.trimGraph();
    });
  }

  public render() {
    timeout(() => {
      this.vue = new SearchVisualizer({
        data: {
          graph: this.model.graph,
          layout: this.getLayout(),
          showEdgeCosts: this.model.showEdgeCosts,
          showNodeHeuristics: this.model.showNodeHeuristics,
          output: null,
          textSize: this.model.textSize,
          simplifyGraph: this.model.simplifyGraph,
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

      this.vue.$on(StepEvents.PRINT_POSITIONS, ()=>{
        this.send({event: StepEvents.PRINT_POSITIONS, nodes: this.vue.graph.nodes})
      })

      if (!this.model.previouslyRendered) {
        this.send({ event: "initial_render" });
      }
    });
  }

  public remove() {
    if (this.vue != null) {
      this.vue.$destroy();
    }
  }

  /**
   * Resets all the styles in the graph (stroke colours and stroke width) back to default.
   */
  private clearStyling() {
    for (const node of this.model.graph.nodes) {
      this.vue.$set(node.styles, "stroke", "black");
      this.vue.$set(node.styles, "strokeWidth", 1);
    }

    for (const edge of this.model.graph.edges) {
      this.vue.$set(edge.styles, "stroke", "black");
      this.vue.$set(edge.styles, "strokeWidth", this.model.lineWidth);
    }
  }

  /**
   * Highlights nodes in the visualization, as described by the event object.
   */
  private highlightNodes(event: SearchEvents.IHighlightNodeEvent) {
    for (const nodeId of event.nodeIds) {
      this.vue.$set(
        this.model.graph.idMap[nodeId].styles,
        "stroke",
        event.colour
      );
      this.vue.$set(this.model.graph.idMap[nodeId].styles, "strokeWidth", 4);
    }
  }

  /**
   * Highlights a path in the visualization, as described by the event object.
   */
  private highlightPath(event: SearchEvents.IHighlightPathEvent) {
    for (const edgeId of event.path) {
      this.vue.$set(
        this.model.graph.idMap[edgeId].styles,
        "stroke",
        event.colour
      );
      this.vue.$set(
        this.model.graph.idMap[edgeId].styles,
        "strokeWidth",
        this.model.lineWidth + 3
      );
    }
  }

  /** Returns the layout based on current settings. */
  private getLayout() {
    switch (this.model.layoutMethod) {
      case "tree":
        return new GraphLayout(
          d3TreeLayout({ rootId: this.model.layoutRootId })
        );
      case "force":
      default:
        return new GraphLayout(d3ForceLayout());
    }
  }

  private trimGraph() {
    const graph = this.model.graph;
    // make backup text of parent
    // child and parent have to be defined since it is connected by an edge
    for (const edge of graph.edges) {
      const child = graph.nodes.find(node => node.id === edge.target.id);
      const parent = graph.nodes.find(node => node.id === edge.source.id);
      child!.parentText = this.format(parent!.name);
    }

    for (const edge of graph.edges) {
      const child = graph.nodes.find(node => node.id === edge.target.id);
      const parent = graph.nodes.find(node => node.id === edge.source.id);
      const childText = this.format(child!.name);
      const parentText = this.format(parent!.name);
      child!.name = childText.replace(child!.parentText + ", ", "");
    }

    return graph;
  }

  private format(str: string): string {
    const characters = str.split("");
    const charsToRemove = ["{", "}", "'"];
    return without(characters, ...charsToRemove).join("");
  }
}
