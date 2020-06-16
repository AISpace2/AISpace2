<template>
  <div tabindex="0" @keydown.stop class="search_builder">
    <GraphVisualizerBase :graph="graph" :transitions="true" :layout="layout" 
                         @dblclick="createNode" @click:node="updateSelection" @click:edge="updateSelection"
                         :legendColor="legendColor" :legendText="legendText" :textSize="textSize">
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode :text="props.node.name"
                          :subtext="nodeHText(props.node)"
                          :fill="nodeFillColour(props.node)"
                          :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node, props.hover)"
                          @updateBounds="updateNodeBounds(props.node, $event)" :textSize="textSize" :hover="props.hover"
        :detailLevel="detailLevel">
        </RoundedRectangleGraphNode>
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
          :stroke="edgeStrokeColour(props.edge, props.hover)"
          :strokeWidth="edgeStrokeWidth(props.edge, props.hover)"
          :text="showEdgeCosts ? props.edge.cost : undefined" 
          :textSize="textSize" 
          :hover="props.hover"
          :graph_node_width="props.edge.styles.targetWidth" 
          :graph_node_height="props.edge.styles.targetHeight">
        </DirectedRectEdge>
      </template>
      <template slot="visualization" slot-scope="props">
        <a class="inline-btn-group" @click="detailLevel = detailLevel > 0 ? detailLevel - 1 : detailLevel">&#8249;</a>
        <label class="inline-btn-group">Detail</label>
        <a class="inline-btn-group" @click="detailLevel = detailLevel < 2 ? detailLevel + 1 : detailLevel">&#8250;</a>

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
        <p class="builder_output">
          <strong>To create variable:</strong> Set the name and the heuristic value of the note below,
          <br />and then double click at a position on the canvas where you want the new node to be created.
          <br />
          <span>
            <label>
              <strong>Name:</strong>
            </label>
            <input
              type="text"
              :value="temp_node_name"
              @focus="$event.target.select()"
              @input="temp_node_name = $event.target.value, cleanMessages()"
            />
            <label>
              <strong>Heuristic:</strong>
            </label>
            <input
              type="number"
              style="width: 150px;"
              :value="temp_node_heuristic"
              @focus="$event.target.select()"
              @input="temp_node_heuristic = $event.target.value, cleanMessages()"
            />
            <label>
              <strong>Type:</strong>
            </label>
            <select id="node-type">
              <option value="search:start">Start</option>
              <option value="search:regular">Regular</option>
              <option value="search:goal">Goal</option>
            </select>
          </span>
          <br />
          <!-- <span>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </span>
          <br /> -->
          <strong>To create edge:</strong> Click on the start node, then click on the end node.
          <br />
          <span
            v-if="(graph.nodes.indexOf(first) >= 0) && (selection == first || selection == null || selection.type == 'edge')"
          >
            Start node:
            <span class="nodeText">{{first.name}}</span>. Click on the end node to create an edge, or click on
            <span
              class="nodeText"
            >{{first.name}}</span> again to unselect it.
            <br />
          </span>
          <label>
            <strong>Cost:</strong>
          </label>
            <input
            type="number"
            style="width: 150px;"
            :value="temp_edge_cost"
            @focus="$event.target.select()"
            @input="temp_edge_cost = $event.target.value, cleanMessages()"
          />
          <br />
          <span>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </span>
        </p>
      </div>
    </div>

    <div>
      <div v-if="mode =='select'">
        <p class="builder_output">
          Set the name and the heuristic value of a node by cliking on it.
          <br />
        </p>
        <div v-if="selection && selection.type !== 'edge'">
          <div v-if="selection && (graph.nodes.indexOf(selection) > -1)">
            <p class="builder_output">
              You selected node
              <span class="nodeText">{{selection.name}}</span>.
              <br />
              <span>
                <label>
                  <strong>Name:</strong>
                </label>
                <input
                  type="text"
                  :value="selection ? temp_node_name : null"
                  @focus="$event.target.select()"
                  @input="temp_node_name = $event.target.value, cleanMessages()"
                  v-on:keyup.enter="isValidModifyName(temp_node_name), isValidModifyHeuristic(temp_node_heuristic)"
                />
                <label>
                  <strong>Heuristic Value:</strong>
                </label>
                <input
                  type="number"
                  v-model.number="temp_node_heuristic"
                  style="width: 150px;"
                  @focus="$event.target.select()"
                  @input="cleanMessages()"
                  v-on:keyup.enter="isValidModifyName(temp_node_name), isValidModifyHeuristic(temp_node_heuristic)"
                />
                <label>
                  <strong>Type:</strong>
                </label>
                <select id="node-type" v-model="selection.type">
                  <option value="search:start">Start</option>
                  <option value="search:regular">Regular</option>
                  <option value="search:goal">Goal</option>
                </select>
                <button
                  ref="btn_select_submit"
                  @click="isValidModifyName(temp_node_name), isValidModifyHeuristic(temp_node_heuristic)"
                >Submit</button>
              </span>
              <br />
            </p>
          </div>
        </div>
        <div v-if="selection && selection.type === 'edge'">
          <label>
            <strong>Cost:</strong>
          </label>
          <input
            type="number"
            style="width: 150px;"
            v-model.number="temp_edge_cost"
            @focus="$event.target.select()"
            @input="cleanMessages()"
            v-on:keyup.enter="isValidModifyCost(temp_edge_cost)"
          />
          <button
            ref="btn_select_submit"
            @click="isValidModifyCost(temp_edge_cost)"
          >Submit</button>
        </div>
        <p>
          <span class="warningText">{{warning_message}}</span>
          <span class="successText">{{succeed_message}}</span>
        </p>
      </div>
      <div v-else-if="mode == 'delete'">
        <p class="builder_output">
          Click on a node or an edge to delete.
          <br />
        </p>
        <p class="successText">{{succeed_message}}</p>
        <div :class="getDeletionConfirmationClass(to_delete)">
          <p v-if="selection">
            <span v-if="selection.type == 'edge'">
            <strong>
              Delete
              <span class="nodeText">{{selection.source.name}}---{{selection.target.name}}</span>?
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
import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode.vue";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";

