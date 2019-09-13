<template>
  <div class="search_builder">
    <GraphVisualizerBase
      :graph="graph"
      :transitions="true"
      :layout="layout"
      @dblclick="createNode"
      @click:node="updateSelection"
      @click:edge="updateSelection"
      :legendColor="legendColor"
      :legendText="legendText"
      :textSize="textSize"
    >
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode
          :text="props.node.name"
          :subtext="nodeHText(props.node)"
          :fill="nodeFillColour(props.node)"
          :stroke="strokeColourN(props.node, props.hover)"
          :stroke-width="nodeStrokeWidth(props.node, props.hover)"
          @updateBounds="updateNodeBounds(props.node, $event)"
          :textSize="textSize"
          :hover="props.hover"
          :detailLevel="detailLevel"
        ></RoundedRectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <DirectedRectEdge
          :x1="updateOverlappedEdege(props.edge).styles.x1"
          :x2="updateOverlappedEdege(props.edge).styles.x2"
          :y1="updateOverlappedEdege(props.edge).styles.y1"
          :y2="updateOverlappedEdege(props.edge).styles.y2"
          :sourceRx="props.edge.source.styles.rx"
          :sourceRy="props.edge.source.styles.ry"
          :targetRx="props.edge.target.styles.rx"
          :targetRy="props.edge.target.styles.ry"
          :stroke="strokeColourE(props.edge, props.hover)"
          :strokeWidth="edgeStrokeWidth(props.edge, props.hover)"
          :text="showEdgeCosts ? props.edge.cost : undefined"
          :textSize="textSize"
          :hover="props.hover"
          :nodeName="props.edge.target.name"
          :graph_node_width="props.edge.styles.targetWidth"
          :graph_node_height="props.edge.styles.targetHeight"
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
        <strong>Mode:</strong>
      </span>
      <SearchToolbar @modechanged="setMode"></SearchToolbar>

      <div v-if="mode == 'create'">
        <p>
          <strong>To create variable:</strong> Set the properties below, then double click on the graph.
          <br />
          <span>
            Node type:
            <span class="radioInputGroup">
              <input
                type="radio"
                id="nt_r"
                value="search:regular"
                v-model="node_type"
                @input="cleanMessages()"
              />
              <label for="nt_r">Regular</label>
            </span>
            <span class="radioInputGroup">
              <input
                type="radio"
                id="nt_s"
                value="search:start"
                v-model="node_type"
                @input="cleanMessages()"
              />
              <label for="nt_s">Start</label>
            </span>
            <span class="radioInputGroup">
              <input
                type="radio"
                id="nt_g"
                value="search:goal"
                v-model="node_type"
                @input="cleanMessages()"
              />
              <label for="nt_g">Goal</label>
            </span>
          </span>
          <br />
          <label>Node Name:</label>
          <input
            type="text"
            :value="temp_v_name"
            @focus="$event.target.select()"
            @input="temp_v_name = $event.target.value, cleanMessages()"
          />
          <label>Node Heuristic:</label>
          <input
            type="text"
            ref="Intonlyinput"
            :value="temp_heuristic"
            @focus="$event.target.select()"
            @blur="resetInputbox_heu($event.target.value)"
            @input="trimNonInt($event.target.value),temp_heuristic = $event.target.value, cleanMessages()"
          />
          <br />
          <span>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </span>
          <br />
          <strong>To create edge:</strong> Set the properties below, then click on the start node, then click on the end node.
          <br />
          <label>Edge Cost:</label>
          <input
            type="text"
            ref="numberonlyinput"
            :value="temp_e_cost"
            @focus="$event.target.select()"
            @blur="resetInputbox_cost($event.target.value)"
            @input="trimNonNumeric($event.target.value),temp_e_cost = $event.target.value, cleanMessages()"
          />
          <br />
          <span
            v-if="(graph.nodes.indexOf(first) >= 0) && (selection == first || selection == null || selection.type == 'edge')"
          >
            Source node:
            <span class="nodeText">{{first.name}}</span>. Select an end
            node to create an edge, or click on
            <span
              class="nodeText"
            >{{first.name}}</span> again to unselect it.
          </span>
          <span>
            <span class="warningText">{{edge_warning_message}}</span>
            <span class="successText">{{edge_succeed_message}}</span>
          </span>
        </p>
      </div>

      <div v-if="mode == 'select'">
        Select a node or an edge to modify its properties.
        <br />
        <div v-if="selection">
          <div v-if="selection.type != 'edge'">
            You selected node
            <span class="nodeText">{{selection.name}}</span>.
            <br />
            <span>
              <strong>Node type:</strong>
              <span class="radioInputGroup">
                <input
                  type="radio"
                  id="nt_r"
                  value="search:regular"
                  v-model="node_type"
                  @input="cleanMessages()"
                  v-on:keyup.enter="UpdateVariable(temp_v_name, temp_heuristic)"
                />
                <label for="nt_r">Regular</label>
              </span>
              <span class="radioInputGroup">
                <input
                  type="radio"
                  id="nt_s"
                  value="search:start"
                  v-model="node_type"
                  @input="cleanMessages()"
                  v-on:keyup.enter="UpdateVariable(temp_v_name, temp_heuristic)"
                />
                <label for="nt_s">Start</label>
              </span>
              <span class="radioInputGroup">
                <input
                  type="radio"
                  id="nt_g"
                  value="search:goal"
                  v-model="node_type"
                  @input="cleanMessages()"
                  v-on:keyup.enter="UpdateVariable(temp_v_name, temp_heuristic)"
                />
                <label for="nt_g">Goal</label>
              </span>
            </span>
            <br />
            <label>
              <strong>Node Name:</strong>
            </label>
            <input
              type="text"
              :value="temp_v_name"
              @focus="$event.target.select()"
              @input="temp_v_name = $event.target.value, cleanMessages()"
              v-on:keyup.enter="UpdateVariable(temp_v_name, temp_heuristic)"
            />
            <label>
              <strong>Node Heuristic:</strong>
            </label>
            <input
              type="text"
              ref="Intonlyinput"
              :value="temp_heuristic"
              @focus="$event.target.select()"
              @input="trimNonInt($event.target.value),temp_heuristic = $event.target.value, cleanMessages()"
              v-on:keyup.enter="UpdateVariable(temp_v_name, temp_heuristic)"
            />
            <button ref="node_submit" @click="UpdateVariable(temp_v_name, temp_heuristic)">Submit</button>
            <br />
          </div>

          <div v-else>
            You selected edge
            <span
              class="nodeText"
            >{{selection.source.name}}-->{{selection.target.name}}</span>.
            <br />
            <label>
              <strong>Edge Cost:</strong>
            </label>
            <input
              type="text"
              ref="numberonlyinput"
              :value="temp_e_cost"
              @focus="$event.target.select()"
              @input="trimNonNumeric($event.target.value),temp_e_cost = $event.target.value, cleanMessages()"
              v-on:keyup.enter="UpdateEdge(temp_e_cost)"
            />
            <button ref="edge_submit" @click="UpdateEdge(temp_e_cost)">Submit</button>
          </div>

          <span>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </span>
        </div>
      </div>

      <div v-if="mode == 'delete'">
        <p class="builder_output">
          Click on a node or an edge to delete.
          <br />
        </p>
        <div :class="getDeletionConfirmationClass(to_delete)">
          <p v-if="selection">
            <span v-if="selection.type == 'edge'">
              <strong>
                Delete
                <span class="nodeText">{{selection.source.name}}-->{{selection.target.name}}</span>?
              </strong>
            </span>
            <span v-else>
              <strong>
                Delete
                <span class="nodeText">{{selection.name}}</span>?
              </strong>
            </span>
          </p>
          <button ref="delete_yes" @click="deleteSelection()">Yes</button>
          <button ref="delete_no" @click="selection = null, to_delete = false">No</button>
        </div>
        <span>
          <span class="warningText">{{warning_message}}</span>
          <span class="successText">{{succeed_message}}</span>
        </span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import * as shortid from "shortid";

