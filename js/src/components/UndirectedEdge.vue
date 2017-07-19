<template>
  <line
    :x1="x1" :y1="y1" :x2="x2" :y2="y2" :stroke="stroke"
    :stroke-width="strokeWidth">
  </line>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

/**
 * An undirected edge between two nodes.
 */
@Component
export default class UndirectedEdge extends Vue {
  /** The x-coordinate of the source point. */
  @Prop() x1: number;
  /** The y-coordinate of the source point. */
  @Prop() y1: number;
  /** The x-coordinate of the target point. */
  @Prop() x2: number;
  /** The y-coordinate of the target point. */
  @Prop() y2: number;
  /** A HTML colour string representing the colour of the edge. */
  @Prop({ default: "black" })
  stroke: string;
  /** The width of the edge, in pixels. */
  @Prop({ default: 4 })
  strokeWidth: number;
  /** True if the edge is being hovered over. */
  @Prop({ default: false })
  hover: boolean;
}
</script>
