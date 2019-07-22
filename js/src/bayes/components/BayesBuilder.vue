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
      <div v-if="mode == 'create'">
        <p style="color: blue">Select an object to create:</p>
        <input type="radio" id="create_variable" value="variable" v-model="create_mode" />
        <label for="create_variable">Variable</label>
        <input type="radio" id="create_edge" value="edge" v-model="create_mode" />
        <label for="create_edge">Edge</label>
        <div v-if="mode == 'create' && create_mode == 'variable'">
          <pre></pre>
          <p style="color: blue">
            Set the name and the domain of the variable below,
            <br/>and then double click at a position on the canvas where you want the new node to be created.
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
          <p>
            <span style="color: red">{{warning_message}}</span>
            <span style="color: green">{{succeed_message}}</span>
          </p>
        </div>
        <div v-else-if="mode == 'create' && create_mode == 'edge'">
          <pre></pre>
          <p
            v-if="(graph.nodes.indexOf(first) < 0)"
            style="color: blue"
          >Select a start node.</p>
          <p
            style="color: blue"
            v-else-if="(graph.nodes.indexOf(first) > -1) && (selection == first || selection == null || selection.type == 'edge')"
          >
            Start node:
            <span style="color: green">{{first.name}}</span>. Select an end node to create an edge.
          </p>
          <pre></pre>
          <p>
            <span style="color: red">{{warning_message}}</span>
            <span style="color: green">{{succeed_message}}</span>
          </p>
        </div>
      </div>
    </div>

    <div>
      <div v-if="mode =='select'">
        <pre></pre>
        <p style="color: blue">
          Set the name and the domain of a node by cliking on it.
        </p>
        <div v-if="selection && (graph.nodes.indexOf(selection) > -1)">
          <p style="color: blue">
            You selected node
            <span style="color: green">{{selection.name}}</span>.
          </p>
          <pre></pre>
          <label>
            <b>Name:</b>
          </label>
          <input
            type="text"
            style="backgroundColor: yellow"
            :value="selection ? temp_node_name : null"
            @focus="$event.target.select()"
            @input="temp_node_name = $event.target.value"
          />
          <label>
            <b>Domain:</b>
          </label>
          <input
            type="text"
            style="backgroundColor: yellow"
            @focus="$event.target.select()"
            :value="selection ? temp_node_domain : null"
            @input="temp_node_domain = $event.target.value"
          />
          (use comma to separate values)
          <button @click="IsValidModify(temp_node_name, temp_node_domain)">Submit</button>
          <p>
            <span style="color: red">{{warning_message}}</span>
            <span style="color: green">{{succeed_message}}</span>
          </p>
        </div>
      </div>
      <div v-else-if="mode == 'delete'">
        <p style="color: blue">Click on a node or an edge to delete.</p>
      </div>
    </div>
    <div>
      <div v-if="mode == 'set_prob'">
        <p style="color: blue">Click on a node to modifiy the probability table here.</p>
        <div v-if="selection">
          <p style="color: blue">
            You selected node
            <span style="color: green">{{selection.name}}</span>. Parents: {
            <span style="color: green">{{selection.parents.join(", ")}}</span>
            }.
          </p>
          <div class="prob_table_grid" v-if="selection.parents.length > 0">
            <div>
              <div class="parent_node" v-for="pn of selection.parents" :key="pn">
                <span style="color: green">{{pn}}</span>
              </div>
              <div
                class="select_node_dm"
                v-for="snn of selection.domain"
                :key="snn"
              >{{selection.name}} = {{snn}}</div>
            </div>
            <div v-for="(p1, index_p1) of allComb(probList(selection))" :key="index_p1">
              <div v-if="p1" class="prob_name" v-for="p2 of p1.split(',')" :key="p2">{{p2}}</div>
              <div
                class="input_box_container"
                v-for="(snn2, index_snn2) of selection.domain"
                :key="index_snn2"
              >
                <input
                  :class="getInputBoxClass(index_p1, temp_node_evidences[(index_p1 * selection.domain.length + index_snn2)])"
                  :ref="generateRef(selection) + index_p1.toString() + '_' + index_snn2.toString()"
                  type="number"
                  @focus="$event.target.select()"
                  :value="temp_node_evidences[index_p1 * selection.domain.length + index_snn2]"
                  @input="$event.target.value ? temp_node_evidences[index_p1 * selection.domain.length + index_snn2] = parseFloat($event.target.value) : temp_node_evidences[index_p1 * selection.domain.length + index_snn2] = null,
                  (index_snn2 === selection.domain.length - 1) ? null : $refs[findLastInputboxRef(index_p1)][0].value = CalLastBoxValue(getSameLineInputBoxVal(index_p1)),
                  (index_snn2 === selection.domain.length - 1) ? null : temp_node_evidences[index_p1 * selection.domain.length + selection.domain.length - 1] = CalLastBoxValue(getSameLineInputBoxVal(index_p1)),
                  updateInputBox($event.target.value)"
                  @change="$event.target.value ? temp_node_evidences[index_p1 * selection.domain.length + index_snn2] = parseFloat($event.target.value) : temp_node_evidences[index_p1 * selection.domain.length + index_snn2] = null"
                />
              </div>
            </div>
          </div>
          <div class="prob_table_grid" v-if="selection.parents.length == 0">
            <div
              class="select_node_dm"
              :key="snn_"
              v-for="snn_ of selection.domain"
            >{{selection.name}} = {{snn_}}</div>
            <div>
              <div
                class="input_box_container"
                v-for="(snn_2, index) of selection.domain"
                :key="index"
              >
                <input
                  :ref="generateRef(selection) + index.toString()"
                  :class="getInputBoxClass(index, temp_node_evidences[index])"
                  type="number"
                  :value="temp_node_evidences[index]"
                  @focus="$event.target.select()"
                  @input="$event.target.value ? temp_node_evidences[index] = Number($event.target.value) : temp_node_evidences[index] = null,
                  (index === selection.domain.length - 1) ? null : $refs[findLastInputboxRef(index)][0].value = CalLastBoxValue(getSameLineInputBoxVal(index)),
                  (index === selection.domain.length - 1) ? null : temp_node_evidences[selection.domain.length - 1] = CalLastBoxValue(getSameLineInputBoxVal(index)),
                  updateInputBox($event.target.value)"
                  @change="$event.target.value ? temp_node_evidences[index] = Number($event.target.value) : temp_node_evidences[index] = null"
                />
              </div>
            </div>
          </div>
          <div>
            <span>
              <button @click="IsEvidencesValid()">Submit</button>
              <button @click="cancelProbSet()">Cancel</button>
            </span>
          </div>
          <span style="color: red">{{warning_message}}</span><span style="color: green">{{succeed_message}}</span>
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

