<template>
    <div>
        <GraphVisualizerBase :graph="graph" @updateSelection="val => selection = val" @dblclick="createNode"
                             :selection="selection"
                             @click:edge="updateSelection"
                             @click:node="updateSelection"
                             @delete="deleteSelection">
            <template slot="node" scope="props">
                <CSPVariableNode v-if="props.node.type === 'csp:variable'" :name="props.node.name"
                                 :domain="props.node.domain"
                                 :focus="props.node === selection">
                </CSPVariableNode>
                <CSPConstraintNode v-if="props.node.type === 'csp:constraint'" :name="props.node.name"
                                   :constraint="props.node.constraint"
                                   :focus="props.node === selection">
                </CSPConstraintNode>
            </template>
            <template slot="edge" scope="props">
                <UndirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2"
                                :stroke="strokeColour(props.link)"></UndirectedEdge>
            </template>
        </GraphVisualizerBase>

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
            <div v-if="selection && selection.type === 'csp:variable'">
                <label>Name</label>
                <input type="text" :value="selection ? selection.name : null"
                       @input="selection ? selection.name = $event.target.value : null" />
                <label>Domain</label>
                <input type="text" :value="selection ? selection.domain : null"
                       @change="selection ? selection.domain = $event.target.value.split(',').map(a => +a) : null" />
            </div>
            <div v-else-if="selection && selection.type === 'csp:constraint'">
                <label>Constraint Type</label>
                <select v-model="selection.constraint">
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
  import GraphVisualizerBase from './GraphVisualizerBase.vue'
  import CSPConstraintNode from './CSPConstraintNode';
  import CSPVariableNode from './CSPVariableNode';
  import UndirectedEdge from './UndirectedEdge';

  import Toolbar from './Toolbar.vue'
  import * as shortid from "shortid";

  export default {
    components: {
      GraphVisualizerBase,
      Toolbar,
      CSPConstraintNode,
      CSPVariableNode,
      UndirectedEdge
    },
    data() {
      return {
        mode: 'select',
        selection: null,
        first: null
      }
    },
    props: ['graph'],
    watch: {
      'selection': function () {
        if (this.mode === 'edge') {
          if (this.first == null) {
            this.first = this.selection;
          } else {
            this.createEdge();
          }
        } else if (this.mode !== 'select') {
          this.selection = null;
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
            domain: [],
            id: shortid.generate()
          })
        } else if (this.mode === 'constraint') {
          this.graph.nodes.push({
            name: 'asdf',
            x, y,
            type: 'csp:constraint',
            constraint: 'gt',
            id: shortid.generate()
          })
        }
      },
      createEdge: function () {
        if (this.mode === 'edge' && this.selection != null && this.first != null) {
          if (this.first.type === 'csp:variable' && this.selection.type === 'csp:variable') {
            console.log('Can\'t create an edge between two variables');
            this.first = null;
            return;
          }

          this.graph.edges.push({
            source: this.first,
            target: this.selection,
            name: "edge1",
            id: shortid.generate()
          });

          this.first = null;
        }
      },

      strokeColour: function (link) {
        if (link === this.selection) {
          return "pink";
        }

        return "black";
      },

      updateSelection: function (selection) {
        if (this.selection === selection) {
          this.selection = null;
        } else {
          this.selection = selection;
        }
      },

      deleteSelection: function () {
        if (this.selection) {
          if (this.selection.source && this.selection.target) {
            this.graph.removeEdge(this.selection);
          } else {
            this.graph.removeNode(this.selection);
          }
          this.selection = null;
        }
      },
    }
  }
</script>

<style scoped>
    text.domain {
        font-size: 12px;
    }
</style>
