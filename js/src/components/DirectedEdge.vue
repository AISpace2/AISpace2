<template>
  <g>
    <path :d="path" stroke="black" stroke-width="5" :stroke="stroke" :stroke-width="strokeWidth">
    </path>
    <polygon :points="`0 0 ${arrowHalfSize * 2} ${arrowHalfSize} 0 ${arrowHalfSize * 2}`"
             :transform="`
              translate(${adjustedX2 - arrowHalfSize},${adjustedY2 - arrowHalfSize}) 
              rotate(${angle}, ${arrowHalfSize}, ${arrowHalfSize}) 
              translate(${-arrowHalfSize - 2}, 0)`"
             :stroke="stroke" :fill="stroke" :stroke-width="strokeWidth">
    </polygon>
    <rect v-if="text" :x="rectX" :y="rectY" :width="rectWidth" :height="rectHeight" fill="white"></rect>
    <text v-if="text" ref="text" :x="centerX" :y="centerY" text-anchor="middle" dominant-baseline="central">{{text}}
    </text>
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
    /** The x-coordinate to place the start of the path. It is adjusted to be on the edge of the node. */
    adjustedX1: number;
    /** The y-coordinate to place the start of the path. It is adjusted to be on the edge of the node. */
    adjustedY1: number;
    /** The x-coordinate to place the end of the path. It is adjusted to be on the edge of the node. */
    adjustedX2: number;
    /** The y-coordinate to place the end of the path. It is adjusted to be on the edge of the node. */
    adjustedY2: number;
    /** The x-coordinate that is the midpoint between the source and target. */
    centerX: number;
    /** The y-coordinate that is the midpoint between the source and target. */
    centerY: number;
    /** The difference between the source and target on the x-axis. */
    deltaX: number;
    /** The difference between the soruce and target on the y-axis. */
    deltaY: number;
    /** The computed path of the line between the source and target. */
    path: string;
    /** The length of the path. This is computed using the original x and y coordinates, not the adjusted ones. */
    pathLength: number;
    /** The x-coordinate to draw the rectangle that acts as the background of the displayed text, if any. */
    rectX: number;
    /** The y-coordinate to draw the rectangle that acts as the background of the displayed text, if any. */
    rectY: number;
    /** The width to draw the rectangle that acts as the background of the displayed text, if any. */
    rectWidth: number;
    /** The height to draw the rectangle that acts as the background of the displayed text, if any. */
    rectHeight: number;

    /// Data
    /** Half the size of the arrow, such that (arrowHalfSize, arrowHalfSize) is the center of the arrow. */
    arrowHalfSize: number;
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
      adjustedX1() {
        let offsetX = this.deltaX * 40 / this.pathLength;
        return this.x1 + offsetX;
      },
      adjustedY1() {
        let offsetY = this.deltaY * 30 / this.pathLength;
        return this.y1 + offsetY;
      },
      adjustedX2() {
        let offsetX = this.deltaX * 40 / this.pathLength;
        return this.x2 - offsetX;
      },
      adjustedY2() {
        let offsetY = this.deltaY * 30 / this.pathLength;
        return this.y2 - offsetY;
      },
      angle() {
        var dx = this.x2 - this.x1;
        var dy = this.y2 - this.y1;
        var rad = Math.atan2(dy, dx);
        var deg = rad * 180 / Math.PI;
        return deg;
      },
      centerX() {
        return this.x1 + (this.x2 - this.x1) / 2;
      },
      centerY() {
        return this.y1 + (this.y2 - this.y1) / 2;
      },
      deltaX() {
        return this.x2 - this.x1;
      },
      deltaY() {
        return this.y2 - this.y1;
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
        return (
          "M" +
          this.adjustedX1 +
          "," +
          this.adjustedY1 +
          "L" +
          this.adjustedX2 +
          "," +
          this.adjustedY2
        );
      },
      pathLength() {
        return Math.sqrt(this.deltaX * this.deltaX + this.deltaY * this.deltaY);
      },
    },
    data() {
      return {
        isMounted: false,
        rectHorizontalPadding: 8,
        rectVerticalPadding: 2,
        arrowHalfSize: 4
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
