<template>
  <div class="csp_builder">
    <GraphVisualizerBase
      :graph="graph"
      :transitions="true"
      :layout="layout"
      @dblclick="createNode"
      @click:edge="updateSelection"
      @click:node="updateSelection"
      @click.native="to_delete ? $refs.delete_yes.focus() : null"
    >
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode
          v-if="props.node.type === 'csp:variable'"
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
        <RectangleGraphNode
          v-if="props.node.type === 'csp:constraint'"
          :text="props.node.name"
          :fill="nodeBackground(props.node, props.hover)"
          :textSize="textSize"
          :hover="props.hover"
          :detailLevel="detailLevel"
          :id="props.node.id"
        ></RectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <UndirectedEdge
          :x1="props.edge.source.x"
          :x2="props.edge.target.x"
          :y1="props.edge.source.y"
          :y2="props.edge.target.y"
          :stroke="strokeColour(props.edge, props.hover)"
          :strokeWidth="strokeWidth(props.edge, props.hover)"
        ></UndirectedEdge>
      </template>
      <template slot="visualization" slot-scope="props">
        <a class="inline-btn-group" @click="props.zoomModeMinus">&#8249;</a>
        <label class="inline-btn-group">{{'Zoom Mode: ' + props.zoomMode}}</label>
        <a class="inline-btn-group" @click="props.zoomModePlus">&#8250;</a>

        <a @click="props.toggleWheelZoom">{{'Wheel Zoom: ' + props.wheelZoom}}</a>

        <a class="inline-btn-group" @click="props.zoomOut">-</a>
        <label class="inline-btn-group">Zoom</label>
        <a class="inline-btn-group" @click="props.zoomIn">+</a>
        
        <a class="inline-btn-group" @click="detailLevel = detailLevel > 0 ? detailLevel - 1 : detailLevel">-</a>
        <label class="inline-btn-group">{{'Detail Level: ' + detailLevel}}</label>
        <a class="inline-btn-group" @click="detailLevel = detailLevel < 2 ? detailLevel + 1 : detailLevel">+</a>

        <a class="inline-btn-group" @click="textSize = textSize > 1 ? textSize - 1 : textSize">-</a>
        <label class="inline-btn-group">{{'Text Size: ' + textSize}}</label>
        <a class="inline-btn-group" @click="textSize = textSize + 1">+</a>

        <a class="inline-btn-group" @click="lineWidth = lineWidth > 1 ? lineWidth - 1 : lineWidth">-</a>
        <label class="inline-btn-group">{{'Line Width: ' + lineWidth}}</label>
        <a class="inline-btn-group" @click="lineWidth = lineWidth + 1">+</a>
      </template>
    </GraphVisualizerBase>

    <div>
      <span>
        <strong>Mode:</strong>
      </span>
      <CSPToolbar @modechanged="setMode"></CSPToolbar>
      <div v-if="mode == 'create'">
        <p>
          <strong>To create variable or constraint:</strong> Select a node type, then double click on the graph to create.
          <br />
          <span>
            <span class="radioInputGroup">
              <input type="radio" id="cm_v" value="variable" v-model="create_sub_mode" />
              <label for="cm_v">Variable</label>
            </span>
            <span class="radioInputGroup">
              <input type="radio" id="cm_c" value="constraint" v-model="create_sub_mode" />
              <label for="cm_c">Constraint</label>
            </span>
          </span>
          <br />
          <span v-if="create_sub_mode == 'variable'">
            <label>
              <strong>Name:</strong>
            </label>
            <input
              type="text"
              :value="temp_v_name"
              @focus="$event.target.select()"
              @input="temp_v_name = $event.target.value, cleanMessages()"
            />
            <label>
              <strong>Domain:</strong>
            </label>
            <span>
              <label for="is_domain_bool">Boolean</label>
              <input
                type="checkbox"
                id="is_domain_bool"
                v-model="isDomainBool"
                @input="cleanMessages()"
              />
            </span>
            <span>
              <input
                v-if="!isDomainBool"
                type="text"
                :value="temp_v_domain"
                @focus="$event.target.select()"
                @input="temp_v_domain = $event.target.value, cleanMessages()"
              />
              <input
                v-else
                class="text_input_box_noUserInput"
                type="text"
                :value="'true, false'"
                readonly="readonly"
              /> (use comma to separate values)
            </span>
          </span>
          <span v-else-if="create_sub_mode == 'constraint'">
            <label>
              <strong>Name:</strong>
            </label>
            <input
              type="text"
              style="width: 150px;"
              :value="temp_c_name"
              @focus="$event.target.select()"
              @input="temp_c_name = $event.target.value, cleanMessages()"
            />
            <br />
            <span>Can only set the properties of the constraint after connected to variable(s).</span>
          </span>
          <br />
          <span>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </span>
          <br />
          <strong>To create edge:</strong> Click on the start node, then click on the end node.
          <br />
          <span
            v-if="first == null || (first.type != 'csp:variable' && first.type != 'csp:constraint')"
          >Select the first node to begin.</span>
          <span v-else>
            Source node:
            <span class="nodeText">{{getNodeType(first)}}</span>. Select an end
            <span class="nodeText">{{getEndNodeType(first)}}</span> to create an edge.
          </span>
          <br />
          <span>
            <span class="warningText">{{edge_warning_message}}</span>
            <span class="successText">{{edge_succeed_message}}</span>
          </span>
        </p>
      </div>
    </div>

    <div v-if="mode == 'select'">
      <p class="builder_output">
        Set the name and the domain of a variable node or the constraint table of a constraint node by cliking on it.
        <br />
      </p>
      <div id="select_variable" v-if="selection && selection.type == 'csp:variable'">
        <p class="builder_output">
          You selected variable node
          <span class="nodeText">{{selection.name}}</span>.
          <br />
          <span>
            <label>
              <strong>Name:</strong>
            </label>
            <input
              type="text"
              :value="temp_v_name"
              @focus="$event.target.select()"
              @input="temp_v_name = $event.target.value, cleanMessages()"
              v-on:keyup.enter="isValidModify(temp_v_name, temp_v_domain)"
            />
            <label>
              <strong>Domain:</strong>
            </label>
            <span>
              <label for="is_domain_bool">Boolean</label>
              <input
                type="checkbox"
                id="is_domain_bool"
                v-model="isDomainBool"
                @input="cleanMessages()"
              />
            </span>
            <span>
              <input
                v-if="!isDomainBool"
                type="text"
                @focus="$event.target.select()"
                :value="temp_v_domain"
                @input="temp_v_domain = $event.target.value, cleanMessages()"
                v-on:keyup.enter="isValidModify(temp_v_name, temp_v_domain)"
              />
              <input
                v-else
                class="text_input_box_noUserInput"
                readonly="readonly"
                type="text"
                @focus="$event.target.select()"
                :value="'true, false'"
                v-on:keyup.enter="isValidModify(temp_v_name, temp_v_domain)"
              /> (use comma to separate values)
            </span>
            <button
              ref="btn_select_submit"
              @click="isValidModify(temp_v_name, temp_v_domain)"
            >Submit</button>
          </span>
          <br />
        </p>
        <p>
          <span class="warningText">{{warning_message}}</span>
          <span class="successText">{{succeed_message}}</span>
        </p>
      </div>
      <div id="select_constraint" v-if="selection && selection.type == 'csp:constraint'">
        <label>
          <strong>Name:</strong>
        </label>
        <input
          type="text"
          style="width: 150px;"
          :value="temp_c_name"
          @focus="$event.target.select()"
          @input="temp_c_name = $event.target.value, cleanMessages()"
          v-on:keyup.enter="UpdateConstraintNode(selection, temp_c_name)"
        />
        <div v-if="findVariablesConnected(selection).length == 0">
          <span>Can only set the properties of the constraint after connected to variable(s).</span>
        </div>
        <div v-else>
          <span id="constraint_type_modify">
            <label>
              <strong>Constraint Type:</strong>
            </label>
            <select v-model="select_constraint_type">
              <option v-for="option of getACT(selection)" :key="option">{{option}}</option>
            </select>
            <span v-if="needInputBox(select_constraint_type)">
              <input
                v-if="select_constraint_type === 'eq_(val)' || select_constraint_type === 'ne_(val)'"
                type="text"
                placeholder="string or number"
                :value="value_in_parentheses"
                @focus="$event.target.select(), inputbox_focused = true"
                @blur="inputbox_focused = false"
                @input="value_in_parentheses_temp = $event.target.value"
                v-on:keyup.enter="InitialTempTableAssign(selection, temp_c_name)"
              />
              <input
                v-if="select_constraint_type !== 'eq_(val)' && select_constraint_type !== 'ne_(val)'"
                type="text"
                placeholder="number"
                ref="numberonlyinput"
                :value="value_in_parentheses"
                @focus="$event.target.select(), inputbox_focused = true"
                @blur="inputbox_focused = false"
                @input="trimNonNumeric($event.target.value),value_in_parentheses_temp = $event.target.value"
                v-on:keyup.enter="InitialTempTableAssign(selection)"
              />
              <button
                ref="show_new_table_btn"
                @click="InitialTempTableAssign(selection), cleanMessages()"
                @keydown="$event.keyCode == 13 ? $event.preventDefault() : false"
                v-on:keyup.enter="UpdateConstraintNode(selection, temp_c_name)"
              >Use New Value</button>
            </span>
          </span>
          <br />
          <p class="constraint_name_readable" ref="constraint_name_readable">
            <span class="nodeText">
              <strong>{{constraintToReadableText(selection)}}</strong>
              <button
                type="button"
                v-if="findVariablesConnected(selection).length === 2"
                id="reverse_order"
                @click="reverseOrder(selection)"
                @keydown="$event.keyCode == 13 ? $event.preventDefault() : false"
                v-on:keyup.enter="UpdateConstraintNode(selection, temp_c_name)"
              >Reverse Order</button>
            </span>
          </p>
          <div v-if="select_constraint_type === 'Custom' ">
            <div class="table_container" ref="table_container">
              <div class="table_header">
                <div class="header_cell" v-for="v of findVariablesConnected(selection)" :key="v">
                  <span class="nodeText">{{v.name}}</span>
                </div>
                <div class="header_cell">True</div>
              </div>
              <div class="table_body">
                <div
                  class="table_row"
                  v-for="(c, index_c) of AllComb(getDomainList(findVariablesConnected(selection)))"
                  :key="c"
                >
                  <div class="table_cell" v-for="d of c.split(',')" :key="d">{{d}}</div>
                  <div class="table_cell">
                    <input
                      type="checkbox"
                      v-model="temp_table[index_c]"
                      @input="select_constraint_type = 'Custom', initially_in_ACT = true, cleanMessages()"
                      @keydown="$event.keyCode == 13 ? $event.preventDefault() : false"
                      v-on:keyup.enter="UpdateConstraintNode(selection, temp_c_name)"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="table_container" ref="table_container">
              <div class="table_header">
                <div class="header_cell" v-for="v of findVariablesConnected(selection)" :key="v">
                  <span class="nodeText">{{v.name}}</span>
                </div>
                <div class="header_cell">True</div>
              </div>
              <div class="table_body">
                <div
                  class="table_row"
                  v-for="(c, index_c) of AllComb(getDomainList(findVariablesConnected(selection)))"
                  :key="c"
                >
                  <div class="table_cell" v-for="d of c.split(',')" :key="d">{{d}}</div>
                  <div class="table_cell">
                    <input
                      type="checkbox"
                      v-model="temp_table[index_c]"
                      @input="select_constraint_type = 'Custom', initially_in_ACT = true, cleanMessages()"
                      @keydown="$event.keyCode == 13 ? $event.preventDefault() : false"
                      onclick="this.checked=!this.checked;"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>  
          <div>
            <p>
              <button ref="btn_table_change" @click="UpdateConstraintNode(selection, temp_c_name)">Submit</button>
              <button
                @click="resetTable()"
                @keydown="$event.keyCode == 13 ? $event.preventDefault() : false"
              >Cancel</button>
            </p>
          </div>
          <p>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </p>
        </div>
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
      <span class="successText">{{succeed_message}}</span>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import * as shortid from "shortid";

