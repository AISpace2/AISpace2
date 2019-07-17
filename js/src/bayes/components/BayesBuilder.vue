<template>
  <div class="bayes_builder">
    <GraphVisualizerBase
      :graph="graph"
      :transitions="true"
      :layout="layout"
      @dblclick="createNode"
      @click:edge="updateSelection"
      @click:node="updateSelection"
    >
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode
          :text="props.node.name"
          :subtext="domainText(props.node)"
          :fill="nodeBackground(props.node, props.hover)"
          :textSize="textSize"
          :hover="props.hover"
          :detailLevel="detailLevel"
          :id="props.node.id"
          @updateBounds="updateNodeBounds(props.node, $event)"
          :strokeWidth="nodeStrokeWidth(props.node)"
        ></RoundedRectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <DirectedRectEdge
          :id="props.edge.id"
          :x1="props.edge.source.x"
          :x2="props.edge.target.x"
          :y1="props.edge.source.y"
          :y2="props.edge.target.y"
          :stroke="strokeColour(props.edge, props.hover)"
          :strokeWidth="strokeWidth(props.edge, props.hover)"
          :nodeName="props.edge.target.name"
          :graph_node_width="props.edge.styles.targetWidth"
          :graph_node_height="props.edge.styles.targetHeight"
        >></DirectedRectEdge>
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
      </span>
      <BayesToolbar @modechanged="setMode"></BayesToolbar>
      <div v-if="mode == 'variable'">
        <pre></pre>
        <p style="color: blue">
          You can create a new variable here. Please change the name and the domain of the new variable,
          <br />and then double click at a position where you want the new node to be created.
          <br />If you don't change the name or the domain, the new node will be generated with default value.
        </p>
        <pre></pre>
        <label>
          <b>Name</b>
        </label>
        <input
          type="text"
          style="backgroundColor: yellow"
          :value="temp_node_name"
          @focus="$event.target.select()"
          @input="temp_node_name = $event.target.value"
        />
        <label>
          <b>Domain (use comma to separate values)</b>
        </label>
        <input
          type="text"
          style="backgroundColor: yellow"
          :value="temp_node_domain"
          @focus="$event.target.select()"
          @input="temp_node_domain = $event.target.value"
        />
        <pre></pre>
        <p style="color: red">{{warning_message}}</p>
      </div>
      <div v-else-if="mode == 'edge'">
        <pre></pre>
        <p
          v-if="(graph.nodes.indexOf(first) < 0)"
          style="color: blue"
        >Select the first node to begin.</p>
        <p
          style="color: blue"
          v-else-if="(graph.nodes.indexOf(first) > -1) && (selection == first || selection == null || selection.type == 'edge')"
        >
          Source node:
          <span style="color: green">{{first.name}}</span>. Select an end node to create an edge.
        </p>
        <pre></pre>
        <p style="color: red">{{warning_message}}</p>
      </div>
    </div>

    <div>
      <div v-if="mode =='select'">
        <pre></pre>
        <p style="color: blue">
          Please select a node.
          <br />You can change the name and the domain of the selected node.
        </p>
        <div v-if="selection && (graph.nodes.indexOf(selection) > -1)">
          <p style="color: blue">
            You selected node
            <span style="color: green">{{selection.name}}</span>
          </p>
          <pre></pre>
          <label>
            <b>New Name</b>
          </label>
          <input
            type="text"
            style="backgroundColor: yellow"
            :value="selection ? temp_node_name : null"
            @focus="$event.target.select()"
            @input="temp_node_name = $event.target.value"
          />
          <label>
            <b>New Domain (use comma to separate values)</b>
          </label>
          <input
            type="text"
            style="backgroundColor: yellow"
            @focus="$event.target.select()"
            :value="selection ? temp_node_domain : null"
            @input="temp_node_domain = $event.target.value"
          />
          <button @click="IsValidModify(temp_node_name, temp_node_domain)">Submit</button>
          <pre></pre>
          <p style="color: red">{{warning_message}}</p>
        </div>
      </div>
      <div v-else-if="mode == 'delete'">
        <pre></pre>
        <p style="color: blue">Click on a node or an edge to delete it.</p>
      </div>
    </div>
    <div>
      <div v-if="mode == 'set_prob'">
        <pre></pre>
        <p style="color: blue">Click on a node to modifiy the probability table here.</p>
        <div v-if="selection">
          <p style="color: blue">
            You selected node:
            <span style="color: rgb(250, 106, 130)">{{selection.name}}</span>, Its parents are: {
            <span style="color: green">{{selection.parents.join(", ")}}</span>
            }.
          </p>
          <div class="prob_table_grid" v-if="selection.parents.length > 0">
            <div>
              <div class="parent_node" v-for="pn of selection.parents">
                <span style="color: green">{{pn}}</span>
              </div>
              <div
                class="select_node_dm"
                v-for="snn of selection.domain"
              >{{selection.name}} = {{snn}}</div>
            </div>
            <div v-for="(p1, index_p1) of allComb(probList(selection))">
              <div v-if="p1" class="prob_name" v-for="p2 of p1.split(',')">{{p2}}</div>
              <div class="input_box_container" v-for="(snn2, index_snn2) of selection.domain">
                <input 
                  :class="getInputBoxClass(index_p1, temp_node_evidences[(index_p1 * selection.domain.length + index_snn2)])"
                  :ref="generateRef(selection) + index_p1.toString() + '_' + index_snn2.toString()"
                  type="number"
                  @focus="$event.target.select()"
                  :value="temp_node_evidences[index_p1 * selection.domain.length + index_snn2]"
                  @input="$event.target.value ? temp_node_evidences[index_p1 * selection.domain.length + index_snn2] = Number($event.target.value) : temp_node_evidences[index_p1 * selection.domain.length + index_snn2] = 0,
                  (index_snn2 === selection.domain.length - 1) ? null : $refs[findLastInputboxRef(index_p1)][0].value = CalLastBoxValue(getSameLineInputBoxVal(index_p1)),
                  (index_snn2 === selection.domain.length - 1) ? null : temp_node_evidences[index_p1 * selection.domain.length + selection.domain.length - 1] = CalLastBoxValue(getSameLineInputBoxVal(index_p1))"
                  @change="$event.target.value ? temp_node_evidences[index_p1 * selection.domain.length + index_snn2] = Number($event.target.value) : temp_node_evidences[index_p1 * selection.domain.length + index_snn2] = 0"
                />
              </div>
            </div>
          </div>
          <div class="prob_table_grid" v-if="selection.parents.length == 0">
            <div class="select_node_dm" v-for="snn_ of selection.domain">{{selection.name}} = {{snn_}}</div>
            <div>
              <div class="input_box_container" v-for="(snn_2, index) of selection.domain">
              <input
                  :ref="generateRef(selection) + index.toString()"
                  :class="getInputBoxClass(index, temp_node_evidences[index])"
                  type="number"
                  :value="temp_node_evidences[index]"
                  @focus="$event.target.select()"
                  @input="$event.target.value ? temp_node_evidences[index] = Number($event.target.value) : temp_node_evidences[index] = 0,
                  (index === selection.domain.length - 1) ? null : $refs[findLastInputboxRef(index)][0].value = CalLastBoxValue(getSameLineInputBoxVal(index)),
                  (index === selection.domain.length - 1) ? null : temp_node_evidences[selection.domain.length - 1] = CalLastBoxValue(getSameLineInputBoxVal(index))"
                  @change="$event.target.value ? temp_node_evidences[index] = Number($event.target.value) : temp_node_evidences[index] = 0"
                />
              </div>
            </div>
          </div>
          <div>
            <span><span style="color: blue">Click Submit to confirm probability changes, click Cancel to cancel.</span>
            <button @click="IsEvidencesValid()">Submit</button>
            <button @click="cancelProbSet()">Cancel</button></span>
          </div>
          <pre><span style="color: red">{{warning_message}}</span><span style="color: green">{{succeed_message}}</span></pre>
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