import { Graph, ISearchGraphNode, ISearchGraphEdge } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import { nodeFillColour, nodeHText } from "../SearchUtils";


type Mode = "select" | "create" | "delete";

/**
 * Component to visually construct a search graph.
 *
 * Currently incomplete.
 */
@Component({
  components: {
    RoundedRectangleGraphNode, 
    SearchToolbar,
    GraphVisualizerBase, 
    DirectedRectEdge }
})
export default class SearchGraphBuilder extends Vue {
  /** The graph being built. */
  graph: Graph<ISearchGraphNode, ISearchGraphEdge>;
  
  /** The mode of the editor. */
  mode: Mode = "select";

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
  lineWidth: number;

  temp_node_name: string = "";
  temp_node_heuristic: number;
  temp_edge_cost: number;

  /** The current node or edge being selected. */
  selection: ISearchGraphNode | ISearchGraphEdge | null = null;
  /** During edge creation, tracks the source node of the edge to be formed. */
  first: ISearchGraphNode | ISearchGraphEdge | null = null;


  warning_message: string = "";
  succeed_message: string = "";

  /** Detect whether the user clicked an node/edge in delete mode */
  to_delete: boolean = false;


  /** Switches to a new mode. */
  setMode(mode: Mode) {
    this.mode = mode;
    this.selection = null;
    this.first = null;
  }

  cleanMessages() {
    this.warning_message = "";
    this.succeed_message = "";
  }


