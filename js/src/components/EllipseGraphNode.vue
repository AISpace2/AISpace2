<template>
  <g>
    <ellipse :rx="size.rx" :ry="size.ry" cx="0" cy="0" :fill="fill" :stroke="stroke" :stroke-width="strokeWidth"></ellipse>
    <text ref="text" x="0" :y="subtext != null ? 8 : 0" text-anchor="middle" alignment-baseline="middle">{{truncatedText}}</text>
    <text v-if="subtext" ref="subtext" x="0" y="-8" text-anchor="middle" alignment-baseline="middle">{{truncatedSubtext}}</text>
  </g>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";

interface EllipseGraphNode extends Vue {
  /// Props
  /** The primary text of the node to display. */
  text: string;
  /** The secondary text of the node to display. Optional. Only used if a non-null value is provided */
  subtext: string;
  /** A HTML colour string used to outline the node. */
  stroke: string;
  /** The width of the stroke to draw around the node. */
  strokeWidth: number;

  /// Data
  /** The final width, in pixels, of the text element containing the (truncated) text. */
  computedTextWidth: number;
  /** The final width, in pixels, of the subtext element containing the (truncated) subtext. */
  computedSubtextWidth: number;
  /** The total height, in pixels, that the text and subtext (if available) take up. */
  computedTotalHeight: number;
  /** 
   * The maximum width of the text, in pixels, before truncation occurs.
   * `computedTextWidth` and `computedSubtextWidth` should always be less than this.
   */
  maxWidth: number;
  /** The radius along the x-axis of the ellipse. Will be updated whenever the text changes. */
  rx: number;
  /** The radius along the y-axis of the ellipse. Will be updated whenever the text changes. */
  ry: number;
  /** The text, truncated to `maxWidth`. This text is displayed in the node. */
  truncatedText: string;
  /** The subtext, truncated to `maxWidth`. This text is displayed in the node, if subtext is provided. */
  truncatedSubtext: string;

  /// Computed
  /** The maximum of `computedTextWidth` and `computedSubtextWidth`. */
  computedTotalWidth: number;
  /** The size of the node, in terms of it's radius along the x, y axis. */
  size: { rx: number; ry: number };

  /// Methods
  /** 
   * Computes the width and height of the rendered text elements and updates the following:
   * - `computedTextWidth`
   * - `computedSubtextWidth`
   * - `computedTotalHeight`
   * - `computedTotalWidth`
   * 
   * You should call this whenever you change the (sub)text.
   */
  computeWidthAndHeight(): void;
  /**
   * Truncates either the text or subtext to a certain index if greater than `maxWidth`.
   * Because of the watchers set up on this component, this will be called recursively
   * until either the text or subtext is less than `maxWidth`.
   */
  truncate(el: "text" | "subtext", truncateTo: number): void;

  /// Misc
  $refs: {
    /** A reference to the primary text element where the text is drawn. */
    text: SVGTextElement;
    /** A reference to the secondary text element where the subtext is drawn, if subtext is provided. */
    subtext: SVGTextElement;
  };

  /// Events
  /* 'updateBounds': The bounds have been updated. Passes a size object {rx: number, ry: number} as an argument.
   *                 To correctly implement automatic node sizing, you should listen for this event and update
   *                 the edges to use this information.
   */
}

/**
 * An elliptical node that supports two lines of text, with automatic truncation and resizing.
 */
export default {
  mounted() {
    this.truncatedText = this.text;
    this.truncatedSubtext = this.subtext ? this.subtext : "";
  },
  computed: {
    computedTotalWidth() {
      return Math.max(this.computedTextWidth, this.computedSubtextWidth);
    },
    size() {
      // Arbitrarily chosen magic constants to make things look good
      this.rx = Math.min(Math.max(this.computedTotalWidth, 25), 50);
      this.ry = Math.min(Math.max(this.computedTotalHeight - 8, 20), 35);
      const bounds = { rx: this.rx, ry: this.ry };
      this.$emit("updateBounds", bounds);
      return bounds;
    }
  },
  data() {
    return {
      computedTextWidth: 0,
      computedSubtextWidth: 0,
      computedTotalHeight: 0,
      maxWidth: 75,
      rx: 0,
      ry: 0,
      truncatedText: "",
      truncatedSubtext: ""
    };
  },
  props: {
    text: {
      required: true,
      type: String
    },
    subtext: {
      required: false,
      type: String
    },
    fill: {
      default: "white",
      type: String
    },
    stroke: {
      default: "black",
      type: String
    },
    strokeWidth: {
      default: 1,
      type: Number
    }
  },
  methods: {
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
    },
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
            this.computedTextWidth === this.computedTotalWidth
          ) {
            this.truncatedSubtext = `${this.subtext.substr(0, truncateTo)}…`;
          }
        }
      });
    }
  },
  watch: {
    text() {
      // Optimization: We can guess that if the new text is too long,
      // we can chop it off around the previous truncation length
      // Note: we can't just keep track of the index where the truncation happened,
      // and use that to bail out of re-truncating,
      // because if the user edits the beginning of the text, it won't update
      const subStrIndexEstimate = this.truncatedText.length;
      // Update text now so we can test to see if it is too long after re-render
      this.truncatedText = this.text;
      this.truncate("text", subStrIndexEstimate);
    },
    truncatedText() {
      this.truncate("text", this.truncatedText.length - 2);
    },
    subtext() {
      // See comments in text watcher
      const subStrIndexEstimate = this.truncatedSubtext.length;
      this.truncatedSubtext = this.text;
      this.truncate("subtext", subStrIndexEstimate);
    },
    truncatedSubtext() {
      this.truncate("subtext", this.truncatedSubtext.length - 2);
    }
  }
} as ComponentOptions<EllipseGraphNode>;
</script>