import BayesToolbar from "./BayesBuilderToolbar.vue";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import RectangleGraphNode from "../../components/RectangleGraphNode.vue";
import DirectedRectEdge from "../../components/DirectedRectEdge.vue";

import { Graph, IBayesGraphNode, IGraphEdge, IGraphJSON } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode";
import { NODATA } from "dns";
import { IBayesObserveEvent } from "../BayesVisualizerEvents";

type Mode = "select" | "variable" | "edge" | "delete" | "set_prob";

/**
 * Component to visually construct a Belief Network graph.
 *
 * Currently incomplete.
 */
@Component({
  components: {
    RoundedRectangleGraphNode,
    BayesToolbar,
    GraphVisualizerBase,
    DirectedRectEdge
  }
})
export default class BayesGraphBuilder extends Vue {
  /** The graph being built by this builder. */
  graph: Graph<IBayesGraphNode>;
  /** Layout object that controls where nodes are drawn. */
  layout: GraphLayout;

  /** The mode of the editor. */
  mode: Mode = "select";
  /** The currently selected node or edge. Actions are preformed on the selection. */
  selection: IBayesGraphNode | IGraphEdge | null = null;
  /** During edge creation, tracks the source node of the edge to be formed. */
  first: IBayesGraphNode | IGraphEdge | null = null;
  textSize: number;
  detailLevel: number;
  temp_node_name: string = "";
  temp_node_domain: string = "";
  warning_message: string = "";
  succeed_message: string = "";
  temp_node_evidences: number[];

