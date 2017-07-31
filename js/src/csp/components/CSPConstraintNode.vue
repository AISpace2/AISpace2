<template>
  <g>
    <rect width="70" height="50" :fill="fillColour" :stroke="stroke" :stroke-width="strokeWidth" x="-35" y="-25"></rect>
    <text x="0" y="0" text-anchor="middle" alignment-baseline="middle" :fill="textColour">{{constraintText}}</text>
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
  @Prop({ default: "black" })
  stroke: string;
  @Prop({ default: 1 })
  strokeWidth: number;
  @Prop({ default: "white" })
  fillColour: string;
  @Prop({default: "black" })
  textColour: string;

  get constraintText() {
    if (this.constraint != null) {
      return `? ${this.constraint} ?`;
    }

    if (this.name != null) {
      return this.name;
    }

    return '';
  }
}
</script>
