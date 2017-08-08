<template>
  <div class="graph-container">
    <svg tabindex="0" ref="mySVG" :width="width" :height="height"
         @mousemove="drag"
         @mouseleave="dragEnd"
         @keydown.delete="$emit('delete')"
         @dblclick="onDblClick">
      <EdgeContainer v-for="edge in graph.edges" :key="edge.id"
                     :transitions="transitionsAllowed && transitions"
                     @mouseover="edgeMouseOver(edge)"
                     @mouseout="edgeMouseOut(edge)"
                     @click="$emit('click:edge', edge)">
        <slot name="edge" :edge="edge"
              :x1="edge.source.x" :y1="edge.source.y"
              :x2="edge.target.x" :y2="edge.target.y"
              :hover="edge === edgeHover"></slot>
      </EdgeContainer>
      <GraphNodeContainer v-for="node in nodes" :key="node.id"
                 :x="node.x" :y="node.y"
                 :transitions="transitionsAllowed && transitions"                 
                 @click="$emit('click:node', node)"
                 @dragstart="dragStart(node, $event)" @dragend="dragEnd"
                 @mouseover="nodeMouseOver(node)" @mouseout="nodeMouseOut(node)"
                 @canTransition="toggleTransition">
        <slot name="node" :node="node" :hover="node === nodeHover"></slot>
      </GraphNodeContainer>
    </svg>
  </div>
</template>

<script lang="ts">
import { debounce } from "underscore";
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

import GraphNodeContainer from "./GraphNodeContainer.vue";
import EdgeContainer from "./EdgeContainer.vue";

import {Graph, IGraphNode, IGraphEdge} from '../Graph';
import { GraphLayout } from '../GraphLayout';

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
  /** If true, animates positional changes and other properties of the nodes/edges in this graph. */
  @Prop({default: false})
  transitions: boolean;
  /** Layout object that controls where nodes are drawn. */
  @Prop({type: Object})
  layout: GraphLayout;

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
  /** True if transitions are allowed. Disable e.g. when nodes are dragged and you don't want transitions. */
  transitionsAllowed = true;
  /** The width of the SVG. Automatically set to width of container. */
  width = 0;
  /** The height of the SVG. Automatically set to height of container. */  
  height = 0;

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

  created() {
    this.graph = this.graph;
    this.handleResize = debounce(this.handleResize, 300);
  }

  mounted() {
    this.width = this.$el.getBoundingClientRect().width;
    this.height = this.width / 1.6;
    this.layout.setup(this.graph, { width: this.width, height: this.height });
    
    // Disable animations for the first draw, because otherwise they fly in from (0, 0) and it looks weird
    this.transitionsAllowed = false;
    Vue.nextTick(() => this.transitionsAllowed = true);

    window.addEventListener('resize', this.handleResize);
  }

  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  }

  /** Re-layout the graph using the current width/height of the SVG. */
  handleResize() {
    this.width = this.$el.getBoundingClientRect().width;
    this.height = this.width / 1.6;
    this.layout.relayout(this.graph, { width: this.width, height: this.height });
  }

  get nodes() {
    if (this.dragTarget != null) {
      // Move the node being dragged to the top, so it appears over everything else
      const i = this.graph.nodes.indexOf(this.dragTarget as IGraphNode);
      if (i !== -1) {
        // Move element at index i to the back of the array
        this.graph.nodes.push(this.graph.nodes.splice(i, 1)[0]);
      }
    }

    return this.graph.nodes;
  }

  dragStart(node: IGraphNode) {
    this.dragTarget = node;
  }

  drag(e: MouseEvent) {
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
    this.transitionsAllowed = true;
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

  /**
   * Toggles transitions on and off.
   * 
   * For example, when nodes are being dragged,
   * we want to disable transitions on nodes and edges so their positions don't lag the mouse.
   */
  toggleTransition(allowed: boolean) {
    this.transitionsAllowed = allowed;
  }

  @Watch('graph')
  onGraphChanged(newVal) {
    this.layout.relayout(this.graph, { width: this.width, height: this.height });
  }
}
</script>

<style scoped>
  .graph-container {
    overflow: hidden;
  }

  svg:focus {
    outline: none;
  }
</style>
