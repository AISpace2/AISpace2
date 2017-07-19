<template>
  <g>
    <ellipse rx="40" ry="30" cx="0" cy="0" :fill="ellipseFill" stroke="black"></ellipse>
    <text x="0" y="-8" text-anchor="middle" alignment-baseline="middle" :fill="textFill">{{name}}</text>
    <text class="domain" x="0" y="7" text-anchor="middle" alignment-baseline="middle" :fill="textFill">
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
  /** True if the node is being focused (e.g. selected). */
  @Prop({ default: false })
  focus: boolean;
  /** True if the node is being hovered over. */
  @Prop({ default: false })
  hover: boolean;

  get domainText() {
    return `{${this.domain.join(",")}}`;
  }

  get ellipseFill() {
    if (this.focus) {
      return "pink";
    }

    if (this.hover) {
      return "black";
    }

    return "white";
  }

  get textFill() {
    if (this.hover) {
      return "white";
    }

    return "black";
  }
}
</script>
