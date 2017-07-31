<template>
  <g>
    <ellipse rx="40" ry="30" cx="0" cy="0" :fill="fillColour" :stroke="stroke" :stroke-width="strokeWidth"></ellipse>
    <text x="0" y="-8" text-anchor="middle" alignment-baseline="middle" :fill="textColour">{{name}}</text>
    <text class="domain" x="0" y="7" text-anchor="middle" alignment-baseline="middle" :fill="textColour">
      {{domainText}}
    </text>
  </g>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

/**
 * A component representing a CSP variable.
 */
@Component
export default class CSPVariableNode extends Vue {
  /** The name of the variable node. */
  @Prop() name: string;
  /** The domain of the variable node. */
  @Prop({ type: Array })
  domain: number[] | string[];
  @Prop({ default: "black" })
  stroke: string;
  @Prop({ default: 1 })
  strokeWidth: number;
  @Prop({ default: "white" })
  fillColour: string;
  @Prop({default: "black" })
  textColour: string;

  get domainText() {
    return `{${this.domain.join(",")}}`;
  }
}
</script>