  /** Switches to a new mode. */
  setMode(mode: Mode) {
    this.mode = mode;
    this.selection = null;
    this.first = null;
  }

  testGenRef(a: number, b: number) {
    return generateRef(this.selection) + a.toString() + '_' + b.toString();
  }

  /** Returns whether there is a node to be drawn */
  IsTempNode(name: string, domain: string) {
    var node_to_be_drawn = true;
    if (
      name === null ||
      name === "" ||
      !name.match(/[a-zA-Z$_][a-zA-Z0-9$_]*/)
    ) {
      node_to_be_drawn = false;
      this.warning_message = "Name not valid. Please enter a new name.";
    } else if (this.NameExists(name)) {
      node_to_be_drawn = false;
      this.warning_message = "Name exists! Please enter a different name.";
    } else if (
      domain === null ||
      domain === "" ||
      !domain.match(/([a-zA-Z0-9$_]+)(,(\s)*[a-zA-Z0-9$_]+)*/)
    ) {
      node_to_be_drawn = false;
      this.warning_message = "Domain not valid, Please enter a new domain.";
    } else {
      this.warning_message = "";
    }
    return node_to_be_drawn;
  }

  /** Returns whether the modified node values are valid, if valid, update the values */
  IsValidModify(name: string, domain: string) {
    if (
      name === null ||
      name === "" ||
      !name.match(/[a-zA-Z$_][a-zA-Z0-9$_]*/)
    ) {
      this.warning_message = "Name not valid. Please enter a new name.";
    } else if (this.NameExists(name) && this.selection.name !== name) {
      this.warning_message = "Name exists! Please enter a different name.";
    } else if (
      domain === null ||
      domain === "" ||
      !domain.match(/([a-zA-Z0-9$_]+)(,(\s)*[a-zA-Z0-9$_]+)*/)
    ) {
      this.warning_message = "Domain not valid, Please enter a new domain..";
    } else {
      this.selection!.name = name;
      var temp = this.domainToBoolean(domain.split(/,\s*/));
      if (this.selection!.domain !== temp) {
        // on domain changes, reset evidence of the node.
        this.selection!.domain = temp;
        this.resetEvidencesOnModify(this.selection);
        // reset evidences of the selected node's children.
        this.graph.edges.forEach(e => {
          if (e.source === this.selection) {
            this.resetEvidencesOnModify(e.target);
          }
        });
      }
      this.warning_message = "";
    }
  }

