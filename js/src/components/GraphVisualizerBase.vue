<template>
  <div>
    <svg tabindex="0" ref="mySVG" width="800" height="500"
         @mousemove="dragSVG"
         @mouseleave="dragEnd"
         @keydown.delete="$emit('delete')"
         @dblclick="onDblClick">
      <marker id="marker-end" viewBox="0 0 10 10" refX="3" refY="5" markerWidth="3" markerHeight="3"
              orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z"></path>
      </marker>
      <EdgeContainer v-for="edge in graph.edges" :key="edge.id"
                     @mouseover="edgeMouseOver(edge)"
                     @mouseout="edgeMouseOut(edge)"
                     @click="$emit('click:edge', edge)">
        <slot name="edge" :edge="edge"
              :x1="edge.source.x" :y1="edge.source.y"
              :x2="edge.target.x" :y2="edge.target.y"
              :hover="edge === edgeHover"></slot>
      </EdgeContainer>
      <GraphNode v-for="node in graph.nodes" :key="node.id"
                 @click="$emit('click:node', node)"
                 @dragstart="dragStart(node, $event)" @dragend="dragEnd"
                 @mouseover="nodeMouseOver(node)" @mouseout="nodeMouseOut(node)"
                 :x="node.x" :y="node.y">
        <slot name="node" :node="node" :hover="node === nodeHover"></slot>
      </GraphNode>
    </svg>
  </div>
</template>

<script>
  import GraphNode from './GraphNode';
  import EdgeContainer from './EdgeContainer';

  export default {
    components: {
      GraphNode,
      EdgeContainer
    },
    props: ['graph'],
    data() {
      return {
        dragTarget: null,
        edgeHover: null,
        nodeHover: null,
        prevPageX: 0,
        prevPageY: 0
      };
    },
    methods: {
      dragStart: function (node, e) {
        this.dragTarget = node;
      },

      dragSVG: function (e) {
        if (this.dragTarget) {
          var svgBounds = this.$refs.mySVG.getBoundingClientRect();

          // Everything below can be replaced with:
          // this.dragTarget.x += e.movementX;
          // this.dragTarget.y += e.movementY;
          // if we don't want to support IE11.
          this.dragTarget.x += (this.prevPageX ? e.pageX - this.prevPageX : 0);
          this.dragTarget.y += (this.prevPageY ? e.pageY - this.prevPageY : 0);

          this.prevPageX = e.pageX;
          this.prevPageY = e.pageY;
        }
      },

      dragEnd: function () {
        this.dragTarget = null;
        this.prevPageX = 0;
        this.prevPageY = 0;
      },

      edgeMouseOver: function (edge) {
        this.edgeHover = edge;
      },

      edgeMouseOut: function (edge) {
        this.edgeHover = null;
      },

      nodeMouseOver: function (edge) {
        this.nodeHover = edge;
      },

      nodeMouseOut: function (edge) {
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
