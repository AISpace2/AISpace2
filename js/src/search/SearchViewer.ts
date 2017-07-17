import { timeout } from "d3";
import * as widgets from "jupyter-js-widgets";
import { debounce } from "underscore";
import Vue from "vue";
import { IEvent, isOutputEvent } from "../Events";
import { Graph, ISearchGraphEdge, ISearchGraphNode } from "../Graph";
import { d3ForceLayoutEngine } from "../GraphLayout";
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
      console.log(event);

      if (isOutputEvent(event)) {
        this.vue.output = event.text;
      } else if (SearchViewerEvents.isClearEvent(event)) {
        this.clearStyling();
      } else if (SearchViewerEvents.isHighlightNodeEvent(event)) {
        this.highlightNode(event);
      } else if (SearchViewerEvents.isHighlightPathEvent(event)) {
        this.highlightPath(event);
      }
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
          height: 0,
          output: null,
          showEdgeCosts: that.model.showEdgeCosts,
          width: 0
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
      template: `
      <div id="app">
          <SearchVisualizer 
              :graph="graph" :output="output" :showEdgeCosts="showEdgeCosts"
              :width="width" :height="height"
              @click:auto-step="autostep"
              @click:step="step"
              @click:fine-step="finestep">
          </SearchVisualizer>
      </div>`
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
   * Highlights a node in the visualization, as described by the event object.
   */
  private highlightNode(event: SearchViewerEvents.IHighlightNodeEvent) {
    const i = this.graph.nodes
      .map(a => a.id)
      .findIndex(a => a === event.nodeId);

    if (i !== -1) {
      Vue.set(this.graph.nodes[i].styles, "stroke", event.colour);
      Vue.set(this.graph.nodes[i].styles, "strokeWidth", 3);
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
      d3ForceLayoutEngine.setup(this.graph, { width, height });
      this.vue.$data.width = width;
      this.vue.$data.height = height;
    }
  }
}