import SearchToolbar from "./SearchBuilderToolbar.vue";
import DirectedRectEdge from "../../components/DirectedRectEdge.vue";
import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";

import { Graph, ISearchGraphNode, ISearchGraphEdge } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import { nodeFillColour, nodeHText } from "../SearchUtils";

type Mode = "create" | "select" | "delete";
type NodeType = "search:start" | "search:goal" | "search:regular";

/**
 * Component to visually construct a search graph.
 *
 * Currently incomplete.
 */
@Component({
  components: {
    RoundedRectangleGraphNode,
    GraphVisualizerBase,
    DirectedRectEdge,
    SearchToolbar
  }
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
  legendText: string[];
  legendColor: string[];

  /** During edge creation, tracks the source node of the edge to be formed. */
  first: ISearchGraphNode | null = null;
  /** The mode of the builder. */
  mode: Mode = "create";
  /** The type of the node to be created. */
  node_type: NodeType = "search:regular";
  temp_v_name: string = "";
  temp_heuristic: string = "0";

  temp_e_cost: string = "1";

  warning_message: string = "";
  succeed_message: string = "";
  edge_succeed_message: string = "";
  edge_warning_message: string = "";

  /** Detect whether the user clicked an node/edge in delet mode */
  to_delete: boolean = false;

  /** The current node or edge being selected. */
  selection: ISearchGraphNode | ISearchGraphEdge | null = null;

  created() {
    this.temp_v_name = this.genNewDefaultName();
    this.temp_heuristic = "0";
  }

  setMode(mode: Mode) {
    this.mode = mode;
    this.selection = null;
    this.first = null;
  }

  /** If use v-show, when the component is hidden,
   * there's no input value (e.g. inputbox, buttons, etc.) focused,
   * This will cause a problem that after click "No" button,
   * Enter key won't work on the builder since the builder is not focused.
   * Therefore, the deletion confirmation must always show,
   * So when it is not needed, make it transparent. */
  getDeletionConfirmationClass(to_delete: boolean) {
    if (to_delete) {
      return "show_deletion_confirmation";
    } else {
      return "hide_deletion_confirmation";
    }
  }

  cleanMessages() {
    this.warning_message = "";
    this.succeed_message = "";
    this.edge_succeed_message = "";
    this.edge_warning_message = "";
  }

  genNewDefaultName() {
    var n_of_nodes = this.graph.nodes.length;
    var new_name = `Node${n_of_nodes}`;
    var acc = 0;
    while (this.NameExists(new_name)) {
      acc += 1;
      new_name = `Node${n_of_nodes + acc}`;
    }
    return new_name;
  }

  /** Check whether the given node name exists */
  NameExists(name: string) {
    var nameExists = false;
    this.graph.nodes.forEach(function(node) {
      if (node.name === name) {
        nameExists = true;
      }
    });
    return nameExists;
  }

  /** Trim non-positive-integer chars. */
  trimNonInt(val: string) {
    if (!val.match(/^[0-9]*$/)) {
      var result = val.replace(/[^\d]/g, "");

      this.$refs.Intonlyinput.value = result;
    }
  }

  /** Trim non-numeric chars. */
  trimNonNumeric(val_origin: string) {
    var val: string = "";
    if (val_origin[0] === "-") {
      val = val_origin.substring(1, val_origin.length);
    } else {
      val = val_origin;
    }
    if (val.match(/^.*[^0-9\.].*$/) || !val.match(/^[0-9]*\.?[0-9]*$/)) {
      var result = val.replace(/[^\d.]/g, "");

      if (!result.match(/^[0-9]*\.?[0-9]*$/)) {
        var indexofdot = result.indexOf(".");
        var result_removed_dot = result.replace(/\./g, "");
        result =
          result_removed_dot.slice(0, indexofdot) +
          "." +
          result_removed_dot.slice(indexofdot, result_removed_dot.length);
      }
      if (val_origin[0] === "-") {
        result = "-" + result;
      }
      this.$refs.numberonlyinput.value = result;
    }
  }

  createNode(x: number, y: number) {
    if (
      this.mode === "create" &&
      this.IsTempVariable(this.temp_v_name, parseInt(this.temp_heuristic))
    ) {
      this.graph.addNode({
        id: shortid.generate(),
        name: this.temp_v_name.trimLeft().trimRight(),
        x,
        y,
        type: this.node_type,
        h: parseInt(this.temp_heuristic)
      });

      this.warning_message = "";
      this.succeed_message = "Node created.";
      this.temp_v_name = this.genNewDefaultName();
    }

    this.first = null;
    this.selection = null;
  }

  IsTempVariable(temp_name: string, temp_heuristic: number) {
    var name = temp_name.trimLeft().trimRight();

    if (name === null || name.match(/^\s*$/)) {
      this.warning_message = "Name not valid. Please enter a new name.";
      this.succeed_message = "";
      return false;
    }

    if (this.NameExists(name) && this.selection.name !== temp_name) {
      this.warning_message = "Name already exists.";
      this.succeed_message = "";
      return false;
    }

    if (temp_heuristic < 0) {
      this.warning_message = "Heuristic cannot be negative.";
      this.succeed_message = "";
      return false;
    }

    if (!Number.isInteger(temp_heuristic)) {
      this.warning_message = "Heuristic must be an integer.";
      this.succeed_message = "";
      return false;
    }

    return true;
  }

  createEdge() {
    if (this.mode === "create" && this.first && this.selection) {
      if (this.EdgeExist(this.first, this.selection)) {
        this.edge_warning_message = "Edge exists.";
        return;
      }

      if (this.selection === this.first) {
        this.first = null;
        this.selection = null;
        return;
      }

      this.graph.addEdge({
        id: shortid.generate(),
        source: this.first.id,
        target: this.selection.id,
        name: "edge1",
        cost: parseFloat(this.temp_e_cost),
        type: "edge"
      });

      this.first = null;
      this.selection = null;
      this.edge_warning_message = "";
      this.edge_succeed_message = "Edge created.";
    }
  }

  /** Check whether two nodes are linked by an edge. */
  EdgeExist(source: ISearchGraphNode, target: ISearchGraphNode) {
    var exist = false;
    this.graph.edges.forEach(e => {
      if (e.target === target && e.source === source) {
        return (exist = true);
      }
    });
    return exist;
  }

  UpdateVariable(temp_name: string, temp_heuristic: string) {
    if (this.IsTempVariable(temp_name, parseInt(temp_heuristic))) {
      this.selection.name = temp_name.trimLeft().trimRight();
      this.selection.h = parseInt(temp_heuristic);
      this.selection.type = this.node_type;
      this.succeed_message = "Node updated.";
    }
  }

  UpdateEdge(temp_cost: string) {
    this.selection.cost = parseFloat(temp_cost);
    this.succeed_message = "Edge updated.";
  }

  /**
   * Separates overlapped edges.
   * Whenever a node involved in two overlapped edges is moved, update the fake node position
   * to make sure the two overlapped edges are splitted and move with node.
   */
  updateOverlappedEdege(edge: ISearchGraphEdge) {
    this.graph.edges.forEach(edge => {
      edge.x1 = edge.source.x;
      edge.x2 = edge.target.x;
      edge.y1 = edge.source.y;
      edge.y2 = edge.target.y;
    });

    this.graph.edges.forEach(e1 => {
      this.graph.edges.forEach(e2 => {
        if (
          e1.source === e2.target &&
          e1.target === e2.source &&
          e1.styles.x1 === e2.styles.x2 &&
          e1.styles.x2 === e2.styles.x1
        ) {
          e1.styles.overlapped = true;
          e2.styles.overlapped = true;
          const xa = e1.source.x;
          const ya = e1.source.y;
          const xb = e1.target.x;
          const yb = e1.target.y;
          const radius = 5;
          const cos: number =
            (yb! - ya!) /
            Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
          const sin: number =
            (xb! - xa!) /
            Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
          // Move both of the two overlapped edge from the original position
          e2.styles.x1 = cos * radius + xb!;
          e2.styles.x2 = cos * radius + xa!;
          e2.styles.y1 = yb! - sin * radius;
          e2.styles.y2 = ya! - sin * radius;
          e1.styles.x1 = xa! - cos * radius;
          e1.styles.x2 = xb! - cos * radius;
          e1.styles.y1 = sin * radius + ya!;
          e1.styles.y2 = sin * radius + yb!;
        }
      });
    });

    if (edge.styles.overlapped === true) {
      const xa = edge.source.x;
      const ya = edge.source.y;
      const xb = edge.target.x;
      const yb = edge.target.y;
      const radius = 5;
      const cos: number =
        (yb! - ya!) /
        Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
      const sin: number =
        (xb! - xa!) /
        Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
      edge.styles.x1 = xa! - cos * radius;
      edge.styles.x2 = xb! - cos * radius;
      edge.styles.y1 = sin * radius + ya!;
      edge.styles.y2 = sin * radius + yb!;
    } else {
      edge.styles.x1 = edge.source.x;
      edge.styles.x2 = edge.target.x;
      edge.styles.y1 = edge.source.y;
      edge.styles.y2 = edge.target.y;
    }
    return edge;
  }

  resetInputbox_heu(val_in_box: string) {
    if (val_in_box === null || val_in_box === "") {
      this.temp_heuristic = "0";
      this.$refs.Intonlyinput.value = "0";
    }
  }

  resetInputbox_cost(val_in_box: string) {
    if (val_in_box === null || val_in_box === "") {
      this.temp_e_cost = "1";
      this.$refs.numberonlyinput.value = "1";
    }
  }

  deleteSelection() {
    if (this.selection) {
      if (this.selection.type === "edge") {
        this.graph.removeEdge(this.selection);
        this.succeed_message = "Edge deleted.";
      } else {
        this.graph.removeNode(this.selection);
        this.succeed_message = "Node deleted.";
      }
      this.selection = null;
      this.to_delete = false;
    }
  }

  strokeColourN(selection: ISearchGraphNode, isHovering: boolean) {
    if (this.selection === selection || isHovering) {
      return "blue";
    }

    return "black";
  }

  strokeColourE(selection: ISearchGraphEdge, isHovering: boolean) {
    if (
      (this.selection === selection || isHovering) &&
      this.mode !== "create"
    ) {
      return "blue";
    }

    return "black";
  }

  nodeStrokeWidth(node: ISearchGraphNode, isHovering: boolean) {
    const isHighlight = isHovering || this.selection === node;
    const hoverWidth = isHighlight ? 3 : 0;

    if (node.styles && node.styles.strokeWidth) {
      return node.styles.strokeWidth + hoverWidth;
    }

    return 1 + hoverWidth;
  }

  /** stroke width of an edge while hovered or not */
  edgeStrokeWidth(edge: ISearchGraphEdge, isHovering: boolean) {
    const isHighlight =
      (isHovering || this.selection === edge) && this.mode !== "create";
    const hoverWidth = isHighlight ? 3 : 0;

    if (edge.styles && edge.styles.strokeWidth) {
      return edge.styles.strokeWidth + hoverWidth;
    }

    return 4 + hoverWidth;
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
      this.first = null;
    } else {
      this.selection = selection;
    }
  }

  // Whenever a node reports it has resized, update it's style so that it redraws.
  updateNodeBounds(
    node: ISearchGraphNode,
    bounds: { width: number; height: number }
  ) {
    node.styles.width = bounds.width;
    node.styles.height = bounds.height;
    this.graph.edges
      .filter(edge => edge.target.id === node.id)
      .forEach(edge => {
        this.$set(edge.styles, "targetWidth", bounds.width);
        this.$set(edge.styles, "targetHeight", bounds.height);
      });
  }

  @Watch("selection")
  onSelectionChanged() {
    if (this.mode === "create") {
      if (this.selection) {
        this.warning_message = "";
        this.succeed_message = "";
        this.edge_succeed_message = "";
        this.edge_warning_message = "";
      }
      if (this.first === null) {
        this.first = this.selection as ISearchGraphNode;
      } else {
        this.createEdge();
      }
      return;
    }

    if (this.mode === "select") {
      this.succeed_message = "";
      this.warning_message = "";

      if (this.selection.type === "edge") {
        this.temp_e_cost = this.selection.cost;
      } else {
        this.node_type = this.selection.type;
        this.temp_v_name = this.selection.name;
        this.temp_heuristic = this.selection.h;
      }
      return;
    }

    if (this.mode === "delete") {
      if (this.selection) {
        this.warning_message = "";
        this.succeed_message = "";
        this.to_delete = true;
        this.$refs.delete_yes.focus();
      } else {
        this.to_delete = false;
      }
      return;
    }
  }

  @Watch("mode")
  onModeChanged() {
    this.selection = null;
    this.first = null;
    this.temp_v_name = "";
    this.temp_heuristic = "0";
    this.temp_e_cost = "1";
    this.node_type = "search:regular";
    this.warning_message = "";
    this.succeed_message = "";
    this.edge_succeed_message = "";
    this.edge_warning_message = "";
    this.to_delete = false;

    if (this.mode === "create") {
      this.temp_v_name = this.genNewDefaultName();
      this.node_type = "search:regular";
      this.temp_heuristic = "0";
      this.temp_e_cost = "1";
    }
  }
}
</script>

<style scoped>
.show_deletion_confirmation {
  opacity: 1;
}

.hide_deletion_confirmation {
  opacity: 0;
}
</style>
