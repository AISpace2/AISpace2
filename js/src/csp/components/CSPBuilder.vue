<template>
  <div class="csp_builder">
    <GraphVisualizerBase 
      :graph="graph" 
      :transitions="true" 
      :layout="layout" 
      :textSize="textSize"
      @dblclick="createNode" 
      @click:edge="updateSelection" 
      @click:node="updateSelection" 
      @delete="deleteSelection" 
    >
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode v-if="props.node.type === 'csp:variable'" :text="props.node.name" :subtext="domainText(props.node)"
                                   :fill="props.node === selection ? 'pink' : 'white'" :textSize="textSize" :hover="props.hover"
                                   :detailLevel="detailLevel">
        </RoundedRectangleGraphNode>
        <RectangleGraphNode v-if="props.node.type === 'csp:constraint'" :text="constraintText(props.node)"
                            :fill="props.node === selection ? 'pink' : 'white'" :textSize="textSize" :hover="props.hover"
                            :detailLevel="detailLevel">
        </RectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <UndirectedEdge 
        :x1="props.edge.source.x" 
        :x2="props.edge.target.x" 
        :y1="props.edge.source.y" 
        :y2="props.edge.target.y" 
        :stroke="strokeColour(props.edge)"
        :strokeWidth="lineWidth"
        ></UndirectedEdge>
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
        <b>Domain Type: </b>
      </span>
      <CSPDomainbar @domainTypechanged="setDomainType"></CSPDomainbar>
    </div>

    <div>
      <span>
        <b>Mode: </b>
      </span>
      <CSPToolbar @modechanged="setMode"></CSPToolbar>
      <div v-if="mode == 'constraint' ">
        <span>Double click on the graph to create a new {{mode}}.</span>
      </div>
    </div>

    <div>
      <div v-if="mode == 'variable' ">
        <p class="builder_output">
          <strong>To create variable:</strong> Set the name and the domain of the variable below,
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
              <strong>Domain:</strong>
            </label>
            <input
              type="text"
              style="width: 150px;"
              :value="temp_node_domain"
              @focus="$event.target.select()"
              @input="temp_node_domain = $event.target.value, cleanMessages()"
            />
            (use comma to separate values)
          </span>
          <br />
          <span>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </span>
        </p>
      </div>
      <div v-if="mode == 'select'">
        <p class="builder_output">
          Set the name and the domain of a node by cliking on it.
          <br />
        </p>
        <div>
          <div v-if="selection && selection.type === 'csp:variable'">
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
                  v-on:keyup.enter="isValidModify(temp_node_name, temp_node_domain)"
                />
                <label>
                  <strong>Domain:</strong>
                </label>
                <input
                  type="text"
                  style="width: 150px;"
                  @focus="$event.target.select()"
                  :value="selection ? temp_node_domain : null"
                  @input="temp_node_domain = $event.target.value, cleanMessages()"
                  v-on:keyup.enter="isValidModify(temp_node_name, temp_node_domain)"
                />
                (use comma to separate values)
                <button
                  ref="btn_select_submit"
                  @click="isValidModify(temp_node_name, temp_node_domain)"
                >Submit</button>
              </span>
              <br />
            </p>
            <p>
              <span class="warningText">{{warning_message}}</span>
              <span class="successText">{{succeed_message}}</span>
            </p>
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
      <div v-if="mode == 'edge'">
        <p class="builder_output">
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
          </span>
        </p>
        <p>
          <span class="warningText">{{warning_message}}</span>
          <span class="successText">{{succeed_message}}</span>
        </p>
      </div>  
      <div v-if="mode == 'delete'">
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

import CSPToolbar from "./CSPBuilderToolbar.vue";
import CSPDomainbar from "./CSPBuilderDomainbar.vue";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import RectangleGraphNode from "../../components/RectangleGraphNode.vue";
import UndirectedEdge from "../../components/UndirectedEdge.vue";

import { Graph, ICSPGraphNode, IGraphEdge } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import * as CSPUtils from "../CSPUtils";
import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode.vue";

type Mode = "select" | "variable" | "constraint" | "edge" | "delete";

type DomainType = "number" | "string" | "boolean";

/**
 * Component to visually construct a CSP graph.
 *
 * Currently incomplete.
 */
