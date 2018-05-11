<template>
  <div>
    <GraphVisualizerBase :graph="graph" :transitions="true" :layout="layout">
      <template slot="node" scope="props">
        <RoundedRectangleGraphNode hover="props.hover" :text="props.node.name" :textColour="nodeTextColour(props.node, props.hover)"
                          :subtext="showNodeHeuristics ? nodeHText(props.node) : undefined"
                          :fill="nodeFillColour(props.node, props.hover)" :hover="props.hover"
                          :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)"
                          @updateBounds="updateNodeBounds(props.node, $event)">
        </RoundedRectangleGraphNode>
      </template>
      <template slot="edge" scope="props">
        <DirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2" :stroke="props.edge.styles.stroke"
                      :strokeWidth="props.edge.styles.strokeWidth" :text="edgeText(props.edge)"
                      :sourceRx="props.edge.source.styles.rx" :sourceRy="props.edge.source.styles.ry"
                      :targetRx="props.edge.target.styles.rx" :targetRy="props.edge.target.styles.ry">
        </DirectedEdge>
      </template>
    </GraphVisualizerBase>
    <div class="footer">
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button id="auto-solve" class="btn btn-default" @click="$emit('click:auto-solve')">Auto Solve</button>
        <button id="pause" class="btn btn-default" @click="$emit('click:pause')">Pause</button>
      </div>
      <div class="output">{{output}}</div>
      <div class="frontier">Frontier: {{frontier}}</div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import DirectedEdge from "../../components/DirectedEdge.vue";
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
    DirectedEdge,
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
  /** The width, in pixels, of the visualizer. */
  width: number;
  /** The width, in pixels, of the visualizer. */
  height: number;
  /** Layout object that controls where nodes are drawn. */
  layout: GraphLayout;

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
  updateNodeBounds(node: ISearchGraphNode, bounds: { rx: number; ry: number }) {
    node.styles.rx = bounds.rx;
    node.styles.ry = bounds.ry;
  }
}

</script>
