<template>
  <div tabindex="0" @keydown.stop class="csp_visualizer">
    <GraphVisualizerBase :graph="graph" @click:node="nodeClicked" @click:edge="edgeClicked" :layout="layout" :transitions="true"
        :legendColor="legendColor" :legendText="legendText">
      <template slot="node" scope="props">
        <RoundedRectangleGraphNode v-if="props.node.type === 'csp:variable'" :text="props.node.name"
                         :subtext="domainText(props.node)" :textSize="textSize"
                         :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                         :textColour="props.hover ? 'white' : 'black'" :fill="props.hover ? 'black' : 'white'"
                          :hover="props.hover" :id="props.node.id">
        </RoundedRectangleGraphNode>
        <RectangleGraphNode v-if="props.node.type === 'csp:constraint'" :text="constraintText(props.node)" :textSize="textSize"
                           :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                           :textColour="props.hover ? 'white' : 'black'" :fill="props.hover ? 'black' : 'white'"
                            :hover="props.hover" :id="props.node.id">
        </RectangleGraphNode>
      </template>
      <template slot="edge" scope="props">
        <UndirectedEdge :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y"
                        :stroke="stroke(props.edge)"
                        :stroke-width="strokeWidth(props.edge, props.hover)"></UndirectedEdge>
      </template>
      <template slot="visualization" scope="props">
        <foreignObject :x="props.width - 80" y="20" width="30" height="30"> <Button @click="textSize++">+</Button> </foreignObject>
        <foreignObject :x="props.width - 80" y="20" width="30" height="30"> <Button @click="textSize++">+</Button> </foreignObject>
        <foreignObject :x="props.width - 80" y="20" width="30" height="30"> <Button @click="textSize--">-</Button> </foreignObject>
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
  /** Layout object that controls where nodes are drawn. */
  layout: GraphLayout;
  // The size of the text inside the node
  textSize: number;
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
}

</script>

<style scoped>
  text.domain {
    font-size: 12px;
  }
</style>