@Component({
  components: {
    RoundedRectangleGraphNode,
    CSPDomainbar,
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
  /** The type of the domain. */
  domainType: DomainType = "number";

  /** The mode of the editor. */
  mode: Mode = "select";
  /** The currently selected node or edge. Actions are preformed on the selection. */
  selection: ICSPGraphNode | IGraphEdge | null = null;
  /** During edge creation, tracks the source node of the edge to be formed. */
  first: ICSPGraphNode | null = null;
  textSize: number;
  lineWidth: number;
  detailLevel: number;
  
  temp_node_name: string = "";
  temp_node_domain: string = "";
  
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

    /** Switches to a new mode. */
  setDomainType(domainType: DomainType) {
    this.domainType = domainType;
  }

  cleanMessages() {
    this.warning_message = "";
    this.succeed_message = "";
  }

  /** Adds a node to the graph at position (x, y). */
  createNode(x: number, y: number) {
    var emptyconstraintParents: string[] = [];
    var domainval = this.handleDomain(this.temp_node_domain);

    if (this.mode === "variable" && this.isTempNode(this.temp_node_name, this.temp_node_domain)) {
      this.graph.addNode({
        id: shortid.generate(),
        name: this.temp_node_name,
        x,
        y,
        type: "csp:variable",
        domain: domainval
      } as ICSPGraphNode);
      
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "1,2,3";
      this.warning_message = "";


    } else if (this.mode === "constraint") {
      this.graph.addNode({
        id: shortid.generate(),
        name: "Constraint",
        x,
        y,
        type: "csp:constraint",
        constraintParents: emptyconstraintParents
      } as ICSPGraphNode);
    }

    this.first = null;
    this.selection = null;

  }

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

  /** Returns whether name and domain for a new node to be created are valid */
  isTempNode(name_raw: string, domain: string) {
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
    } else if (
      domain === null ||
      domain === "" ||
      !domain.match(/^.+(,(\s)*.*)*$/)
    ) {
      node_to_be_drawn = false;
      this.warning_message = "Domain not valid.";
      this.succeed_message = "";
    } else if (this.checkDomainDuplicates(domain)) {
      node_to_be_drawn = false;
      this.warning_message = "Domain contains duplicated values.";
      this.succeed_message = "";
    } else {
      this.warning_message = "";
      this.succeed_message = "Variable created.";
    }
    return node_to_be_drawn;
  }

  /** Adds a new edge to the graph. */
  createEdge() {
    if (this.mode === "edge" && this.selection != null && this.first != null) {

      this.cleanMessages();

      if (this.first === this.selection){
        this.first = null;
        this.selection = null;
        return;
      }

      // Can't create an edge between two variables
      if (
        this.first.type === "csp:variable" &&
        this.selection.type === "csp:variable"
      ) {
        console.log("Can't create an edge between two variables");
        this.first = null;
        this.selection = null;
        this.warning_message = "Can't create an edge between two variables.";
        this.succeed_message = "";
        return;
      }

      // Can't create an edge between two constraints
      if (
        this.first.type === "csp:constraint" &&
        this.selection.type === "csp:constraint"
      ) {
        console.log("Can't create an edge between two constraints");
        this.first = null;
        this.selection = null;
        this.warning_message = "Can't create an edge between two constraints.";
        this.succeed_message = "";
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
        if (e.source === this.selection && e.target === this.first) {
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
        name: "edge1"
      });

      // Update related constraint's variable
      if(this.selection.type === "csp:constraint"){
        this.selection.constraintParents.push(this.first.name);
      } else {
        this.first.constraintParents.push(this.selection.name);
      }


      this.first = null;
      this.selection = null;
      this.warning_message = "";
      this.succeed_message = "Edge created.";



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
      this.first = null;
    } else {
      this.selection = selection;
    }
  }

  /** Returns whether the modified node name and domain are valid,
   * if valid, update the values */
  isValidModify(name: string, domain: string) {
    if (name === null || name.match(/^\s*$/)) {
      this.warning_message = "Name not valid.";
      this.succeed_message = "";
    } else if (this.NameExists(name) && this.selection.name !== name) {
      this.warning_message = "Name already exists.";
      this.succeed_message = "";
    } else if (
      domain === null ||
      domain === "" ||
      !domain.match(/^.+(,(\s)*.*)*$/)
    ) {
      this.warning_message = "Domain not valid.";
      this.succeed_message = "";
    } else if (this.checkDomainDuplicates(domain)) {
      this.warning_message = "Domain contains duplicated values.";
      this.succeed_message = "";
    } else {
      var oldname = this.selection.name.slice(0);
      this.selection!.name = name.trimLeft().trimRight();
      var newname = this.selection.name.slice(0);

      // Update related constraints' variable name
      this.graph.edges.forEach(e => {
        if (e.source === this.selection) {
          e.target.constraintParents[e.target.constraintParents.indexOf(oldname)] = newname;
        } else if (e.target === this.selection) {
          e.source.constraintParents[e.target.constraintParents.indexOf(oldname)] = newname;
        }

      });

      this.selection!.domain = this.handleDomain(domain);

      this.warning_message = "";
      this.succeed_message = "Node updated.";
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

  /** This will handle domain:
   * - If domain has duplicated value, send a warning message
   * - If domain has white-spaces at the beginning or the end, trim the domain
   * - Remove any empty string
   * - If domain only contains "true" or "false", convert to boolean list
   */
  handleDomain(domain_raw: string) {
    var domain_temp = domain_raw
      .trimLeft()
      .trimRight()
      .split(/,\s*/)
      .filter(x => x !== "");
    

    if(this.domainType === "number"){
      let domain: number[] = [];
      domain_temp.forEach(d => {          
        var temp = d.trimLeft().trimRight();
        domain.push(Number(temp));
      });
      return domain;
    } else if (this.domainType === "string"){
      let domain: string[] = [];
      domain_temp.forEach(d => {
        var temp = d.trimLeft().trimRight();
        domain.push(temp);
      });
      return domain;
    } else if (this.domainType === "boolean"){
      let domain: boolean[] = [];
      domain_temp.forEach(d => {
        var temp = d.trimLeft().trimRight();
        domain.push(Boolean(temp));
      });
      return domain;
    }
      
    return null;
     
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
      if (this.graph.edges.indexOf(this.selection as IGraphEdge) > -1) {
        var source = this.selection.source;
        var target = this.selection.target;

        // Remove related constraint's variable
        if(source.type === "csp:constraint"){
          source.constraintParents.splice(source.constraintParents.indexOf(source.name), 1);
        } else {
          target.constraintParents.splice(target.constraintParents.indexOf(source.name), 1);
        }

        this.graph.removeEdge(this.selection as IGraphEdge);
        this.succeed_message = "Edge deleted.";
      }
      if (this.graph.nodes.indexOf(this.selection as ICSPGraphNode) > -1) {
        if (this.selection.type === "csp:variable") {
          this.graph.edges.forEach(edge => {
            if (edge.source === this.selection) {
              edge.target.constraintParents.splice(edge.target.constraintParents.indexOf(edge.source.name), 1);
            } else if (edge.target === this.selection){
              edge.source.constraintParents.splice(edge.source.constraintParents.indexOf(edge.source.name), 1);
            }
          });
        }
        this.graph.removeNode(this.selection as ICSPGraphNode);
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

    if (this.mode === "edge") {
      if (this.first === null) {
        this.first = this.selection as ICSPGraphNode;
      } else {
        this.createEdge();
      }
    } else if (this.mode === "variable" || this.mode === "constraint" ) {
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "1,2,3";
      this.selection = null;
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
      this.temp_node_name = this.selection.name!;
      this.temp_node_domain = `${this.selection.domain!.join(", ")}`;
    } else {
      this.selection = null;
    }
  }

  @Watch("mode")
  onModeChanged() {
    this.temp_node_name = "";
    this.temp_node_domain = "";
    this.warning_message = "";
    this.succeed_message = "";
    this.first = null;
    this.to_delete = false;

    if (this.mode === "variable" || this.mode === "constraint" ) {
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "1,2,3";
      this.selection = null;
    }

  }

  @Watch("first")
  onFirstChange() {
    if (this.selection) {
      this.cleanMessages();
    }
  }

  @Watch("domainType")
  onDomainTypeChanged(){
    if(this.domainType === "number"){
      this.graph.nodes.forEach(node => {
        let domain: number[] = [];
        node.domain.forEach(d => {
          domain.push(Number(d));
        });
        node.domain = domain;
        })
    } else if (this.domainType === "string"){
      this.graph.nodes.forEach(node => {
        let domain: string[] = [];
        node.domain.forEach(d => {
          domain.push(String(d));
        });
        node.domain = domain;
      })
    } else if (this.domainType === "boolean"){
      this.graph.nodes.forEach(node => {
        let domain: boolean[] = [];
        node.domain.forEach(d => {
          domain.push(Boolean(d));
        });
        node.domain = domain;
      })
    }  
  }

}


</script>

<style scoped>
text.domain {
  font-size: 12px;
}

.show_deletion_confirmation {
  opacity: 1;
}

.hide_deletion_confirmation {
  opacity: 0;
}
</style>