type Mode = "select" | "create" | "delete" | "set_prob";

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
  prev_mode: Mode = "select";
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
  create_mode: string = "variable";
  /** MAX_DIGITS is to solve the problem of float type number calculation in js,
   * to get precise result, we use integer calculation instead,
   * for each prob, we multiply it with MAX_DIGITS and round it to an integer,
   * the user cannot use prob more than 12 digits after "0.",
   * if they do so, the calculation will be incorrect and the whole line will be
   * valued as invalid.*/
  MAX_DIGITS: number = 10000000000;
  ROUND: number = 10;

  /** Switches to a new mode.
   * - Selection will remain unchanged if switch between "select" and "set_prob" mode.
   */
  setMode(mode: Mode) {
    this.mode = mode;
    if (!(this.mode === "set_prob" && this.prev_mode === "select")) {
      if (!(this.mode === "select" && this.prev_mode === "set_prob")) {
        this.selection = null;
      }
    } else {
      this.prev_mode = "set_prob";
    }
  }

  /** Returns whether name and domain for a new node to be created are valid */
  IsTempNode(name_raw: string, domain: string) {
    var name = name_raw.trimLeft().trimRight();
    var node_to_be_drawn = true;
    if (
      name === null ||
      name === "" ||
      !name.match(/^[a-zA-Z$_]+[a-zA-Z0-9$_ ]*$/)
    ) {
      node_to_be_drawn = false;
      this.warning_message = "Name not valid. Please enter a new name.";
      this.succeed_message = "";
    } else if (this.NameExists(name)) {
      node_to_be_drawn = false;
      this.warning_message = "Name already exists.";
      this.succeed_message = "";
    } else if (
      domain === null ||
      domain === "" ||
      !domain.match(/^[a-zA-Z0-9$_ ]+(,(\s)*[a-zA-Z0-9$_ ]*)*$/)
    ) {
      node_to_be_drawn = false;
      this.warning_message = "Domain not valid, Please enter a new domain.";
      this.succeed_message = "";
    } else {
      this.warning_message = "";
      this.succeed_message = "Variable created.";
    }
    return node_to_be_drawn;
  }

  /** Returns whether the modified node name and domain are valid,
   * if valid, update the values */
  IsValidModify(name: string, domain: string) {
    if (
      name === null ||
      name === "" ||
      !name.match(/^[a-zA-Z$_]+[a-zA-Z0-9$_ ]*$/)
    ) {
      this.warning_message = "Name not valid. Please enter a new name.";
      this.succeed_message = "";
    } else if (this.NameExists(name) && this.selection.name !== name) {
      this.warning_message = "Name already exists.";
    } else if (
      domain === null ||
      domain === "" ||
      !domain.match(/^[a-zA-Z0-9$_ ]+(,(\s)*[a-zA-Z0-9$_ ]*)*$/)
    ) {
      this.warning_message = "Domain not valid. Please enter a new domain.";
      this.succeed_message = "";
    } else {
      this.selection!.name = name;
      var newdomain = this.handleDomain(domain);

      if (this.selection!.domain.join(",") !== newdomain.join(",")) {
        // When new domain has a different length with the previous domain, modify evidences:
        if (this.selection!.domain.length !== newdomain.length) {
          // get dictionary before selection's domain is changed:
          var dicOriginal = this.dicEvidences(this.selection);

          var olddomain = this.selection!.domain.slice(0);

          this.selection!.domain = newdomain;

          this.selection!.evidences = [];
          // get dictionary of current selection's evidences:
          var dicAfter = this.dicEvidences(this.selection);

          this.handleEvidencesOnDomainChange(dicOriginal, dicAfter, this
            .selection as IBayesGraphNode);

          this.selection!.evidences = this.disdicEvidence(dicAfter, this
            .selection as IBayesGraphNode);

          this.graph.edges.forEach(e => {
            if (e.source === this.selection) {
              this.selection.domain = olddomain;
              var dicOriginal_child = this.dicEvidences(
                e.target as IBayesGraphNode
              );

              this.dicOriginal_child = dicOriginal_child;

              e.target.evidences = [];
              this.selection.domain = newdomain;
              var dicAfter_child = this.dicEvidences(
                e.target as IBayesGraphNode
              );

              this.dicAfter_child = dicAfter_child;

              this.handleEvidencesOnDomainChange(
                dicOriginal_child,
                dicAfter_child,
                e.target as IBayesGraphNode
              );

              e.target.evidences = this.disdicEvidence(
                dicAfter_child,
                e.target as IBayesGraphNode
              );
            }
          });
        }
        // When domain remains the same length, no need to modify evidences.
        else {
          this.selection!.domain = newdomain;
        }
      }
      this.warning_message = "";
      this.succeed_message = "Node updated.";
    }
  }

  /** This will handle domain:
   * - If domain has duplicated value, delete duplicates
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
    var domain: string[] = [];
    domain_temp.forEach(d => {
      var temp = d.trimLeft().trimRight();
      domain.push(temp);
    });

    // remove duplicates
    while (domain.find(x => domain.indexOf(x, domain.indexOf(x) + 1) !== -1)) {
      var duplicated = domain.find(
        x => domain.indexOf(x, domain.indexOf(x) + 1) !== -1
      );
      domain = domain.filter(x => x !== duplicated);
      domain.push(duplicated!);
    }

    // Covert true/false strings to boolean
    if (domain.find(x => x !== "false" && x !== "true")) {
      return domain;
    } else {
      return [false, true];
    }
  }

  /** create a dictionary for evidences */
  dicEvidences(node: IBayesGraphNode) {
    var result = {};
    if (node.parents.length > 0) {
      var allprobNames = this.allComb(this.probList_with_parents_name(node));
      for (var i = 0; i < allprobNames.length; i++) {
        var key = allprobNames[i];
        result[key] = {};
        node.domain.forEach(d_0 => {
          var d: string = d_0.toString();
          if (node.evidences.length > 0) {
            result[key][d] =
              node.evidences[i * node.domain.length + node.domain.indexOf(d_0)];
          } else {
            result[key][d] = "no value";
          }
        });
      }
    } else {
      node.domain.forEach(d_0 => {
        var d: string = d_0.toString();
        if (node.evidences.length > 0) {
          result[d] = node.evidences[node.domain.indexOf(d_0)];
        } else {
          result[d] = "no value";
        }
      });
    }
    return result;
  }

  /** Generate evidence list from evidence dictionary */
  disdicEvidence(dicEvidences: Object, node: IBayesGraphNode) {
    var result: any[] = [];
    if (node.parents.length > 0) {
      var allprobNames = this.allComb(this.probList_with_parents_name(node));
      allprobNames.forEach(pn => {
        node.domain.forEach(d_0 => {
          var d = d_0.toString();
          result.push(dicEvidences[pn][d]);
        });
      });
    } else {
      node.domain.forEach(d_0 => {
        var d = d_0.toString();
        result.push(dicEvidences[d]);
      });
    }
    return result;
  }

  /** Modify evidences on  node's domain changed
   * If the length of the selected domain changes, in each line:
   *  - if any elements remain the same name, normalize them
   *  - if there's new element added,
   *     these element will be assigned with prob = 0,
   *  - if there's only new elements no old elements: average
   * If the lengthe doesn't change, keep all probs unchanged.
   * @param dicOriginal is dictionary of @param node's evidences before domain(either node's domain or its's parents' domain) changed,
   * @param dicAfter is dictionary of @param nodes's evidences after domain changed*/
  handleEvidencesOnDomainChange(
    dicOriginal: Object,
    dicAfter: Object,
    node: IBayesGraphNode
  ) {
    var listOfkeys = Object.keys(dicAfter);
    if (node.parents.length > 0) {
      listOfkeys.forEach(k => {
        var curr_sum_of_line = 0;
        if (dicOriginal[k]) {
          node.domain.forEach(d_0 => {
            var d = d_0.toString();
            if (dicOriginal[k][d]) {
              dicAfter[k][d] = "need_to_be_normalized";
              curr_sum_of_line += dicOriginal[k][d];
            } else {
              dicAfter[k][d] = 0;
            }
          });
        } else {
          node.domain.forEach(d_0 => {
            var d = d_0.toString();
            dicAfter[k][d] = 0;
          });
        }
        var ratio = 1 / curr_sum_of_line;
        var sum_of_line_except_last_rounded = 0;
        node.domain.forEach(d_0 => {
          var d = d_0.toString();
          if (curr_sum_of_line !== 0) {
            if (dicAfter[k][d] === "need_to_be_normalized") {
              if (node.domain.indexOf(d_0) !== node.domain.length - 1) {
                var temp = parseFloat(
                  (dicOriginal[k][d] * ratio).toFixed(this.ROUND)
                );
                dicAfter[k][d] = temp;
                sum_of_line_except_last_rounded += temp;
              } else {
                dicAfter[k][d] = parseFloat(
                  (1 - sum_of_line_except_last_rounded).toFixed(this.ROUND)
                );
              }
            }
          } else {
            if (node.domain.indexOf(d_0) !== node.domain.length - 1) {
              var temp = parseFloat(
                (1 / node.domain.length).toFixed(this.ROUND)
              );
              dicAfter[k][d] = temp;
              sum_of_line_except_last_rounded += temp;
            } else {
              dicAfter[k][d] = parseFloat(
                (1 - sum_of_line_except_last_rounded).toFixed(this.ROUND)
              );
            }
          }
        });
      });
    } else {
      // When the selected node doesn't have parents
      var curr_sum_of_line = 0;
      var sum_of_line_except_last_rounded = 0;
      listOfkeys.forEach(k => {
        if (dicOriginal[k]) {
          dicAfter[k] = "need_to_be_normalized";
          curr_sum_of_line += dicOriginal[k];
        } else {
          dicAfter[k] = 0;
        }
      });

      var ratio = 1 / curr_sum_of_line;
      listOfkeys.forEach(k => {
        if (curr_sum_of_line !== 0) {
          if (dicAfter[k] === "need_to_be_normalized") {
            if (node.domain[node.domain.length - 1].toString() !== k) {
              var temp = parseFloat(
                (dicOriginal[k] * ratio).toFixed(this.ROUND)
              );
              dicAfter[k] = temp;
              sum_of_line_except_last_rounded += temp;
            } else {
              dicAfter[k] = parseFloat(
                (1 - sum_of_line_except_last_rounded).toFixed(this.ROUND)
              );
            }
          }
        } else {
          // Situation when all old values in domain are deleted
          if (node.domain[node.domain.length - 1].toString() !== k) {
            var temp = parseFloat((1 / node.domain.length).toFixed(this.ROUND));
            dicAfter[k] = temp;
            sum_of_line_except_last_rounded += temp;
          } else {
            dicAfter[k] = 1 - sum_of_line_except_last_rounded;
          }
        }
      });
    }
  }

  /**
   * Find all combinations of parents.
   * e.g. parents = {name: "Node1", domain: ["true", "false"]}, {name: "Node2", domain: ["a", "b"]}
   * => returns [["Node1 = true", "Node1 = false"], ["Node2 = a", "Node2 = b"]]
   */
  probList_with_parents_name(node: IBayesGraphNode) {
    if (node.parents.length === 0 || node.parents === null) {
      return [];
    }
    var probNameList: string[][] = [];
    node.parents.forEach(p => {
      var domains = this.domainToString(
        this.graph.nodes.find(n => n.name === p)!
      );
      var probNameList_curr_p: string[] = [];
      domains.forEach(d => {
        probNameList_curr_p.push(p + "=" + d);
      });
      probNameList.push(probNameList_curr_p);
    });
    return probNameList;
  }

  /** Generate evidences for a newly created node */
  initialEvidences(domain: string[] | boolean[]) {
    var evidences: number[] = [];
    var curr_sum = 0;
    for (var i = 0; i < domain.length; i++) {
      if (i !== domain.length - 1) {
        var temp = parseFloat((1 / domain.length).toFixed(this.ROUND));
        evidences.push(temp);
        curr_sum += temp;
      } else {
        evidences.push(parseFloat((1 - curr_sum).toFixed(this.ROUND)));
      }
    }
    return evidences;
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
      this.mode === "create" &&
      this.create_mode === "variable" &&
      this.IsTempNode(this.temp_node_name, this.temp_node_domain)
    ) {
      var emptystrarr: string[] = [];
      var domainval = this.handleDomain(this.temp_node_domain);
      var evidencearr = this.initialEvidences(domainval);

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
      this.mode === "create" &&
      this.create_mode === "edge" &&
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

      var dicOriginal = this.dicEvidences(this.selection as IBayesGraphNode);

      this.selection.parents.push(this.first.name);

      var dicAfter = this.dicEvidences(this.selection as IBayesGraphNode);

      this.handleEvidencesOnParentAdded(dicOriginal, dicAfter, this
        .selection as IBayesGraphNode);

      this.selection.evidences = this.disdicEvidence(dicAfter, this
        .selection as IBayesGraphNode);

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
    this.succeed_message = "";
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
        this.succeed_message = "";
        return (canEdgeBeAdded = false);
      }
      if (e.source === source && e.target === target) {
        this.warning_message = "Edge already exists.";
        this.succeed_message = "";
        return (canEdgeBeAdded = false);
      }
    });
    if (canEdgeBeAdded) {
      this.succeed_message = "Edge created.";
    }
    return canEdgeBeAdded;
  }

  /** Handle the children @param node's evidences when a parent is added
   * params:
   * @param dicOriginal is the dictionary of @param node's evidences before a parent is added,
   * @param dicAfter is the dictionary of @param node's evidences after a parent is added.
   *
   * - this function copy orginal line in prob table for each assignment of the new parent.
   */
  handleEvidencesOnParentAdded(
    dicOriginal: Object,
    dicAfter: Object,
    node: IBayesGraphNode
  ) {
    var listOfkeys = Object.keys(dicAfter);
    if (node.parents.length === 1) {
      listOfkeys.forEach(k => {
        node.domain.forEach(d_0 => {
          var d = d_0.toString();
          dicAfter[k][d] = dicOriginal[d];
        });
      });
    } else {
      listOfkeys.forEach(k => {
        // first generate the old key which can help with getting value from dicOriginal
        var temp = k.split(",");
        temp.pop();
        var oldkey = temp.join(",");
        node.domain.forEach(d_0 => {
          var d = d_0.toString();
          dicAfter[k][d] = dicOriginal[oldkey][d];
        });
      });
    }
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
        var dicOriginal = this.dicEvidences(this.selection.target);

        // remove edge.source from edge.target.parents
        this.selection.target.parents.splice(
          this.selection.target.parents.indexOf(this.selection.source.name),
          1
        );

        this.selection.target.evidences = [];
        var dicAfter = this.dicEvidences(this.selection.target);

        // update edge.target's evidences
        this.handleEvidencesOnParentDeleted(
          dicOriginal,
          dicAfter,
          this.selection.target,
          this.selection.source
        );

        this.graph.removeEdge(this.selection as IGraphEdge);
      }
      if (this.graph.nodes.indexOf(this.selection as IBayesGraphNode) > -1) {
        this.cleanParentsEvidenceOnNodeDel(this.selection as IBayesGraphNode);
        this.graph.removeNode(this.selection as IBayesGraphNode);
      }
      this.selection = null;
    }
  }

  /** Remove the deleted node from all children's parents lists, and update children's evidences*/
  cleanParentsEvidenceOnNodeDel(node: IBayesGraphNode) {
    this.graph.edges.forEach(edge => {
      if (edge.source === node) {
        var child = edge.target;

        var dicOriginal = this.dicEvidences(child as IBayesGraphNode);

        child.parents.splice(child.parents.indexOf(node.name), 1);

        child.evidences = [];
        var dicAfter = this.dicEvidences(child as IBayesGraphNode);

        this.handleEvidencesOnParentDeleted(
          dicOriginal,
          dicAfter,
          child as IBayesGraphNode,
          node as IBayesGraphNode
        );

        child.evidences = this.disdicEvidence(
          dicAfter,
          child as IBayesGraphNode
        );
      }
    });
  }

  /** Handle the children @param node's evidences when a parent is deleted
   * @param dicOriginal is the dictionary of @param node's evidences before the parent is deleted,
   * @param dicAfter is the dictionary of @param node's evidences after the parent is deleted,
   * @param parent is the deleted parent.
   * When a parent is deleted, the evidences in @param node only remain the probs of
   * when the deleted parent is assigned with the first value in its domain
   */
  handleEvidencesOnParentDeleted(
    dicOriginal: Object,
    dicAfter: Object,
    node: IBayesGraphNode,
    parent: IBayesGraphNode
  ) {
    var newlistOfkeys = Object.keys(dicAfter);
    if (node.parents.length === 0) {
      var oldkey = parent.name + "=" + parent.domain[0].toString();
      newlistOfkeys.forEach(k => {
        dicAfter[k] = dicOriginal[oldkey][k];
      });
    } else {
      var oldlistOfkeys = Object.keys(dicOriginal);
      var firstdomainofparent = parent.name + "=" + parent.domain[0];
      oldlistOfkeys.forEach(ok => {
        var temp = ok.split(",");
        if (temp.includes(firstdomainofparent)) {
          var index = temp.indexOf(firstdomainofparent);
          temp.splice(index, 1);

          var key = temp.join(",");
          node.domain.forEach(d_0 => {
            var d = d_0.toString();
            dicAfter[key][d] = dicOriginal[ok][d];
          });
        }
      });
    }
  }

  /**
   * Find all combinations of parents.
   * e.g. parents = {name: "Node1", domain: ["true", "false"]}, {name: "Node2", domain: ["a", "b"]}
   * => returns [["true", "false"], ["a", "b"]]
   */
  probList(node: IBayesGraphNode) {
    if (node.parents.length === 0 || node.parents === null) {
      return [];
    }
    var probNameList: string[][] = [];
    node.parents.forEach(p => {
      var domains = this.domainToString(
        this.graph.nodes.find(n => n.name === p)!
      );
      var probNameList_curr_p: string[] = [];
      domains.forEach(d => {
        probNameList_curr_p.push(d);
      });
      probNameList.push(probNameList_curr_p);
    });
    return probNameList;
  }

  domainToString(node: IBayesGraphNode) {
    return node.domain!.join(",").split(",");
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
      var str = temp.join("-");
      var result = str + "_" + node.name;
      return result;
    } else {
      return "";
    }
  }

  /** Check whether modified temp_node_evidences is valid, and
   * Update selection.evidences if modification is valid
   */
  IsEvidencesValid() {
    this.warning_message = "";
    this.succeed_message = "";
    var isvalid: boolean = true;

    if (this.temp_node_evidences.findIndex(e => e > 1 || e < 0) > -1) {
      this.warning_message = "The highlited values are invalid.";
      isvalid = false;
    }
    if (
      this.temp_node_evidences.findIndex(e => e === null || e === undefined) >
      -1
    ) {
      this.warning_message = "Please fill in all input boxes.";
      isvalid = false;
    }

    if (
      this.CalAllSumOfSameLineInputBox(this.temp_node_evidences).find(
        x => x / this.MAX_DIGITS !== 1
      )
    ) {
      if (this.warning_message !== "") {
        this.warning_message =
          "The highlighted values are invalid. The highlited line doesn't sum up to 1.";
      } else {
        this.warning_message = "The highlited line doesn't sum up to 1.";
      }
      isvalid = false;
    }

    if (isvalid) {
      this.selection.evidences = this.temp_node_evidences.slice(0);
      this.succeed_message = "Probabilities updated.";
    }

    this.$forceUpdate();
  }

  /**-----------------------------Prob Set Mode Autofill----------------------------------- */

  /** Returns a list of sums of all rows of prob inputbox */
  CalAllSumOfSameLineInputBox(evidences: number[]) {
    // first slice the node's evidences
    var linesums: number[] = [];
    var sliced = [];
    var chunksize = this.selection.domain.length;
    for (var i = 0; i < evidences.length; i += chunksize) {
      sliced.push(evidences.slice(i, i + chunksize));
    }
    sliced.forEach(s => {
      var s_ = s.map(x => x * this.MAX_DIGITS);
      linesums.push(s_.reduce((a, b) => a + b, 0));
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
    if (
      val > 1 ||
      val < 0 ||
      this.CalSumOfSameLineInputBox(index) !== this.MAX_DIGITS
    ) {
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
      sameRowProbIndexes.forEach(index_ => {
        sameRowProbVals.push(
          Math.round(this.temp_node_evidences[index_] * this.MAX_DIGITS)
        );
      });
    }

    return sameRowProbVals;
  }

  /** Calculate the value presented in the last prob inputbox when other boxes are changed.
   */
  CalLastBoxValue(vals: number[]) {
    var result = this.MAX_DIGITS - vals.reduce((a, b) => a + b, 0);
    return result / this.MAX_DIGITS;
  }

  /** Find the reference of the last inputbox of a row */
  findLastInputboxRef(prob_name_index: number) {
    var pni = prob_name_index.toString();
    var l = this.selection.domain.length;
    var ref_prefix = this.generateRef(this.selection);
    if (this.selection.parents.length > 0) {
      return ref_prefix + pni + "_" + (l - 1).toString();
    } else {
      return ref_prefix + (l - 1).toString();
    }
  }

  /** Avoid issue that the user can't input 0s after "0."
   * since the inputbox is checking values immediately */
  updateInputBox(value: string) {
    if (value.match(/^[0-9]+\.*([0-9]*[1-9]+)*$/)) {
      this.$forceUpdate();
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
    this.temp_node_name = "";
    this.temp_node_domain = "";
    if (!(this.mode == "create" && this.create_mode === "edge")) {
      this.warning_message = "";
      this.succeed_message = "";
    }

    if (this.mode == "create" && this.create_mode === "edge") {
      if (this.first == null) {
        this.first = this.selection as IBayesGraphNode;
      } else {
        this.createEdge();
      }
    } else if (this.mode === "select" && this.selection) {
      this.temp_node_name = this.selection.name!;
      this.temp_node_domain = `${this.selection.domain!.join(", ")}`;
    } else if (this.mode === "delete" && this.selection) {
      this.deleteSelection();
    } else if (this.mode === "create" && this.create_mode == "variable") {
      this.selection = null;
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "false, true";
    } else if (this.mode === "set_prob" && this.selection) {
      this.temp_node_evidences = this.selection.evidences.slice(0);
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
    this.temp_node_evidences = [];

    // Remain selection unchanged if the previous mode is select and current mode is set_prob
    if (this.mode !== "set_prob") {
      this.prev_mode = this.mode;
    }

    if (this.mode === "create" && this.create_mode === "variable") {
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "false, true";
      this.selection = null;
    }

    if (this.mode === "select" && this.selection) {
      this.temp_node_name = this.selection.name!;
      this.temp_node_domain = `${this.selection.domain!.join(", ")}`;
    }

    if (this.mode === "set_prob" && this.selection) {
      this.temp_node_evidences = this.selection.evidences.slice(0);
    }
  }

  @Watch("create_mode")
  onCreateModeChange() {
    if (this.mode === "create" && this.create_mode === "variable") {
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "false, true";
      this.warning_message = "";
      this.succeed_message = "";
      this.selection = null;
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
  border: 2px solid #4caf50;
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

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
