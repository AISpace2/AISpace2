<template>
  <div tabindex="0" @keydown.stop class="csp_visualizer">
    <GraphVisualizerBase :graph="graph" @click:node="nodeClicked" @click:edge="edgeClicked" :layout="layout" :transitions="true"
        :legendColor="legendColor" :legendText="legendText" :textSize="textSize">
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode v-if="props.node.type === 'csp:variable'" :text="props.node.name"
                         :subtext="domainText(props.node)" :textSize="textSize"
                         :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                         :textColour="props.hover ? 'white' : 'black'" :fill="props.hover ? 'black' : 'white'"
                          :hover="props.hover" :id="props.node.id" :detailLevel="detailLevel">
        </RoundedRectangleGraphNode>
        <RectangleGraphNode v-if="props.node.type === 'csp:constraint'" :text="constraintText(props.node)" :textSize="textSize"
                           :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                           :textColour="props.hover ? 'white' : 'black'" :fill="props.hover ? 'black' : 'white'"
                            :hover="props.hover" :id="props.node.id" :detailLevel="detailLevel">
        </RectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <UndirectedEdge :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y"
                        :stroke="stroke(props.edge)"
                        :stroke-width="strokeWidth(props.edge, props.hover)"></UndirectedEdge>
      </template>
      <template slot="visualization" slot-scope="props">
        <a @click="props.toggleLegend">Toggle Legend</a>

        <a class="inline-btn-group" @click="detailLevel = detailLevel > 0 ? detailLevel - 1 : detailLevel">&#8249;</a>
        <label class="inline-btn-group">Detail</label>
        <a class="inline-btn-group" @click="detailLevel = detailLevel < 2 ? detailLevel + 1 : detailLevel">&#8250;</a>

        <a class="inline-btn-group" @click="textSize = textSize - 1">-</a>
        <label class="inline-btn-group">{{textSize}}</label>
        <a class="inline-btn-group" @click="textSize = textSize + 1">+</a>
      </template>
    </GraphVisualizerBase>
    <div>
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button v-if="needACButton" id="auto-arc-consistency" class="btn btn-default" @click="$emit('click:auto-arc-consistency')">Auto Arc Consistency</button>
        <button id="auto-solve" class="btn btn-default" @click="$emit('click:auto-solve')">Auto Solve</button>
        <button id="pause" class="btn btn-default" @click="$emit('click:pause')">Pause</button>
        <button id="print-positions" class = "btn btn-default" @click="$emit('click:print-positions')">Print Positions</button>
        <button id="reset" class="btn btn-default" @click="$emit('reset')">Reset</button>
      </div>
      <div v-if="output" class="output">
          <div v-for="sub in output.split('\n')" :key ="sub">
              <span v-bind:class="chooseClass(sub)">{{sub}}</span>
          </div>
      </div>
      <div v-if="preSolution" class="output">
          <span>Solution history:</span>
          <div v-for="subSol in preSolution.split('\n')" :key ="subSol">
              <span v-bind:class="chooseClass(subSol)">{{subSol}}</span>
          </div>
      </div>
      <div v-if="FocusNode.domain.length > 1 && needSplit">
        <div>Current variable: <span class="nodeText">{{FocusNode.nodeName}}</span>.</div>
        <div>Choose value(s) to split:</div>
        <div v-for="key in FocusNode.domain" :key = "key">
          <input type="checkbox" :id="key" :value= "key" v-model="FocusNode.checkedNames">
          <label :for = "key">{{key}}</label>
        </div>
        <span>
          <button id="selectHalf" class = "btn btn-default" @click="selectHalf()">Select Half</button>
          <button id="selectRandom" class = "btn btn-default" @click="selectRandom()">Select Random</button>
        </span>
        <div>
          <button id="submitCheckBox" class = "btn btn-default" @click="$emit('click:submit')">Submit</button>
        </div>
      </div>
      <div v-if="warningMessage" class="warningText">{{warningMessage}}</div>
      <div class="output">{{positions}}</div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode.vue";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import RectangleGraphNode from "../../components/RectangleGraphNode.vue";
import UndirectedEdge from "../../components/UndirectedEdge.vue";

import { Graph, ICSPGraphNode, IGraphEdge } from "../../Graph";
import { GraphLayout } from "../../GraphLayout";
import * as CSPUtils from "../CSPUtils";

/**
 * A CSP visualization that can be driven by backend code.
 *
 * Events Emitted
 * - 'click:edge': An edge has been clicked. The first argument is the edge.
 * - 'click:fine-step': The "fine step" button has been clicked.
 * - 'click:step': The "step" button has been clicked.
 * - 'click:auto-solve': The "auto solve" button has been clicked.
 * - 'click:auto-arc-consistency': The "auto arc consistency" button has been clicked.
 */
