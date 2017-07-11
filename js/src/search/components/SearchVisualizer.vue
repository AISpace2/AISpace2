<template>
  <div>
    <GraphVisualizerBase :graph="graph">
      <template slot="node" scope="props">
        <SearchRegularNode v-if="props.node.type === 'search:regular'" :name="props.node.name">
        </SearchRegularNode>
  
        <SearchStartNode v-if="props.node.type === 'search:start'" :name="props.node.name">
        </SearchStartNode>
  
        <SearchGoalNode v-if="props.node.type === 'search:goal'" :name="props.node.name">
        </SearchGoalNode>
      </template>
      <template slot="edge" scope="props">
        <UndirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2">
        </UndirectedEdge>
      </template>
    </GraphVisualizerBase>
    <div>{{output}}</div>
  </div>
</template>

<script>
import GraphVisualizerBase from '../../components/GraphVisualizerBase';
import UndirectedEdge from '../../components/UndirectedEdge';
import SearchRegularNode from './SearchRegularNode';
import SearchStartNode from './SearchStartNode';
import SearchGoalNode from './SearchGoalNode';

export default {
  components: { GraphVisualizerBase, SearchRegularNode, UndirectedEdge, SearchGoalNode, SearchStartNode },
  props: {
    graph: {
      type: Object,
      required: true
    },
    output: {
      type: String,
      required: false,
      default: ''
    }
  }
}
</script>