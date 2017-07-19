<template>
  <g>
    <rect width="70" height="50" stroke="black" :fill="rectFill" x="-35" y="-25"></rect>
    <text x="0" y="0" text-anchor="middle" alignment-baseline="middle" :fill="textFill">A {{constraint}} 0</text>
  </g>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

/**
 * A component representing a CSP constraint.
 */
@Component
export default class CSPConstraintNode extends Vue {
  /** Text representing the name of the constraint. */
  @Prop() name: string;
  /** Text representing the constraint. */
  @Prop() constraint: string;
  /** True if the node is being focused (e.g. selected). */
  @Prop({ default: false })
  focus: boolean;
  /** True if the node is being hovered over. */
  @Prop({ default: false })
  hover: boolean;

  get rectFill() {
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
