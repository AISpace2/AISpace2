<template>
  <g @click="isExpanded = !isExpanded" :id="id">
    <rect :width="size.width" :height="size.height"
          :x="-size.width/2" :y="-size.height/2"
          :fill="fill" :stroke="stroke" :stroke-width="strokeWidth" :rx="this.showFullTextFlag() ? 30 : 25"></rect>

    <text id="text" :font-size="textSize" ref="text" x="0" :y="subtext != null ? -8 : 0" :fill="textColour" text-anchor="middle" alignment-baseline="middle">
      {{displayText}}
    </text>
    <text :v-show="subtext !== undefined" id="subtext" :font-size="textSize"  v-if="subtext != null" ref="subtext" x="0" y="8" :fill="textColour" text-anchor="middle" alignment-baseline="middle" style="white-space: pre;">
      {{displaySubText}}
    </text>
  </g>
</template>

<script lang="ts">
  import Vue, { ComponentOptions } from "vue";
  import Component from "vue-class-component";
  import { Prop, Watch } from "vue-property-decorator";
  import RectangleGraphNode from "./RectangleGraphNode.vue";
  /**
   * An elliptical node that supports two lines of text, with automatic truncation and resizing.
   *
   * Events Emitted:
   * - 'updateBounds':
   *       The bounds (size of node) have be    en updated.
   *       Passes a size object {rx: number, ry: number} as an argument.
   *       To correctly implement automatic node sizing, you should listen for this event and update
   *       the edges to use this information. E.g. for DirectedEdge, update (source|dest)R(x|y) prop.
   */
  @Component
  export default class RoundedRectangleGraphNode extends RectangleGraphNode {
    @Prop({ required: false})
    subtext: string;
    /** The final width, in pixels, of the text element containing the (truncated) text. */
    computedTextWidth = 0;
    /** The final width, in pixels, of the subtext element containing the (truncated) subtext. */
    computedSubtextWidth = 0;
    /** The total height, in pixels, that the text and subtext (if available) take up. */
    computedTotalHeight = 0;
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
      this.measureTextHeight(this.text, this.flag.TEXT);
      this.measureTextHeight(this.subtext, this.flag.SUBTEXT);
    }
    /** The maximum of `computedTextWidth` and `computedSubtextWidth`. */
    get computedTotalWidth() {
      return Math.max(this.computedTextWidth, this.computedSubtextWidth);
    }
    get displaySubText() {
      let text = this.showFullTextFlag() ? this.subtext : this.truncatedSubtext;
      return this.format(text);
    }

    /**
     * Computes the width and height of the rendered text elements and updates the following:
     * - `computedTextWidth`
     * - `computedSubtextWidth`
     * - `computedTotalHeight`
     * - `computedTotalWidth`
     *
     * You should call this whenever you change the (sub)text.
     * Changed from using getBoundingClientRect().width to measureText
     * that uses canvas to measure the width of the text content itself
     *
     * This is due to long subtext exceeding the space allocated to the textbox itself
     */
    computeWidthAndHeight() {
      let textHeight, textWidth, subtextHeight, subtextWidth = 0;

      if (this.$refs.text === null || this.$refs.text === undefined) {
        textHeight = 0;
      } else if (this.cache.height != -1) {
        textHeight = this.cache.height;
      } else {
        textHeight = this.$refs.text.getBoundingClientRect().height;
      }

      textWidth = this.measureTextWidth(this.text);

      if (this.$refs.subtext === null || this.$refs.subtext === undefined) {
        subtextHeight = 0;
      } else if (this.cache.subHeight != -1) {
        subtextHeight = this.cache.subHeight;
      } else {
        subtextHeight = this.$refs.subtext.getBoundingClientRect().height;
      }

      subtextWidth = this.measureTextWidth(this.subtext);

      this.computedTextWidth = textWidth;
      this.computedSubtextWidth = subtextWidth;
      this.computedTotalHeight = textHeight + subtextHeight;
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
        if (this.$refs.subtext.getBoundingClientRect().width + this.padding.subtext > this.maxWidth) {
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
        if(this.$refs.subtext === undefined) return;
        if (this.showNoTextFlag()) {
          this.truncatedSubtext = "";
        } else {
          this.computeWidthAndHeight();
          if (this.$refs.subtext.getBoundingClientRect().width + this.padding.subtext > this.maxWidth) {
            this._truncateSubtext();
          }}
      });
    }

    get rawWidth() {
      return this.computedTotalWidth;
    }

    @Watch("subtext")
    onSubtextChanged() {
      this.truncatedSubtext = this.subtext;
      this.fitSubtext();
    }

    @Watch("textSize")
    onTextSizeChange() {
      this.measureTextHeight(this.text, this.flag.TEXT);
      this.measureTextHeight(this.subtext, this.flag.SUBTEXT);
      this.updateText();
    }

    @Watch("detailLevel")
    onDetailLevelChanged() {
      this.updateText();
    }

    updateText() {
      this.truncatedText = this.text;
      this.fitText();
      this.truncatedSubtext = this.subtext;
      this.fitSubtext();
    }
  }
</script>
