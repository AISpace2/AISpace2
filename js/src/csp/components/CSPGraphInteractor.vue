<template>
    <div>
        <GraphVisualizerBase :graph="graph" @click:edge="edgeClicked">
            <template slot="node" scope="props">
                <CSPVariableNode v-if="props.node.type === 'csp:variable'" :name="props.node.name"
                                 :domain="props.node.domain" :hover="props.hover">
                </CSPVariableNode>
                <CSPConstraintNode v-if="props.node.type === 'csp:constraint'" :name="props.node.name"
                                   :constraint="props.node.constraint" :hover="props.hover">
                </CSPConstraintNode>
            </template>
            <template slot="edge" scope="props">
                <UndirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2"
                                :stroke="stroke(props.edge)"
                                :stroke-width="strokeWidth(props.edge, props.hover)"></UndirectedEdge>
            </template>
        </GraphVisualizerBase>
        <div id="footer">
            <div id="controls" class="btn-group">
                <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
                <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
                <button id="auto-step" class="btn btn-default" @click="$emit('click:auto-step')">Auto Step</button>
            </div>
            <div id="output">{{output}}</div>
        </div>
    </div>
</template>

<script>
  import GraphVisualizerBase from '../../components/GraphVisualizerBase';
  import CSPConstraintNode from './CSPConstraintNode';
  import CSPVariableNode from './CSPVariableNode';
  import UndirectedEdge from '../../components/UndirectedEdge';
  export default {
    components: {GraphVisualizerBase, CSPConstraintNode, CSPVariableNode, UndirectedEdge},
    methods: {
      edgeClicked: function (edge) {
        this.$emit('click:edge', edge);
      },
      stroke: function (edge) {
        if (edge.styles != null) {
          return edge.styles.stroke;
        }

        return null;
      },
      strokeWidth: function (edge, isHovering) {
        if (isHovering) {
          return 7;
        }

        if (edge.styles && edge.styles.strokeWidth) {
          return edge.styles.strokeWidth;
        }

        return 4;
      }
    },
    props: ['graph', 'output']
  }
</script>

<style scoped>
    text.domain {
        font-size: 12px;
    }
</style>
