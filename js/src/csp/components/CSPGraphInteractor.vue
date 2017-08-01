<template>
  <div>
    <GraphVisualizerBase :graph="graph" @click:edge="edgeClicked" :width="width" :height="height" :transitions="true">
      <template slot="node" scope="props">
        <EllipseGraphNode v-if="props.node.type === 'csp:variable'" :text="props.node.name"
                         :subtext="domainText(props.node)" 
                         :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                         :textColour="props.hover ? 'white' : 'black'" :fill="props.hover ? 'black' : 'white'">
        </EllipseGraphNode>
        <RectangleGraphNode v-if="props.node.type === 'csp:constraint'" :text="constraintText(props.node)"
                           :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                           :textColour="props.hover ? 'white' : 'black'" :fill="props.hover ? 'black' : 'white'">
        </RectangleGraphNode>
      </template>
      <template slot="edge" scope="props">
        <UndirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2"
                        :stroke="stroke(props.edge)"
                        :stroke-width="strokeWidth(props.edge, props.hover)"></UndirectedEdge>
      </template>
    </GraphVisualizerBase>
    <div>
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button id="auto-step" class="btn btn-default" @click="$emit('click:auto-step')">Auto Step</button>
      </div>
      <div class="output">{{output}}</div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

import EllipseGraphNode from "../../components/EllipseGraphNode.vue";
import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import RectangleGraphNode from "../../components/RectangleGraphNode.vue";
import UndirectedEdge from "../../components/UndirectedEdge.vue";

import { Graph, ICSPGraphNode, IGraphEdge } from "../../Graph";
import * as CSPGraphUtils from "../CSPGraphUtils";

/**
 * Used to draw a CSP graph that can show the visualization of code.
 */
@Component({
  components: {
    EllipseGraphNode,
    GraphVisualizerBase,
    RectangleGraphNode,
    UndirectedEdge
  }
})
export default class CSPGraphInteractor extends Vue {
  /** The graph being displayed. */
  @Prop({ type: Object })
  graph: Graph<ICSPGraphNode>;
  /** Text describing what is currently happening. */
  @Prop() output: string;
  /** The width, in pixels, of the interactor. */
  @Prop({ default: undefined })
  width: number;
  /** The height, in pixels, of the interactor. */
  @Prop({ default: undefined })
  height: number;

  /** Events Emitted */
  /**
    * 'click:edge': An edge has been clicked. The first argument is the edge.
    * 'click:fine-step': The "fine step" button has been clicked.
    * 'click:step': The "step" button has been clicked.
    * 'click:auto-step': The "autostep" button has been clicked.
    */

  edgeClicked(edge: IGraphEdge) {
    this.$emit("click:edge", edge);
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
    if (isHovering) {
      return 7;
    }

    if (edge.styles && edge.styles.strokeWidth) {
      return edge.styles.strokeWidth;
    }

    return 4;
  }

  domainText(node: ICSPGraphNode) {
    return CSPGraphUtils.domainText(node);
  }

  constraintText(node: ICSPGraphNode) {
    return CSPGraphUtils.constraintText(node);
  }
}
</script>

<style scoped>
  text.domain {
    font-size: 12px;
  }
</style>
