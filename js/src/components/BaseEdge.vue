<template>
    <g>
        <path :d="path" stroke="black" stroke-width="5" :stroke="stroke" :stroke-width="strokeWidth"></path>
        <!-- We draw the marker instead of using marker-end on the path because markers don't inherit the lines colour. -->
        <polygon :points="`0 0 ${arrowHalfSize * 2} ${arrowHalfSize} 0 ${arrowHalfSize * 2}`" :transform="`
                  translate(${adjustedX2 - arrowHalfSize},${adjustedY2 - arrowHalfSize})
                  rotate(${angle}, ${arrowHalfSize}, ${arrowHalfSize})
                  translate(${-arrowHalfSize - 2}, 0)`" :stroke="stroke" :fill="stroke" :stroke-width="strokeWidth">
        </polygon>

        <!-- The white background for the text. There is no way to colour the background of text in SVG. -->
        <!-- rect v-if="text" :x="rectX" :y="rectY" :width="rectWidth" :height="rectHeight" fill="white"></rect -->
        <g :transform="`translate(${textX}, ${textY})
            rotate(${angleText})`">
            <!-- Text x/y are not animated, so we wrap it in a group. -->
            <text class = "textstroke" v-if="text" ref="text" text-anchor="middle" fill="white" dominant-baseline="central">{{text}}</text>
        </g>
    </g>
</template>

<script lang="ts">
  import Vue, { ComponentOptions } from "vue";
  import Component from "vue-class-component";
  import { Prop } from "vue-property-decorator";

  /**
   * An edge with an arrow pointing to the target, with support for text. Note: this is a base class. Do not display this without extending
   */
  @Component
  export default class BaseEdge extends Vue {
    @Prop({default: ""}) id: string;
    /** The x-coordinate of the center of the source node of the edge. */
    @Prop() x1: number;
    /** The y-coordinate of the center of the source node of the edge. */
    @Prop() y1: number;
    /** The x-coordinate of the center of the target node of the edge. */
    @Prop() x2: number;
    /** The y-coordinate of the center of the target node of the edge. */
    @Prop() y2: number;
    @Prop({default: ""}) nodeName: string;
    /** A HTML colour string representing the colour of the line. */
    @Prop({ default: "black" })
    stroke: string;
    /** The width, in pixels, of the line. */
    @Prop({ default: 4 })
    strokeWidth: number;
    /** The text displayed on the middle of the line. */
    @Prop({ type: [String, Number], required: false })
    text?: string | number;

    /** Half the size of the arrow, such that (arrowHalfSize, arrowHalfSize) is the center of the arrow. */
    arrowHalfSize = 4;
    /** The padding along the x-axis to add to the rectangle that acts as the background of the displayed text. */
    rectHorizontalPadding = 8;
    /** The padding along the y-axis to add to the rectangle that acts as the background of the displayed text. */
    rectVerticalPadding = 2;
    /** Used to track if the component has been mounted (and thus the $refs become available) */
    isMounted = false;

    $refs: {
      /** The text element containing the text for this edge. */
      text: SVGTextElement;
    };

    mounted() {
      this.isMounted = true;
    }

    /** The x-coordinate to place the start of the path. It is adjusted to be on the edge of the node. */
    get adjustedX1() {
      return this.x1;
    }

    /** The y-coordinate to place the start of the path. It is adjusted to be on the edge of the node. */
    get adjustedY1() {
      return this.y1;
    }

    /** The x-coordinate to place the end of the path. It is adjusted to be on the edge of the node. */
    get adjustedX2() {
      return this.x2;
    }

    /** The y-coordinate to place the end of the path. It is adjusted to be on the edge of the node. */
    get adjustedY2() {
      return this.y2;
    }

    /** The angle of the line, in degrees, between the source and target. */
    get angle() {
      var dx = this.adjustedX2 - this.adjustedX1;
      var dy = this.adjustedY2 - this.adjustedY1;
      var rad = Math.atan2(dy, dx);
      var deg = rad * 180 / Math.PI;
      return deg;
    }

    /** The angle of the text aligning with the edge */
    get angleText() {
      let angle = 0;
      var dx = this.adjustedX2 - this.adjustedX1;
      var dy = this.adjustedY2 - this.adjustedY1;
      if (dx > 0 && dy > 0) {
        angle = this.angle;
      }
      if (dx < 0 && dy < 0) {
        angle = this.angle -180;
      }
      if (dx < 0 && dy > 0) {
        angle = this.angle - 180;
      }
      if (dx > 0 && dy < 0) {
        angle = this.angle;
      }
      return angle;
    }

    /** The x-coordinate that is the midpoint between the source and target of the adjusted path. */
    get centerX() {
      if(this.adjustedX1 === this.adjustedX2 && this.adjustedY1 === this.adjustedY2){
        return this.adjustedX1 + 80;
      } else return this.adjustedX1 + (this.adjustedX2 - this.adjustedX1) / 2;
    }

    get textX() {
      return this.centerX;
    }

    /** The y-coordinate that is the midpoint between the source and target of the adjusted path. */
    get centerY() {
      if(this.adjustedX1 === this.adjustedX2 && this.adjustedY1 === this.adjustedY2){
        return this.adjustedY1;
      } else return this.adjustedY1 + (this.adjustedY2 - this.adjustedY1) / 2;
    }

    get textY() {
      return this.centerY;
    }

    /** The difference between the source and target on the x-axis. */
    get deltaX() {
      return this.x2 - this.x1;
    }

    /** The difference between the soruce and target on the y-axis. */
    get deltaY() {
      return this.y2 - this.y1;
    }

    /** The x-coordinate to draw the rectangle that acts as the background of the displayed text, if any. */
    get rectX() {
      return this.centerX - this.rectWidth / 2;
    }

    /** The y-coordinate to draw the rectangle that acts as the background of the displayed text, if any. */
    get rectY() {
      return this.centerY - this.rectHeight / 2;
    }

    /** The width to draw the rectangle that acts as the background of the displayed text, if any. */
    get rectWidth() {
      // Hack: the check for this.text forces the bbox to be recomputed (refs aren't reactive!)
      if (this.isMounted && this.text) {
        return this.$refs.text.getBBox().width + this.rectHorizontalPadding;
      }
      return 0;
    }

    /** The height to draw the rectangle that acts as the background of the displayed text, if any. */
    get rectHeight() {
      // Hack: the check for this.text forces the bbox to be recomputed (refs aren't reactive!)
      if (this.isMounted && this.text) {
        return this.$refs.text.getBBox().height + this.rectVerticalPadding;
      }
      return 0;
    }

    /** The computed path of the line between the source and target. */
    get path() {
      if(this.adjustedX1 === this.adjustedX2 && this.adjustedY1 === this.adjustedY2)
      {
        return (
        "M" +
        this.adjustedX1 +
        "," +
        this.adjustedY1 +
        "L" +
        String(this.adjustedX1 + 60) +
        "," +
        String(this.adjustedY1 + 60) +

        "M" +
        this.adjustedX1 +
        "," +
        this.adjustedY1 +
        "L" +
        String(this.adjustedX1 + 60) +
        "," +
        String(this.adjustedY1 - 60) +

        "M" +
        String(this.adjustedX1 + 60) +
        "," +
        String(this.adjustedY1 + 60) +
        "L" +
        String(this.adjustedX1 + 60) +
        "," +
        String(this.adjustedY1 - 60)
      );
      } else return (
        "M" +
        this.adjustedX1 +
        "," +
        this.adjustedY1 +
        "L" +
        this.adjustedX2 +
        "," +
        this.adjustedY2
      );
    }

    /** The length of the path. This is computed using the original x and y coordinates, not the adjusted ones. */
    get pathLength() {
      return Math.sqrt(this.deltaX * this.deltaX + this.deltaY * this.deltaY);
    }
  }

</script>

<style scoped>
    text {
        user-select: none;
        background: none;
        cursor: default;
    }
    .textstroke{
      text-shadow: -1px -1px 0 black,
                    0   -1px 0 black,
                    1px -1px 0 black,
                    1px  0   0 black,
                    1px  1px 0 black,
                    0    1px 0 black,
                   -1px  1px 0 black,
                   -1px  0   0 black;

    }
</style>
