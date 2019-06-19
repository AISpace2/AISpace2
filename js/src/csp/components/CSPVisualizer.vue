<template>
  <div tabindex="0" @keydown.stop class="csp_visualizer">
    <GraphVisualizerBase :graph="graph" @click:node="nodeClicked" @click:edge="edgeClicked" :layout="layout" :transitions="true"
        :legendColor="legendColor" :legendText="legendText">
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
        <button id="auto-arc-consistency" class="btn btn-default" @click="$emit('click:auto-arc-consistency')">Auto Arc Consistency</button>
        <button id="auto-solve" class="btn btn-default" @click="$emit('click:auto-solve')">Auto Solve</button>
        <button id="pause" class="btn btn-default" @click="$emit('click:pause')">Pause</button>
        <button id="print-positions" class = "btn btn-default" @click="$emit('click:print-positions')">Print Positions</button>
      </div>
      <div class="output" style="white-space: pre;">{{output}}</div>
      <div v-if="pre_solution" class="pre_solution" style="white-space: pre;">Solutions found: {{pre_solution}}</div>  
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

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
  /** The graph being displayed. */
  graph: Graph<ICSPGraphNode>;
  /** Text describing what is currently happening. */
  output: string;
  /** The text representing the solutions found so far. Persistent until new solution found. */
  pre_solution: string;
  /** Layout object that controls where nodes are drawn. */
  layout: GraphLayout;
  // The size of the text inside the node
  textSize: number;
  // detail of the domain
  detailLevel: number;
  legendText: string[];
  legendColor: string[];

  edgeClicked(edge: IGraphEdge) {
    this.$emit("click:edge", edge);
  }

  nodeClicked(node: ICSPGraphNode) {
    this.$emit("click:node", node);
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

    return 4 + hoverWidth;
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

  addTextSize(){
    this.textSize ++;
  }

  minusTextSize(){
    if(this.textSize > 0) this.textSize --;
  }
}

</script>
