<template>
    <div>
        <GraphVisualizerBase :graph="graph" @click:node="updateSelection" @click:edge="updateSelection">
            <template slot="node" scope="props">
                <SearchRegularNode v-if="props.node.type === 'search:regular'" :name="props.node.name" :focus="props.node === selection">
                </SearchRegularNode>
    
                <SearchStartNode v-if="props.node.type === 'search:start'" :name="props.node.name" :focus="props.node === selection">
                </SearchStartNode>
    
                <SearchGoalNode v-if="props.node.type === 'search:goal'" :name="props.node.name" :focus="props.node === selection">
                </SearchGoalNode>
            </template>
            <template slot="edge" scope="props">
                <DirectedEdge :x1="props.x1" :x2="props.x2" :y1="props.y1" :y2="props.y2" :stroke="strokeColour(props.edge)"                        :strokeWidth="props.edge.styles.strokeWidth">
                </DirectedEdge>
            </template>
        </GraphVisualizerBase>
        <div>
            <div v-if="selection && selection.type !== 'edge'">
                <label for="node-type">Type</label>
                <select id="node-type" v-model="selection.type">
                    <option value="search:start">Start</option>
                    <option value="search:regular">Regular</option>
                    <option value="search:goal">Goal</option>
                </select>
            </div>
        </div>
    </div>
</template>

<script>
import GraphVisualizerBase from '../../components/GraphVisualizerBase';
import DirectedEdge from '../../components/DirectedEdge';
import SearchRegularNode from './SearchRegularNode';
import SearchStartNode from './SearchStartNode';
import SearchGoalNode from './SearchGoalNode';

export default {
    components: { GraphVisualizerBase, SearchRegularNode, DirectedEdge, SearchGoalNode, SearchStartNode },
    data() {
        return {
            selection: null
        };
    },
    methods: {
        strokeColour: function (edge) {
            if (this.selection === edge) {
                return 'pink';
            }

            return 'black';
        },
        updateSelection: function (selection) {
            if (this.selection === selection) {
                this.selection = null;
            } else {
                this.selection = selection;
            }
        },
    },
    props: {
        graph: {
            type: Object,
            required: true
        }
    }
}
</script>