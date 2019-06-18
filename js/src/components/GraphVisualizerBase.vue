<template xmlns:html="http://www.w3.org/1999/xhtml">
  <div class="graph-container">
    <svg tabindex="0" ref="svg" :width="width" :height="height"
         @mousemove="dragNode"
         @mouseleave="dragNodeEnd"
         @keydown.delete="$emit('delete')"
         @dblclick="onDblClick">
      <EdgeContainer v-for="edge in graph.edges" :key="edge.id"
                     :transitions="transitionsAllowed && transitions"
                     @mouseover="edgeMouseOver(edge)"
                     @mouseout="edgeMouseOut(edge)"
                     @click="$emit('click:edge', edge)">
        <slot name="edge" :edge="edge" :hover="edge === edgeHovered"></slot>
      </EdgeContainer>
      <GraphNodeContainer v-for="node in nodes" :key="node.id"
                          :x="node.x" :y="node.y"
                          :transitions="transitionsAllowed && transitions"
                          @click="$emit('click:node', node)"
                          @dragstart="dragNodeStart(node, $event)" @dragend="dragNodeEnd"
                          @mouseover="nodeMouseOver(node)" @mouseout="nodeMouseOut(node)"
                          @canTransition="toggleTransition">
        <slot name="node" :node="node" :hover="node === nodeHovered"></slot>
      </GraphNodeContainer>
      <foreignObject class="dropdown noselect" :x="btnProp(width).x" :y="btnProp().y" width="112px">
        <button class="dropbtn">Visualization Options</button>
        <div class="dropdown-content">
          <slot name="visualization" :toggleLegend="toggleLegendVisibility"></slot>
        </div>
      </foreignObject>
    </svg>
    <!-- Resize handle -->
    <div class="handle" ref="handle"></div>
  </div>
</template>

