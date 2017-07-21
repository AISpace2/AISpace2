<template>
  <g>
    <ellipse :rx="size.rx" :ry="size.ry" cx="0" cy="0" :fill="fill" :stroke="stroke" :stroke-width="strokeWidth"></ellipse>
    <text ref="text" x="0" :y="subtext != null ? -8 : 0" :fill="textColour" text-anchor="middle" alignment-baseline="middle">
      {{truncatedText}}
    </text>
    <text v-if="subtext != null" ref="subtext" x="0" y="8" :fill="textColour" text-anchor="middle" alignment-baseline="middle">
      {{truncatedSubtext}}
    </text>
    <title>{{text}}</title>
  </g>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

/**
 * An elliptical node that supports two lines of text, with automatic truncation and resizing.
 */
@Component
export default class EllipseGraphNode extends Vue {
  /** The primary text of the node to display. */
  @Prop() text: string;
  /** The secondary text of the node to display. Optional. Only used if a non-null value is provided */
  @Prop() subtext: string;
  /** A HTML colour string used for the node's fill colour. */
  @Prop({ default: "white" })
  fill: string;
  /** A HTML colour string used to outline the node. */
  @Prop({ default: "black" })
  stroke: string;
  /** The width of the stroke to draw around the node. */
  @Prop({ default: 1 })
  strokeWidth: number;
  /** The colour of the (sub)text inside the node. */
  @Prop({default: 'black'})
  textColour: string;

  /** The final width, in pixels, of the text element containing the (truncated) text. */
  computedTextWidth = 0;
  /** The final width, in pixels, of the subtext element containing the (truncated) subtext. */
  computedSubtextWidth = 0;
  /** The total height, in pixels, that the text and subtext (if available) take up. */
  computedTotalHeight = 0;
  /** The maximum width of the text, in pixels, before truncation occurs. */
  maxWidth = 75;
  /** The radius along the x-axis of the ellipse. Will be updated whenever the text changes. */
  rx = 0;
  /** The radius along the y-axis of the ellipse. Will be updated whenever the text changes. */
  ry = 0;
  /** The text, truncated to `maxWidth`. This text is displayed in the node. */
  truncatedText = "";
  /** The subtext, truncated to `maxWidth`. This text is displayed in the node, if subtext is provided. */
  truncatedSubtext = "";

  $refs: {
    /** A reference to the primary text element where the text is drawn. */
    text: SVGTextElement,
    /** A reference to the secondary text element where the subtext is drawn, if subtext is provided. */
    subtext: SVGTextElement
  };

  /** Emitted Events */
  /* 'updateBounds': The bounds have been updated. Passes a size object {rx: number, ry: number} as an argument.
   *               To correctly implement automatic node sizing, you should listen for this event and update
   *               the edges to use this information.
   */

  mounted() {
    this.truncatedText = this.text;
    this.truncatedSubtext = this.subtext ? this.subtext : "";
  }

  /** The maximum of `computedTextWidth` and `computedSubtextWidth`. */
  get computedTotalWidth() {
    return Math.max(this.computedTextWidth, this.computedSubtextWidth);
  }

  /** The size of the node, in terms of it's radius along the x, y axis. */
  get size() {
    // Arbitrarily chosen magic constants to make things look good
    this.rx = Math.min(Math.max(this.computedTotalWidth, 25), 50);
    this.ry = Math.min(Math.max(this.computedTotalHeight - 12, 20), 35);
    const bounds = { rx: this.rx, ry: this.ry };
    this.$emit("updateBounds", bounds);
    return bounds;
  }

  /**
   * Computes the width and height of the rendered text elements and updates the following:
   * - `computedTextWidth`
   * - `computedSubtextWidth`
   * - `computedTotalHeight`
   * - `computedTotalWidth`
   *
   * You should call this whenever you change the (sub)text.
   */
  computeWidthAndHeight() {
    const textHeight =
      this.$refs.text != null
        ? this.$refs.text.getBoundingClientRect().height
        : 0;
    const subtextHeight =
      this.$refs.subtext != null
        ? this.$refs.subtext.getBoundingClientRect().height
        : 0;
    const textWidth =
      this.$refs.text != null
        ? this.$refs.text.getBoundingClientRect().width
        : 0;
    const subtextWidth =
      this.$refs.subtext != null
        ? this.$refs.subtext.getBoundingClientRect().width
        : 0;

    this.computedTextWidth = textWidth;
    this.computedSubtextWidth = subtextWidth;
    this.computedTotalHeight = textHeight + subtextHeight;
  }

  /**
   * Truncates either the text or subtext to a certain index if greater than `maxWidth`.
   * Because of the watchers set up on this component, this will be called recursively
   * until either the text or subtext is less than `maxWidth`.
   */
  truncate(el: "text" | "subtext", truncateTo: number) {
    Vue.nextTick(() => {
      this.computeWidthAndHeight();

      if (this.computedTotalWidth > this.maxWidth) {
        // Find out which element is to blame for going over the max width
        if (
          el === "text" &&
          this.computedTextWidth === this.computedTotalWidth
        ) {
          this.truncatedText = `${this.text.substr(0, truncateTo)}…`;
        }

        if (
          el === "subtext" &&
          this.computedSubtextWidth === this.computedTotalWidth
        ) {
          this.truncatedSubtext = `${this.subtext.substr(0, truncateTo)}…`;
        }
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
    this.truncate("text", subStrIndexEstimate);
  }

  @Watch("truncatedText")
  onTruncatedTextChanged() {
    this.truncate("text", this.truncatedText.length - 2);
  }

  @Watch("subtext")
  onSubtextChanged() {
    // See comments in text watcher
    const subStrIndexEstimate = this.truncatedSubtext.length;
    this.truncatedSubtext = this.subtext;
    this.truncate("subtext", subStrIndexEstimate);
  }

  @Watch("truncatedSubtext")
  onTruncatedSubtextChanged() {
    this.truncate("subtext", this.truncatedSubtext.length - 2);
  }
}
</script>
