<template>
    <div>
        <svg tabindex="0" ref="mySVG" width="800" height="500"
             @mousemove="dragSVG"
             @keydown.delete="$emit('delete')"
             @dblclick="onDblClick">
            <EdgeContainer v-for="link in graph.links" :key="link.id"
                           @mouseover="linkMouseOver(link)"
                           @mouseout="linkMouseOut(link)"
                           @click="$emit('click:edge', link)">
                <slot name="edge" :link="link"
                      :x1="link.source.x" :y1="link.source.y"
                      :x2="link.target.x" :y2="link.target.y"
                      :hover="link === linkHover"></slot>
            </EdgeContainer>
            <GraphNode v-for="node in graph.nodes" :key="node.id"
                       :transform="`translate(${node.x}, ${node.y})`"
                       @click="$emit('click:node', node)"
                       @dragstart="dragstart(node, $event)" @dragend="dragend(node)"
                       @mouseover="nodeMouseOver(node)" @mouseout="nodeMouseOut(node)">
                <slot name="node" :node="node" :hover="node === nodeHover"></slot>
            </GraphNode>
        </svg>
    </div>
</template>

<script>
  import GraphNode from './GraphNode';
  import NodeLink from './NodeLink';
  import EdgeContainer from './EdgeContainer';

  export default {
    components: {
      GraphNode,
      NodeLink,
      EdgeContainer
    },
    props: ['graph', 'selection'],
    data() {
      return {
        dragTarget: null,
        linkHover: null,
        nodeHover: null
      };
    },
    methods: {
      dragstart: function (node, e) {
        this.dragTarget = node;
      },

      dragSVG: function (e) {
        if (this.dragTarget) {
          var svgBounds = this.$refs.mySVG.getBoundingClientRect();
          this.dragTarget.x = e.pageX - svgBounds.left;
          this.dragTarget.y = e.pageY - svgBounds.top;
        }
      },

      dragend: function () {
        this.dragTarget = null;
      },

      linkMouseOver: function (link) {
        this.linkHover = link;
      },

      linkMouseOut: function (link) {
        this.linkHover = null;
      },

      nodeMouseOver: function (link) {
        this.nodeHover = link;
      },

      nodeMouseOut: function (link) {
        this.nodeHover = null;
      },

      onDblClick: function (e) {
        var svgBounds = this.$refs.mySVG.getBoundingClientRect();
        var x = e.pageX - svgBounds.left;
        var y = e.pageY - svgBounds.top;
        this.$emit('dblclick', x, y, e);
      }
    }
  }

</script>

<style scoped>
    svg:focus {
        outline: none;
    }
</style>