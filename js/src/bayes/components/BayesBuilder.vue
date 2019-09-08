<template>
  <div class="bayes_builder">
    <GraphVisualizerBase
      :graph="graph"
      :transitions="true"
      :layout="layout"
      :textSize="textSize"
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
        <strong>Mode:</strong>
      </span>
      <BayesToolbar @modechanged="setMode"></BayesToolbar>
      <div v-if="mode == 'create'">
        <p class="builder_output">
          <strong>To create variable:</strong> Set the properties below, then double click on the graph.
          <br />
          <span>
            <label>
              <strong>Name:</strong>
            </label>
            <input
              type="text"
              :value="temp_node_name"
              @focus="$event.target.select()"
              @input="temp_node_name = $event.target.value"
            />
            <label>
              <strong>Domain:</strong>
            </label>
            <input
              type="text"
              style="width: 150px;"
              :value="temp_node_domain"
              @focus="$event.target.select()"
              @input="temp_node_domain = $event.target.value"
            />
            (use comma to separate values)
          </span>
          <br />
          <span>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </span>
          <br />
          <strong>To create edge:</strong> Click on the start node, then click on the end node.
          <br />
          <span v-if="(graph.nodes.indexOf(first) >= 0) && (selection == first || selection == null || selection.type == 'edge')">
            Start node:
            <span class="nodeText">{{first.name}}</span>. Select an end
            node to create an edge, or click on <span class="nodeText">{{first.name}}</span> again to unselect it.
          </span>
          <span>
            <span class="warningText">{{edge_warning_message}}</span>
            <span class="successText">{{edge_succeed_message}}</span>
          </span>
        </p>
      </div>
    </div>

    <div>
      <div v-if="mode =='select'" v-on:keyup.enter="$refs.btn_select_submit.click()">
        <p class="builder_output">
          Select a node to modify its properties.
          <br />
        </p>
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
                @input="temp_node_name = $event.target.value"
              />
              <label>
                <strong>Domain:</strong>
              </label>
              <input
                type="text"
                style="width: 150px;"
                @focus="$event.target.select()"
                :value="selection ? temp_node_domain : null"
                @input="temp_node_domain = $event.target.value"
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
      </div>
      <div v-else-if="mode == 'delete'">
        <p class="builder_output">
          Click on a node or an edge to delete.
          <br />
          <br />
        </p>
        <p class="successText">{{succeed_message}}</p>
      </div>
    </div>
    <div>
      <div v-if="mode == 'set_prob'" v-on:keyup.enter="$refs.btn_prob_submit.click()">
        <p class="builder_output">
          Click on a node to modifiy its probability table.
          <br />
        </p>
        <div v-if="selection">
          <p class="builder_output">
            You selected node
            <span class="nodeText">{{selection.name}}</span>. Parents: {
            <span class="nodeText">{{selection.parents.join(", ")}}</span>
            }.
          </p>
          <div class="prob_table_grid_container" v-if="selection.parents.length > 0">
            <div class="prob_table_grid">
              <div class="header">
                <div class="parent_node" v-for="pn of selection.parents" :key="pn">
                  <span class="nodeText">{{pn}}</span>
                </div>
                <div
                  class="select_node_dm"
                  v-for="snn of selection.domain"
                  :key="snn"
                >{{selection.name}} = {{snn}}</div>
              </div>
              <div class="body">
                <div
                  class="row"
                  v-for="(p1, index_p1) of allComb(probList(selection))"
                  :key="index_p1"
                >
                  <div class="prob_name" v-for="p2 of p1.split(',')" :key="p2">
                    <div>{{p2}}</div>
                  </div>
                  <div
                    class="text_input_box_container"
                    v-for="(snn2, index_snn2) of selection.domain"
                    :key="index_snn2"
                  >
                    <input
                      :class="{ 'text_input_box_invalid': isInvalidInputeBox(index_p1, temp_node_evidences[(index_p1 * selection.domain.length + index_snn2)])}"
                      :ref="generateRef(selection) + index_p1.toString() + '_' + index_snn2.toString()"
                      type="text"
                      @focus="$event.target.select()"
                      @keydown="$event.target.value === 'NaN' ? $event.target.value = '' : null"
                      @keyup="($event.target.value === null || $event.target.value === ''|| $event.target.value.match(/^\.[0-9]*$/) || $event.target.value.match(/^[0-9]*\.$/)) ? handleEmptyOrDotInput($event.target.value, index_p1, index_snn2) : null"
                      :value="temp_node_evidences[index_p1 * selection.domain.length + index_snn2]"
                      @input="handleInputValue($event.target.value, index_p1, index_snn2)"
                      @blur="onBlurRest($event.target.value, index_p1, index_snn2)"
                    />
                  </div>
                </div>
              </div>
              <div class="uniform_btns">
                <div v-for="(x, index_x) of allComb(probList(selection))" :key="index_x">
                  <div class="uniform_btn_container">
                    <button class="uniform_btn" @click="uniformThisRow(index_x)">Uniform</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="prob_table_grid_container" v-if="selection.parents.length == 0">
            <div class="prob_table_grid">
              <div class="header">
                <div
                  class="select_node_dm"
                  :key="snn_"
                  v-for="snn_ of selection.domain"
                >{{selection.name}} = {{snn_}}</div>
              </div>
              <div class="body">
                <div class="row">
                  <div
                    class="text_input_box_container"
                    v-for="(snn_2, index) of selection.domain"
                    :key="index"
                  >
                    <input
                      :ref="generateRef(selection) + index.toString()"
                      :class="{ 'text_input_box_invalid': isInvalidInputeBox(index, temp_node_evidences[index])}"
                      type="text"
                      :value="temp_node_evidences[index]"
                      @focus="$event.target.select($event.target.value)"
                      @keydown="$event.target.value === 'NaN' ? $event.target.value = '' : null"
                      @keyup="($event.target.value === null || $event.target.value === '' || $event.target.value.match(/^\.[0-9]*$/) || $event.target.value.match(/^[0-9]*\.$/)) ? handleEmptyOrDotInput($event.target.value, 0, index) : null"
                      @input="handleInputValue($event.target.value, 0, index)"
                      @blur="onBlurRest($event.target.value, 0, index)"
                    />
                  </div>
                </div>
              </div>
              <div class="uniform_btns">
                <div class="uniform_btn_container">
                  <button class="uniform_btn" @click="uniformAllRows()">Uniform</button>
                </div>
              </div>
            </div>
          </div>
          <div>
            <span>
              <button @click="uniformAllRows()">All Uniform</button>
              <button ref="btn_prob_submit" @click="isEvidenceValid()">Submit</button>
              <button @click="cancelProbSet()">Cancel</button>
            </span>
          </div>
          <p>
            <span class="warningText">{{warning_message}}</span>
            <span class="successText">{{succeed_message}}</span>
          </p>
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
import { parse } from "path";

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
  mode: Mode = "create";
  prev_mode: Mode = "create";
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
  edge_succeed_message: string = "";
  edge_warning_message: string = "";
  temp_node_evidences: [];
  temp: string;
  /** MAX_DIGITS is to solve the problem of float type number calculation in js,
   * to get precise result, we use integer calculation instead,
   * for each prob, we multiply it with MAX_DIGITS and round it to an integer,
   * the user cannot use prob more than 12 digits after "0.",
   * if they do so, the calculation will be incorrect and the whole line will be
   * valued as invalid.*/
  MAX_DIGITS: number = 10000000000;
  ROUND: number = 10;

  created() {
    this.temp_node_name = this.genNewDefaultName();
    this.temp_node_domain = "false,true";
  }

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
      this.selection!.name = name.trimLeft().trimRight();
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
            dicAfter[k] = parseFloat(
              (1 - sum_of_line_except_last_rounded).toFixed(this.ROUND)
            );
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

  uniformAllRows() {
    var temp = this.initialEvidences(this.selection!.domain);
    if (this.selection!.parents.length > 0) {
      var number_of_rows = Math.round(
        this.selection!.evidences.length / this.selection!.domain.length
      );
      var temp2: number[] = [];
      for (var i = 0; i < number_of_rows; i++) {
        temp.forEach(t => {
          temp2.push(t);
        });
      }
      this.temp_node_evidences = temp2;
    } else {
      var temp = this.initialEvidences(this.selection!.domain);
      this.temp_node_evidences = temp;
    }
    this.$forceUpdate();
  }

  uniformThisRow(index_of_row: number) {
    var row_length = this.selection!.domain.length;
    var temp = this.initialEvidences(this.selection!.domain);
    for (var i = 0; i < row_length; i++) {
      this.temp_node_evidences[index_of_row * row_length + i] = temp[i];
    }
    this.$forceUpdate();
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
      this.isTempNode(this.temp_node_name, this.temp_node_domain)
    ) {
      var emptystrarr: string[] = [];
      var domainval = this.handleDomain(this.temp_node_domain);
      var evidencearr = this.initialEvidences(domainval);

      this.graph.addNode({
        id: shortid.generate(),
        name: this.temp_node_name.trimLeft().trimRight(),
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
    this.first = null;
    this.selection = null;
    this.cleanEdgeMessage();
  }

  /** Adds a new edge to the graph. */
  createEdge() {
    if (
      this.mode === "create" &&
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

      this.edge_warning_message = "";
      this.first = null;
      this.selection = null;
    }
    this.first = null;
    this.selection = null;
    this.warning_message = "";
    this.succeed_message = "";
  }

  /** Check whether the edge can be created */
  canEdgeBeAdded(source: IBayesGraphNode, target: IBayesGraphNode) {
    var canEdgeBeAdded = true;
    this.edge_warning_message = "";
    this.edge_succeed_message = "";
    if (source === null || target === null) {
      return false;
    }
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
        this.edge_warning_message = "No bi-direction edges between two nodes.";
        this.edge_succeed_message = "";
        return (canEdgeBeAdded = false);
      }
      if (e.source === source && e.target === target) {
        this.edge_warning_message = "Edge already exists.";
        this.edge_succeed_message = "";
        return (canEdgeBeAdded = false);
      }
    });
    if (canEdgeBeAdded) {
      this.edge_succeed_message = "Edge created.";
    }
    return canEdgeBeAdded;
  }

  cleanEdgeMessage() {
    if (this.mode === "create") {
      this.edge_warning_message = "";
      this.edge_succeed_message = "";
    }
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
      this.first = null;
    } else {
      this.selection = selection;
    }
  }

  /** Remove the current selection from the graph. */
  deleteSelection() {
    if (this.selection && this.mode === "delete") {
      if (this.graph.edges.indexOf(this.selection as IGraphEdge) > -1) {
        var source = this.selection.source;
        var target = this.selection.target;

        var dicOriginal = this.dicEvidences(target);

        // remove edge.source from edge.target.parents
        target.parents.splice(target.parents.indexOf(source.name), 1);

        target.evidences = [];
        var dicAfter = this.dicEvidences(target);

        // update edge.target's evidences
        this.handleEvidencesOnParentDeleted(
          dicOriginal,
          dicAfter,
          target,
          source
        );

        target.evidences = this.disdicEvidence(dicAfter, target);

        this.graph.removeEdge(this.selection as IGraphEdge);
        this.succeed_message = "Edge deleted.";
      }
      if (this.graph.nodes.indexOf(this.selection as IBayesGraphNode) > -1) {
        this.cleanParentsEvidenceOnNodeDel(this.selection as IBayesGraphNode);
        this.graph.removeNode(this.selection as IBayesGraphNode);
        this.succeed_message = "Node deleted.";
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

  /** This function is to add a white block at the end of the last of the header of the prob table
   */

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
  isEvidenceValid() {
    this.warning_message = "";
    this.succeed_message = "";
    var isvalid: boolean = true;

    this.temp_node_evidences.forEach((ev, index) => {
      if (ev === null || ev === undefined || Number.isNaN(ev) || ev === ".") {
        this.temp_node_evidences[index] = 0;
      }
    });

    if (this.temp_node_evidences.findIndex(e => e > 1 || e < 0) > -1) {
      this.warning_message = "The hightlighted values are invalid.";
      isvalid = false;
    }

    if (
      this.calAllSumOfSameLineInputBox(this.temp_node_evidences).find(
        x => x / this.MAX_DIGITS !== 1
      )
    ) {
      if (this.warning_message !== "") {
        this.warning_message =
          "The highlighted values are invalid. The hightlighted line doesn't sum up to 1.";
      } else {
        this.warning_message = "The highlighted line doesn't sum up to 1.";
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
  calAllSumOfSameLineInputBox(evidences: []) {
    // first slice the node's evidences
    var linesums: number[] = [];
    var sliced = [];
    var chunksize = this.selection.domain.length;
    for (var i = 0; i < evidences.length; i += chunksize) {
      sliced.push(evidences.slice(i, i + chunksize));
    }
    sliced.forEach(s => {
      s.forEach((se, index) => {
        if (se === "." || se === null) {
          s[index] = 0;
        } else if (typeof se === "string") {
          if (
            se !== "." &&
            (se.match(/^\.[0-9]*$/) || se.match(/^[0-9]*\.$/))
          ) {
            s[index] = parseFloat(se);
          }
        }
      });
      var s_ = s.map(x => x * this.MAX_DIGITS);
      linesums.push(s_.reduce((a, b) => a + b, 0));
    });

    return linesums;
  }

  calSumOfSameLineInputBox(index: number) {
    if (this.selection.parents.length > 0) {
      return this.calAllSumOfSameLineInputBox(this.temp_node_evidences)[index];
    } else {
      return this.calAllSumOfSameLineInputBox(this.temp_node_evidences)[0];
    }
  }

  cancelProbSet() {
    this.temp_node_evidences = this.selection.evidences.slice(0);
    this.warning_message = "";
    this.succeed_message = "";
    this.$forceUpdate();
  }

  isInvalidInputeBox(index: number, val: number | string) {
    return val > 1 || val < 0 || (Number.isNaN(parseFloat(val)) && val !== "." && val !== "" && val !== null) ||
      this.calSumOfSameLineInputBox(index) !== this.MAX_DIGITS;
  }

  /** This is to prevent non-numeric input in Safari since type="number" doesn't work in Safari */
  handleInputValue(val: string, pni: number, di: number) {
    if ( val.length === 0 ||
      val === null ||
      val === "." ||
      val.match(/^\.[0-9]*$/) ||
      val.match(/^[0-9]*\.$/) ) {
      this.temp_node_evidences.forEach((e, index) => {
        if (e === null || e === ".") {
          this.temp_node_evidences[index] = 0;
        } else if (typeof e === "string") {
          if (e.match(/^\.[0-9]*$/) || e.match(/^[0-9]*\.$/)) {
            this.temp_node_evidences[index] = parseFloat(e);
          }
        }
      });
    } else if (val.match(/^.*[^0-9\.].*$/) || !val.match(/^[0-9]*\.?[0-9]*$/)) {
      var result = val.replace(/[^\d.]/g, "");
      if (!result.match(/^[0-9]*\.?[0-9]*$/)) {
        var indexofdot = result.indexOf(".");
        var result_removed_dot = result.replace(/\./g, "");
        result = result_removed_dot.slice(0, indexofdot) + "." + result_removed_dot.slice(indexofdot, result_removed_dot.length);
      }
      this.$refs[this.findInputboxRef(pni, di)][0].value = result;
    } else {
      this.fillLastInputbox(val, pni, di);
      this.updateInputBox(val, pni, di);
    }
  }

  /** Update the color of the inputbox when the box has been emptied */
  handleEmptyOrDotInput(val: string, pni: number, di: number) {
    if (val.match(/^\.[0-9]*$/) || val.match(/^[0-9]*\.$/)) {
      val === "." ? this.fillLastInputbox("0", pni, di) : this.fillLastInputbox(val, pni, di);
      this.$forceUpdate();
      this.temp_node_evidences[pni * this.selection.domain.length + di] = val;
    } else if (val === "" || val === null) {
      this.fillLastInputbox("0", pni, di);
      this.$forceUpdate();
      this.temp_node_evidences[pni * this.selection.domain.length + di] = null;
    }
  }

  /** When user cursor leaves current input box,
   * - if the value is "", "." or null, reset them to 0
   * - if the value is, for example, "4.", set it to "4"
   * - if the value is, for example, ".4", set it to "0.4"*/
  onBlurRest(val: string, pni: number, di: number) {
    if (val === "" || val === null || val === ".") {
      this.temp_node_evidences[pni * this.selection.domain.length + di] = 0;
      this.$refs[this.findInputboxRef(pni, di)][0].value = "0";
    } else if (val.match(/^\.[0-9]*$/) || val.match(/^[0-9]*\.$/)) {
      this.temp_node_evidences[
        pni * this.selection.domain.length + di
      ] = parseFloat(val);
      this.$refs[this.findInputboxRef(pni, di)][0].value = parseFloat(val);
    }
  }

  /** Autofill last input box in a row to keep sum of this row = 1 */
  fillLastInputbox(val: string, pni: number, di: number) {
    if (this.selection.parents.length > 0) {
      this.temp_node_evidences[
        pni * this.selection.domain.length + di
      ] = parseFloat(val);
      if (di !== this.selection.domain.length - 1) {
        var lastboxval = this.CalLastBoxValue(this.getSameLineInputBoxVal(pni));
        this.$refs[this.findLastInputboxRef(pni)][0].value = lastboxval;
        this.temp_node_evidences[
          pni * this.selection.domain.length + this.selection.domain.length - 1
        ] = lastboxval;
      }
    } else {
      this.temp_node_evidences[di] = parseFloat(val);
      if (di !== this.selection.domain.length - 1) {
        var lastboxval = this.CalLastBoxValue(this.getSameLineInputBoxVal(di));
        this.$refs[this.findLastInputboxRef(di)][0].value = lastboxval;
        this.temp_node_evidences[this.selection.domain.length - 1] = lastboxval;
      }
    }
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
    var l = this.selection.domain.length;
    var ref_prefix = this.generateRef(this.selection);
    if (this.selection.parents.length > 0) {
      return ref_prefix + prob_name_index + "_" + (l - 1).toString();
    } else {
      return ref_prefix + (l - 1).toString();
    }
  }

  /** Find the reference of the inputbox */
  findInputboxRef(prob_name_index: number, domain_index: number) {
    var ref_prefix = this.generateRef(this.selection);
    if (this.selection.parents.length > 0) {
      return ref_prefix + prob_name_index + "_" + domain_index;
    } else {
      return ref_prefix + domain_index;
    }
  }

  /** Avoid issue that the user can't input 0s after "0."
   * since the inputbox is checking values immediately */
  updateInputBox(value: string, pni: number, di: number) {
    if (!value.match(/^[0-9]+\.$/)) {
      if (
        value.match(/^[0-9]*\.?([0-9]*[1-9]+)*$/) ||
        value.match(/^([0-9\.]*[^0-9\.]+[0-9\.]*)+$/)
      ) {
        this.$forceUpdate();
      }
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

    if (!(this.mode === "create" || this.mode === "delete")) {
      this.edge_warning_message = "";
      this.edge_succeed_message = "";
      this.warning_message = "";
      this.succeed_message = "";
    }

    if (this.mode === "create") {
      this.temp_node_name = this.genNewDefaultName();
      this.temp_node_domain = "false, true";
      if (this.first === null) {
        this.first = this.selection as IBayesGraphNode;
      } else {
        this.createEdge();
      }
    } else if (this.mode === "select" && this.selection) {
      this.temp_node_name = this.selection.name!;
      this.temp_node_domain = `${this.selection.domain!.join(", ")}`;
    } else if (this.mode === "delete" && this.selection) {
      this.deleteSelection();
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
    this.edge_succeed_message = "";
    this.edge_warning_message = "";
    this.temp_node_evidences = [];
    this.first = null;

    // Remain selection unchanged if the previous mode is select and current mode is set_prob
    if (this.mode !== "set_prob") {
      this.prev_mode = this.mode;
    }

    if (this.mode === "create") {
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

  @Watch("first")
  onFirstChange() {
    if (this.selection) {
      this.edge_succeed_message = "";
      this.edge_warning_message = "";
      this.warning_message = "";
      this.succeed_message = "";
    }
  }
}
</script>

<style scoped>
text.domain {
  font-size: 12px;
}

.prob_table_grid {
  display: grid;
  grid-template-areas:
    "header header"
    "body uniform_btns"
    "body uniform_btns";
  background-color: white;
  white-space: nowrap;
  max-height: 100%;
  max-width: 100%;
  margin: 0;
}

.prob_table_grid_container {
  display: inline-block;
  background-color: white;
  white-space: nowrap;
  max-height: 300px;
  max-width: 700px;
  border: 2px solid #4caf50;
  overflow: scroll;
  padding-bottom: 20px;
}

.header {
  background-color: white;
  grid-area: header;
  position: sticky;
  top: 0;
  z-index: 999;
}

.parent_node {
  text-align: center;
  font-weight: bold;
  background-color: white;
  display: inline-block;
  width: 125px;
  height: 20px;
  overflow-x: hidden;
  padding-top: 10px;
}

div.parent_node:hover {
  overflow-x: scroll;
}

div.select_node_dm {
  text-align: center;
  color: rgb(250, 106, 130);
  font-weight: bold;
  background-color: white;
  display: inline-block;
  width: 125px;
  height: 20px;
  overflow: hidden;
  padding-top: 10px;
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

.row {
  float: left;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin: 0;
  height: 20px;
}

.body {
  grid-area: body;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.uniform_btns {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  grid-area: uniform_btns;
  position: sticky;
  right: 0;
}

.uniform_btn_container {
  height: 20px;
  margin: 0;
}

.text_input_box_invalid {
  background-color: pink;
}
</style>
