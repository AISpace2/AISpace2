<template>
  <div>
    <svg tabindex="0" ref="mySVG" width="800" height="500" @mousemove="dragSVG" @keydown.delete="deleteSelection" @dblclick="onDblClick">
      <node-link :key="link.name" v-for="link in graph.links" :x1="link.source.x" :x2="link.target.x" :y1="link.source.y" :y2="link.target.y" @click="toggleSelection(link)" :colour="isSelected(link)">
      </node-link>
      <graph-node v-for="node in graph.nodes" :key="node.name" :class="{selected: node === selected}" @click="toggleSelection(node)" @dragstart="dragstart(node, $event)" @dragend="dragend(node)" :transform="`translate(${node.x}, ${node.y})`">
        <slot name="node" v-bind="node" :selected="node === selected"></slot>
      </graph-node>
    </svg>
  </div>
</template>

<script>
import GraphNode from './GraphNode.vue'
import NodeLink from './NodeLink';
import { removeNode, removeEdge } from './GraphUtils';

export default {
  name: 'app',
  components: {
    GraphNode,
    NodeLink,
  },
  props: ['graph'],
  data() {
    return {
      selected: null,
      dragselection: null,
      firstVar: null
    };
  },
  computed: {},
  mounted() {
  },
  watch: {
    'selected': function (val) {
      this.$emit('updateNodeSelection', this.selected);
    }
  },
  methods: {
    toggleSelection: function (el) {
      this.selected = this.selected === el ? null : el;
    },
    isSelected: function (el) {
      if (el === this.selected) {
        return "pink";
      }

      return "black";
    },

    dragstart: function (node, e) {
      this.dragselection = node;
    },

    dragSVG: function (e) {
      if (this.dragselection) {
        var svgBounds = this.$refs.mySVG.getBoundingClientRect();
        this.dragselection.x = e.pageX - svgBounds.left;
        this.dragselection.y = e.pageY - svgBounds.top;
      }
    },

    dragend: function () {
      this.dragselection = null;
    },

    deleteSelection: function () {
      if (this.selected) {
        if (this.selected.source && this.selected.target) {
          removeEdge(this.graph, this.selected);
        } else {
          removeNode(this.graph, this.selected);
        }
        this.selected = null;
      }
    },

    onDblClick: function (e) {
      var svgBounds = this.$refs.mySVG.getBoundingClientRect();
      var x = e.pageX - svgBounds.left;
      var y = e.pageY - svgBounds.top;
      this.$emit('dblclick', x, y, e);
      this.selected = null;
    }
  }
}
</script>

<style>
svg:focus {
  outline: none;
}

#app svg {
  border: 1px solid lavenderblush;
}
</style>
