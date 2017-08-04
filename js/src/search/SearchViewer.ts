import { timeout } from "d3";
import * as widgets from "jupyter-js-widgets";
import { debounce } from "underscore";
import Vue from "vue";
import { IEvent, isOutputEvent } from "../Events";
import { Graph, ISearchGraphEdge, ISearchGraphNode } from "../Graph";
import {
  d3ForceLayoutEngine,
  d3TreeLayoutEngine,
  IGraphLayoutParams
} from "../GraphLayout";
import * as StepEvents from "../StepEvents";
import SearchVisualizer from "./components/SearchVisualizer.vue";
import * as SearchViewerEvents from "./SearchViewerEvents";
import SearchViewerModel from "./SearchViewerModel";

export default class SearchViewer extends widgets.DOMWidgetView {
  public model: SearchViewerModel;
  private graph: Graph<ISearchGraphNode, ISearchGraphEdge>;
  private vue: any;

  public initialize(opts: any) {
    super.initialize(opts);
    this.graph = Graph.fromJSON(this.model.graphJSON) as Graph<
      ISearchGraphNode,
      ISearchGraphEdge
    >;
    this.listenTo(this.model, "view:msg", (event: IEvent) => {
      // tslint:disable-next-line:no-console
      console.log(event);

      if (isOutputEvent(event)) {
        this.vue.output = event.text;
      } else if (SearchViewerEvents.isClearEvent(event)) {
        this.clearStyling();
      } else if (SearchViewerEvents.isHighlightNodeEvent(event)) {
        this.highlightNodes(event);
      } else if (SearchViewerEvents.isHighlightPathEvent(event)) {
        this.highlightPath(event);
      }
    });

    this.listenTo(this.model, "change:graph_json", () => {
      this.graph = Graph.fromJSON(this.model.graphJSON, this.graph) as Graph<
        ISearchGraphNode,
        ISearchGraphEdge
      >;

      this.layoutGraph({
        width: this.$el.width(),
        height: this.$el.width() / 1.6
      }).then(() => {
        this.vue.graph = this.graph;
      });
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

      this.vue = new SearchVisualizer({
        data: {
          graph: this.graph,
          width: 0,
          height: 0,
          showEdgeCosts: this.model.showEdgeCosts,
          showNodeHeuristics: this.model.showNodeHeuristics,
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
  }

  /**
   * Resets all the styles in the graph (stroke colours and stroke width) back to default.
   */
  private clearStyling() {
    for (const node of this.graph.nodes) {
      this.vue.$set(node.styles, "stroke", "black");
      this.vue.$set(node.styles, "strokeWidth", 1);
    }

    for (const edge of this.graph.edges) {
      this.vue.$set(edge.styles, "stroke", "black");
      this.vue.$set(edge.styles, "strokeWidth", 4);
    }
  }

  /**
   * Highlights nodes in the visualization, as described by the event object.
   */
  private highlightNodes(event: SearchViewerEvents.IHighlightNodeEvent) {
    for (const nodeId of event.nodeIds) {
      this.vue.$set(this.graph.idMap[nodeId].styles, "stroke", event.colour);
      this.vue.$set(this.graph.idMap[nodeId].styles, "strokeWidth", 3);
    }
  }

  /**
   * Highlights a path in the visualization, as described by the event object.
   */
  private highlightPath(event: SearchViewerEvents.IHighlightPathEvent) {
    for (const edgeId of event.path) {
      this.vue.$set(this.graph.idMap[edgeId].styles, "stroke", event.colour);
      this.vue.$set(this.graph.idMap[edgeId].styles, "strokeWidth", 8);
    }
  }

  /** Resize the width and height of the graph. */
  private handleResize() {
    const width = this.$el.width();
    const height = width / 1.6;

    if (this.vue != null) {
      this.layoutGraph({ width, height });
      this.vue.width = width;
      this.vue.height = height;
    }
  }

  /** Layout the graph using the current layout method. */
  private layoutGraph(layoutParams: IGraphLayoutParams) {
    switch (this.model.layoutMethod) {
      case "tree": {
        const opts = { root: this.graph.nodes[0] };
        const root = this.graph.nodes.find(
          n => n.id === this.model.layoutRootId
        );

        if (root != null) {
          opts.root = root;
        }

        return d3TreeLayoutEngine.setup(this.graph, layoutParams, opts);
      }
      case "force":
      default:
        return d3ForceLayoutEngine.setup(this.graph, layoutParams);
    }
  }
}