  /** Updates the user selection. If the selection was previously selected, unselects it. */
  updateSelection(selection: ISearchGraphNode | ISearchGraphEdge) {
    if (this.selection === selection) {
      this.selection = null;
      this.first = null;
    } else {
      this.selection = selection;
    }
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

  // =========================================================
  // canvas-related functions 
  nodeStrokeColour(selection: ISearchGraphNode, isHovering: boolean ) {
    if (selection === this.selection || isHovering ) {
      return "pink";
    }

    return "black";
  }


  edgeStrokeColour(selection: ISearchGraphEdge, isHovering: boolean) {
    if ((selection === this.selection || isHovering) && (this.mode == "select" || this.mode == "delete")) {
      return "pink";
    }

    return "black";
  }



  nodeStrokeWidth(node: ISearchGraphNode, isHovering: boolean ) {
    if (this.selection === node || isHovering ) {
      return 3;
    }

    return 1;
  }
  
  /** stroke width of an edge while hovered or not */
  edgeStrokeWidth(edge: ISearchGraphEdge, isHovering: boolean) {
    const isHighlight = isHovering && (this.mode == "select" || this.mode == "delete");
    const hoverWidth = isHighlight ? 3 : 0;

    if (edge.styles && edge.styles.strokeWidth) {
      return edge.styles.strokeWidth + hoverWidth;
    }

    return this.lineWidth + hoverWidth;
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


  // =========================================================
  // select-related functions 

  /** Returns whether the modified node name is valid,
   * if valid, update the values */
  isValidModifyName(name: string) {
    if (name === null || name.match(/^\s*$/)) {
      this.warning_message = "Name not valid.";
      this.succeed_message = "";
    } else if (this.NameExists(name) && this.selection.name !== name) {
      this.warning_message = "Name already exists.";
      this.succeed_message = "";
    } else {

      this.selection!.name = name;

      // this.warning_message = "";
      // this.succeed_message = "Node updated.";
    }
  }


  /** Returns whether the modified node heuristic is valid,
   * if valid, update the values */
  isValidModifyHeuristic(heuristic: number) {
    if (heuristic < 0) {
      this.warning_message = "Heuristic can't be negative.";
      this.succeed_message = "";
    } else if ( heuristic === null ) {
      this.warning_message = "Heuristic not valid.";
      this.succeed_message = "";
    } else {

      this.selection!.heuristic = heuristic;

      this.warning_message = "";
      this.succeed_message = "Node updated.";
    }
  }

  /** Returns whether the modified edge cost is valid,
   * if valid, update the values */
  isValidModifyCost(cost: number) {
    if (cost < 0) {
      this.warning_message = "Cost can't be negative.";
      this.succeed_message = "";
    } else if ( cost === null ) {
      this.warning_message = "Cost not valid.";
      this.succeed_message = "";
    } else {
      console.log(this.selection!.cost);
      console.log(cost);

      this.selection!.cost = cost;
      console.log(this.selection!.cost);
      console.log(cost);

      this.warning_message = "";
      this.succeed_message = "Edge updated.";
    }
  }

  // =========================================================
  // create-related functions 

  /** This is to avoid generate an existing node name if some node was deleted */
  genNewDefaultName() {
    var new_name = `Node${this.graph.nodes.length + 1}`;
    var acc = 0;
    while (this.NameExists(new_name)) {
      acc += 1;
      new_name = `Node${this.graph.nodes.length + acc}`;
    }
    return new_name;
  }


  /** Adds a node to the graph at position (x, y). */
  createNode(x: number, y: number) {
    if (this.mode === "create" && this.isTempNode(this.temp_node_name, this.temp_node_heuristic)) {
      this.graph.addNode({
        id: shortid.generate(),
        name: this.temp_node_name,
        x,
        y,
        heuristic: this.temp_node_heuristic
      } as ISearchGraphNode);

      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_heuristic = 0;
      this.warning_message = "";
    }
    this.first = null;
    this.selection = null;
    
    this.warning_message = "";
    this.succeed_message = "Node created.";
  }
  
  /** Returns whether name and heuristic for a new node to be created are valid */
  isTempNode(name_raw: string, heuristic: number) {
    var name = name_raw.trimLeft().trimRight();
    var node_to_be_drawn = true;
    if (name === null || name.match(/^\s*$/)) {
      node_to_be_drawn = false;
      this.warning_message = "Name not valid.";
      this.succeed_message = "";
    } else if (this.NameExists(name)) {
      node_to_be_drawn = false;
      this.warning_message = "Name already exists.";
      this.succeed_message = "";
    } else if (heuristic < 0) {
      node_to_be_drawn = false;
      this.warning_message = "Heuristic can't be negative.";
      this.succeed_message = "";
    } else if ( heuristic === null ) {
      node_to_be_drawn = false;
      this.warning_message = "Heuristic not valid.";
      this.succeed_message = "";
    } else {
      return node_to_be_drawn;
    }
  }





  /** Adds a new edge to the graph. */
  createEdge() {
    if (this.mode === "create" && this.selection != null && this.first != null &&
    (this.graph.nodes.indexOf(this.first as ISearchGraphNode) > -1) && (this.graph.nodes.indexOf(this.selection as ISearchGraphNode) > -1)
    && this.isTempEdge(this.temp_edge_cost)){

      this.cleanMessages();

      if (this.first === this.selection){
        this.first = null;
        this.selection = null;
        return;
      }

      
      // Can't create an edge if it already exists
      this.graph.edges.forEach(e => {
        if (e.source === this.first && e.target === this.selection) {
          this.first = null;
          this.selection = null;
          this.warning_message = "Edge already exists.";
          this.succeed_message = "";
          return;
        }
      });


      this.graph.addEdge({
        id: shortid.generate(),
        source: this.first.id,
        target: this.selection.id,
        name: "edge1",
        cost: this.temp_edge_cost
      });


      this.first = null;
      this.selection = null;
      
      this.temp_edge_cost = 1;
      
      this.warning_message = "";
      this.succeed_message = "Edge created.";



    }
  }

  /** Returns whether cost for a new edge to be created is valid */
  isTempEdge(cost: number) {
    if (cost < 0) {
      this.warning_message = "Cost can't be negative.";
      this.succeed_message = "";
      return false;
    } else if ( cost === null ) {
      this.warning_message = "Cost not valid.";
      this.succeed_message = "";
      return false;
    } else {
      return true;
    }
  }

  // =========================================================
  // delete-related functions 


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


  /** Remove the current selection from the graph. */
  deleteSelection() {
    if (this.selection && this.mode === "delete") {
      if (this.graph.edges.indexOf(this.selection as ISearchGraphEdge) > -1) {
        var source = this.selection.source;
        var target = this.selection.target;


        this.graph.removeEdge(this.selection as ISearchGraphEdge);
        this.succeed_message = "Edge deleted.";
      }
      if (this.graph.nodes.indexOf(this.selection as ISearchGraphNode) > -1) {
        this.graph.removeNode(this.selection as ISearchGraphNode);
        this.succeed_message = "Node deleted.";
      }
      this.selection = null;
      this.to_delete = false;
    }
  }

  @Watch("selection")
  onSelectionChanged() {
    if (this.mode === "select") {
      this.warning_message = "";
      this.succeed_message = "";
    }

    if (this.mode === "create") {
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_heuristic = 0;
      if (this.first === null) {
        this.first = this.selection as ISearchGraphNode;
      } else {
        this.createEdge();
      }
    } else if (this.mode === "delete"){
      if (this.selection) {
        this.warning_message = "";
        this.succeed_message = "";
        this.to_delete = true;
        this.$refs.delete_yes.focus();
      } else {
        this.to_delete = false;
      }
    } else if (this.mode === "select" && this.selection) {

      // selected an edge 
      if (this.graph.edges.indexOf(this.selection as ISearchGraphEdge) > -1) {

        console.log(this.temp_edge_cost);
        console.log(this.selection.cost!);
        this.temp_edge_cost = this.selection.cost!;    
      }
      // selected a node
      if (this.graph.nodes.indexOf(this.selection as ISearchGraphNode) > -1) {
        this.temp_node_name = this.selection.name!;
        this.temp_node_heuristic = this.selection.heuristic;
      }

    } else {
      this.selection = null;
    }
  }

  @Watch("mode")
  onModeChanged() {
    this.temp_node_name = "";
    this.temp_node_heuristic = null;
    this.temp_edge_cost = null;
    this.warning_message = "";
    this.succeed_message = "";
    this.first = null;
    this.to_delete = false;

    if (this.mode === "create") {
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_heuristic = 0;
      this.temp_edge_cost = 1;
      this.selection = null;
    }

    if (this.mode === "select" && this.selection) {
      this.temp_node_name = this.selection.name!;
      this.temp_node_heuristic = this.selection.heuristic;
    }
  }

  @Watch("first")
  onFirstChange() {
    if (this.selection) {
      this.cleanMessages();
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
