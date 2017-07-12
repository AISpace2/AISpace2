<template>
    <div>
        <svg tabindex="0" ref="mySVG" width="800" height="500"
             @mousemove="dragSVG"
             @mouseleave="dragEnd"
             @keydown.delete="$emit('delete')"
             @dblclick="onDblClick">
            <EdgeContainer v-for="link in graph.edges" :key="link.id"
                           @mouseover="linkMouseOver(link)"
                           @mouseout="linkMouseOut(link)"
                           @click="$emit('click:edge', link)">
                <slot name="edge" :link="link"
                      :x1="link.source.x" :y1="link.source.y"
                      :x2="link.target.x" :y2="link.target.y"
                      :hover="link === linkHover"></slot>
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
    props: ['graph', 'selection'],
    data() {
      return {
        dragTarget: null,
        linkHover: null,
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