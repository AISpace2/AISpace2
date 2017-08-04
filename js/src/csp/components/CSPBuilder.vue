<template>
  <div>
    <GraphVisualizerBase :graph="graph" :width="width" :height="height"
      @dblclick="createNode" @click:edge="updateSelection" @click:node="updateSelection" @delete="deleteSelection">
      <template slot="node" scope="props">
        <EllipseGraphNode v-if="props.node.type === 'csp:variable'" :text="props.node.name" :subtext="domainText(props.node)"
                         :fill="props.node === selection ? 'pink' : 'white'">
        </EllipseGraphNode>
        <RectangleGraphNode v-if="props.node.type === 'csp:constraint'" :text="constraintText(props.node)"
                           :fill="props.node === selection ? 'pink' : 'white'">
        </RectangleGraphNode>
      </template>
      <template slot="edge" scope="props">
        <UndirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2" :stroke="strokeColour(props.edge)"></UndirectedEdge>
      </template>
    </GraphVisualizerBase>

    <div>
      <span>
        <b>Mode: </b>
      </span>
      <CSPToolbar @modechanged="setMode"></CSPToolbar>
      <div v-if="mode == 'variable' || mode == 'constraint' ">
        <span>Double click on the graph to create a new {{mode}}.</span>
      </div>
      <div v-else-if="mode == 'edge'">
        <span v-if="first == null">Select the first node to begin.</span>
        <span v-else>Source node: {{first.name}}. Select an end node to create an edge.</span>
      </div>
    </div>

    <div>
      <div v-if="selection && selection.type === 'csp:variable'">
        <label>Name</label>
        <input type="text" :value="selection ? selection.name : null" @input="selection ? selection.name = $event.target.value : null" />
        <label>Domain</label>
        <input type="text" :value="selection ? selection.domain : null" @change="selection ? selection.domain = $event.target.value.split(',').map(a => +a) : null" />
      </div>
      <div v-else-if="selection && selection.type === 'csp:constraint'">
        <label>Constraint Type</label>
        <select v-model="selection.constraint" :disabled="selection.constraint == null">
          <option value="lt">Less than (&#60;)</option>
          <option value="gt">Greater than (&#62;)</option>
          <option value="eq">Equal to (=)</option>
          <option value="undefined" v-if="selection.constraint == null">Python Constraint</option>
        </select>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

import CSPToolbar from "./CSPBuilderToolbar.vue";
import EllipseGraphNode from "../../components/EllipseGraphNode.vue";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import RectangleGraphNode from "../../components/RectangleGraphNode.vue";
import UndirectedEdge from "../../components/UndirectedEdge.vue";

import { Graph, ICSPGraphNode, IGraphEdge } from "../../Graph";
import * as CSPGraphUtils from "../CSPGraphUtils";

type Mode = "select" | "variable" | "constraint" | "edge";

/**
 * Component to visually construct a CSP graph.
 */
@Component({
  components: {
    CSPToolbar,
    EllipseGraphNode,
    GraphVisualizerBase,
    RectangleGraphNode,
    UndirectedEdge
  }
})
export default class CSPGraphBuilder extends Vue {
  /** The graph being built by this builder. */
  graph: Graph<ICSPGraphNode>;
  /** The width, in pixels, of the graph builder. */
  width: number;
  /** The height, in pixels, of the graph builder. */
  height: number;

  /** The mode of the editor. */
  mode: Mode = "select";

  /** The currently selected node or edge. Actions are preformed on the selection. */
  selection: ICSPGraphNode | IGraphEdge | null = null;
  /** During edge creation, tracks the source node of the edge to be formed. */
  first: ICSPGraphNode | null = null;

  /** Switches to a new mode. */
  setMode(mode: Mode) {
    this.mode = mode;
    this.selection = null;
    this.first = null;
  }

  /** Adds a node to the graph at position (x, y). */
  createNode(x: number, y: number) {
    if (this.mode === "variable") {
      this.graph.addNode({
        name: "asdf",
        x,
        y,
        type: "csp:variable",
        domain: []
      });
    } else if (this.mode === "constraint") {
      this.graph.addNode({
        name: "asdf",
        x,
        y,
        type: "csp:constraint",
        constraint: "gt"
      });
    }
  }

  /** Adds a new edge to the graph. */
  createEdge() {
    if (this.mode === "edge" && this.selection != null && this.first != null) {
      if (
        this.first.type === "csp:variable" &&
        this.selection.type === "csp:variable"
      ) {
        console.log("Can't create an edge between two variables");
        this.first = null;
        this.selection = null;
        return;
      }

      this.graph.addEdge({
        source: this.first,
        target: this.selection,
        name: "edge1"
      });

      this.first = null;
      this.selection = null;
    }
  }

  strokeColour(edge: IGraphEdge) {
    if (edge === this.selection) {
      return "pink";
    }

    return "black";
  }

  domainText(node: ICSPGraphNode) {
    return CSPGraphUtils.domainText(node);
  }

  constraintText(node: ICSPGraphNode) {
    return CSPGraphUtils.constraintText(node);
  }

  /** Updates the user selection. If the selection was previously selected, unselects it. */
  updateSelection(selection: ICSPGraphNode | IGraphEdge) {
    if (this.selection === selection) {
      this.selection = null;
    } else {
      this.selection = selection;
    }
  }

  /** Remove the current selection from the graph. */
  deleteSelection() {
    if (this.selection) {
      if (this.selection.type === "edge") {
        this.graph.removeEdge(this.selection);
      } else {
        this.graph.removeNode(this.selection);
      }
      this.selection = null;
    }
  }

  @Watch("selection")
  onSelectionChanged() {
    if (this.mode === "edge") {
      if (this.first == null) {
        this.first = this.selection as ICSPGraphNode;
      } else {
        this.createEdge();
      }
    } else if (this.mode !== "select") {
      this.selection = null;
    }
  }
}
</script>

<style scoped>
text.domain {
  font-size: 12px;
}
</style>
