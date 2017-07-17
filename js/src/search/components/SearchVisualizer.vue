<template>
  <div>
    <GraphVisualizerBase :graph="graph">
      <template slot="node" scope="props">
        <SearchRegularNode v-if="props.node.type === 'search:regular'" :name="props.node.name"
                           :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)">
        </SearchRegularNode>

        <SearchStartNode v-if="props.node.type === 'search:start'" :name="props.node.name"
                         :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)">
        </SearchStartNode>

        <SearchGoalNode v-if="props.node.type === 'search:goal'" :name="props.node.name"
                        :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)">
        </SearchGoalNode>
      </template>
      <template slot="edge" scope="props">
        <DirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2" :stroke="props.edge.styles.stroke"
                      :strokeWidth="props.edge.styles.strokeWidth" :text="showEdgeCosts ? props.edge.cost : undefined">
        </DirectedEdge>
      </template>
    </GraphVisualizerBase>
    <div class="footer">
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button id="auto-step" class="btn btn-default" @click="$emit('click:auto-step')">Auto Step</button>
      </div>
      <div>{{output}}</div>
    </div>
  </div>
</template>

<script>
  import GraphVisualizerBase from "../../components/GraphVisualizerBase";
  import DirectedEdge from "../../components/DirectedEdge";
  import SearchRegularNode from "./SearchRegularNode";
  import SearchStartNode from "./SearchStartNode";
  import SearchGoalNode from "./SearchGoalNode";

  export default {
    components: {
      GraphVisualizerBase,
      SearchRegularNode,
      DirectedEdge,
      SearchGoalNode,
      SearchStartNode
    },
    props: {
      graph: {
        type: Object,
        required: true
      },
      output: {
        type: String,
        required: false,
        default: ""
      },
      showEdgeCosts: {
        type: Boolean,
        required: false,
        default: true
      }
    },
    methods: {
      nodeStroke(node) {
        if (node.styles && node.styles.stroke) {
          return node.styles.stroke;
        }

        return "black";
      },
      nodeStrokeWidth(node) {
        if (node.styles && node.styles.strokeWidth) {
          return node.styles.strokeWidth;
        }

        return 1;
      }
    }
  };
</script>
