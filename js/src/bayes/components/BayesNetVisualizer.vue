<template>
  <div tabindex="0" @keydown.stop class="csp_visualizer">
    <GraphVisualizerBase :graph="graph" @click:node="nodeClicked" @click:edge="edgeClicked" :layout="layout" :transitions="true"
        :legendColor="legendColor" :legendText="legendText">
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode :text="props.node.name" :textSize="textSize"
                         :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                         :textColour="props.hover ? 'white' : 'black'" :fill="props.hover ? 'black' : 'white'"
                          :hover="props.hover" :id="props.node.id" :detailLevel="detailLevel">
        </RoundedRectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <DirectedRectEdge :id="props.edge.id" :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y" :stroke="props.edge.styles.stroke"
                          :strokeWidth="props.edge.styles.strokeWidth" :nodeName="props.edge.target.name"
                          :graph_node_width="props.edge.styles.targetWidth" :graph_node_height="props.edge.styles.targetHeight">
        </DirectedRectEdge>
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
        <button id="auto-solve" class="btn btn-default" @click="$emit('click:auto-solve')">Auto Solve</button>
        <button id="pause" class="btn btn-default" @click="$emit('click:pause')">Pause</button>
        <button id="print-positions" class = "btn btn-default" @click="$emit('click:print-positions')">Print Positions</button>
      </div>
      <div class="output">{{output}}</div>
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
import DirectedRectEdge from "../../components/DirectedRectEdge.vue";

import {Graph, ICSPGraphNode, IGraphEdge, ISearchGraphEdge, ISearchGraphNode} from "../../Graph";
import { GraphLayout } from "../../GraphLayout";

/**
 * A CSP visualization that can be driven by backend code.
 * 
 * Events Emitted
 * - 'click:edge': An edge has been clicked. The first argument is the edge.
 * - 'click:fine-step': The "fine step" button has been clicked.
 * - 'click:step': The "step" button has been clicked.
 * - 'click:auto-solve': The "auto solve" button has been clicked.
 */
@Component({
  components: {
    RoundedRectangleGraphNode,
    GraphVisualizerBase,
    RectangleGraphNode,
    DirectedRectEdge
  }
})
export default class BayesNetInteractor extends Vue {
  /** The graph being displayed. */
  graph: Graph;
  /** Text describing what is currently happening. */
  output: string;
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