  /** Reset evidences, it should be called:
   * - a parent of this node is removed
   * - an edge towards this node is removed
   * - an edge towards this node is added
   * - the domain of this node changes
   */
  resetEvidencesOnModify(node: IBayesGraphNode) {
    if (node.parents.length > 0) {
      var l = this.allComb(this.probList(node)).length;
      node.evidences = [];
      if (node.domain.length !== 0) {
          for (var i = 0; i < l * node.domain.length; i++) {
              node.evidences.push(1 / node.domain.length);
          }
      }
    } else {
      for (var i = 0; i < node.domain.length; i++) {
        node.evidences.push(1 / node.domain.length);
      }
    }
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

  /** This is to avoid generate an existing node name if some node was deleted */
  genNewDefaultName() {
    var new_name = `Node${this.graph.nodes.length}`;
    var acc = 0;
    while (this.NameExists(new_name)) {
      acc += 1;
      new_name = `Node${this.graph.nodes.length + acc}`;
    }
    return new_name;
  }

  /** Adds a node to the graph at position (x, y). */
  createNode(x: number, y: number) {
    if (
      this.mode === "variable" &&
      this.IsTempNode(this.temp_node_name, this.temp_node_domain)
    ) {
      var emptystrarr: string[] = [];
      var evidencearr: number[] = [];
      var domainval = this.domainToBoolean(this.temp_node_domain.split(/,\s*/));

      for (var i = 0; i < domainval.length; i ++) {
        evidencearr.push(1 / domainval.length);
        }

      this.graph.addNode({
        id: shortid.generate(),
        name: this.temp_node_name,
        x,
        y,
        parents: emptystrarr,
        evidences: evidencearr,
        domain: domainval
      } as IBayesGraphNode);
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "false, true";
      this.warning_message = "";
    }
  }

  /** Adds a new edge to the graph. */
  createEdge() {
    if (
      this.mode === "edge" &&
      this.selection !== null &&
      this.first !== null &&
      this.canEdgeBeAdded(
        this.first as IBayesGraphNode,
        this.selection as IBayesGraphNode
      )
    ) {
      this.graph.addEdge({
        id: shortid.generate(),
        source: this.first.id,
        target: this.selection.id,
        name: "edge1"
      });

      this.selection.parents.push(this.first.name);
      this.resetEvidencesOnModify(this.selection);
      this.warning_message = "";
      this.first = null;
      this.selection = null;
    }
    this.first = null;
    this.selection = null;
  }

  /** Check whether the edge can be created */
  canEdgeBeAdded(source: IBayesGraphNode, target: IBayesGraphNode) {
    var canEdgeBeAdded = true;
    this.warning_message = "";
    if (source === target) {
      return false;
    }
    if (
      this.graph.nodes.indexOf(source) < 0 ||
      this.graph.nodes.indexOf(target) < 0
    ) {
      return false;
    }
    this.graph.edges.forEach(e => {
      if (e.source === target && e.target === source) {
        this.warning_message = "No bi-direction edges between two nodes.";
        return (canEdgeBeAdded = false);
      }
      if (e.source === source && e.target === target) {
        this.warning_message = "Edge already exists.";
        return (canEdgeBeAdded = false);
      }
    });
    return canEdgeBeAdded;
  }

  strokeColour(edge: IGraphEdge, isHovering: boolean) {
    if ((edge === this.selection || isHovering) && this.mode == "delete") {
      return "pink";
    }

    return "black";
  }

  nodeStrokeWidth(node: IBayesGraphNode) {
    if (node.styles && node.styles.strokeWidth) {
      return node.styles.strokeWidth;
    }

    return undefined;
  }

  nodeBackground(node: IBayesGraphNode, isHovering: boolean) {
    if ((this.selection === node || isHovering) && this.mode !== "variable") {
      return "pink";
    }
    return "white";
  }

  /** stroke width of an edge while hovered or not */
  strokeWidth(edge: IGraphEdge, isHovering: boolean) {
    const isHighlight = isHovering && this.mode === "delete";
    const hoverWidth = isHighlight ? 3 : 0;

    if (edge.styles && edge.styles.strokeWidth) {
      return edge.styles.strokeWidth + hoverWidth;
    }

    return 4 + hoverWidth;
  }

  domainText(node: IBayesGraphNode) {
    return `{${node.domain!.join(", ")}}`;
  }

  domainToString(node: IBayesGraphNode) {
    return node.domain!.join(",").split(",");
  }

  domainToBoolean(domain: string[]) {
    var temp = domain;
    if (domain.join(",").match(/(true,\s*false)|(false,\s*true)/)) {
      return [false, true];
    } else {
      return domain;
    }
  }

  /** Updates the user selection. If the selection was previously selected, unselects it. */
  updateSelection(selection: IBayesGraphNode | IGraphEdge) {
    if (this.selection === selection) {
      this.selection = null;
    } else {
      this.selection = selection;
    }
  }

  /** Remove the current selection from the graph. */
  deleteSelection() {
    if (this.selection && this.mode === "delete") {
      if (this.graph.edges.indexOf(this.selection as IGraphEdge) > -1) {
        // remove edge.source from edge.target.parents
        this.selection.target.parents.splice(
          this.selection.target.parents.indexOf(this.selection.source.name),
          1
        );
        // reset edge.target's evidences 
        this.resetEvidencesOnModify(this.selection.target);
        this.graph.removeEdge(this.selection as IGraphEdge);
      }
      if (this.graph.nodes.indexOf(this.selection as IBayesGraphNode) > -1) {
        this.cleanParentsEvidenceOnNodeDel(this.selection as IBayesGraphNode);
        this.graph.removeNode(this.selection as IBayesGraphNode);
      }
      this.selection = null;
    }
  }

  /** Remove the deleted node from all children's parents lists, and reset children's evidences*/
  cleanParentsEvidenceOnNodeDel(node: IBayesGraphNode) {
    this.graph.edges.forEach(edge => {
      if (edge.source === node) {
        edge.target.parents.splice(edge.target.parents.indexOf(node.name), 1);
        this.resetEvidencesOnModify(edge.target);
      }
    });
  }

  /**
   * Find all combinations of parents. 
   * e.g. parents = {name: "Node1", domain: ["true", "false"]}, {name: "Node2", domain: ["a", "b"]}
   * => returns [["Node1 = true", "Node1 = false"], ["Node2 = a", "Node2 = b"]]
   */
  probList(node: IBayesGraphNode) {
    if (node.parents.length === 0 || node.parents === null) {
      return [];
    }
    var probNameList: string[][] = [];
    node.parents.forEach(p => {
      var domains = this.domainToString(this.graph.nodes.find(n => n.name === p));
      var probNameList_curr_p: string[] = [];
      domains.forEach(d => {
        probNameList_curr_p.push(d);
      });
      probNameList.push(probNameList_curr_p);
    });
    return probNameList;
  }

  /**
   * Find all possible combinations of node parents domains.
   * e.g.
   * arr = [["Node1 = true", "Node1 = false"]],
   *      => returns ["Node1 = true", "Node1 = false"].
   * arr = [["Node1 = true", "Node2 = false"], ["Node2 = a", Node2 = "b"]],
   *      => returns ["Node1 = true,Node2 = a", "Node1 = true,Node2 = b",
   *                  "Node1 = false,Node2 =a", "Node1 = false,Node2 = b"].
   */
  allComb(arr: string[][]) {
    if (arr.length === 0) {
      return [];
    }
    if (arr.length === 1) {
      return arr[0];
    }
    const output = arr.reduce((acc, cu) => {
      let ret: string[] = [];
      acc.map(obj => {
        cu.map(obj_1 => {
          ret.push(obj + "," + obj_1);
        });
      });
      return ret;
    });
    return output;
  }


  /** For each line of prob inputboxes generate its reference
   * the format is: Parent1Name-Parent2Name_SelectedNodeName
   * and for each prob inputbox in this line, the reference won't be generate here, 
   * but the format is:
   * Parent1Name-Parent2Name_SelectedNodeName[index of row]_[index of domain of selected]
   */
  generateRef(node: IBayesGraphNode) {
    if (node) {
      var temp = node.parents.slice(0);
      var str = temp.join('-');
      var result = str + '_' + node.name;
      return result; 
    }  else {
      return '';
    }
  }

  /** Check whether modified temp_node_evidences is valid, and
   * Update selection.evidences if modification is valid
   */
  IsEvidencesValid() {
    this.warning_message = "";
    this.succeed_message = "";
    var isvalid: boolean = true;
  
    if (this.temp_node_evidences.find( e => (e > 1 || e < 0))) {
      this.warning_message = "The highlited values are invalid!";
      isvalid = false;
    }
      
    if (this.CalAllSumOfSameLineInputBox(this.temp_node_evidences).find(x => x !== 1)) {
      if (this.warning_message !== "") {
          this.warning_message = "The highlighted values are invalid! The highlited line doesn't sum up to 1!";
        } else {
          this.warning_message = "The highlited line doesn't sum up to 1!";
        }
        isvalid = false;
    }

    if (isvalid) {
      this.selection.evidences = this.temp_node_evidences.slice(0);
      this.succeed_message = "Probabilities updated.";
    }

    this.$forceUpdate();
  
  }

    /** Returns a list of sums of all rows of prob inputbox */
    CalAllSumOfSameLineInputBox(evidences: number[]) {
    // first slice the node's evidences
      var linesums = [];
      var sliced = [];
      var chunksize = this.selection.domain.length;
      for (var i = 0; i < evidences.length; i += chunksize){
        sliced.push(evidences.slice(i, i+chunksize));
    }
      sliced.forEach(s => {
        linesums.push(s.reduce((a, b) => a + b, 0))
    });

      return linesums;
  }

  CalSumOfSameLineInputBox(index: number) {
    if (this.selection.parents.length > 0) {
      return this.CalAllSumOfSameLineInputBox(this.temp_node_evidences)[index];
    } else {
      return this.CalAllSumOfSameLineInputBox(this.temp_node_evidences)[0];
    }
  }

  cancelProbSet() {
    this.temp_node_evidences = this.selection.evidences.slice(0);
    this.warning_message = "";
    this.succeed_message = "";
    this.$forceUpdate();
  }

  getInputBoxClass(index: number, val: number) {
    var inputboxclass = "input_box";
    if (val > 1 || val < 0 || this.CalSumOfSameLineInputBox(index) !== 1) {
      inputboxclass = "input_box_invalid";
    }
    return inputboxclass;
  }

 /** Get values for all prob inputboxes in the same row except for the last 
   * for some reason this.refs doesn't work here
   * values are from temp_node_evidences.
  */
  getSameLineInputBoxVal(index: number) {
    var sameRowProbVals: number[] = [];
    if (this.selection) {
      var number_of_domain = this.selection.domain.length;
      var sameRowProbIndexes: number[] = [];
      for (var i = 0; i < number_of_domain - 1; i++) {
        if (this.selection.parents.length > 0) {
          sameRowProbIndexes.push(number_of_domain * index + i);
        } else {
          sameRowProbIndexes.push(i);
        }
      }
      sameRowProbIndexes.forEach(index_ =>{
        sameRowProbVals.push(this.temp_node_evidences[index_]);
      });
      }

      return sameRowProbVals;
  }


  /** Calculate the value presented in the last prob inputbox when other boxes are changed.
  */
  CalLastBoxValue(vals: number[]) {
    var result = 1 - vals.reduce((a, b) => a + b, 0);
    return result;
  }

  findLastInputboxRef(prob_name_index: number) {
    var pni = prob_name_index.toString();
    var l = this.selection.domain.length;
    var ref_prefix = this.generateRef(this.selection);
    if (this.selection.parents.length > 0) {
      return ref_prefix + pni + '_' + (l - 1).toString(); 
    } else {
      return ref_prefix + (l - 1).toString(); 
    }
  }

  // Whenever a node reports it has resized, update it's style so that it redraws.
  updateNodeBounds(
    node: IBayesGraphNode,
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
    if (this.mode === "edge") {
      if (this.first == null) {
        this.first = this.selection as IBayesGraphNode;
      } else {
        this.createEdge();
      }
    } else if (this.mode === "select" && this.selection) {
      this.temp_node_name = this.selection.name!;
      this.temp_node_domain = `${this.selection.domain!.join(", ")}`;
      this.warning_message = "";
    } else if (this.mode === "delete" && this.selection) {
      this.deleteSelection();
    } else if (this.mode == "variable") {
      this.selection = null;
    } else if (this.mode === "set_prob" && this.selection) {
      this.temp_node_name = "";
      this.temp_node_domain = "";
      this.warning_message = "";
      this.temp_node_evidences = this.selection.evidences.slice(0);
    } else {
      this.selection = null;
      this.temp_node_name = "";
      this.temp_node_domain = "";
      this.warning_message = "";
    }
  }

  @Watch("mode")
  onModeChanged() {
    if (this.mode === "variable") {
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "false, true";
      this.warning_message = "";
    } else if (this.mode === "select" && this.selection) {
      this.temp_node_name = this.selection.name!;
      this.temp_node_domain = `${this.selection.domain!.join(", ")}`;
      this.warning_message = "";
    } else {
      this.temp_node_name = "";
      this.temp_node_domain = "";
      this.warning_message = "";
    }
  }
}
</script>

<style scoped>
text.domain {
  font-size: 12px;
}

.prob_table_grid {
  display: inline-block;
  background-color: white;
  white-space: nowrap;
  max-height: 300px;
  max-width: 700px;
  padding: 10px;
  border: 2px solid #4CAF50;
  overflow: scroll;
}

.parent_node {
  text-align: center;
  font-weight: bold;
  display: inline-block;
  width: 125px;
  height: 20px;
  overflow-x: hidden;
}

div.parent_node:hover {
  overflow-x: scroll;
}

div.select_node_dm {
  text-align: center;
  color: rgb(250, 106, 130);
  font-weight: bold;
  display: inline-block;
  width: 125px;
  height: 20px;
  overflow: hidden;
}

div.select_node_dm:hover {
  overflow-x: scroll;
}

div.prob_name {
  text-align: center;
  display: inline-block;
  width: 125px;
  height: 20px;
  overflow-x: hidden;
}

div.prob_name:hover {
  overflow-x: scroll;
}

div.input_box_container {
  text-align: center;
  display: inline-block;
  width: 125px;
  height: 20px;
}

.input_box {
  width: 100px;
  background-color: yellow;
}

.input_box_invalid {
  width: 100px;
  background-color: pink;
}

input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
</style>
