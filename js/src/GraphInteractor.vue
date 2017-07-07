<template>
  <div id="app">
    <div>
      <svg ref="mySVG" width="800" height="500" @mousemove="dragSVG">
        <node-link :key="link.name" v-for="link in graph.links" :x1="link.source.x" :x2="link.target.x"
                   :y1="link.source.y"
                   :y2="link.target.y"
                   @mouseover="linkMouseOver(link)"
                   @mouseout="linkMouseOut(link)"
                   :stroke="link.style && link.style.stroke ? link.style.stroke : null"
                   :strokeWidth="strokeWidth(link)"
                   @click="$emit('click:link', link)"
        ></node-link>
        <graph-node v-for="node in graph.nodes"
                    :key="node.name"
                    @dragstart="dragstart(node, $event)"
                    @dragend="dragend(node)"
                    @mouseover="nodeMouseOver(node)"
                    @mouseout="nodeMouseOut(node)"
                    :transform="`translate(${node.x}, ${node.y})`"
        >
          <slot name="node" v-bind="node" :hovered="node === nodeHover"></slot>
        </graph-node>
      </svg>
    </div>
  </div>
</template>

<script>
  import GraphNode from './GraphNode.vue'
  import NodeLink from './NodeLink';

  export default {
    name: 'app',
    components: {
      GraphNode,
      NodeLink
    },
    props: ['graph'],
    data() {
      return {
        nodeHover: null,
        dragselection: null,
        linkHover: null
      };
    },
    methods: {
      linkThickness: function (photo) {
        if (photo === this.linkHover) {
          return 7;
        }

        return 4;
      },

      nodeFill: function(node) {
        if (node === this.nodeHover) {
          return "black";
        }

        return "white";
      },

      nodeTextFill: function(node) {
          if (node === this.nodeHover) {
            return "white";
          }

          return "black";
      },

      dragstart: function (node, e) {
        this.dragselection = node;
      },

      dragSVG: function (e) {
        if (this.dragselection) {
          var bounds = this.$refs.mySVG.getBoundingClientRect();
          this.dragselection.x = e.clientX - bounds.left;
          this.dragselection.y = e.clientY - bounds.top;
        }
      },

      dragend: function () {
        this.dragselection = null;
      },

      linkMouseOver: function(link) {
        this.linkHover = link;
      },

      linkMouseOut: function(link) {
        this.linkHover = null;
      },

      nodeMouseOver: function(link) {
        this.nodeHover = link;
      },

      nodeMouseOut: function(link) {
        this.nodeHover = null;
      },

      strokeWidth: function(link) {
        if (link === this.linkHover) {
          return 7;
        }

        return link.style && link.style.strokeWidth ? link.style.strokeWidth : null;
      }
    },
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
  }

  #app svg {
    border: 1px solid lavenderblush;
  }

</style>
