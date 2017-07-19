<template>
  <div>
    <svg tabindex="0" ref="mySVG" :width="width" :height="height"
         @mousemove="dragSVG"
         @mouseleave="dragEnd"
         @keydown.delete="$emit('delete')"
         @dblclick="onDblClick">
      <EdgeContainer v-for="edge in graph.edges" :key="edge.id"
                     @mouseover="edgeMouseOver(edge)"
                     @mouseout="edgeMouseOut(edge)"
                     @click="$emit('click:edge', edge)">
        <slot name="edge" :edge="edge"
              :x1="edge.source.x" :y1="edge.source.y"
              :x2="edge.target.x" :y2="edge.target.y"
              :hover="edge === edgeHover"></slot>
      </EdgeContainer>
      <GraphNodeContainer v-for="node in nodes" :key="node.id"
                 @click="$emit('click:node', node)"
                 @dragstart="dragStart(node, $event)" @dragend="dragEnd"
                 @mouseover="nodeMouseOver(node)" @mouseout="nodeMouseOut(node)"
                 :x="node.x" :y="node.y">
        <slot name="node" :node="node" :hover="node === nodeHover"></slot>
      </GraphNodeContainer>
    </svg>
  </div>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

import GraphNodeContainer from "./GraphNodeContainer.vue";
import EdgeContainer from "./EdgeContainer.vue";

import {Graph, IGraphNode, IGraphEdge} from '../Graph';

/**
 * Base class for all graph visualizers.
 *
 * This component handles rendering nodes and edges, handling drag and hover behaviours,
 * and propogating some events up to the parent. It provides slots to customize
 * how nodes and edges are displayed.
 * 
 * For nodes in the slot with name "node", it passes the following down as props:
 * {
 *   node: IGraphNode, // The node being rendered
 *   hover: boolean // True if the node is being hovered over
 * }
 * 
 * For edges in the slot with name "edge", it passes the following down as props:
 * {
 *   edge: IGraphEdge, // The edge being rendered,
 *   hover: boolean, // True if the edge is being hovered over
 *   x1, y1, x2, y2: number // The center coordinates of the source and target of the edge
 * }
 */
@Component({
  components: {
    GraphNodeContainer,
    EdgeContainer,
  }
})
export default class GraphVisualizeBase extends Vue {
  /** The graph to render. */
  @Prop({type: Object}) graph: Graph;
  /** The width of the graph, in pixels */
  @Prop({default: 600}) width: number;
  /** The height of the graph, in pixels. */
  @Prop({default: 480}) height: number;

  /** The node or edge currently being dragged. */
  dragTarget: IGraphNode|IGraphEdge|null = null;
  /** The edge being hovered over. */
  edgeHover: IGraphEdge|null = null;
  /** The node being hovered over. */
  nodeHover: IGraphNode|null = null;
  /** Tracks the pageX of the previous MouseEvent. Used to compute the delta mouse position. */
  prevPageX = 0;
  /** Tracks the pageY of the previous MouseEvent. Used to compute the delta mouse position. */
  prevPageY = 0;

  $refs: {
    /** The SVG element that the graph is drawn in. */
    mySVG: SVGElement;
  }

  /** Emitted Events */
  /**
   * 'dblclick': The user has double-clicked on the graph. Arguments passed: x, y, MouseEvent
   * 'delete': The user has pressed 'Delete' or 'Backspace' while the graph is focused.
   * 'click:node': A node has been clicked. Passes the node as the first argument.
   * 'click:edge': An edge has been clicked. Passes the edge as the first argument.
   */

    get nodes() {
      let i = this.graph.nodes.indexOf(this.dragTarget as IGraphNode);
      if (i !== -1) {
        // Move element at index i to the back of the array
        this.graph.nodes.push(this.graph.nodes.splice(i, 1)[0]);
      }

      return this.graph.nodes;
    }

    dragStart(node: IGraphNode) {
      this.dragTarget = node;
    }

    dragSVG(e: MouseEvent) {
      if (this.dragTarget) {
        var svgBounds = this.$refs.mySVG.getBoundingClientRect();

        // Everything below can be replaced with:
        // this.dragTarget.x += e.movementX;
        // this.dragTarget.y += e.movementY;
        // if we don't want to support IE11.
        this.dragTarget.x += this.prevPageX ? e.pageX - this.prevPageX : 0;
        this.dragTarget.y += this.prevPageY ? e.pageY - this.prevPageY : 0;

        this.prevPageX = e.pageX;
        this.prevPageY = e.pageY;
      }
    }

    dragEnd() {
      this.dragTarget = null;
      this.prevPageX = 0;
      this.prevPageY = 0;
    }

    edgeMouseOver(edge: IGraphEdge) {
      this.edgeHover = edge;
    }

    edgeMouseOut(edge: IGraphEdge) {
      this.edgeHover = null;
    }

    nodeMouseOver(node: IGraphNode) {
      this.nodeHover = node;
    }

    nodeMouseOut(node: IGraphNode) {
      this.nodeHover = null;
    }

    /**
     * Handles the user double-clicking on the graph.
     * The x and y position within the SVG are calculated and passed to the event.
     */
    onDblClick(e: MouseEvent) {
      var svgBounds = this.$refs.mySVG.getBoundingClientRect();
      var x = e.pageX - svgBounds.left;
      var y = e.pageY - svgBounds.top;
      this.$emit("dblclick", x, y, e);
    }
  }
</script>

<style scoped>
  svg:focus {
    outline: none;
  }
</style>
