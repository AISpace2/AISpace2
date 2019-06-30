<template>
  <div tabindex="0" @keydown.stop class="search_builder">
    <GraphVisualizerBase
      :graph="graph"
      :transitions="true"
      :layout="layout"
      @click:node="updateSelection"
      @click:edge="updateSelection"
      @delete="deleteSelection"
    >
      <template slot="node" slot-scope="props">
        <RoundGraphNode
          :text="props.node.name"
          :subtext="nodeHText(props.node)"
          :fill="nodeFillColour(props.node)"
          :stroke="strokeColour(props.node)"
          :stroke-width="nodeStrokeWidth(props.node)"
          @updateBounds="updateNodeBounds(props.node, $event)"
          :textSize="textSize"
          :hover="props.hover"
          :detailLevel="detailLevel"
        ></RoundGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <DirectedRectEdge
          :x1="props.edge.source.x"
          :x2="props.edge.target.x"
          :y1="props.edge.source.y"
          :y2="props.edge.target.y"
          :sourceRx="props.edge.source.styles.rx"
          :sourceRy="props.edge.source.styles.ry"
          :targetRx="props.edge.target.styles.rx"
          :targetRy="props.edge.target.styles.ry"
          :stroke="strokeColour(props.edge)"
          :strokeWidth="props.edge.styles.strokeWidth"
          :text="showEdgeCosts ? props.edge.cost : undefined"
          :textSize="textSize"
          :hover="props.hover"
        ></DirectedRectEdge>
      </template>
      <template slot="visualization" slot-scope="props">
        <a
          class="inline-btn-group"
          @click="detailLevel = detailLevel > 0 ? detailLevel - 1 : detailLevel"
        >&#8249;</a>
        <label class="inline-btn-group">Detail</label>
        <a
          class="inline-btn-group"
          @click="detailLevel = detailLevel < 2 ? detailLevel + 1 : detailLevel"
        >&#8250;</a>
        <a class="inline-btn-group" @click="textSize = textSize - 1">-</a>
        <label class="inline-btn-group">{{textSize}}</label>
        <a class="inline-btn-group" @click="textSize = textSize + 1">+</a>
      </template>
    </GraphVisualizerBase>
    <div>
      <span>
        <b>Mode:</b>
        <template>
          <span>
            <input type="radio" id="setRadio" value="select" name="set-radio" v-model="mode">
            <label for="setRadio">Set Property</label>
            <input type="radio" id="edgeRadio" value="edge" name="edge-radio" v-model="mode">
            <label for="edgeRadio">Create Variable</label>
          </span>
        </template>
      </span>
      <template>
        <span></span>
      </template>
    </div>
    <div>
      <div v-if="selection && selection.type !== 'edge'">
        <label for="node-name">Name</label>
        <input type="text" v-model="selection.name">
        <label for="node-h">Heuristic Value</label>
        <input type="number" step="0.1" min="0" v-model="selection.h">
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
      <div>
        <span>Push "Del" to delete selected node or edge</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

import DirectedRectEdge from "../../components/DirectedRectEdge.vue";
import RoundGraphNode from "../../components/RoundGraphNode";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import * as shortid from "shortid";

import { Graph, ISearchGraphNode, ISearchGraphEdge } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import { nodeFillColour, nodeHText } from "../SearchUtils";
/**
 * Component to visually construct a search graph.
 *
 * Currently incomplete.
 */

type Mode = "select" | "edge";

@Component({
  components: { RoundGraphNode, GraphVisualizerBase, DirectedRectEdge }
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
  detailLevel: number;

  /** The mode of the editor. Initial should be select because the initially selected node in CSPBuilderToolbar is select*/
  mode: Mode = "select";
  /** The current node or edge being selected. */
  selection: ISearchGraphNode | ISearchGraphEdge | null = null;
  /** During edge creation, tracks the source node of the edge to be formed. */
  sourceNode: ISearchGraphNode | null = null;

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

  // Deletes selected node or edge when "Del" is pressed
  deleteSelection(selection: ISearchGraphNode | ISearchGraphEdge) {
    if (this.selection.type === "edge") {
      this.graph.removeEdge(this.selection);
    } else {
      this.graph.removeNode(this.selection);
    }
    this.selection = null;
  }

  // Generate edge between two search graph nodes. Function gets called when(In edge mode & selected 2 nodes sequentially)
  createEdge() {
    if (
      this.mode === "edge" &&
      this.selection != null &&
      this.sourceNode != null
    ) {
      this.graph.addEdge({
        id: shortid.generate(),
        source: this.sourceNode.id,
        target: this.selection.id,
        name: "edge"
      });

      this.sourceNode = null;
      this.selection = null;
    }
  }

  updateNodeBounds(
    node: ISearchGraphNode,
    bounds: { width: number; height: number }
  ) {
    node.styles.width = bounds.width;
    node.styles.height = bounds.height;
  }

  // Watch for when mode selection is done
  @Watch("selection")
  onSelectionChanged() {
    if (this.mode === "edge") {
      if (this.sourceNode == null) {
        this.sourceNode = this.selection as ISearchGraphNode;
      } else {
        this.createEdge();
      }
    } else if (this.mode !== "select") {
      this.selection = null;
    }
  }
}
</script>
