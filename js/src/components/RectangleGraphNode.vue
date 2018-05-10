<template>
  <g>
    <rect :width="width" :height="height" :x="-width / 2" :y="-height / 2" :fill="fill" :stroke="stroke" :stroke-width="strokeWidth"></rect>
    <text ref="text" x="0" :y="0" :fill="textColour" text-anchor="middle" :font-size="textSize" alignment-baseline="middle">
      {{displayText}}
    </text>
    <title>{{text}}</title>
  </g>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

/**
 * A rectangular node that supports one line of text, with automatic truncation and resizing.
 * 
 * This is not as robust as EllipseGraphNode. In particularly, it doesn't report size changes,
 * and only supports one line of text.
 */
@Component
export default class RectangleGraphNode extends Vue {
  /** The primary text of the node to display. */
  @Prop() text: string;
  /** A HTML colour string used for the node's fill colour. */
  @Prop({ default: "white" })
  fill: string;
  /** A HTML colour string used to outline the node. */
  @Prop({ default: "black" })
  stroke: string;
  /** The width of the stroke to draw around the node. */
  @Prop({ default: 1 })
  strokeWidth: number;
  /** The colour of the text inside the node. */
  @Prop({ default: "black" })
  textColour: string;
  // The size of the text inside the node
  @Prop({default: 15}) textSize: number;
  @Prop({default: false}) hover: boolean;

  /** The maximum width of the text, in pixels, before truncation occurs. */
  maxWidth = 90;
  /** The text, truncated to `maxWidth`. This text is displayed in the node. */
  truncatedText = "";
  /** The real width, in pixels, of the text. Updated by calling `computeWidthAndHeight()`. */
  textWidth = 0;
  /** The real height, in pixels, of the text. Updated by calling `computeWidthAndHeight()`. */
  textHeight = 0;

  $refs: {
    /** A reference to the primary text element where the text is drawn. */
    text: SVGTextElement;
  };

  mounted() {
    this.truncatedText = this.text;
    this.fitText();
  }

  /** Width of the rectangle. */
  get width() {
    this.computeWidthAndHeight();
    if (this.hover){
      return this.textWidth;
    } else {
      return Math.min(Math.max(this.textWidth, 50), this.maxWidth) + 10;
    }
  }

  /** Height of the rectangle. */
  get height() {
    return Math.min(Math.max(this.textHeight, 30), 45) + 5;
  }

  get displayText() {
    return this.hover ? this.text : this.truncatedText;
  }

  /**
   * Computes the width and height of the rendered text elements and updates the following:
   * - `textHeight`
   * - `textWidth`
   *
   * You should call this whenever you change the text.
   */
  computeWidthAndHeight() {
    this.textHeight =
      this.$refs.text != null
        ? this.$refs.text.getBoundingClientRect().height
        : 0;
    this.textWidth =
      this.$refs.text != null
        ? this.measureText(this.text)
        : 0;
  }

  /**
   * Truncates text until it is less than `maxWidth`.
   * 
   * This function uses binary search to speed up the truncation.
   */
  _truncateText(lowerBound = 0, upperBound = this.text.length) {
    if (lowerBound >= upperBound) return;

    const mid = Math.floor((upperBound + lowerBound) / 2);
    this.truncatedText = `${this.text.substr(0, mid + 1)}…`;

    // Vue doesn't update DOM (and thus box sizes) until next tick
    Vue.nextTick(() => {
      this.computeWidthAndHeight();
      if (this.textWidth > this.maxWidth) {
        this._truncateText(lowerBound, mid - 1);
      } else {
        this._truncateText(mid + 1, upperBound);
      }
    });
  }

  /**
   * Trims text to fit inside the node as necessary.
   */
  fitText() {
    Vue.nextTick(() => {
      this.computeWidthAndHeight();
      if (this.textWidth > this.maxWidth) {
        this._truncateText();
      }
    });
  }

  // measure text width in pixels
  measureText(text) {
    let canvas = document.createElement('canvas');
    let context = canvas.getContext("2d");
    context.font = this.textSize.toString() + "pt serif";
    return context.measureText(text).width;
  }

  @Watch("text")
  onTextChanged() {
    this.truncatedText = this.text;
    this.fitText();
  }
}

</script>
