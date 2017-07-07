<template>
  <div>
    <graph-builder :graph="graph" @updateNodeSelection="val => selectedNode = val" @dblclick="createNode">
      <template slot="node" scope="node">
        <g v-if="node.type === 'csp:variable'">
          <ellipse rx="40" ry="30" cx="0" cy="0" :fill="node.selected ? 'pink' : 'white'" stroke="black"></ellipse>
          <text x="0" y="-8" text-anchor="middle" alignment-baseline="middle" fill="black">{{node.name}}</text>
          <text class="domain" x="0" y="7" text-anchor="middle" alignment-baseline="middle" fill="black">
            {{node.domain}}
          </text>
  
        </g>
        <g v-if="node.type === 'csp:constraint'">
          <rect width="70" height="50" stroke="black" :fill="node.selected ? 'pink' : 'white'" x="-35" y="-25"></rect>
          <text x="0" y="0" text-anchor="middle" alignment-baseline="middle" fill="black">A {{node.constraint}} 0</text>
        </g>
      </template>
    </graph-builder>
  
    <div>
      <toolbar :mode="mode" @modechanged="updateMode"></toolbar>
      <div v-if="mode == 'variable' || mode == 'constraint' ">
        <span>Double click on the graph to create a new {{mode}}.</span>
      </div>
      <div v-else-if="mode == 'edge'">
        <span v-if="first == null">Select the first node to begin.</span>
        <span v-else>Source node: {{first.name}}. Select an end node to create an edge.</span>
      </div>
    </div>
  
    <div>
      <div v-if="selectedNode && selectedNode.type === 'csp:variable'">
        <label>Name</label>
        <input type="text" :value="selectedNode ? selectedNode.name : null" @input="selectedNode ? selectedNode.name = $event.target.value : null"></input>
        <label>Domain</label>
        <input type="text" :value="selectedNode ? selectedNode.domain : null" @change="selectedNode ? selectedNode.domain = $event.target.value.split(',').map(a => +a) : null"></input>
      </div>
      <div v-else-if="selectedNode && selectedNode.type === 'csp:constraint'">
        <label>Constraint Type</label>
        <select v-model="selectedNode.constraint">
          <option value="lt">Less than (&#60;)</option>
          <option value="gt">Greater than (&#62;)</option>
          <option value="eq">Equal to (=)</option>
          <option value="custom">Custom</option>
        </select>
      </div>
    </div>
    <pre>{{$data}}</pre>
  </div>
</template>


<script>
import GraphBuilder from './GraphBuilder.vue'
import Toolbar from './Toolbar.vue'

export default {
  components: {
    GraphBuilder,
    Toolbar
  },
  data() {
    return {
      mode: 'variable',
      selectedNode: null,
      first: null
    }
  },
  props: ['graph'],
  watch: {
    'selectedNode': function () {
      if (this.mode === 'edge') {
        if (this.first == null) {
          this.first = this.selectedNode;
        } else {
          this.createEdge();
        }
      }
    }
  },
  methods: {
    updateMode: function (mode) {
      this.mode = mode;
    },
    createNode: function (x, y) {
      if (this.mode === 'variable') {
        this.graph.nodes.push({
          name: 'asdf',
          x, y,
          type: 'csp:variable',
          domain: []
        })
      } else if (this.mode === 'constraint') {
        this.graph.nodes.push({
          name: 'asdf',
          x, y,
          type: 'csp:constraint',
          constraint: 'gt'
        })
      }
    },
    createEdge: function () {
      if (this.mode === 'edge' && this.selectedNode != null && this.first != null) {
        if (this.first.type === 'csp:variable' && this.selectedNode.type === 'csp:variable') {
          console.log('Can\'t create an edge between two variables');
          this.first = null;
          return;
        }

        this.graph.links.push({
          source: this.first,
          target: this.selectedNode,
          name: "edge1"
        });

        this.first = null;
      }
    }
  }
}
</script>

<style scoped>
text.domain {
  font-size: 12px;
}
</style>