@Component({
  components: {
    RoundedRectangleGraphNode,
    GraphVisualizerBase,
    RectangleGraphNode,
    UndirectedEdge
  }
})
export default class CSPGraphInteractor extends Vue {
  // The graph being displayed
  graph: Graph<ICSPGraphNode>;
  // The copy of initial graph used for resetting
  iniGraph: Graph<ICSPGraphNode>;
  // Text describing what is currently happening
  output: string;
  // Text descrbing warnings
  warningMessage: string;
  // The text representing the solutions found so far
  preSolution: string;
  // The text representing the positions for nodes
  positions: string;
  // Layout object that controls where nodes are drawn. */
  layout: GraphLayout;
  // The size of the text inside the node
  textSize: number;
  // Detail of the domain
  detailLevel: number;
  legendText: string[];
  legendColor: string[];
  // Whether the auto arc consistency button will show up
  needACButton: boolean;
  // Whether we need domain spliting
  needSplit: boolean;
  // space needed to print solution history
  spaces: number;
  // default spaces used to print history of solutions
  origin: number;
  // the dictionary of domains need split
  history: object;
  // the order that domains were added to history
  doOrder: number;
  // index that tracks the branch we are splitting
  ind: number;
  // the indent spacing between shown in domain spliting history
  indent: number;
  // The line width of the edges in the graph
  lineWidth: number;


  data() {
    return {
      FocusNode: {
        domain:[],
        checkedNames: [],
        nodeName: String
      }
    }
  }

  selectHalf() {
    let size = this.FocusNode.domain.length;
    this.FocusNode.checkedNames = [];
    for (let index = 0; index < size / 2; index ++) {
        this.FocusNode.checkedNames.push(this.FocusNode.domain[index]);
    }
  }

  selectRandom() {
    let size = Math.floor(Math.random() * (this.FocusNode.domain.length - 1) + 1);
    this.FocusNode.checkedNames = [];
    for (let index = 0; index < size; index ++) {
        let rand = Math.floor(Math.random() * this.FocusNode.domain.length);
        if (!this.FocusNode.checkedNames.includes(this.FocusNode.domain[rand])) {
            this.FocusNode.checkedNames.push(this.FocusNode.domain[rand]);
        }
    }
  }

  chooseClass(sub: string) {
      var solution: boolean = false;
      var warning: boolean = false;
      if (this.output) {
          solution = sub.includes('Solution found') || sub.includes('Solution: ');
          warning  = sub.includes('No more solutions');
      }
      return { 'solutionText': solution, 'warningText': warning };
  }

  edgeClicked(edge: IGraphEdge) {
    this.$emit("click:edge", edge);
  }

  nodeClicked(node: ICSPGraphNode) {
    this.$emit("click:node", node);
    if (this.needSplit) {
      this.FocusNode.domain = node.domain;
      this.FocusNode.nodeName = node.name;
      this.FocusNode.checkedNames = [];
      if (node.type == "csp:constraint") {
          this.warningMessage = "Can not split on constraints.";
          this.FocusNode.domain = [];
      } else if (node.domain.length == 1) {
          this.warningMessage = "Can only split on variable whose domain has more than 1 value."
      } else {
         //this.output = "Please choose the values in the selected domain."
          this.warningMessage = null;
      }
    }
  }

  nodeStrokeColour(node: ICSPGraphNode, isHovering: boolean = false) {
    if (node.styles && node.styles.stroke) {
      return node.styles.stroke;
    }

    return undefined;
  }

  nodeStrokeWidth(node: ICSPGraphNode) {
    if (node.styles && node.styles.strokeWidth) {
      return node.styles.strokeWidth;
    }

    return undefined;
  }

  stroke(edge: IGraphEdge) {
    if (edge.styles != null) {
      return edge.styles.stroke;
    }

    return undefined;
  }

  strokeWidth(edge: IGraphEdge, isHovering: boolean) {
    const hoverWidth = isHovering ? 3 : 0;

    if (edge.styles && edge.styles.strokeWidth) {
      return edge.styles.strokeWidth + hoverWidth;
    }

    return this.lineWidth + hoverWidth;
  }

  domainText(node: ICSPGraphNode) {
    return CSPUtils.domainText(node);
  }

  constraintText(node: ICSPGraphNode) {
    return CSPUtils.constraintText(node);
  }

  get textBtnProp() {
    return {
      width: 30,
      height: 30,
      y: 20
    };
  }

  @Watch("output")
  onOutPutChange() {
    this.warningMessage = null;
  }

  addTextSize(){
    this.textSize ++;
  }

  minusTextSize(){
    if(this.textSize > 0) this.textSize --;
  }
}

</script>
