<template>
  <div tabindex="0" @keydown.stop>
    <GraphVisualizerBase :graph="graph" :transitions="true" :layout="layout"
                         @click:node="updateSelection" @click:edge="updateSelection">
      <template slot="node" scope="props">
        <RoundedRectangleGraphNode :text="props.node.name"
                          :subtext="nodeHText(props.node)"
                          :fill="nodeFillColour(props.node)"
                          :stroke="strokeColour(props.node)" :stroke-width="nodeStrokeWidth(props.node)"
                          @updateBounds="updateNodeBounds(props.node, $event)" :textSize="textSize" :hover="props.hover">
        </RoundedRectangleGraphNode>
      </template>
      <template slot="edge" scope="props">
        <DirectedRectEdge :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y"
                      :sourceRx="props.edge.source.styles.rx" :sourceRy="props.edge.source.styles.ry"
                      :targetRx="props.edge.target.styles.rx" :targetRy="props.edge.target.styles.ry"
                      :stroke="strokeColour(props.edge)"
                      :strokeWidth="props.edge.styles.strokeWidth"
                      :text="showEdgeCosts ? props.edge.cost : undefined" :textSize="textSize" :hover="props.hover">
        </DirectedRectEdge>
      </template>
    </GraphVisualizerBase>
    <div>
      <div v-if="selection && selection.type !== 'edge'">
        <label for="node-name">Name</label>
        <input type="text" v-model="selection.name" />
        <label for="node-h">Heuristic Value</label>
        <input type="number" step="0.1" min="0" v-model="selection.h" />
        <label for="node-type">Type</label>
        <select id="node-type" v-model="selection.type">
          <option value="search:start">Start</option>
          <option value="search:regular">Regular</option>
          <option value="search:goal">Goal</option>
        </select>
      </div>
      <div v-if="selection && selection.type === 'edge'">
        <label for="edge-cost">Edge Cost</label>
        <input type="number" v-model.number="selection.cost">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import DirectedRectEdge from "../../components/DirectedRectEdge.vue";
import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode";

import { Graph, ISearchGraphNode, ISearchGraphEdge } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import { nodeFillColour, nodeHText } from "../SearchUtils";

/**
 * Component to visually construct a search graph.
 * 
 * Currently incomplete.
 */
@Component({
  components: {RoundedRectangleGraphNode, GraphVisualizerBase, DirectedRectEdge }
})
export default class SearchGraphBuilder extends Vue {
  /** The graph being built. */
  graph: Graph<ISearchGraphNode, ISearchGraphEdge>;
  /** True if edge costs should be shown on the edges. */
  showEdgeCosts: boolean;
  /** True if node heuristics should be shown on the nodes. */
  showNodeHeuristics: boolean;
  /** Layout object that controls where nodes are drawn. */
  layout: GraphLayout;
  textSize: number;

  /** The current node or edge being selected. */
  selection: ISearchGraphNode | ISearchGraphEdge | null = null;

  strokeColour(selection: ISearchGraphNode | ISearchGraphEdge) {
    if (this.selection === selection) {
      return "blue";
    }

    return "black";
  }

  nodeStrokeWidth(node: ISearchGraphNode) {
    if (this.selection === node) {
      return 3;
    }

    return 1;
  }

  nodeFillColour(node: ISearchGraphNode) {
    return nodeFillColour(node);
  }

  nodeHText(node: ISearchGraphNode) {
    if (!this.showNodeHeuristics) {
      return undefined;
    }

    return nodeHText(node);
  }

  updateSelection(selection: ISearchGraphNode | ISearchGraphEdge) {
    if (this.selection === selection) {
      this.selection = null;
    } else {
      this.selection = selection;
    }
  }

  updateNodeBounds(node: ISearchGraphNode, bounds: { width: number; height: number }) {
    node.styles.width = bounds.width;
    node.styles.height = bounds.height;
  }
}

</script>
