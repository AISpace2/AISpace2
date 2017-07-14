<template>
  <g>
    <path :d="path" stroke="black" stroke-width="5" marker-end="url(#marker-end)" :stroke="stroke != null ? stroke : 'black'" :stroke-width="strokeWidth != null ? strokeWidth : 4">
    </path>
    <rect v-if="text" :x="rectX" :y="rectY" :width="rectWidth" :height="rectHeight" fill="white"></rect>
    <text v-if="text" ref="text" :x="centerX" :y="centerY" text-anchor="middle" dominant-baseline="central">{{text}}</text>
  </g>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";

interface DirectedEdge extends Vue {
  /// Props
  /** The x-coordinate of the center of the source node of the edge. */
  x1: number;
  /** The y-coordinate of the center of the source node of the edge. */
  y1: number;
  /** The x-coordinate of the center of the target node of the edge. */
  x2: number;
  /** The y-coordinate of the center of the target node of the edge. */
  y2: number;
  /** A HTML colour string representing the colour of the line. */
  stroke: string;
  /** The width, in pixels, of the line. */
  strokeWidth: number;
  /** The text displayed on the middle of the line. */
  text?: string | number;

  /// Computed Properties
  /** The x-coordinate that is the midpoint between the source and target. */
  centerX: number;
  /** The y-coordinate that is the midpoint between the source and target. */

  centerY: number;
  /** The x-coordinate to draw the rectangle that acts as the background of the displayed text, if any. */
  rectX: number;
  /** The y-coordinate to draw the rectangle that acts as the background of the displayed text, if any. */

  rectY: number;
  /** The width to draw the rectangle that acts as the background of the displayed text, if any. */
  rectWidth: number;
  /** The height to draw the rectangle that acts as the background of the displayed text, if any. */
  rectHeight: number;
  /** The computed path of the line between the source and target. */
  path: string;

  /// Data
  /** The padding along the x-axis to add to the rectangle that acts as the background of the displayed text. */
  rectHorizontalPadding: number;
  /** The padding along the y-axis to add to the rectangle that acts as the background of the displayed text. */
  rectVerticalPadding: number;
  /** Used to track if the component has been mounted (and thus the $refs become available) */
  isMounted: boolean;

  /// Misc
  $refs: {
    /** The text element containing the text for this edge. */
    text: SVGTextElement;
  };
}

export default {
  computed: {
    centerX() {
      return this.x1 + (this.x2 - this.x1) / 2;
    },
    centerY() {
      return this.y1 + (this.y2 - this.y1) / 2;
    },
    rectX() {
      return this.centerX - this.rectWidth / 2;
    },
    rectY() {
      return this.centerY - this.rectHeight / 2;
    },
    rectWidth() {
      // Hack: the check for this.text forces the bbox to be recomputed (refs aren't reactive!)
      if (this.isMounted && this.text) {
        return this.$refs.text.getBBox().width + this.rectHorizontalPadding;
      }
      return 0;
    },
    rectHeight() {
      // Hack: the check for this.text forces the bbox to be recomputed (refs aren't reactive!)
      if (this.isMounted && this.text) {
        return this.$refs.text.getBBox().height + this.rectVerticalPadding;
      }
      return 0;
    },
    path() {
      let diffX = this.x2 - this.x1;
      let diffY = this.y2 - this.y1;

      let pathLength = Math.sqrt(diffX * diffX + diffY * diffY);

      let offsetX = diffX * 50 / pathLength;
      let offsetY = diffY * 40 / pathLength;

      let offsetXSource = diffX * 40 / pathLength;
      let offsetYSource = diffY * 30 / pathLength;

      return (
        "M" +
        (this.x1 + offsetXSource) +
        "," +
        (this.y1 + offsetYSource) +
        "L" +
        (this.x2 - offsetX) +
        "," +
        (this.y2 - offsetY)
      );
    }
  },
  data() {
    return {
      isMounted: false,
      rectHorizontalPadding: 8,
      rectVerticalPadding: 2
    };
  },
  mounted() {
    this.isMounted = true;
  },
  props: {
    x1: {
      type: Number,
      required: true
    },
    y1: {
      type: Number,
      required: true
    },
    x2: {
      type: Number,
      required: true
    },
    y2: {
      type: Number,
      required: true
    },
    stroke: {
      type: String,
      required: false,
      default: "black"
    },
    strokeWidth: {
      type: Number,
      required: false,
      default: 4
    },
    text: {
      type: [String, Number],
      required: false
    }
  }
} as ComponentOptions<DirectedEdge>;
</script>
