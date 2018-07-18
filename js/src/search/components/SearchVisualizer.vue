<template>
  <div class="search_visualizer">
    <GraphVisualizerBase :graph="graph" :transitions="true" :layout="layout" :legendColor="legendColor" :legendText="legendText">
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode :id="props.node.id" hover="props.hover" :text="props.node.name" :textColour="nodeTextColour(props.node, props.hover)"
                                   :subtext="showNodeHeuristics ? nodeHText(props.node) : undefined" :detailLevel="detailLevel"
                                   :fill="nodeFillColour(props.node, props.hover)" :hover="props.hover"
                                   :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)"
                                   @updateBounds="updateNodeBounds(props.node, $event)" :textSize="textSize">
        </RoundedRectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <DirectedRectEdge :id="props.edge.id" :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y" :stroke="props.edge.styles.stroke"
                          :strokeWidth="props.edge.styles.strokeWidth" :text="edgeText(props.edge)" :nodeName="props.edge.target.name"
                          :graph_node_width="props.edge.styles.targetWidth" :graph_node_height="props.edge.styles.targetHeight">
        </DirectedRectEdge>
      </template>
      <template slot="visualization" slot-scope="props">
        <a @click="props.toggleLegend">Toggle Legend</a>
        <a @click="$emit('toggle:showFullDomain')">Change Domain</a>

        <a class="inline-btn-group" @click="detailLevel = detailLevel > 0 ? detailLevel - 1 : detailLevel">&#8249;</a>
        <label class="inline-btn-group">Detail</label>
        <a class="inline-btn-group" @click="detailLevel = detailLevel < 2 ? detailLevel + 1 : detailLevel">&#8250;</a>

        <a class="inline-btn-group" @click="textSize = textSize - 1">-</a>
        <label class="inline-btn-group">{{textSize}}</label>
        <a class="inline-btn-group" @click="textSize = textSize + 1">+</a>
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
    /** Text describing what is currently happening. */
    output: string;
    /** The text representing the frontier. Persistent until frontier changes. */
    frontier: string;
    /** True if edge costs should be shown on the edges. */
    showEdgeCosts: boolean;
    /** True if node heuristics should be shown on the nodes. */
    showNodeHeuristics: boolean;
    // /** The width, in pixels, of the visualizer. */
    // width: number;
    // /** The width, in pixels, of the visualizer. */
    // height: number;
    /** Layout object that controls where nodes are drawn. */
    layout: GraphLayout;
    // The size of the text inside the node
    textSize: number;
    // Display setting for text
    // 0 is hide all text
    // 1 is show truncated version
    // 2 is show all text
    detailLevel: number;
    legendText: string[];
    legendColor: string[];

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
  }

</script>
