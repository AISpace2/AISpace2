<template>
  <div tabindex="0" @keydown.stop class="csp_visualizer">
    <button id="query-mode" :style="stateStyle('query')" class = "btn btn-default" @click="isQuerying = true">Query</button>
    <button id="observe-mode" :style="stateStyle('observe')" class = "btn btn-default" @click="isQuerying = false">Observe</button>
    <GraphVisualizerBase :graph="graph" @click:node="nodeClicked" @click:edge="edgeClicked" :layout="layout" :transitions="true"
    >
      <template slot="node" slot-scope="props">
        <RoundedRectangleGraphNode :text="props.node.name" :textSize="textSize" :subtext= "probText(props.node)"
                                   :textColour="props.hover ? 'white' : 'black'" :fill="props.hover ? 'black' : 'white'"
                                   :hover="props.hover" :id="props.node.id" :detailLevel="detailLevel" @updateBounds="updateNodeBounds(props.node, $event)"
                                   :stroke-width="nodeStrokeWidth(props.node)">
        </RoundedRectangleGraphNode>
      </template>
      <template slot="edge" slot-scope="props">
        <DirectedRectEdge :id="props.edge.id" :x1="props.edge.source.x" :x2="props.edge.target.x" :y1="props.edge.source.y" :y2="props.edge.target.y" :stroke="props.edge.styles.stroke"
                          :strokeWidth="strokeWidth(props.edge, props.hover)" :nodeName="props.edge.target.name"
                          :graph_node_width="props.edge.styles.targetWidth" :graph_node_height="props.edge.styles.targetHeight">
        </DirectedRectEdge>
      </template>
      <template slot="visualization" slot-scope="props">
        <a class="inline-btn-group" @click="detailLevel = detailLevel > 0 ? detailLevel - 1 : detailLevel">&#8249;</a>
        <label class="inline-btn-group">Detail: {{detailLevel}}</label>
        <a class="inline-btn-group" @click="detailLevel = detailLevel < 2 ? detailLevel + 1 : detailLevel">&#8250;</a>

        <a class="inline-btn-group" @click="textSize = textSize - 1">-</a>
        <label class="inline-btn-group">Size: {{textSize}}</label>
        <a class="inline-btn-group" @click="textSize = textSize + 1">+</a>

        <a class="inline-btn-group" @click="decimalPlace = decimalPlace - 1">-</a>
        <label class="inline-btn-group">Decimal: {{decimalPlace}}</label>
        <a class="inline-btn-group" @click="decimalPlace = decimalPlace + 1">+</a>
      </template>
    </GraphVisualizerBase>
    <div>
      <div id="controls" class="btn-group">
        <button id="reset" class = "btn btn-default" @click="$emit('reset')">Reset</button>
        <button id="print-positions" class = "btn btn-default" @click="$emit('click:print-positions')">Print Positions</button>
      </div>
      <div class="output" style="white-space: pre;">{{output}}</div>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import Component from "vue-class-component";

  import RoundedRectangleGraphNode from "../../components/RoundedRectangleGraphNode.vue";
  import GraphVisualizerBase from "../../components/GraphVisualizerBase.vue";
  import RectangleGraphNode from "../../components/RectangleGraphNode.vue";
  import DirectedRectEdge from "../../components/DirectedRectEdge.vue";

  import {Graph, IBayesGraphNode, IGraphEdge} from "../../Graph";
  import { GraphLayout } from "../../GraphLayout";

  /**
   * A Bayesian Network visualization that can be driven by backend code.
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
    // If true, node click will query the node's probability
    // If False, node click will make observation
    isQuerying: boolean;
    // the number of decimal places to show for the node's probability
    decimalPlace: number;

    edgeClicked(edge: IGraphEdge) {
      this.$emit("click:edge", edge);
    }

    nodeClicked(node: IBayesGraphNode) {
      if (this.isQuerying) {
        this.$emit("click:query-node", node);
      } else {
        this.$emit("click:observe-node", node);
        this.$emit("click:query-node", node);
      }
    }

    strokeWidth(edge: IGraphEdge, isHovering: boolean) {
      const hoverWidth = isHovering ? 3 : 0;

      if (edge.styles && edge.styles.strokeWidth) {
        return edge.styles.strokeWidth + hoverWidth;
      }

      return 4 + hoverWidth;
    }

    /** Properties for text button for visualization */
    get textBtnProp() {
      return {
        width: 30,
        height: 30,
        y: 20
      };
    }

    nodeStrokeWidth(node: IBayesGraphNode) {
      if (node.styles && node.styles.strokeWidth) {
        return node.styles.strokeWidth;
      }

      return undefined;
    }

    // Returns a formatted string representing the probability of a variable node after query
    probText(node: IBayesGraphNode) {
      if (node.prob === undefined) {
	    if (node.observed === undefined) return undefined;
	    return "\n" + "Obs: " + node.observed;
	  }
      else {
        let text = "";
        for (var key in node.prob) {
          text += key + ": " + node.prob[key].toFixed(this.decimalPlace) + ", ";
        }
        text = text.slice(0, -2)  // delete last comma and space
	      if (node.observed === undefined) return text;
        return  "Obs: " + node.observed + "\n" + text;
      }
	  }

    addTextSize(){
      this.textSize ++;
    }

    minusTextSize(){
      if(this.textSize > 0) this.textSize --;
    }

    // Whenever a node reports it has resized, update it's style so that it redraws.
    updateNodeBounds(node: IBayesGraphNode, bounds: { width: number; height: number }) {
      node.styles.width = bounds.width;
      node.styles.height = bounds.height;
      this.graph.edges
        .filter(edge => edge.target.id === node.id)
        .forEach(edge => {
          this.$set(edge.styles, "targetWidth", bounds.width);
          this.$set(edge.styles, "targetHeight", bounds.height);
        });
    }

    // style selection for state observation and query button
    stateStyle(state: string): string {
      const selectedStyle = "color: white; background-color:grey";
      const unselectedStyle = "background-color:white";

      if (state === "query") {
        return this.isQuerying ? selectedStyle : unselectedStyle;
      } else if (state === "observe") {
        return this.isQuerying ? unselectedStyle : selectedStyle;
      }

      return unselectedStyle;
    }
  }

</script>
