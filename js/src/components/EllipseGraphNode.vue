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
   *
   * Events Emitted:
   * - 'updateBounds':
   *       The bounds (size of node) have been updated.
   *       Passes a size object {rx: number, ry: number} as an argument.
   *       To correctly implement automatic node sizing, you should listen for this event and update
   *       the edges to use this information. E.g. for DirectedEdge, update (source|dest)R(x|y) prop.
   */
  @Component
  export default class EllipseGraphNode extends Vue {
    /** The primary text of the node to display. */
    @Prop() text: string;
    /** The secondary text of the node to display. Optional. Only used if a non-null value is provided */
    @Prop({ required: false })
    subtext: string;
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
    @Prop({ default: "black" })
    textColour: string;
    // The size of the text inside the node
    @Prop({default: 10}) textSize: number;
    /** Flag to see if the node is hovered over */
    @Prop({default: false}) hover: boolean

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
      text: SVGTextElement;
      /** A reference to the secondary text element where the subtext is drawn, if subtext is provided. */
      subtext: SVGTextElement;
    };
    mounted() {
      this.truncatedText = this.text;
      this.fitText();
      if (this.subtext != null) {
        this.truncatedSubtext = this.subtext ? this.subtext : "";
        this.fitSubtext();
      }
    }
    /** The maximum of `computedTextWidth` and `computedSubtextWidth`. */
    get computedTotalWidth() {
      return Math.max(this.computedTextWidth, this.computedSubtextWidth);
    }
    /** The size of the node, in terms of it's radius along the x, y axis. */
    get size() {
      var bounds = { rx: 0, ry: 0 };

      if (!this.hover) {
        // Arbitrarily chosen magic constants to make things look good
        bounds = {
          rx: Math.min(Math.max(this.computedTotalWidth, 25), 50),
          ry: Math.min(Math.max(this.computedTotalHeight - 12, 20), 35)
        };
      } else {
        // custom set by user visualizer (i.e. CSPVisualizer.vue)
        bounds = {
          rx: this.computedTotalWidth,
          ry: this.computedTotalHeight
        };
      }
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
          ? this.measureText(this.text)
          : 0;
      const subtextWidth =
        this.$refs.subtext != null
          ? this.measureText(this.subtext)
          : 0;
      this.computedTextWidth = textWidth;
      this.computedSubtextWidth = subtextWidth;
      this.computedTotalHeight = textHeight + subtextHeight;
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
        if (this.computedTextWidth > this.maxWidth) {
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
        if (this.computedTextWidth > this.maxWidth) {
          this._truncateText();
        }
      });
    }
    /**
     * Truncates subtext until it is less than `maxWidth`.
     *
     * This function uses binary search to speed up the truncation.
     */
    _truncateSubtext(lowerBound = 0, upperBound = this.subtext.length) {
      if (lowerBound >= upperBound) return;
      const mid = Math.floor((upperBound + lowerBound) / 2);
      this.truncatedSubtext = `${this.subtext.substr(0, mid + 1)}…`;
      // Vue doesn't update DOM (and thus box sizes) until next tick
      Vue.nextTick(() => {
        this.computeWidthAndHeight();
        if (this.computedSubtextWidth > this.maxWidth) {
          this._truncateSubtext(lowerBound, mid - 1);
        } else {
          this._truncateSubtext(mid + 1, upperBound);
        }
      });
    }
    /**
     * Trims subtext to fit inside the node as necessary.
     */
    fitSubtext() {
      Vue.nextTick(() => {
        this.computeWidthAndHeight();
        if (this.computedSubtextWidth > this.maxWidth) {
          this._truncateSubtext();
        }
      });
    }

    // measure text width in pixels
    measureText(text: string) {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext("2d");
      context.font = this.textSize.toString();
      return context.measureText(text).width;
    }

    @Watch("text")
    onTextChanged() {
      this.truncatedText = this.text;
      this.fitText();
    }
    @Watch("subtext")
    onSubtextChanged() {
      this.truncatedSubtext = this.subtext;
      this.fitSubtext();
    }
  }
</script>