<template>
  <div class="search_visualizer">
    <GraphVisualizerBase :graph="graph" :transitions="true" :layout="layout" :legendColor="legendColor" :legendText="legendText">
      <template slot="node" scope="props">
        <RoundedRectangleGraphNode :id="props.node.id" hover="props.hover" :text="props.node.name" :textColour="nodeTextColour(props.node, props.hover)"
                                   :subtext="showNodeHeuristics ? nodeHText(props.node) : undefined" :detailLevel="detailLevel"
                                   :fill="nodeFillColour(props.node, props.hover)" :hover="props.hover"
                                   :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)"
                                   @updateBounds="updateNodeBounds(props.node, $event)" :textSize="textSize">
        </RoundedRectangleGraphNode>
      </template>
      <template slot="edge" scope="props">
        <DirectedRectEdge :id="props.edge.id" :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y" :stroke="props.edge.styles.stroke"
                          :strokeWidth="props.edge.styles.strokeWidth" :text="edgeText(props.edge)" :nodeName="props.edge.target.name"
                          :graph_node_width="props.edge.styles.targetWidth" :graph_node_height="props.edge.styles.targetHeight">
        </DirectedRectEdge>
      </template>
      <template slot="visualization" scope="props">
        <foreignObject class="dropdown noselect" :x="btnProp(props.width).x" :y="btnProp().y" width="100%">
          <button class="dropbtn">Visualization Options</button>
          <div class="dropdown-content">
            <a @click="$emit('toggle:showFullDomain')">Change Graph</a>
            <a @click="detailLevel = (detailLevel + 1) % 3">Change Detail</a>
            <a @click="toggleLegendVisibility">Toggle Legend</a>
            <a class="inline-btn-group" @click="textSize = textSize - 1">-</a>
            <label class="inline-btn-group">{{textSize}}</label>
            <a class="inline-btn-group" @click="textSize = textSize + 1">+</a>
          </div>
        </foreignObject>
      </template>
    </GraphVisualizerBase>
    <div class="footer">
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button id="auto-solve" class="btn btn-default" @click="$emit('click:auto-solve')">Auto Solve</button>
        <button id="pause" class="btn btn-default" @click="$emit('click:pause')">Pause</button>
        <button id="print-positions" class="btn btn-default" @click="$emit('click:print-positions')">Print Positions</button>
      </div>
      <div class="output">{{output}}</div>
      <div class="frontier">Frontier: {{frontier}}</div>
    </div>
    {{textSize}}
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";
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
    /** The graph being visualized. */
    graph: Graph<ISearchGraphNode, ISearchGraphEdge>;
    /** Text describing what is currently happening. */
    output: string;
    /** The text representing the frontier. Persistent until frontier changes. */
    frontier: string;
    /** True if edge costs should be shown on the edges. */
    showEdgeCosts: boolean;
    /** True if node heuristics should be shown on the nodes. */
    showNodeHeuristics: boolean;
    /** The width, in pixels, of the visualizer. */
    width: number;
    /** The width, in pixels, of the visualizer. */
    height: number;
    /** Layout object that controls where nodes are drawn. */
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

    toggleLegendVisibility() {
      let lg = $(".legend_group");
      let attr = "visibility";
      let show = "visible";
      let hide = "hidden";

      if (lg.css(attr) === hide) {
        lg.css(attr, show)
      } else {
        lg.css(attr, hide);
      }
    }
  }

</script>
<style scoped>
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
    background-color: silver;
    width: 25%;
  }

  .dropdown-content label.inline-btn-group {
    color: black;
    padding: 1em 0.5em;
    text-align: center;
    width: 40%;
    font-size: 0.75em;
    text-decoration: none;
    display: inline-block;
    border-bottom: 1px solid rgba(0, 0, 255, .1);
  }

  .dropdown-content a:hover {background-color: #ddd;}

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
</style>
