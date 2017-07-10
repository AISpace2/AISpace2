<template>
    <div>
        <GraphVisualizerBase :graph="graph" @click:edge="linkClicked">
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
                                :stroke="props.link.style.stroke"
                                :stroke-width="edgeStrokeWidth(props.link, props.hover)"></UndirectedEdge>
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
  import GraphVisualizerBase from './GraphVisualizerBase';
  import CSPConstraintNode from './CSPConstraintNode';
  import CSPVariableNode from './CSPVariableNode';
  import UndirectedEdge from './UndirectedEdge';
  export default {
    components: {GraphVisualizerBase, CSPConstraintNode, CSPVariableNode, UndirectedEdge},
    methods: {
      linkClicked: function (link) {
        this.$emit('click:link', link);
      },

      edgeStrokeWidth: function (link, isHovering) {
        if (isHovering) {
          return 7;
        }

        if (link.style && link.style.strokeWidth) {
          return link.style.strokeWidth;
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
