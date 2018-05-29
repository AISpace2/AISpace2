<template>
  <div>
    <GraphVisualizerBase :graph="graph" :transitions="true" :layout="layout"
      @dblclick="createNode" @click:edge="updateSelection" @click:node="updateSelection" @delete="deleteSelection">
      <template slot="node" scope="props">
        <RoundedRectangleGraphNode v-if="props.node.type === 'csp:variable'" :text="props.node.name" :subtext="domainText(props.node)"
                         :fill="props.node === selection ? 'pink' : 'white'" :textSize="textSize" :hover="props.hover">
        </RoundedRectangleGraphNode>
        <RectangleGraphNode v-if="props.node.type === 'csp:constraint'" :text="constraintText(props.node)"
                           :fill="props.node === selection ? 'pink' : 'white'" :textSize="textSize" :hover="props.hover">
        </RectangleGraphNode>
      </template>
      <template slot="edge" scope="props">
        <UndirectedEdge :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y" :stroke="strokeColour(props.edge)"></UndirectedEdge>
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
import * as shortid from "shortid";

import CSPToolbar from "./CSPBuilderToolbar.vue";=
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import RectangleGraphNode from "../../components/RectangleGraphNode.vue";
import UndirectedEdge from "../../components/UndirectedEdge.vue";

import { Graph, ICSPGraphNode, IGraphEdge } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import * as CSPUtils from "../CSPUtils";
import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode";

type Mode = "select" | "variable" | "constraint" | "edge";

/**
 * Component to visually construct a CSP graph.
 * 
 * Currently incomplete.
 */
@Component({
  components: {
    RoundedRectangleGraphNode,
    CSPToolbar,
    GraphVisualizerBase,
    RectangleGraphNode,
    UndirectedEdge
  }
})
export default class CSPGraphBuilder extends Vue {
  /** The graph being built by this builder. */
  graph: Graph<ICSPGraphNode>;
  /** Layout object that controls where nodes are drawn. */
  layout: GraphLayout;

  /** The mode of the editor. */
  mode: Mode = "select";
  /** The currently selected node or edge. Actions are preformed on the selection. */
  selection: ICSPGraphNode | IGraphEdge | null = null;
  /** During edge creation, tracks the source node of the edge to be formed. */
  first: ICSPGraphNode | null = null;
  textSize: number;

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
        id: shortid.generate(),
        name: "asdf",
        x,
        y,
        type: "csp:variable",
        domain: []
      });
    } else if (this.mode === "constraint") {
      this.graph.addNode({
        id: shortid.generate(),
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
        id: shortid.generate(),
        source: this.first.id,
        target: this.selection.id,
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
    return CSPUtils.domainText(node);
  }

  constraintText(node: ICSPGraphNode) {
    return CSPUtils.constraintText(node);
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
