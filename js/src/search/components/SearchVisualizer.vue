<template>
  <div class="search_visualizer">
    <GraphVisualizerBase :graph="graph" :transitions="true" :layout="layout" :legendColor="legendColor" :legendText="legendText">
      <template slot="node" scope="props">
        <RoundedRectangleGraphNode :id="props.node.id" hover="props.hover" :text="props.node.name" :textColour="nodeTextColour(props.node, props.hover)"
                                   :subtext="showNodeHeuristics ? nodeHText(props.node) : undefined" :simplifyGraph="simplifyGraph"
                                   :fill="nodeFillColour(props.node, props.hover)" :hover="props.hover"
                                   :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)"
                                   @updateBounds="updateNodeBounds(props.node, $event)" :textSize="textSize">
        </RoundedRectangleGraphNode>
      </template>
      <template slot="edge" scope="props">
        <DirectedRectEdge :id="props.edge.id" :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y" :stroke="props.edge.styles.stroke"
                          :strokeWidth="props.edge.styles.strokeWidth" :text="edgeText(props.edge)" :nodeName="props.edge.target.name"
                          :graph_node_width="props.edge.styles.targetWidth" :graph_node_height="props.edge.styles.targetHeight">
        </DirectedRectEdge>
      </template>
      <template slot="visualization" scope="props">
        <foreignObject id="toggle_hide_text" :x="props.width - 120" :y="btnProp.y">
          <div class="btn-group-test">
            <button @click="simplifyGraph = true">Hide Text</button>
            <button @click="simplifyGraph = false">Show Text</button>
            <button @click="switchGraph">Switch Graph</button>
            <button @click="props.hideLegend">Hide Legend</button>
            <button @click="props.showLegend">Show Legend</button>
          </div>
        </foreignObject>
      </template>
    </GraphVisualizerBase>
    <div class="footer">
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button id="auto-solve" class="btn btn-default" @click="$emit('click:auto-solve')">Auto Solve</button>
        <button id="pause" class="btn btn-default" @click="$emit('click:pause')">Pause</button>
        <button id="print-positions" class="btn btn-default" @click="$emit('click:print-positions')">Print Positions</button>
      </div>
      <div class="output">{{output}}</div>
      <div class="frontier">Frontier: {{frontier}}</div>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
  import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
  import DirectedRectEdge from "../../components/DirectedRectEdge.vue";
  import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode.vue";
  import { Graph, ISearchGraphNode, ISearchGraphEdge } from "../../Graph";
  import { GraphLayout } from "../../GraphLayout";
  import { nodeFillColour, nodeHText } from "../SearchUtils";

  /**
   * A Search visualization that can be driven by backend code.
   *
   * Events Emitted:
   * - 'click:fine-step': The "fine step" button has been clicked.
   * - 'click:step': The "step" button has been clicked.
   * - 'click:auto-solve': The "auto solve" button has been clicked.
   */
  @Component({
    components: {
      GraphVisualizerBase,
      DirectedRectEdge,
      RoundedRectangleGraphNode,
    }
  })
  export default class SearchVisualizer extends Vue {
    /** The graph being visualized. */
    graph: Graph<ISearchGraphNode, ISearchGraphEdge>;
    originalGraph: Graph<ISearchGraphNode, ISearchGraphEdge>;
    /** The graph without common text (parent and child mutual text). */
    simplifiedGraph: Graph<ISearchGraphNode, ISearchGraphEdge>;
    /** Text describing what is currently happening. */
    output: string;
    /** The text representing the frontier. Persistent until frontier changes. */
    frontier: string;
    /** True if edge costs should be shown on the edges. */
    showEdgeCosts: boolean;
    /** True if node heuristics should be shown on the nodes. */
    showNodeHeuristics: boolean;
    /** The width, in pixels, of the visualizer. */
    width: number;
    /** The width, in pixels, of the visualizer. */
    height: number;
    /** Layout object that controls where nodes are drawn. */
    layout: GraphLayout;
    // The size of the text inside the node
    textSize: number;
    // True if want to truncate or minimize total number of nodes when number of node exceed a set number
    simplifyGraph: boolean;
    legendText: string[];
    legendColor: string[];

    created() {
      this.graph = this.simplifiedGraph;
    }

    nodeFillColour(node: ISearchGraphNode, hover: boolean) {
      if (hover) {
        return "black";
      }

      return nodeFillColour(node);
    }

    nodeTextColour(node: ISearchGraphNode, hover: boolean) {
      if (hover) {
        return "white";
      }

      return "black";
    }

    nodeStroke(node: ISearchGraphNode) {
      if (node.styles && node.styles.stroke) {
        return node.styles.stroke;
      }

      return "black";
    }

    nodeStrokeWidth(node: ISearchGraphNode) {
      if (node.styles && node.styles.strokeWidth) {
        return node.styles.strokeWidth;
      }

      return 1;
    }

    nodeHText(node: ISearchGraphNode) {
      if (!this.showNodeHeuristics) {
        return undefined;
      }

      return nodeHText(node);
    }

    edgeText(edge: ISearchGraphEdge) {
      let text = "";

      if (edge.name != null) {
        text = edge.name;
      }

      if (this.showEdgeCosts) {
        text += ` (${edge.cost})`;
      }

      return text;
    }

    /**
     * Whenever a node reports it has resized, update it's style so that it redraws.
     */
    updateNodeBounds(node: ISearchGraphNode, bounds: { width: number; height: number }) {
      node.styles.width = bounds.width;
      node.styles.height = bounds.height;
      this.graph.edges
        .filter(edge => edge.target.id === node.id)
        .forEach(edge => {
          this.$set(edge.styles, "targetWidth", bounds.width);
          this.$set(edge.styles, "targetHeight", bounds.height);
        });
    }

    get btnProp() {
      return {
        // first btn's and y position
        // x is missing because it will be hard coded adjusted based on svg's width
        // which can only be accessed in the template
        y: 20,
        // other btn's offset position from the previous one
        xOffset: 0,
        yOffset: 40,
      }
    }

    switchGraph() {
      console.log("switch graph");
      this.$set(this, "graph", this.simplifiedGraph);
    }
  }

</script>
<style scoped>

  .btn-group-test button {
    background-color: red; /* Green background */
    border: 1px solid white; /* Green border */
    color: white; /* White text */
    cursor: pointer; /* Pointer/hand icon */
    width: 80pt; /* Set a width if needed */
    display: block; /* Make the buttons appear below each other */
    font-size: 10px;
  }

  .btn-group-text button:not(:last-child) {
    border-bottom: none; /* Prevent double borders */
  }

  /* Add a background color on hover */
  .btn-group-test button:hover {
    background-color: darkred;
  }
</style>
