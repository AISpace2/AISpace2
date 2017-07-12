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
                <UndirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2"
                                :stroke="props.link.styles.stroke">
                </UndirectedEdge>
            </template>
        </GraphVisualizerBase>
        <div class="footer">
            <div id="controls" class="btn-group">
                <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
                <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
                <button id="auto-step" class="btn btn-default" @click="$emit('click:auto-step')">Auto Step</button>
            </div>
            <div>{{output}}</div>
        </div>
    </div>
</template>

<script>
  import GraphVisualizerBase from '../../components/GraphVisualizerBase';
  import UndirectedEdge from '../../components/UndirectedEdge';
  import SearchRegularNode from './SearchRegularNode';
  import SearchStartNode from './SearchStartNode';
  import SearchGoalNode from './SearchGoalNode';

  export default {
    components: {GraphVisualizerBase, SearchRegularNode, DirectedEdge, SearchGoalNode, SearchStartNode},
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