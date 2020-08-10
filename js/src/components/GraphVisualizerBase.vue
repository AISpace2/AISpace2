<template xmlns:html="http://www.w3.org/1999/xhtml">
  <div class="graph-container">
    <svg ref="zoom" width="100%" :height="graphContainerHeight">
      <rect width="100%" height="100%" fill="aliceblue" />
      <g :transform="`scale(${scaleFactor}) translate(${translateX},${translateY})`">
        <svg tabindex="0" ref="svg" :width="width" :height="height"
            @mousemove="dragNode"
            @mouseleave="dragNodeEnd"
            @keydown.delete="$emit('delete')"
            @dblclick="onDblClick">
          <rect width="100%" height="100%" fill="white" />          
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
        </svg>
      </g>
    </svg>
    <foreignObject class="dropdown noselect">
      <button class="dropbtn" >Visualization Options</button>
      <div class="dropdown-content">
        <!-- Legend toggle -->
        <a v-if="haveLegend" @click="toggleLegendVisibility">{{'Legend: ' + showLegend}}</a>

        <!-- Zoom handle -->
        <a class="inline-btn-group" @click="zoomModeMinus">&#8249;</a>
        <label class="inline-btn-group">{{'Zoom Mode: ' + zoomMode}}</label>
        <a class="inline-btn-group" @click="zoomModePlus">&#8250;</a>

        <a @click="toggleWheelZoom">{{'Wheel Zoom: ' + wheelZoom}}</a>

        <a class="inline-btn-group" @click="zoomOut">-</a>
        <label class="inline-btn-group">Zoom In/Out</label>
        <a class="inline-btn-group" @click="zoomIn">+</a>

        <a @click="resetZoom">Zoom to Fit</a>
        <!-- Zoom handle end -->

        <slot name="visualization" :toggleLegend="toggleLegendVisibility" :showLegend="showLegend"></slot>
      </div>
    </foreignObject>
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
    @Prop() textSize: number;

    /** The node or edge currently being dragged. */
    dragTarget: IGraphNode | IGraphEdge | null = null;
    rawXSlope: number
    rawXIntercept: number
    rawYSlope: number
    rawYIntercept: number
    /** The edge being hovered over. */
    edgeHovered: IGraphEdge | null = null;
    /** The node being hovered over. */
    nodeHovered: IGraphNode | null = null;
    /** Tracks the pageX of the previous MouseEvent. Used to compute the delta mouse position. */
    prevPageX: number | null = 0;
    /** Tracks the pageY of the previous MouseEvent. Used to compute the delta mouse position. */
    prevPageY: number | null = 0;
    /** True if transitions are allowed. Disable e.g. when nodes are dragged and you don't want transitions. */
    transitionsAllowed: boolean  = false;
    /** The width of the SVG, which is affected by transform. */
    width = 0;
    /** The height of the SVG, which is affected by transform. */
    height = 0;
    /** The height of the zoom SVG. Automatically set to height of container. */
    graphContainerHeight = 0;

    /** The scale of the SVG.*/
    scaleFactor = 1;
    translateX = 0;
    translateY = 0;
    zoomMove: boolean = false;
    zoomStartX: number | null = 0;
    zoomStartY: number | null = 0;
    
    /**  Visualization Options. */
    haveLegend: boolean = false;
    showLegend: "on" | "off" = "on";
    zoomMode: number = 1;
    wheelZoom:  "on" | "off" = "off";

    $refs: {
      /** The SVG element that the graph is drawn in. */
      svg: SVGSVGElement;
      /** The div element representing a resize handle. */
      handle: HTMLDivElement;
      /** The SVG element for zooming. */
      zoom: SVGSVGElement;
    };

    created() {
      this.graph = this.graph;
      this.handleResize = debounce(this.handleResize, 300);
    }

    mounted() {
      this.width = this.$el.getBoundingClientRect().width;
      this.graphContainerHeight = this.width / 1.8;
      this.height = this.graphContainerHeight;
      this.layout.setup(this.graph, { width: this.width, height: this.height });

      // Disable animations for the first draw, because otherwise they fly in from (0, 0) and it looks weird
      // this.transitionsAllowed = false;
      // Vue.nextTick(() => (this.transitionsAllowed = true));

      window.addEventListener("resize", this.updateHeight);

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
        this.graphContainerHeight += this.prevPageY ? e.pageY - this.prevPageY : 0;
        this.prevPageY = e.pageY;
        this.updateHeight();
      };

      let stopResizing = (e: MouseEvent) => {
        window.removeEventListener("mousemove", startResizing, false);
        window.removeEventListener("mouseup", stopResizing, false);
        this.prevPageY = null;
      };

      this.$refs.svg.addEventListener("wheel", e => {
        if(this.wheelZoom === "off"){
          return;
        }
        if(this.zoomMode === 1){
          e.preventDefault();

          var zoomRect = this.$refs.zoom.getBoundingClientRect()
          var updateScaleFactor = Math.pow((1/0.95), -e.deltaY / 120)
          this.scaleFactor = this.scaleFactor * updateScaleFactor

          var transX = ((zoomRect.width*(1-updateScaleFactor))/zoomRect.width * (e.clientX - zoomRect.left))/this.scaleFactor
          this.layout.translation(this.graph, transX, 0);
          this.width = this.width / updateScaleFactor

          var transY = ((zoomRect.height*(1-updateScaleFactor))/zoomRect.height * (e.clientY - zoomRect.top))/this.scaleFactor
          this.layout.translation(this.graph, 0, transY);
          this.height = this.height / updateScaleFactor

          return;
        }else if(this.zoomMode === 2){
          e.preventDefault();

          var zoomRect = this.$refs.zoom.getBoundingClientRect()
          var updateScaleFactor = Math.pow((1/0.95), -e.deltaY / 120)
          this.graph.nodes.forEach(node => {
            var nodeRect = document.getElementById(node.id).getBoundingClientRect()
            node.x += ((e.clientX - (nodeRect.left + nodeRect.width / 2)) * (1-updateScaleFactor)) * this.scaleFactor
            node.y += ((e.clientY - (nodeRect.top + nodeRect.height / 2)) * (1-updateScaleFactor)) * this.scaleFactor
          });

          return;
        }
      });

      this.$refs.svg.addEventListener("mousedown", e => {
        this.zoomMove = true
        this.zoomStartX = e.pageX;
        this.zoomStartY = e.pageY;
        return;        
      });

      this.$refs.svg.addEventListener("mousemove", e => {
        if(this.zoomMove && !this.dragTarget){
          this.layout.translation(this.graph, (e.pageX - this.zoomStartX)/this.scaleFactor, (e.pageY - this.zoomStartY)/this.scaleFactor);

          this.zoomStartX = e.pageX;
          this.zoomStartY = e.pageY;
        }
        
      });

      this.$refs.svg.addEventListener("mouseup", e => {
        this.zoomMove = false;
        return
      });

      this.$refs.svg.addEventListener("mouseleave", e => {
        this.zoomMove = false;
        return
      });

      if(this.legendText){
        this.haveLegend = true;
        this.addLegend();
      }

    }

    beforeDestroy() {
      window.removeEventListener("resize", this.updateHeight);
    }

    /** Update the height of the SVG. */
    updateHeight(){
      this.height = this.$refs.zoom.getBoundingClientRect().height / this.scaleFactor

    }

    /** Re-layout the graph using the current width/height of the SVG. */
    handleResize() {
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
      var tempNodes: IGraphNode[] = []

      for (let i = 0; i < this.graph.nodes.length; i++) {
        if(i == 0){
          tempNodes.push(this.graph.nodes[i])
        }else if(this.graph.nodes[i].x !== tempNodes[0].x && this.graph.nodes[i].y !== tempNodes[0].y){
          tempNodes.push(this.graph.nodes[i])
          break;
        }else if(i == this.graph.nodes.length - 1){
          tempNodes.push(this.graph.nodes[i])
        }
      }

      this.rawXSlope = (tempNodes[0].rawX-tempNodes[1].rawX)/(tempNodes[0].x-tempNodes[1].x)

      this.rawYSlope = (tempNodes[0].rawY-tempNodes[1].rawY)/(tempNodes[0].y-tempNodes[1].y)
      if(isNaN(this.rawXSlope && this.rawYSlope)){      
      this.rawXSlope = (tempNodes[0].rawX)/(tempNodes[0].x)
      this.rawYSlope = (tempNodes[0].rawY)/(tempNodes[0].y)
      }else if(isNaN(this.rawXSlope)){
        this.rawXSlope = this.rawYSlope
      }else if(isNaN(this.rawYSlope)){
        this.rawYSlope = this.rawXSlope
      }
      this.rawXIntercept = tempNodes[0].rawX - this.rawXSlope*tempNodes[0].x
      this.rawYIntercept = tempNodes[0].rawY - this.rawYSlope*tempNodes[0].y

    }

    dragNode(e: MouseEvent) {
      if (this.dragTarget) {
        const svgBounds = this.$refs.svg.getBoundingClientRect();

        // Everything below can be replaced with:
        // this.dragTarget.x += e.movementX;
        // this.dragTarget.y += e.movementY;
        // if we don't want to support IE11.
        this.dragTarget.x += this.prevPageX ? (e.pageX - this.prevPageX)/this.scaleFactor : 0;
        this.dragTarget.y += this.prevPageY ? (e.pageY - this.prevPageY)/this.scaleFactor : 0;

        this.prevPageX = e.pageX;
        this.prevPageY = e.pageY;
      }
    }

    dragNodeEnd() {
      this.dragTarget.rawX = this.dragTarget.x * this.rawXSlope + this.rawXIntercept
      this.dragTarget.rawY = this.dragTarget.y * this.rawYSlope + this.rawYIntercept
      this.dragTarget = null;
      // this.transitionsAllowed = true;
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
      var zoomBounds = this.$refs.zoom.getBoundingClientRect();
      var x = (e.pageX - zoomBounds.left)/this.scaleFactor;
      var y = (e.pageY - zoomBounds.top)/this.scaleFactor;
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
      let legendRectSize = 10 * this.textSize / 15;
      let legendSpacing = 3 * this.textSize / 15;
      let position = {
        // x and y of the first element in the legend
        x: 10,
        y: 20
      };

      let color = d3.scaleOrdinal<string>()
        .domain(this.legendText)
        .range(this.legendColor);

      let legend = d3.select(this.$refs.zoom)
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
        .attr('font-size', this.textSize)
        .text(function(d) { return d; });

      // make sure the legend is initally off
      this.toggleLegendVisibility();
    }

    /** Toggle button functionality for displaying and hiding legend box */
    toggleLegendVisibility() {
      let lg = d3.select(this.$refs.zoom).select(".legend_group");

      if (lg.style("visibility") === "hidden") {
        this.showLegend = "on"
        lg.attr("visibility", "visible");
      } else {
        this.showLegend = "off"
        lg.attr("visibility", "hidden");
      }
    }

    zoomModePlus(){
      if(this.zoomMode < 2){
        this.toggleZoomMode(1);
      }
    }

    zoomModeMinus(){
      if(this.zoomMode > 1){
        this.toggleZoomMode(-1);
      }
    }

    /** Toggle button functionality for zoom mode */
    toggleZoomMode(factor: number) {
      this.zoomMode += factor
    }

    toggleWheelZoom() {
      if(this.wheelZoom === "on"){
        this.wheelZoom = "off";
      }else{
        this.wheelZoom = "on";
      }
    }

    resetZoom(){
      this.scaleFactor = 1;
      this.translateX = 0;
      this.translateY = 0;
      this.width = this.$refs.zoom.getBoundingClientRect().width;
      this.height = this.$refs.zoom.getBoundingClientRect().height;
      this.layout.relayout(this.graph, { width: this.width, height: this.height });
    }

    zoomIn(){
      this.zoomClicked(1);
    }

    zoomOut(){
      this.zoomClicked(-1);
    }

    zoomClicked(factor: number){
      if(this.zoomMode === 1){
        var zoomRect = this.$refs.zoom.getBoundingClientRect()
        var updateScaleFactor = Math.pow((1/0.95), factor)
        this.scaleFactor = this.scaleFactor * updateScaleFactor

        var transX = ((zoomRect.width*(1-updateScaleFactor))/2)/this.scaleFactor
        this.layout.translation(this.graph, transX, 0);
        this.width = this.width / updateScaleFactor

        var transY = ((zoomRect.height*(1-updateScaleFactor))/2)/this.scaleFactor
        this.layout.translation(this.graph, 0, transY);
        this.height = this.height / updateScaleFactor
      }else if(this.zoomMode === 2){
        var zoomRect = this.$refs.zoom.getBoundingClientRect()
        var updateScaleFactor = Math.pow((1/0.95), factor)
        this.graph.nodes.forEach(node => {
          var nodeRect = document.getElementById(node.id).getBoundingClientRect()
          node.x += ((zoomRect.left + zoomRect.width / 2 - (nodeRect.left + nodeRect.width / 2)) * (1-updateScaleFactor)) * this.scaleFactor
          node.y += ((zoomRect.left + zoomRect.width / 2 - (nodeRect.top + nodeRect.height / 2)) * (1-updateScaleFactor)) * this.scaleFactor
        });
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
    onGraphChanged(newVal: Graph, oldVal: Graph) {
      // Whenever nodes or edges are added, re-layout the graph
      if (oldVal.should_relayout) {
          this.layout.relayout(this.graph, {
              width: this.width,
              height: this.height
          });
      }
    }

    @Watch("textSize")
    onTextSizeChanged(newVal: number) {
      let legendRectSize = 10 * newVal / 15;
      let legendSpacing = 3 * newVal / 15;
      let legend = d3.selectAll(".legend");

      legend.select('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)

      legend.select('text')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .attr('font-size', newVal)
        .text(function(d) { return d; });
    }

  }

</script>

<style scoped>
  .graph-container {
    border: 1px solid gray;
    overflow: hidden;
    position: relative;
    margin-bottom: 10px;
    -webkit-user-select: none;
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
    padding: 0.5em 2em;
    font-size: 0.75em;
    border: none;
  }

  .dropdown {
    position: absolute;
    right: 0;
    top: 0;
    display: inline-block;
  }

  .dropdown-content {
    display: none;
    /* position: absolute; */
    background-color: #f1f1f1;
    max-width: 10em;
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
    padding: 0.5em 0em;
    font-size: 0.75em;
    text-decoration: none;
    text-align: center;
    display: block;
    border-bottom: 1px solid rgba(0, 0, 255, .1);
    width: 100%
  }

  .dropdown-content a:hover {background-color: #ddd;}

  .dropdown-content a.inline-btn-group {
    color: white;
    font-size: 0.75em;
    text-decoration: none;
    text-align: center;
    display: inline-block;
    border-bottom: 1px solid rgba(0, 0, 255, .1);
    background-color: darkgrey;
    width: 17%;
  }

  .dropdown-content label.inline-btn-group {
    color: black;
    padding: 0.5em 0em;
    text-align: center;
    width: 60%;
    font-size: 0.75em;
    text-decoration: none;
    display: inline-block;
    border-bottom: 1px solid rgba(0, 0, 255, .1);
  }
</style>
