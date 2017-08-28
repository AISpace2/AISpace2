<template>
  <!-- We only use a path rather than a line because no browsers animate lines but some (Chrome) animate paths. -->
  <path :d="path" :stroke="stroke" :stroke-width="strokeWidth"></path>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

/**
 * An undirected edge between two nodes.
 * 
 * Unlike DirectedEdge, it can just draw the line from point-to-point without worrying
 * about where the edge of the node is:
 * the nodes are drawn on top and so we get the occlusion for free.
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

  get path() {
    return `M${this.x1},${this.y1}L${this.x2},${this.y2}`;
  }
}

</script>
