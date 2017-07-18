<template>
  <div>
    <GraphVisualizerBase :graph="graph" :width="width" :height="height">
      <template slot="node" scope="props">
        <EllipseGraphNode :text="props.node.name" :fill="nodeFillColour(props.node)"
                          :stroke="nodeStroke(props.node)" :stroke-width="nodeStrokeWidth(props.node)"
                          @updateBounds="updateNodeBounds(props.node, $event)">
        </EllipseGraphNode>
      </template>
      <template slot="edge" scope="props">
        <DirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2" :stroke="props.edge.styles.stroke"
                      :strokeWidth="props.edge.styles.strokeWidth" :text="showEdgeCosts ? props.edge.cost : undefined"
                      :sourceRx="props.edge.source.styles.rx" :sourceRy="props.edge.source.styles.ry"
                      :targetRx="props.edge.target.styles.rx" :targetRy="props.edge.target.styles.ry">
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
  import EllipseGraphNode from '../../components/EllipseGraphNode';

  export default {
    components: {
      GraphVisualizerBase,
      DirectedEdge,
      EllipseGraphNode
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
      },
      width: {
        type: Number,
        default: undefined,
      },
      height: {
        type: Number,
        default: undefined
      }
    },
    methods: {
       nodeFillColour: function(node) {
        switch (node.type) {
          case "search:start":
          return "orchid";
          case "search:goal":
          return "gold";
          default:
          return "white";
        }
      },
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
      },
      updateNodeBounds: function(node, bounds) {
        node.styles.rx = bounds.rx;
        node.styles.ry = bounds.ry;
      }
    }
  };
</script>
