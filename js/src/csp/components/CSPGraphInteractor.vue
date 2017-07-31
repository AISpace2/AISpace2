<template>
  <div>
    <GraphVisualizerBase :graph="graph" @click:edge="edgeClicked" :width="width" :height="height">
      <template slot="node" scope="props">
        <CSPVariableNode v-if="props.node.type === 'csp:variable'" :name="props.node.name"
                         :domain="props.node.domain" 
                         :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                         :textColour="props.hover ? 'white' : 'black'" :fillColour="props.hover ? 'black' : 'white'">
        </CSPVariableNode>
        <CSPConstraintNode v-if="props.node.type === 'csp:constraint'" :name="props.node.name"
                           :constraint="props.node.constraint" 
                           :stroke="nodeStrokeColour(props.node, props.hover)" :stroke-width="nodeStrokeWidth(props.node)"
                           :textColour="props.hover ? 'white' : 'black'" :fillColour="props.hover ? 'black' : 'white'">
        </CSPConstraintNode>
      </template>
      <template slot="edge" scope="props">
        <UndirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2"
                        :stroke="stroke(props.edge)"
                        :stroke-width="strokeWidth(props.edge, props.hover)"></UndirectedEdge>
      </template>
    </GraphVisualizerBase>
    <div id="footer">
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button id="auto-step" class="btn btn-default" @click="$emit('click:auto-step')">Auto Step</button>
      </div>
      <div id="output">{{output}}</div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
import CSPConstraintNode from "./CSPConstraintNode.vue";
import CSPVariableNode from "./CSPVariableNode.vue";
import UndirectedEdge from "../../components/UndirectedEdge.vue";

import { Graph, ICSPGraphNode, IGraphEdge } from "../../Graph";

/**
 * Used to draw a CSP graph that can show the visualization of code.
 */
@Component({
  components: {
    GraphVisualizerBase,
    CSPConstraintNode,
    CSPVariableNode,
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
}
</script>

<style scoped>
  text.domain {
    font-size: 12px;
  }
</style>
