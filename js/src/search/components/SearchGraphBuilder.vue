<template>
  <div>
    <GraphVisualizerBase :graph="graph" @click:node="updateSelection" @click:edge="updateSelection">
      <template slot="node" scope="props">
        <EllipseGraphNode :text="props.node.name"
                          :fill="nodeFillColour(props.node)"
                          :stroke="strokeColour(props.node)" :stroke-width="nodeStrokeWidth(props.node)"
                          @updateBounds="updateNodeBounds(props.node, $event)">
        </EllipseGraphNode>
      </template>
      <template slot="edge" scope="props">
        <DirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2"
                      :sourceRx="props.edge.source.styles.rx" :sourceRy="props.edge.source.styles.ry"
                      :targetRx="props.edge.target.styles.rx" :targetRy="props.edge.target.styles.ry"
                      :stroke="strokeColour(props.edge)"
                      :strokeWidth="props.edge.styles.strokeWidth"
                      :text="props.edge.cost">
        </DirectedEdge>
      </template>
    </GraphVisualizerBase>
    <div>
      <div v-if="selection && selection.type !== 'edge'">
        <label for="node-name">Name</label>
        <input type="text" v-model="selection.name" />
        <label for="node-type">Type</label>
        <select id="node-type" v-model="selection.type">
          <option value="search:start">Start</option>
          <option value="search:regular">Regular</option>
          <option value="search:goal">Goal</option>
        </select>
      </div>
      <div v-if="selection && selection.type === 'edge'">
        <label for="edge-cost">Edge Cost</label>
        <input type="number" v-model.number="selection.cost">
      </div>
    </div>
  </div>
</template>

<script>
  import GraphVisualizerBase from '../../components/GraphVisualizerBase';
  import DirectedEdge from '../../components/DirectedEdge';
  import EllipseGraphNode from '../../components/EllipseGraphNode';

  export default {
    components: {GraphVisualizerBase, DirectedEdge, EllipseGraphNode},
    data() {
      return {
        selection: null
      };
    },
    methods: {
      strokeColour: function (selection) {
        if (this.selection === selection) {
          return 'blue';
        }

        return 'black';
      },
      nodeStrokeWidth: function(node) {
        if (this.selection === node) {
          return 3;
        }

        return 1;
      },
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
      updateSelection: function (selection) {
        if (this.selection === selection) {
          this.selection = null;
        } else {
          this.selection = selection;
        }
      },
      updateNodeBounds: function(node, bounds) {
        node.styles.rx = bounds.rx;
        node.styles.ry = bounds.ry;
      }
    },
    props: {
      graph: {
        type: Object,
        required: true
      }
    }
  }
</script>
