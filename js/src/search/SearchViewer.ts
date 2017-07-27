import { timeout } from "d3";
import * as widgets from "jupyter-js-widgets";
import { debounce } from "underscore";
import Vue from "vue";
import { IEvent, isOutputEvent } from "../Events";
import { Graph, ISearchGraphEdge, ISearchGraphNode } from "../Graph";
import {
  cytoscapeLayoutEngine,
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
      } else if (event.action === "add_neigh") {
        this.graph.nodes.push();
      }
    });

    this.listenTo(this.model, "change:graph_json", () => {
      this.graph = Graph.fromJSON(this.model.graphJSON) as Graph<
        ISearchGraphNode,
        ISearchGraphEdge
      >;

      this.layoutGraph({
        width: this.$el.width(),
        height: this.$el.width() / 1.6
      });

      this.vue.$data.graph = this.graph;
    });

    $(window).resize(() => {
      this.handleResize();
    });
  }

  public render() {
    const that = this;
    const App = Vue.extend({
      components: { SearchVisualizer },
      data() {
        return {
          graph: that.graph,
          showEdgeCosts: that.model.showEdgeCosts,
          showNodeHeuristics: that.model.showNodeHeuristics,
          output: null,
          width: 0,
          height: 0
        };
      },
      methods: {
        autostep() {
          that.send({ event: StepEvents.AUTO_STEP_CLICK });
        },
        finestep() {
          that.send({ event: StepEvents.FINE_STEP_CLICK });
        },
        step() {
          that.send({ event: StepEvents.STEP_CLICK });
        }
      },
      render(createElement: Vue.CreateElement) {
        return createElement(SearchVisualizer, {
          props: {
            graph: this.graph,
            width: this.width,
            height: this.height,
            showEdgeCosts: this.showEdgeCosts,
            showNodeHeuristics: this.showNodeHeuristics,
            output: this.output
          },
          on: {
            "click:auto-step": this.autostep,
            "click:step": this.step,
            "click:fine-step": this.finestep
          }
        });
      }
    });

    timeout(() => {
      // Workaround: Since nodes need some position before rendering, assign 0
      this.graph.nodes.forEach(node => {
        node.x = 0;
        node.y = 0;
      });

      this.vue = new App().$mount();

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
      Vue.set(node.styles, "stroke", "black");
      Vue.set(node.styles, "strokeWidth", 1);
    }

    for (const edge of this.graph.edges) {
      Vue.set(edge.styles, "stroke", "black");
      Vue.set(edge.styles, "strokeWidth", 4);
    }
  }

  /**
   * Highlights nodes in the visualization, as described by the event object.
   */
  private highlightNodes(event: SearchViewerEvents.IHighlightNodeEvent) {
    for (const nodeId of event.nodeIds) {
      const i = this.graph.nodes.map(a => a.id).findIndex(a => a === nodeId);

      if (i !== -1) {
        Vue.set(this.graph.nodes[i].styles, "stroke", event.colour);
        Vue.set(this.graph.nodes[i].styles, "strokeWidth", 3);
      }
    }
  }

  /**
   * Highlights a path in the visualization, as described by the event object.
   */
  private highlightPath(event: SearchViewerEvents.IHighlightPathEvent) {
    for (const edge of this.graph.edges) {
      if (event.path.includes(edge.id)) {
        Vue.set(edge.styles, "stroke", event.colour);
        Vue.set(edge.styles, "strokeWidth", 8);
      }
    }
  }

  /** Resize the width and height of the graph. */
  private handleResize() {
    const width = this.$el.width();
    const height = width / 1.6;

    if (this.vue != null) {
      this.layoutGraph({ width, height });
      this.vue.$data.width = width;
      this.vue.$data.height = height;
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

        d3TreeLayoutEngine.setup(this.graph, layoutParams, opts);
        break;
      }
      case "force":
      default:
        d3ForceLayoutEngine.setup(this.graph, layoutParams);
    }
  }
}
