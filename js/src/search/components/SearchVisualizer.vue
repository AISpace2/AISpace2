<template>
  <div class="search_visualizer">
    <GraphVisualizerBase :graph="graph" :transitions="true" :layout="layout" :legendColor="legendColor" :legendText="legendText" :textSize="textSize">
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode :id="props.node.id" :text="props.node.name" :textColour="nodeTextColour(props.node, props.hover)"
                                   :subtext="nodeHText(props.node)" :detailLevel="detailLevel"
                                   :fill="nodeFillColour(props.node, props.hover)" :hover="props.hover"
                                   :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)"
                                   :maxWidth="nodemaxWidth(props.node)"
                                   @updateBounds="updateNodeBounds(props.node, $event)" :textSize="textSize">
        </RoundedRectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <DirectedRectEdge :id="props.edge.id" :x1="updateOverlappedEdege(props.edge).styles.x1" :x2="updateOverlappedEdege(props.edge).styles.x2" :y1="updateOverlappedEdege(props.edge).styles.y1" :y2="updateOverlappedEdege(props.edge).styles.y2" :stroke="props.edge.styles.stroke"
                          :strokeWidth="lineWidth" :text="edgeText(props.edge)" :nodeName="props.edge.target.name"
                          :graph_node_width="props.edge.styles.targetWidth" :graph_node_height="props.edge.styles.targetHeight">
        </DirectedRectEdge>
      </template>
      <template slot="visualization" slot-scope="props">
        <!-- <a @click="$emit('toggle:showFullDomain')">Change Domain</a> -->

        <a class="inline-btn-group" @click="sleepTimeUpdate(-0.1)">-</a>
        <label class="inline-btn-group">{{'Sleep Time: ' + sleepTime}}</label>
        <a class="inline-btn-group" @click="sleepTimeUpdate(0.1)">+</a>
        
        <a class="inline-btn-group" @click="detailLevel = detailLevel > 0 ? detailLevel - 1 : detailLevel">-</a>
        <label class="inline-btn-group">{{'Detail Level: ' + detailLevel}}</label>
        <a class="inline-btn-group" @click="detailLevel = detailLevel < 2 ? detailLevel + 1 : detailLevel">+</a>

        <a class="inline-btn-group" @click="textSize = textSize > 1 ? textSize - 1 : textSize">-</a>
        <label class="inline-btn-group">{{'Text Size: ' + textSize}}</label>
        <a class="inline-btn-group" @click="textSize = textSize + 1">+</a>

        <a class="inline-btn-group" @click="lineWidth = lineWidth > 1 ? lineWidth - 1 : lineWidth">-</a>
        <label class="inline-btn-group">{{'Line Width: ' + lineWidth}}</label>
        <a class="inline-btn-group" @click="lineWidth = lineWidth + 1">+</a>

        <a @click="showEdgeCosts = showEdgeCosts ? false : true">{{'Show Edge Costs: ' + showEdgeCosts}}</a>
        <a @click="showNodeHeuristics = showNodeHeuristics ? false : true">{{'Show Node Heuristics: ' + showNodeHeuristics}}</a>

      </template>
    </GraphVisualizerBase>
    <div class="footer">
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button id="auto-solve" class="btn btn-default" @click="$emit('click:auto-solve')">Auto Solve</button>
        <button id="pause" class="btn btn-default" @click="$emit('click:pause')">Pause</button>
        <button id="print-positions" class="btn btn-default" @click="$emit('click:print-positions')">Print Positions</button>
        <button id="reset" class="btn btn-default" @click="$emit('reset')">Reset</button>
      </div>
      <div class="output" style="white-space: pre-wrap">Frontier: {{frontier}}</div>
      <div v-if="output" class="output">
          <div v-for="sub in output.split('\n')" :key ="sub">
              <span v-bind:class="chooseClass(sub)" style="white-space: pre-wrap">{{sub}}</span>
          </div>
      </div>
      <div v-if="preSolution" class="output">
          <span>Solution history:</span>
          <div v-for="subSol in preSolution.split('\n')" :key ="subSol">
              <span class="solutionText">{{subSol}}</span>
          </div>
      </div>
      <div class="output">{{positions}}</div>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
  import { Prop, Watch } from "vue-property-decorator";
  import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
  import DirectedRectEdge from "../../components/DirectedRectEdge.vue";
  import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode.vue";
  import { Graph, ISearchGraphNode, ISearchGraphEdge } from "../../Graph";
  import { GraphLayout } from "../../GraphLayout";
  import { nodeFillColour, nodeHText } from "../SearchUtils";

  /**
   * A Search visualization that can be driven by backend code.
   *
   * Events Emitted:
   * - 'click:fine-step': The "fine step" button has been clicked.
   * - 'click:step': The "step" button has been clicked.
   * - 'click:auto-solve': The "auto solve" button has been clicked.
   */
  @Component({
    components: {
      GraphVisualizerBase,
      DirectedRectEdge,
      RoundedRectangleGraphNode,
    }
  })
  export default class SearchVisualizer extends Vue {
    // The graph being visualized
    graph: Graph<ISearchGraphNode, ISearchGraphEdge>;
    // The copy of initial graph used for resetting
    iniGraph: Graph<ISearchGraphNode, ISearchGraphEdge>;
    // Text describing what is currently happening
    output: string;
    // The text representing the frontier
    frontier: string;
    // The text representing the solutions found so far. Persistent until new solution found
    preSolution: string;
    // The text representing the positions for nodes
    positions: string;
    // True if edge costs should be shown on the edges
    showEdgeCosts: boolean;
    // True if node heuristics should be shown on the nodes
    showNodeHeuristics: boolean;
    // The width, in pixels, of the visualizer
    // width: number;
    // The width, in pixels, of the visualizer
    // height: number;
    // Layout object that controls where nodes are drawn
    layout: GraphLayout;
    // The size of the text inside the node
    textSize: number;
    // Display setting for text
    // 0 is hide all text
    // 1 is show truncated version
    // 2 is show all text
    detailLevel: number;
    legendText: string[];
    legendColor: string[];
    // The line width of the edges in the graph
    lineWidth: number;
    // The time delay between consecutive display calls
    sleepTime: number;

    sleepTimeUpdate(factor: number){
      if((this.sleepTime > 0.1 && factor < 0) || (this.sleepTime < 2 && factor > 0)){
        this.sleepTime += factor
        this.sleepTime = Math.round(this.sleepTime*10)/10
        this.$emit('toggle:sleepTimeUpdate', this.sleepTime)
        console.log(this.sleepTime)
      }
    }

    chooseClass(sub: string) {
      var solution: boolean = false;
      var warning: boolean = false;
      if (this.output) {
          solution = sub.includes("Solution found") || sub.includes("New best path");
          warning  = sub.includes("No more solutions");
      }
      return { 'solutionText': solution, 'warningText': warning };
    }

    nodeFillColour(node: ISearchGraphNode, hover: boolean) {
      if (hover) {
        return "black";
      }

      return nodeFillColour(node);
    }

    nodeTextColour(node: ISearchGraphNode, hover: boolean) {
      if (hover) {
        return "white";
      }

      return "black";
    }

    nodeStroke(node: ISearchGraphNode) {
      if (node.styles && node.styles.stroke) {
        return node.styles.stroke;
      }

      return "black";
    }

    nodeStrokeWidth(node: ISearchGraphNode) {
      if (node.styles && node.styles.strokeWidth) {
        return node.styles.strokeWidth;
      }

      return 1;
    }

    nodeHText(node: ISearchGraphNode) {
      if (!this.showNodeHeuristics) {
        return undefined;
      }

      return nodeHText(node);
    }

    edgeText(edge: ISearchGraphEdge) {
      let text = "";

      if (edge.name != null) {
        text = edge.name;
      }

      if (this.showEdgeCosts) {
        text += ` (${edge.cost})`;
      }

      return text;
    }

    nodemaxWidth(node: ISearchGraphNode) {
      if (!node.styles.radius) {
        return 100;
      }
      return node.styles.radius * 2;
    }

  /**
   * Whenever a node involved in two overlapped edges is moved, update the fake node position
   * to make sure the two overlapped edges are splitted and move with node.
   */
  updateOverlappedEdege(edge: ISearchGraphEdge) {
    if (edge.styles.overlapped === true) {
      const xa = edge.source.x;
      const ya = edge.source.y;
      const xb = edge.target.x;
      const yb = edge.target.y;
      const radius = 5;
      const cos: number =
        (yb! - ya!) /
        Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
      const sin: number =
        (xb! - xa!) /
        Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
      edge.styles.x1 = xa! - cos * radius;
      edge.styles.x2 = xb! - cos * radius;
      edge.styles.y1 = sin * radius + ya!;
      edge.styles.y2 = sin * radius + yb!;
    } else {
      edge.styles.x1 = edge.source.x;
      edge.styles.x2 = edge.target.x;
      edge.styles.y1 = edge.source.y;
      edge.styles.y2 = edge.target.y;
    }

    this.graph.edges.forEach(e1 => {
      this.graph.edges.forEach(e2 => {
        if (
          e1.source === e2.target &&
          e1.target === e2.source &&
          e1.styles.x1 === e2.styles.x2 &&
          e1.styles.x2 === e2.styles.x1
        ) {
          e1.styles.overlapped = true;
          e2.styles.overlapped = true;
          const xa = e1.source.x;
          const ya = e1.source.y;
          const xb = e1.target.x;
          const yb = e1.target.y;
          const radius = 5;
          const cos: number =
            (yb! - ya!) /
            Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
          const sin: number =
            (xb! - xa!) /
            Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
          // Move both of the two overlapped edge from the original position
          e2.styles.x1 = cos * radius + xb!;
          e2.styles.x2 = cos * radius + xa!;
          e2.styles.y1 = yb! - sin * radius;
          e2.styles.y2 = ya! - sin * radius;
          e1.styles.x1 = xa! - cos * radius;
          e1.styles.x2 = xb! - cos * radius;
          e1.styles.y1 = sin * radius + ya!;
          e1.styles.y2 = sin * radius + yb!;
        }
      });
    });

    if (edge.styles.overlapped === true) {
      const xa = edge.source.x;
      const ya = edge.source.y;
      const xb = edge.target.x;
      const yb = edge.target.y;
      const radius = 5;
      const cos: number =
        (yb! - ya!) /
        Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
      const sin: number =
        (xb! - xa!) /
        Math.sqrt(Math.pow(yb! - ya!, 2) + Math.pow(xb! - xa!, 2));
      edge.styles.x1 = xa! - cos * radius;
      edge.styles.x2 = xb! - cos * radius;
      edge.styles.y1 = sin * radius + ya!;
      edge.styles.y2 = sin * radius + yb!;
    } else {
      edge.styles.x1 = edge.source.x;
      edge.styles.x2 = edge.target.x;
      edge.styles.y1 = edge.source.y;
      edge.styles.y2 = edge.target.y;
    }

    return edge;
  }

  /**
   * Whenever a node reports it has resized, update it's style so that it redraws.
   */
  updateNodeBounds(node: ISearchGraphNode, bounds: { width: number; height: number }) {
    node.styles.width = bounds.width;
    node.styles.height = bounds.height;
    this.graph.edges
      .filter(edge => edge.target.id === node.id)
      .forEach(edge => {
        this.$set(edge.styles, "targetWidth", bounds.width);
        this.$set(edge.styles, "targetHeight", bounds.height);
      });
  }

  @Watch("lineWidth")
  onLineWidthChange(){
    this.graph.edges.forEach(edge => {
      this.$set(edge.styles, "strokeWidth", this.lineWidth);
    });
  }
}

</script>