<script lang="ts">
  import * as d3 from "d3";
  import { debounce } from "underscore";
  import Vue, { ComponentOptions } from "vue";
  import Component from "vue-class-component";
  import { Prop, Watch } from "vue-property-decorator";

  import GraphNodeContainer from "./GraphNodeContainer.vue";
  import EdgeContainer from "./EdgeContainer.vue";

  import { Graph, IGraphNode, IGraphEdge } from "../Graph";
  import { GraphLayout } from "../GraphLayout";

  /**
   * Base class for all graph visualizers.
   *
   * This component handles rendering nodes and edges, handling drag and hover behaviours,
   * and propagating some events up to the parent. It provides slots to customize
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
   *
   * Events Emitted:
   * - 'dblclick': The user has double-clicked on the graph. Arguments passed: x, y, MouseEvent
   * - 'delete': The user has pressed 'Delete' or 'Backspace' while the graph is focused.
   * - 'click:node': A node has been clicked. Passes the node as the first argument.
   * - 'click:edge': An edge has been clicked. Passes the edge as the first argument.
   */
  @Component({
    components: {
      GraphNodeContainer,
      EdgeContainer
    }
  })
  export default class GraphVisualizeBase extends Vue {
    /** The graph to render. */
    @Prop({ type: Object })
    graph: Graph;
    /** If true, animates positional changes and other properties of the nodes/edges in this graph. */
    @Prop({ default: false })
    transitions: boolean;
    /** Layout object that controls where nodes are drawn. */
    @Prop({ type: Object })
    layout: GraphLayout;
    @Prop() legendText: string[];
    @Prop() legendColor: string[];

    /** The node or edge currently being dragged. */
    dragTarget: IGraphNode | IGraphEdge | null = null;
    /** The edge being hovered over. */
    edgeHovered: IGraphEdge | null = null;
    /** The node being hovered over. */
    nodeHovered: IGraphNode | null = null;
    /** Tracks the pageX of the previous MouseEvent. Used to compute the delta mouse position. */
    prevPageX = 0;
    /** Tracks the pageY of the previous MouseEvent. Used to compute the delta mouse position. */
    prevPageY: number | null = 0;
    /** True if transitions are allowed. Disable e.g. when nodes are dragged and you don't want transitions. */
    transitionsAllowed = true;
    /** The width of the SVG. Automatically set to width of container. */
    width = 0;
    /** The height of the SVG. Automatically set to height of container. */

    height = 0;

    $refs: {
      /** The SVG element that the graph is drawn in. */
      svg: SVGSVGElement;
      /** The div element representing a resize handle. */
      handle: HTMLDivElement;
    };

    created() {
      this.graph = this.graph;
      this.handleResize = debounce(this.handleResize, 300);
    }

    mounted() {
      this.width = this.$el.getBoundingClientRect().width;
      this.height = this.width / 1.8;
      this.layout.setup(this.graph, { width: this.width, height: this.height });

      // Disable animations for the first draw, because otherwise they fly in from (0, 0) and it looks weird
      this.transitionsAllowed = false;
      Vue.nextTick(() => (this.transitionsAllowed = true));

      window.addEventListener("resize", this.handleResize);

      // Custom resize handling. In the future, we could switch to using CSS resize.
      // However, it is not support in IE/Edge right now, and Safari does not emit any resize events,
      // even with a ResizeObserver polyfill.
      let initialiseResize = (e: Event) => {
        e.preventDefault();
        window.addEventListener("mousemove", startResizing, false);
        window.addEventListener("mouseup", stopResizing, false);
      };

      this.$refs.handle.addEventListener("mousedown", initialiseResize, false);

      let startResizing = (e: MouseEvent) => {
        e.preventDefault();

        // Everything below can be replaced with:
        // this.width.x += e.movementX;
        // this.height.y += e.movementY;
        // if we don't want to support IE11.
        this.height += this.prevPageY ? e.pageY - this.prevPageY : 0;
        this.prevPageY = e.pageY;
        this.handleResize();
      };

      let stopResizing = (e: MouseEvent) => {
        window.removeEventListener("mousemove", startResizing, false);
        window.removeEventListener("mouseup", stopResizing, false);
        this.prevPageY = null;
      };

      this.addLegend();
    }

    beforeDestroy() {
      window.removeEventListener("resize", this.handleResize);
    }

    /** Re-layout the graph using the current width/height of the SVG. */
    handleResize() {
      this.width = this.$el.getBoundingClientRect().width;
      this.layout.relayout(this.graph, {
        width: this.width,
        height: this.height
      });
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

    dragNodeStart(node: IGraphNode) {
      this.dragTarget = node;
    }

    dragNode(e: MouseEvent) {
      if (this.dragTarget) {
        const svgBounds = this.$refs.svg.getBoundingClientRect();

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

    dragNodeEnd() {
      this.dragTarget = null;
      this.transitionsAllowed = true;
      this.prevPageX = 0;
      this.prevPageY = 0;
    }

    edgeMouseOver(edge: IGraphEdge) {
      this.edgeHovered = edge;
    }

    edgeMouseOut(edge: IGraphEdge) {
      this.edgeHovered = null;
    }

    nodeMouseOver(node: IGraphNode) {
      this.nodeHovered = node;
      this.moveToFront(node);
    }

    nodeMouseOut(node: IGraphNode) {
      this.nodeHovered = null;
    }

    /**
     * Handles the user double-clicking on the graph.
     * The x and y position within the SVG are calculated and passed to the event.
     */
    onDblClick(e: MouseEvent) {
      var svgBounds = this.$refs.svg.getBoundingClientRect();
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

    moveToFront(node: IGraphNode) {
      const svg = this.$refs.svg;
      const nodeElem = svg.getElementById(node.id).parentElement;
      svg.appendChild(nodeElem!);
    }

    // Taken and modified based on
    // http://www.competa.com/blog/d3-js-part-7-of-9-adding-a-legend-to-explain-the-data/
    /** Adds legend box to the graph */
    addLegend() {
      let legendRectSize = 10;
      let legendSpacing = 3;
      let position = {
        // x and y of the first element in the legend
        x: 10,
        y: 20
      };

      let color = d3.scaleOrdinal<string>()
        .domain(this.legendText)
        .range(this.legendColor);

      let legend = d3.select(this.$refs.svg)
        .append("g").attr("class", "legend_group")
        .selectAll("g")
        .data(color.domain())
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, i) {
          let x = position.x;
          let y = (i + 1) * position.y;
          return 'translate(' + x + ',' + y + ')';
        });
      legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', color)
        .style('stroke', color);

      legend.append('text')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .text(function(d) { return d; });
    }

    /** Toggle button functionality for displaying and hiding legend box */
    toggleLegendVisibility() {
      let lg = d3.select(this.$refs.svg).select(".legend_group");

      if (lg.style("visibility") === "hidden") {
        lg.attr("visibility", "visible");
      } else {
        lg.attr("visibility", "hidden");
      }
    }

    /** Aggregate visualization option's buttons properties here */
    btnProp(canvasWidth: number) {
      return {
        // first btn's and y position
        // which can only be accessed in the template
        x: canvasWidth - 108,
        y: 0,
        // other btn's offset position from the previous one
        xOffset: 0,
        yOffset: 40,
        width: "100%"
      }
    }

    @Watch("graph")
    onGraphChanged(newVal: Graph) {
      // Whenever nodes or edges are added, re-layout the graph
      this.layout.relayout(this.graph, {
        width: this.width,
        height: this.height
      });
    }
  }

</script>

<style scoped>
  .graph-container {
    border: 1px solid gray;
    overflow: hidden;
    position: relative;
    margin-bottom: 10px;
  }

  svg {
    display: block;
  }

  svg:focus {
    outline: none;
  }

  .handle {
    background-color: #727272;
    width: 10px;
    height: 10px;
    cursor: ns-resize;
    position: absolute;
    right: 0;
    bottom: 0;
  }

  .dropbtn {
    background-color: #4CAF50;
    color: white;
    padding: 1em;
    font-size: 0.7em;
    border: none;
  }

  .dropdown {
    position: relative;
    display: inline-block;
  }

  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #f1f1f1;
    min-width: 8em;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    z-index: 1;
  }

  .dropdown:hover .dropdown-content {display: block;}

  .dropdown:hover .dropbtn {background-color: #3e8e41;}

  .noselect {
    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
    -khtml-user-select: none; /* Konqueror HTML */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
  }

  .dropdown-content a {
    color: black;
    padding: 1em 1em;
    font-size: 0.75em;
    text-decoration: none;
    display: block;
    border-bottom: 1px solid rgba(0, 0, 255, .1);
  }

  .dropdown-content a:hover {background-color: #ddd;}

  .dropdown-content a.inline-btn-group {
    color: white;
    font-size: 0.75em;
    text-decoration: none;
    display: inline-block;
    border-bottom: 1px solid rgba(0, 0, 255, .1);
    background-color: darkgrey;
    width: 10%;
  }

  .dropdown-content label.inline-btn-group {
    color: black;
    padding: 1em 0.5em;
    text-align: center;
    width: 55%;
    font-size: 0.75em;
    text-decoration: none;
    display: inline-block;
    border-bottom: 1px solid rgba(0, 0, 255, .1);
  }
</style>
