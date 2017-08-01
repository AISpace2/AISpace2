<template>
  <g>
    <rect :width="width" :height="height" :x="-width / 2" :y="-height / 2"
          :fill="fill" :stroke="stroke" :stroke-width="strokeWidth"></rect>
    <text ref="text" x="0" :y="0" :fill="textColour" text-anchor="middle" alignment-baseline="middle">
      {{truncatedText}}
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
  }

  /** Width of the rectangle. */
  get width() {
    return Math.min(Math.max(this.textWidth, 50), this.maxWidth) + 10;
  }

  /** Height of the rectangle. */
  get height() {
    return Math.min(Math.max(this.textHeight, 30), 45) + 5;
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
        ? this.$refs.text.getBoundingClientRect().width
        : 0;
  }

  /**
   * Truncates the text to a certain index if greater than `maxWidth`.
   * Because of the watchers set up on this component, this will be called recursively
   * until the text is less than `maxWidth`.
   */
  truncate(truncateTo: number) {
    Vue.nextTick(() => {
      this.computeWidthAndHeight();

      if (this.textWidth > this.maxWidth) {
        this.truncatedText = `${this.text.substr(0, truncateTo)}…`;
      }
    });
  }

  @Watch("text")
  onTextChanged() {
    // Optimization: We can guess that if the new text is too long,
    // we can chop it off around the previous truncation length
    // Note: we can't just keep track of the index where the truncation happened,
    // and use that to bail out of re-truncating,
    // because if the user edits the beginning of the text, it won't update
    const subStrIndexEstimate = this.truncatedText.length;
    // Update text now so we can test to see if it is too long after re-render
    this.truncatedText = this.text;
    this.truncate(subStrIndexEstimate);
  }

  @Watch("truncatedText")
  onTruncatedTextChanged() {
    this.truncate(this.truncatedText.length - 2);
  }
}

</script>
