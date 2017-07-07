<template>
  <div>
    <GraphInteractor :graph="graph" @click:link="linkClicked">
      <template slot="node" scope="node">
        <g v-if="node.type === 'csp:variable'">
          <ellipse rx="40" ry="30" cx="0" cy="0" :fill="node.hovered ? 'pink' : 'white'" stroke="black"></ellipse>
          <text x="0" y="-8" text-anchor="middle" alignment-baseline="middle" fill="black">{{node.name}}</text>
          <text class="domain" x="0" y="7" text-anchor="middle" alignment-baseline="middle" fill="black">
            {{domainText(node)}}
          </text>
  
        </g>
        <g v-if="node.type === 'csp:constraint'">
          <rect width="70" height="50" stroke="black" :fill="node.hovered ? 'azure' : 'white'" x="-35" y="-25"></rect>
          <text x="0" y="0" text-anchor="middle" alignment-baseline="middle" fill="black">A {{node.constraint}} 0</text>
        </g>
      </template>
    </GraphInteractor>
    <div id="footer">
      <div id="controls" class="btn-group">
        <button id="fine-step" class="btn btn-default" @click="$emit('click:fine-step')">Fine Step</button>
        <button id="step" class="btn btn-default" @click="$emit('click:step')">Step</button>
        <button id="auto-step" class="btn btn-default" @click="$emit('click:auto-step')">Auto Step</button>
      </div>
      <div id="output">{{output}}</div>
    </div>
  </div>
</template>

<script>
import GraphInteractor from './GraphInteractor.vue';
export default {
  components: { GraphInteractor },
  methods: {
    domainText: function(variableNode) {
      return `{${variableNode.domain.join(',')}}`
    },
    linkClicked: function(link) {
      this.$emit('click:link', link);
    }
  },
  props: ['graph', 'output']
}
</script>

<style scoped>
text.domain {
  font-size: 12px;
}
</style>