import CSPToolbar from "./CSPBuilderToolbar.vue";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import RectangleGraphNode from "../../components/RectangleGraphNode.vue";
import UndirectedEdge from "../../components/UndirectedEdge.vue";

import { Graph, ICSPGraphNode, IGraphEdge, IGraphNode } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import * as CSPUtils from "../CSPUtils";
import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode.vue";
import { prependListener } from "cluster";

type Mode = "create" | "select" | "delete";
type CreateSubMode = "variable" | "constraint";

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
  mode: Mode = "create";
  /** The currently selected node or edge. Actions are preformed on the selection. */
  selection: ICSPGraphNode | IGraphEdge | null = null;
  /** During edge creation, tracks the source node of the edge to be formed. */
  first: ICSPGraphNode | null = null;
  textSize: number;
  lineWidth: number;
  detailLevel: number;
  /** The sub-mode of the create mode. */
  create_sub_mode: CreateSubMode = "variable";
  isDomainBool: boolean = false;
  temp_v_name: string = "";
  temp_v_domain: string = "";
  temp_c_name: string = "";
  temp_c_name_input_part: string = "";
  warning_message: string = "";
  succeed_message: string = "";
  edge_succeed_message: string = "";
  edge_warning_message: string = "";
  select_constraint_type: string = "";
  /** To record whether the user has reversed the order without submission */
  reversed: boolean = false;
  /** A backup of graph before the order is reversed */
  reversed_constraint_without_submission: ICSPGraphNode | null = null;
  /** Remember the value inside parentheses parsed from constraint node name, such as:
   * value of val in Equals(val), value of num in GreaterThan(val)
   */
  value_in_parentheses: string | null = null;
  value_in_parentheses_temp: string | null = null;
  /** A temporal value to remember the table assignment of current selected constraint node */
  temp_table: boolean[] = [];
  /** If the imported csp problem has a predefined constraint type
   * that is not in default ACT, it is set to be false,
   * once the user change any assignment in table,
   * it will become true, and the predefined constraint then treated as Custom
   */
  initially_in_ACT: boolean = false;

  /** Check whether when in select mode and a constraint is selected,
   * whether the user is focused on an inputbox, if so,
   * pressing enter key will adapt the new value to the temp table,
   * else pressing enter key will comfirm the update of the table.
   */
  inputbox_focused: boolean = false;

  /** Detect whether the user clicked an node/edge in delet mode */
  to_delete: boolean = false;

  constraints_need_input = [
    "ne_(val)",
    "eq_(val)",
    "gt_(val)",
    "lt_(val)",
    "le_(val)",
    "ge_(val)"
  ];

  /** Switches to a new mode. */
  created() {
    this.temp_v_name = this.genNewDefaultNameV();
    this.temp_v_domain = "1, 2, 3";
    this.AddConstraintNameToAllNodes();
  }

  AddConstraintNameToAllNodes() {
    this.graph.nodes.forEach(n => {
      if (n.type === "csp:constraint") {
        this.selectboxDefault(n);
      }
    });
    this.value_in_parentheses = null;
    this.value_in_parentheses_temp = null;
    this.select_constraint_type = "";
  }

  cleanMessages() {
    this.warning_message = "";
    this.succeed_message = "";
    this.edge_succeed_message = "";
    this.edge_warning_message = "";
  }

  setMode(mode: Mode) {
    this.mode = mode;
    this.selection = null;
    this.first = null;
  }

  getNodeType(node: ICSPGraphNode) {
    if (node.type === "csp:variable") {
      return "Variable - " + node.name;
    } else if (node.type === "csp:constraint") {
      return "Constraint - " + node.name;
    }
  }

  getEndNodeType(node: ICSPGraphNode) {
    if (node.type === "csp:variable") {
      return "constraint node";
    } else if (node.type === "csp:constraint") {
      return "variable node";
    }
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

  /** This is to avoid generate an existing variable name if some node was deleted */
  genNewDefaultNameV() {
    var vnodes = this.graph.nodes.filter(x => x.type === "csp:variable");
    var new_name = `Var${vnodes.length + 1}`;
    var acc = 0;
    while (this.NameExists(new_name)) {
      acc += 1;
      new_name = `Var${vnodes.length + acc}`;
    }
    return new_name;
  }

  /** This is to avoid generate an existing constraint name if some node was deleted */
  genNewDefaultNameC() {
    var cnodes = this.graph.nodes.filter(x => x.name === "Empty Constraint");
    var new_name = `Empty Constraint${cnodes.length + 1}`;
    var acc = 0;
    while (this.NameExists(new_name)) {
      acc += 1;
      new_name = `Empty Constraint${cnodes.length + acc}`;
    }
    return new_name;
  }

  /** Adds a node to the graph at position (x, y). */
  createNode(x: number, y: number) {
    if (
      this.mode === "create" &&
      this.create_sub_mode === "variable" &&
      this.IsTempVariable(this.temp_v_name, this.temp_v_domain)
    ) {
      var domainval: string[] | boolean[] | number[] = [];
      if (this.isDomainBool) {
        domainval = [true, false];
      } else {
        domainval = this.handleDomain(this.temp_v_domain);

        if (this.checkDomainType(domainval) === "number") {
          var domainN: number[] = [];
          domainval.forEach(d => {
            domainN.push(Number(d));
          });
          domainval = domainN;
        }

      }
      this.graph.addNode({
        id: shortid.generate(),
        name: this.temp_v_name,
        x,
        y,
        type: "csp:variable",
        domain: domainval
      });

      this.temp_v_name = this.genNewDefaultNameV();
      this.temp_v_domain = "1, 2, 3";
      this.succeed_message = "Variable node created.";
      this.warning_message = "";
    } else if (
      this.mode === "create" &&
      this.create_sub_mode === "constraint"
    ) {
      this.graph.addNode({
        id: shortid.generate(),
        name: this.temp_c_name,
        x,
        y,
        condition_name: "Custom",
        combinations_for_true: [],
        type: "csp:constraint"
      });

      this.temp_c_name = this.genNewDefaultNameC();
      this.succeed_message = "Constraint node created.";
      this.warning_message = "";
    }

    this.first = null;
    this.selection = null;
  }

  /** Returns whether name and domain for a new node to be created are valid */
  IsTempVariable(name_raw: string, domain: string) {
    var name = name_raw.trimLeft().trimRight();
    var node_to_be_drawn = true;
    if (name === null || name.match(/^\s*$/)) {
      this.warning_message = "Name not valid. Please enter a new name.";
      this.succeed_message = "";
      node_to_be_drawn = false;
    } else if (this.NameExists(name)) {
      node_to_be_drawn = false;
      this.warning_message = "Name already exists.";
      this.succeed_message = "";
    } else if (
      domain === null ||
      domain === "" ||
      !domain.match(/^.+(,(\s)*.*)*$/)
    ) {
      node_to_be_drawn = false;
      this.warning_message = "Domain not valid, Please enter a new domain.";
      this.succeed_message = "";
    } else if (this.checkDomainDuplicates(domain)) {
      node_to_be_drawn = false;
      this.warning_message = "Domain contains duplicated values.";
      this.succeed_message = "";
    } else {
      this.warning_message = "";
      this.succeed_message = "Variable node created.";
    }
    return node_to_be_drawn;
  }

  /** Returns whether the modified node name and domain are valid,
   * if valid, update the values */
  isValidModify(name: string, domain: string) {

    if (name === null || name.match(/^\s*$/)) {
      this.warning_message = "Name not valid.";
      this.succeed_message = "";
      return;
    }

    if (this.NameExists(name) && name !== this.selection.name) {
      this.warning_message = "Name already exists.";
      this.succeed_message = "";
      return;
    }

    var domain_changed = false;

    if (this.isDomainBool) {
      //update new name
      var oldname = this.selection!.name.slice(0);
      this.selection!.name = name.trimLeft().trimRight();
      

      //update new domain
      
      if (typeof this.selection!.domain[0] !== "boolean") {
        domain_changed = true;
        var domainB: boolean[] = [true, false];      
        this.selection!.domain = domainB;
      }

    }else{
      if (domain === null || domain === "" || !domain.match(/^.+(,(\s)*.*)*$/)) {
        this.warning_message = "Domain not valid.";
        this.succeed_message = "";
        return;
      }

      if (this.checkDomainDuplicates(domain)) {
        this.warning_message = "Domain contains duplicated values.";
        this.succeed_message = "";
        return;
      }
      //update new name
      var oldname = this.selection!.name.slice(0);
      this.selection!.name = name.trimLeft().trimRight();
      

      //update new domain
      var newdomain = this.handleDomain(domain);
      if ((typeof this.selection!.domain[0] !== typeof newdomain[0]) || (this.selection!.domain.join(",") !== newdomain.join(","))) {
        domain_changed = true;
        if (this.checkDomainType(newdomain) === "number") {
          var domainN: number[] = [];
          newdomain.forEach(d => {
            domainN.push(Number(d));
          });
          this.selection!.domain = domainN;
        } else {
          this.selection!.domain = newdomain;
        }
      }

      

    }

    // if domain changed reset constraint type to default
    // if only name changed, not change constraint type.
    if (domain_changed) {
      this.graph.edges.forEach(e => {
        var constraint_node: ICSPGraphNode;
        if (e.source === this.selection && e.target.type === "csp:constraint") {
          // this.nameChangeOnDeletionOrAddition(e.target as ICSPGraphNode);
          constraint_node = e.target as ICSPGraphNode;
        } else if (
          e.target === this.selection &&
          e.source.type === "csp:constraint"
        ) {
          // this.nameChangeOnDeletionOrAddition(e.source as ICSPGraphNode);
          constraint_node = e.source as ICSPGraphNode;
        }
        constraint_node.condition_name = "Custom";
        constraint_node.combinations_for_true = [];
        var connected_v = this.findVariablesConnected(constraint_node)
        constraint_node.condition_name = this.trueCombinations(
          connected_v,
          constraint_node.combinations_for_true
        );
      });
    } else {
      this.graph.edges.forEach(e => {
        if (e.source === this.selection && e.target.type === "csp:constraint") {
          var cn_name = e.target.name.slice(0);
          var newname = this.selection.name.slice(0);
          var new_cn_name = cn_name.replace(
            "'" + oldname + "'",
            "'" + newname + "'"
          );
          e.target.name = new_cn_name;
          this.genNewCBNTsForTrue(e.target as ICSPGraphNode, newname, oldname);
        } else if (
          e.target === this.selection &&
          e.source.type === "csp:constraint"
        ) {
          var cn_name = e.source.name.slice(0);
          var newname = this.selection.name.slice(0);
          var new_cn_name = cn_name.replace(
            "'" + oldname + "'",
            "'" + newname + "'"
          );
          e.source.name = new_cn_name;
          this.genNewCBNTsForTrue(e.source as ICSPGraphNode, newname, oldname);
        }
      });
    }

    this.warning_message = "";
    this.succeed_message = "Node updated.";
  }

  genNewCBNTsForTrue(node: ICSPGraphNode, newname: string, oldname: string) {
    // Update constraint node's combinations_for_true field.
    var new_cbnts_for_true: Object[] = [];
    var connected_v = this.findVariablesConnected(node!);
    var connected_v_names = connected_v.map(v => v.name);
    var connected_v_names_old = connected_v_names.slice(0);
    connected_v_names_old.forEach((n, index) => {
      if (n === newname) {
        connected_v_names_old[index] = oldname;
      }
    });

    connected_v_names_old.forEach((n_old, index) => {
      var element: Object = {};
      element[connected_v_names[index]] = node.combinations_for_true[n_old];
      new_cbnts_for_true.push(element);
    });

    node.combinations_for_true = new_cbnts_for_true;
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

  /** This will handle domain:
   * - If domain has white-spaces at the beginning or the end, trim the domain
   * - Remove any empty string
   */
  handleDomain(domain_raw: string) {
    var domain_temp = domain_raw
      .trimLeft()
      .trimRight()
      .split(/,\s*/)
      .filter(x => x !== "");
    var domain: string[] = [];
    domain_temp.forEach(d => {
      var temp = d.trimLeft().trimRight();
      domain.push(temp);
    });

    return domain;
  }

  checkDomainDuplicates(domain_raw: string) {
    var domain_temp = domain_raw
      .trimLeft()
      .trimRight()
      .split(/,\s*/)
      .filter(x => x !== "");
    var domain: string[] = [];
    domain_temp.forEach(d => {
      var temp = d.trimLeft().trimRight();
      domain.push(temp);
    });

    if (domain.find(x => domain.indexOf(x, domain.indexOf(x) + 1) !== -1)) {
      return true;
    } else {
      return false;
    }
  }

  /** Adds a new edge to the graph. */
  createEdge() {
    if (
      this.mode === "create" &&
      this.selection != null &&
      this.first != null
    ) {
      if (
        this.first.type === "csp:variable" &&
        this.selection.type === "csp:variable"
      ) {
        this.edge_warning_message =
          "Can't create an edge between two variables";
        this.first = null;
        this.selection = null;
        return;
      }

      if (
        this.first.type === "csp:constraint" &&
        this.selection.type === "csp:constraint"
      ) {
        this.edge_warning_message =
          "Can't create an edge between two constraints.";
        this.first = null;
        this.selection = null;
        return;
      }

      if (this.edgeExist(this.first as ICSPGraphNode, this.selection as ICSPGraphNode)) {
        this.edge_warning_message = "Edge exists.";
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

      var constraint_node: ICSPGraphNode = this.first;
      if (this.selection.type === "csp:constraint") {
        constraint_node = this.selection as ICSPGraphNode;
      }

      // this.nameChangeOnDeletionOrAddition(constraint_node);
      constraint_node.condition_name = "Custom";
      constraint_node.combinations_for_true = [];
      var connected_v = this.findVariablesConnected(constraint_node)
      constraint_node.condition_name = this.trueCombinations(
        connected_v,
        constraint_node.combinations_for_true
      );

      this.edge_succeed_message = "Edge created.";

      this.first = null;
      this.selection = null;
    }
  }

  edgeExist(source: ICSPGraphNode, target: ICSPGraphNode) {
    var exist = false;
    this.graph.edges.forEach(e => {
      if (
        (e.target === target && e.source === source) ||
        (e.source === target && e.target === source)
      ) {
        return (exist = true);
      }
    });
    return exist;
  }

  nodeStrokeWidth(node: ICSPGraphNode) {
    if (node.styles && node.styles.strokeWidth) {
      return node.styles.strokeWidth;
    }

    return undefined;
  }

  /** stroke width of an edge while hovered or not */
  strokeWidth(edge: IGraphEdge, isHovering: boolean) {
    const isHighlight = isHovering && this.mode === "delete";
    const hoverWidth = isHighlight ? 3 : 0;

    if (edge.styles && edge.styles.strokeWidth) {
      return edge.styles.strokeWidth + hoverWidth;
    }

    return this.lineWidth + hoverWidth;
  }

  nodeBackground(node: ICSPGraphNode, isHovering: boolean) {
    if (this.selection === node || isHovering) {
      return "pink";
    }
    return "white";
  }

  // Whenever a node reports it has resized, update it's style so that it redraws.
  updateNodeBounds(
    node: ICSPGraphNode,
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

  strokeColour(edge: IGraphEdge, isHovering: boolean) {
    if ((edge === this.selection || isHovering) && this.mode == "delete") {
      return "pink";
    }

    return "black";
  }

  domainText(node: ICSPGraphNode) {
    return CSPUtils.domainText(node);
  }

  /** Updates the user selection. If the selection was previously selected, unselects it. */
  updateSelection(selection: ICSPGraphNode | IGraphEdge) {
    if (this.selection === selection) {
      this.selection = null;
      this.first = null;
    } else {
      this.selection = selection;
    }
  }

  /** Remove the current selection from the graph. */
  deleteSelection() {
    if (this.selection) {
      if (this.selection.type === "edge") {
        var constraint_node: ICSPGraphNode;
        if (this.selection.source.type === "csp:constraint") {
          constraint_node = this.selection.source as ICSPGraphNode;
        } else if (this.selection.target.type === "csp:constraint") {
          constraint_node = this.selection.target as ICSPGraphNode;
        }
        this.graph.removeEdge(this.selection);

        // this.nameChangeOnDeletionOrAddition(constraint_node!);
        constraint_node.condition_name = "Custom";
        constraint_node.combinations_for_true = [];
        var connected_v = this.findVariablesConnected(constraint_node)
        constraint_node.condition_name = this.trueCombinations(
          connected_v,
          constraint_node.combinations_for_true
        );

        this.succeed_message = "Edge removed.";
      } else {
        if (this.selection.type === "csp:variable") {
          // find constraint nodes it is connected to
          var constraint_nodes: ICSPGraphNode[] = [];
          this.graph.edges.forEach(e => {
            if (e.source === this.selection) {
              constraint_nodes.push(e.target as ICSPGraphNode);
            } else if (e.target === this.selection) {
              constraint_nodes.push(e.source as ICSPGraphNode);
            }
          });

          this.graph.removeNode(this.selection);

          if (constraint_nodes.length > 0) {
            constraint_nodes.forEach(cn => {
              // this.nameChangeOnDeletionOrAddition(cn);
              cn.condition_name = "Custom";
              cn.combinations_for_true = [];
              var connected_v = this.findVariablesConnected(cn)
              cn.condition_name = this.trueCombinations(
                connected_v,
                cn.combinations_for_true
              );
            });
          }
        } else {
          this.graph.removeNode(this.selection);
        }

        this.succeed_message = "Node removed.";
      }
      this.selection = null;
      this.to_delete = false;
    }
  }

  /** Find all variables that are connected to the constraint */
  findVariablesConnected(node: ICSPGraphNode) {
    var variables: ICSPGraphNode[] = [];
    if (node.type === "csp:constraint") {
      var temp = this.graph.edges.filter(
        e => e.source === node || e.target === node
      );
      temp.forEach(e => {
        if (e.source === node) {
          variables.push(e.target as ICSPGraphNode);
        } else if (e.target === node) {
          variables.push(e.source as ICSPGraphNode);
        }
      });
    }
    return variables;
  }

  /** Get types of domain of all varaibles that are connected to the constraint
   * - If no variable or only one variable connected to C, return default ["FALSE", "TRUE", "Custom"]
   * - If two variable connected t C
   */
  getACT(node: ICSPGraphNode) {
    var act = ["Custom"];
    var connected_variables = this.findVariablesConnected(node);

    if (connected_variables.length === 1) {
      act = ["eq_(val)", "ne_(val)"].concat(act);
      if (this.checkDomainType(connected_variables[0].domain) === "boolean") {
        act = ["truth", "not_"].concat(act);
      } else if (
        this.checkDomainType(connected_variables[0].domain) === "number"
      ) {
        act = ["lt_(val)", "gt_(val)", "le_(val)", "ge_(val)"].concat(act);
      }
      return act;
    }

    if (connected_variables.length === 2) {
      act = ["eq", "ne"].concat(act);
      if (
        this.checkDomainType(connected_variables[0].domain) === "boolean" &&
        this.checkDomainType(connected_variables[1].domain) === "boolean"
      ) {
        act = ["and_", "or_", "implies", "xor"].concat(act);
      } else if (
        this.checkDomainType(connected_variables[0].domain) === "number" &&
        this.checkDomainType(connected_variables[1].domain) === "number"
      ) {
        act = ["lt", "gt", "le", "ge"].concat(act);
      }
      return act;
    }

    if (connected_variables.length > 2) {
      return act;
    }
  }

  checkPredefined(node: ICSPGraphNode) {
    var connected_variables = this.findVariablesConnected(node);
    var n_of_v_connected = connected_variables.length;
    var predefined = false;

    var allconstraints = ['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains', 'countOf',
           'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt', 'iadd', 'iand',
           'iconcat', 'ifloordiv', 'ilshift', 'imatmul', 'imod', 'imul',
           'index', 'indexOf', 'inv', 'invert', 'ior', 'ipow', 'irshift',
           'is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le',
           'length_hint', 'lshift', 'lt', 'matmul', 'methodcaller', 'mod',
           'mul', 'ne', 'neg', 'not_', 'or_', 'pos', 'pow', 'rshift',
           'setitem', 'sub', 'truediv', 'truth', 'xor', 'implies', 'ne_', 'eq_',
           'lt_', 'gt_', 'le_', 'ge_'];

    if(allconstraints.includes(node.condition_name)){
      predefined = true;
    }
    return predefined;
  }

  /** Selectbox default selection:
   * - If the selected constraint node is "Empty Constraint", set default to getACT(selection)[0],
   * - If the selected constraint node is defined, set default to the given constraint.
   */
  selectboxDefault(node: ICSPGraphNode) {
    var connected_variables = this.findVariablesConnected(node);
    var n_of_v_connected = connected_variables.length;

    console.log("node.condition_name: " + node.condition_name)

    if (node.condition_name === "Custom" || node.condition_name.includes("lambda")){
      this.value_in_parentheses = null;
      this.value_in_parentheses_temp = null;
      this.select_constraint_type = "Custom"
    }else if (node.condition_name.indexOf("(") > -1){
      // get the value inside "()"
      var index1 = node.condition_name.indexOf("(")
      var index2 = node.condition_name.indexOf(")")
      this.value_in_parentheses = node.condition_name.substring(index1+1, index2);
      this.value_in_parentheses_temp = node.condition_name.substring(index1+1, index2);
      this.select_constraint_type = node.condition_name.replace(this.value_in_parentheses, "val")
    }else{
      this.value_in_parentheses = null;
      this.value_in_parentheses_temp = null;
      this.select_constraint_type = node.condition_name
    }
  }

  /**Check whether Equal(val) is for strings or numbers.*/
  checkEqualsType(node: ICSPGraphNode) {
    if (node.type !== "csp:constraint") {
      return;
    }
    var connected_v = this.findVariablesConnected(node);
    var type_of_equal = "number";

    // in actual situation there will be only one variable connected to constraint Equals(val)
    connected_v.forEach(v => {
      if (this.checkDomainType(v.domain!) !== "number") {
        type_of_equal = "string";
        return;
      }
    });

    if (connected_v.length === 1 && type_of_equal === "number") {
      type_of_equal = "string";
    }

    return type_of_equal;
  }

  /** If the constraint node has a type of custom,
   * change the condition_name field to the python code of
   * all true combinations.*/
  trueCombinations(nodes: ICSPGraphNode[], combinations: Object[]) {
    var acc: string[] = [];

    var vars: string[] = [];
    nodes.forEach((n, index) => {
      vars.push("var" + index);
    });

    combinations.forEach(c => {
      var single_c: string[] = [];
      nodes.forEach((n, index) => {
        var type = this.checkDomainType(n.domain);
        if (type === "string") {
          single_c.push(vars[index] + " == '" + c[n.name] + "'");
        } else if (type === "boolean") {
          if (c[n.name] === "true") {
            single_c.push(vars[index] + " == " + "True");
          } else if (c[n.name] === "false") {
            single_c.push(vars[index] + " == " + "False");
          }
        } else {
          single_c.push(vars[index] + " == " + c[n.name]);
        }
      });
      acc.push(single_c.join(" and "));
    });

    var result = "lambda " + vars.join(", ") + ": (" + acc.join(") or (") + ")";
    return result;
  }

  /** Check the type of domain:
   * if domain is boolean[] return "boolean"
   * if domain is number[] return "number"
   * if domain is string[]:
   *    - if all strings are numeric, return "number";
   *    - else return "string";
   */
  checkDomainType(domain: any[]) {
    if (typeof domain[0] === "boolean") {
      return "boolean";
    } else if (typeof domain[0] === "number") {
      return "number";
    } else {
      // // some imported csp problem have domain value type that is otehr than string or boolean,
      // // first convert them into string
      // domain.forEach((d, index) => {
      //   domain[index] = d.toString();
      // });
      var type = "number";
      domain.forEach(d => {
        if (isNaN(d)) {
          type = "string";
          return;
        }
      });
      return type;
    }
  }

  /** Returns whether the type of constraint need a input box */
  needInputBox(type: string) {
    if (this.constraints_need_input.indexOf(type) > -1) {
      return true;
    } else {
      return false;
    }
  }

  /** Trim non-numeric chars when constraint type is LessThan(val), GreaterThan(val) */
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

  domainToString(node: ICSPGraphNode) {
    return node.domain!.join(",").split(",");
  }

  /** Get a list of domain of all variables connected to a constraint node,
   * takes in the list of variables connected to the constraint node as parameter for
   * convenient reorder.
   */
  getDomainList(connected_vs: ICSPGraphNode[]) {
    if (connected_vs.length === 0) {
      return [];
    }

    var domainlist: string[][] = [];
    connected_vs.forEach(v => {
      domainlist.push(this.domainToString(v));
    });
    return domainlist;
  }

  getDomainList_withNodeName(connected_vs: ICSPGraphNode[]) {
    if (connected_vs.length === 0) {
      return [];
    }
    var domainlist: string[][] = [];
    connected_vs.forEach(v => {
      var stringdomain = this.domainToString(v);
      stringdomain.forEach((sd, index) => {
        stringdomain[index] = v.name + "=" + sd;
      });
      domainlist.push(stringdomain);
    });
    return domainlist;
  }

  /** Find all combinations of domains of connected variables*/
  AllComb(arr: string[][]) {
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

  objectToArray(keys_in_order: string[], object: Object) {
    var temp = [];
    keys_in_order.forEach(k => {
      temp.push(object[k]);
    });
    return temp;
  }
  /**These are the original code for initial temp table assignment,
   * currently we have introduced a new field called combinations_for_true
   * The table will be assigned according to combinations_for_true
   * The code is commented out as a backup
   */
  /** Initial temp table assignment on selected constraint node change*/

  InitialTempTableAssign(node: ICSPGraphNode) {
    var prev_val_in_parentheses = this.value_in_parentheses;

    if (this.value_in_parentheses_temp !== null) {
      this.value_in_parentheses = this.value_in_parentheses_temp;
    }

    if (
      (!this.value_in_parentheses ||
        this.value_in_parentheses.match(/^\s*$/)) &&
      this.constraints_need_input.indexOf(this.select_constraint_type) > -1 &&
      this.mode === "select"
    ) {
      this.value_in_parentheses = prev_val_in_parentheses;
      this.succeed_message = "";
      this.warning_message = "Comparison parameter not specified.";
      return;
    } else {
      this.warning_message = "";
    }

    if (node.type === "csp:constraint") {
      var v_connected = this.findVariablesConnected(node);
      var table_rows = this.AllComb(this.getDomainList(v_connected));

      // First initial all relationships to be true
      if (this.select_constraint_type !== "Custom") {
        this.temp_table = [];
      }
      if (this.temp_table.length === 0) {
        for (var i = 0; i < table_rows.length; i++) {
          this.temp_table.push(true);
        }
      }

      // Read pre-defined truth table:
      if (node.combinations_for_true) {
        var name_connected_v = v_connected.map(x => x.name);
        var combinations_for_true: string[] = [];

        // convert node.combinations_for_true to an array of arrays
        node.combinations_for_true.forEach(c => {
          combinations_for_true.push(
            this.objectToArray(name_connected_v, c).join(",")
          );
        });

        // check whether each combination of domains is in the true list
        table_rows.forEach((c, index) => {
          var in_combinations_for_true = true;
          if (combinations_for_true.indexOf(c) < 0) {
            in_combinations_for_true = false;
          }

          this.temp_table[index] = in_combinations_for_true;
        });
      }

      // Situation when only one variable is connected to the selected constraint:
      if (v_connected.length === 1) {
        switch (this.select_constraint_type) {
          case "eq_(val)":
            this.domainToString(v_connected[0]).forEach((d, index) => {
              if (d === this.value_in_parentheses) {
                this.temp_table[index] = true;
              } else {
                this.temp_table[index] = false;
              }
            });
            break;

          case "ne_(val)":
            this.domainToString(v_connected[0]).forEach((d, index) => {
              if (d !== this.value_in_parentheses) {
                this.temp_table[index] = true;
              } else {
                this.temp_table[index] = false;
              }
            });
            break;

          case "lt_(val)":
            this.domainToString(v_connected[0]).forEach((d, index) => {
              if (Number(d) < Number(this.value_in_parentheses)) {
                this.temp_table[index] = true;
              } else {
                this.temp_table[index] = false;
              }
            });
            break;

          case "ge_(val)":
            this.domainToString(v_connected[0]).forEach((d, index) => {
              if (!(Number(d) < Number(this.value_in_parentheses))) {
                this.temp_table[index] = true;
              } else {
                this.temp_table[index] = false;
              }
            });
            break;

          case "gt_(val)":
            this.domainToString(v_connected[0]).forEach((d, index) => {
              if (Number(d) > Number(this.value_in_parentheses)) {
                this.temp_table[index] = true;
              } else {
                this.temp_table[index] = false;
              }
            });
            break;

          case "le_(val)":
            this.domainToString(v_connected[0]).forEach((d, index) => {
              if (!(Number(d) > Number(this.value_in_parentheses))) {
                this.temp_table[index] = true;
              } else {
                this.temp_table[index] = false;
              }
            });
            break;

          case "truth":
            this.domainToString(v_connected[0]).forEach((d, index) => {
              if (this.StringToBoolean(d)) {
                this.temp_table[index] = true;
              } else {
                this.temp_table[index] = false;
              }
            });
            break;

          case "not_":
            this.domainToString(v_connected[0]).forEach((d, index) => {
              if (!this.StringToBoolean(d)) {
                this.temp_table[index] = true;
              } else {
                this.temp_table[index] = false;
              }
            });
            break;
        }
      }

      // Situation when there are two variables connected to the selected constraint:
      if (v_connected.length === 2) {
        switch (this.select_constraint_type) {
          case "eq":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (twovals[0] === twovals[1]) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "ne":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (twovals[0] !== twovals[1]) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "lt":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (Number(twovals[0]) < Number(twovals[1])) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "ge":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (!(Number(twovals[0]) < Number(twovals[1]))) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "gt":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (Number(twovals[0]) > Number(twovals[1])) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "le":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (!(Number(twovals[0]) > Number(twovals[1]))) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "and_":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (
                this.StringToBoolean(twovals[0]) &&
                this.StringToBoolean(twovals[1])
              ) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "or_":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (
                this.StringToBoolean(twovals[0]) ||
                this.StringToBoolean(twovals[1])
              ) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "xor":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (
                (this.StringToBoolean(twovals[0]) ||
                  this.StringToBoolean(twovals[1])) &&
                !(
                  this.StringToBoolean(twovals[0]) &&
                  this.StringToBoolean(twovals[1])
                )
              ) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;

          case "implies":
            table_rows.forEach((r, index_r) => {
              var twovals = r.split(",");
              if (
                !this.StringToBoolean(twovals[0]) ||
                this.StringToBoolean(twovals[1])
              ) {
                this.temp_table[index_r] = true;
              } else {
                this.temp_table[index_r] = false;
              }
            });
            break;
        }
      }
    }
  }

  resetTable() {
    if (this.reversed) {
      this.reverseOrder(this.selection as ICSPGraphNode);
    }
    this.selectboxDefault(this.selection! as ICSPGraphNode);
    this.InitialTempTableAssign(this.selection as ICSPGraphNode);
  }

  StringToBoolean(str: string) {
    switch (str) {
      case "true":
        return true;
        break;

      case "false":
        return false;
    }
  }

  constraintToReadableText(node: ICSPGraphNode) {
    var connected_v = this.findVariablesConnected(node);
    var nodeNames = connected_v.map(v => v.name);
    var type = this.select_constraint_type;

    // check whether the constraint type is initially in ACT
    // e.g. if it is meet_at, then it is not

    if (type === "Custom" && this.initially_in_ACT) {
      return `Custom(${nodeNames})`;
    } else if (
      type === "Custom" &&
      this.selection.name.match(/^Empty Constraint\d*$/)
    ) {
      return `Custom(${nodeNames})`;
    } else if (type === "Custom" && !this.initially_in_ACT) {
      return `Custom(${nodeNames})`;
    }

    if (connected_v.length === 1) {
      var constraints1 = ["ne_(val)", "eq_(val)", "lt_(val)", "gt_(val)", "le_(val)", "ge_(val)"];
      var shouldshow1 = ["!=", "=", "<", ">", "<=", ">="];
      if (constraints1.includes(type)) {
        return `${connected_v[0].name} ${
          shouldshow1[constraints1.indexOf(type)]
        } ${this.value_in_parentheses}`;
      }
      var constraints2 = ["truth", "not_"];
      var shouldshow2 = [" = True", " = False"];
      if (constraints2.includes(type)) {
        return `${connected_v[0].name}${
          shouldshow2[constraints2.indexOf(type)]
        }`;
      }
    }

    if (connected_v.length === 2) {
      var constraints = [
        "and_",
        "or_",
        "xor",
        "implies",
        "eq",
        "lt",
        "gt",
        "ne",
        "le",
        "ge"
      ];
      var shouldshow = ["and", "or", "xor", "implies", "=", "<", ">", "!=", "<=", ">="];
      if (constraints.includes(type)) {
        return `${connected_v[0].name} ${
          shouldshow[constraints.indexOf(type)]
        } ${connected_v[1].name}`;
      }
    }

    if (connected_v.length > 2) {
      return `Custom(${nodeNames})`;
    }
  }

  reverseOrder(node: ICSPGraphNode) {
    var connected_v = this.findVariablesConnected(node);
    if (connected_v.length === 2) {
      var index1 = this.graph.edges.findIndex(
        e =>
          (e.source === connected_v[0] && e.target === node) ||
          (e.target === connected_v[0] && e.source === node)
      );
      var index2 = this.graph.edges.findIndex(
        e =>
          (e.source === connected_v[1] && e.target === node) ||
          (e.target === connected_v[1] && e.source === node)
      );
      var temp = this.graph.edges[index1];
      this.graph.edges[index1] = this.graph.edges[index2];
      this.graph.edges[index2] = temp;
      this.InitialTempTableAssign(node);
      this.$forceUpdate();
    }
    this.reversed = !this.reversed;
    if (this.reversed) {
      this.reversed_constraint_without_submission = node;
    } else {
      this.reversed_constraint_without_submission = null;
    }
    this.cleanMessages();
  }

  // Convert temp table to node.combinations_for_true
  dicTempTable(node: ICSPGraphNode) {
    var connected_v = this.findVariablesConnected(node);
    var name_connected_v = connected_v.map(v => v.name);
    var allcomb = this.AllComb(this.getDomainList(connected_v));
    var combinations_for_true: Object[] = [];

    allcomb.forEach((c, index) => {
      if (this.temp_table[index] === true) {
        var temp = c.split(",");
        var object = {};
        for (var i = 0; i < temp.length; i++) {
          object[name_connected_v[i]] = temp[i];
        }
        combinations_for_true.push(object);
      }
    });

    node.combinations_for_true = combinations_for_true;
    console.log("this.select_constraint_type: " + this.select_constraint_type)
    if (this.select_constraint_type === "Custom") {
      node.condition_name = this.trueCombinations(
        connected_v,
        node.combinations_for_true
      );
    }else if(this.select_constraint_type.includes("(")){
      node.condition_name = this.select_constraint_type.replace("val", this.value_in_parentheses)
      console.log("node.condition_name: " + node.condition_name)
    }else{
      node.condition_name = this.select_constraint_type
    }
  }

  UpdateConstraintNode(node: ICSPGraphNode, name: string) {
    if (name === null || name.match(/^\s*$/)) {
      this.warning_message = "Name not valid.";
      this.succeed_message = "";
      return;
    }
    
    if (this.NameExists(name) && name !== this.selection.name) {
      this.warning_message = "Name already exists.";
      this.succeed_message = "";
      return;
    }

    if (
      this.constraints_need_input.indexOf(this.select_constraint_type) > -1 &&
      !this.value_in_parentheses
    ) {
      this.warning_message = "Comparison parameter not specified.";
      this.succeed_message = "";
      return;
    }
    
    //update new name
    // this.nameChange(node);
    this.selection!.name = name.trimLeft().trimRight();

    this.dicTempTable(node);
    this.warning_message = "";
    this.succeed_message = "Constraint node updated.";
    this.reversed = false;
    this.reversed_constraint_without_submission = null;
  }

  @Watch("selection")
  onSelectionChanged() {
    this.value_in_parentheses_temp = null;
    this.inputbox_focused = false;

    if (this.mode === "create") {
      this.warning_message = "";
      this.succeed_message = "";

      if (this.selection) {
        this.warning_message = "";
        this.succeed_message = "";
        this.edge_succeed_message = "";
        this.edge_warning_message = "";
      }

      if (this.first == null) {
        this.first = this.selection as ICSPGraphNode;
      } else {
        this.createEdge();
      }
      return;
    }
    if (this.mode === "select") {
      this.warning_message = "";
      this.succeed_message = "";

      if (this.selection && this.selection.type === "edge") {
        this.selection = null;
      }

      if (this.selection && this.selection.type === "csp:constraint") {
        this.temp_c_name = this.selection.name;
        if (
          this.findVariablesConnected(this.selection! as ICSPGraphNode).length > 0
        ) {
          this.selectboxDefault(this.selection! as ICSPGraphNode);
          this.InitialTempTableAssign(this.selection as ICSPGraphNode);
        }
      }
      if (this.selection && this.selection.type === "csp:variable") {
        this.temp_v_name = this.selection.name;
        this.temp_v_domain = this.selection.domain!.join(",");
      }

      if (
        this.reversed &&
        this.reversed_constraint_without_submission !== null
      ) {
        this.reverseOrder(this.reversed_constraint_without_submission);
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
  onModeChange() {
    this.temp_v_name = "";
    this.temp_v_domain = "";
    this.temp_c_name = "";
    this.warning_message = "";
    this.succeed_message = "";
    this.edge_succeed_message = "";
    this.edge_warning_message = "";
    this.first = null;
    this.selection = null;
    this.inputbox_focused = false;
    this.to_delete = false;

    if (this.mode === "create") {
      this.temp_v_name = this.genNewDefaultNameV();
      this.temp_v_domain = "1, 2, 3";
      this.temp_c_name = this.genNewDefaultNameC();
    }
  }

  @Watch("isDomainBool")
  onIsDomainBoolChange() {
    this.temp_c_name = this.genNewDefaultNameC();
  }

  @Watch("create_sub_mode")
  onCSMChange() {
    this.temp_v_name = this.genNewDefaultNameV();
    this.temp_v_domain = "1, 2, 3";
    this.temp_c_name = this.genNewDefaultNameC();
    this.succeed_message = "";
    this.warning_message = "";
    this.edge_succeed_message = "";
    this.edge_warning_message = "";
  }

  @Watch("select_constraint_type")
  OnTypeChange() {
    this.value_in_parentheses_temp = null;
    this.InitialTempTableAssign(this.selection as ICSPGraphNode);
    this.cleanMessages();
    if (
      this.select_constraint_type === "Custom" &&
      this.selection.name.substring(0, 6) !== "Custom" &&
      !this.selection.name.match(/^Empty Constraint\d*$/) &&
      this.checkPredefined(this.selection as ICSPGraphNode)
    ) {
      this.initially_in_ACT = false;
    } else {
      this.initially_in_ACT = true;
    }
  }

  @Watch("lineWidth")
  onLineWidthChange(){
    this.graph.edges.forEach(edge => {
      this.$set(edge.styles, "strokeWidth", this.lineWidth);
    });
  }
}
</script>

<style scoped>
text.domain {
  font-size: 12px;
}

.text_input_box_noUserInput {
  background-color: lightgray;
}

.table_container {
  display: inline-block;
  background-color: white;
  white-space: nowrap;
  max-height: 300px;
  max-width: 700px;
  border: 2px solid #4caf50;
  overflow: scroll;
  padding-bottom: 20px;
}

.table_header {
  background-color: white;
  position: sticky;
  top: 0;
  z-index: 999;
}

.header_cell {
  text-align: center;
  font-weight: bold;
  display: inline-block;
  background-color: white;
  width: 125px;
  height: 20px;
  overflow-x: hidden;
  padding-top: 10px;
}

.header_cell:hover {
  overflow-x: hidden;
}

.table_row {
  float: left;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin: 0;
  height: 20px;
  border-bottom: 1px solid lightgray;
}

.table_body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.table_cell {
  text-align: center;
  display: inline-block;
  background-color: white;
  width: 125px;
  height: 20px;
  overflow-x: hidden;
}

.table_cell:hover {
  overflow-x: hidden;
}

.show_deletion_confirmation {
  opacity: 1;
}

.hide_deletion_confirmation {
  opacity: 0;
}
</style>
