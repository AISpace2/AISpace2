<template>
  <g @click="isExpanded = !isExpanded" :id="id">
    <rect :width="size.width" :height="size.height"
          :x="-size.width/2" :y="-size.height/2"
          :fill="fill" :stroke="stroke" :stroke-width="strokeWidth" :rx="this.showFullTextFlag() ? 30 : 25"></rect>

    <text id="text" :font-size="textSize" ref="text" x="0" :y="subtext != null ? (subtext.length != 0 ? -size.height/2 + textSize : 0) : 0" :fill="textColour" text-anchor="middle" alignment-baseline="middle">
      {{displayText}}
    </text>
    <text :v-show="subtext !== undefined" id="subtext" :font-size="textSize - 2"  v-if="subtext != null" ref="subtext" x="0" :y="-size.height/2 + textSize + 2" :fill="textColour" text-anchor="middle" alignment-baseline="middle">
      <tspan x="0" dy="1.6em" id="subspan" v-for = "key in displayTest" style="white-space: pre; font-weight: bold;">{{key}}</tspan>
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
   *       The bounds (size of node) have been updated.
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
    /** The total width, in pixels, that the text and subtext (if available) take up. */
    computedTotalWidth = 0;    
    /** The subtext, truncated to `maxTextWidth`. This text is displayed in the node, if subtext is provided. */
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
      this.computeWidthAndHeight();
    }

    height() {
      this.computeWidthAndHeight();
      if (this.showNoTextFlag() || this.text === "{}") {
        return this.minHeight;
      }
      return Math.max(this.computedTotalHeight, this.minHeight) + this.padding.heightPadding;
    }

    get displaySubText() {
      let text = this.showFullTextFlag() ? this.subtext : this.truncatedSubtext;
      return this.format(text);
    }

    get displayTest() {
      let text = this.showFullTextFlag() ? this.subtext : this.truncatedSubtext;
      return this.format(text).split('\n');
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
        textWidth = 0;
      } else {
        textHeight = this.$refs.text.getBBox().height;
        textWidth = this.$refs.text.getBBox().width;
      }

      if (this.$refs.subtext === null || this.$refs.subtext === undefined) {
        subtextHeight = 0;
        subtextWidth = 0;
      } else {
        subtextHeight = this.$refs.subtext.getBBox().height;
        subtextWidth = this.$refs.subtext.getBBox().width;
      }

      this.computedTextWidth = textWidth;
      this.computedSubtextWidth = subtextWidth;
      this.computedTotalWidth = Math.max(this.computedTextWidth, this.computedSubtextWidth);
      this.computedTotalHeight = textHeight + subtextHeight;
    }

    /**
     * Truncates subtext until it is less than `maxTextWidth`.
     *
     * This function uses binary search to speed up the truncation.
     */
    _truncateSubtext(lowerBound = 0, upperBound = this.subtext.length) {
      if (lowerBound >= upperBound) return;
      const mid = Math.floor((upperBound + lowerBound) / 2);
      this.truncatedSubtext = `${this.subtext.substr(0, mid + 1)}…`;
      // Vue doesn't update DOM (and thus box sizes) until next tick
      Vue.nextTick(() => {
        if (this.$refs.subtext.getBBox().width + this.padding.subtext > this.maxTextWidth) {
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
        if (this.showNoTextFlag()) {
          this.truncatedSubtext = "";
        } else if (this.showTruncatedTextFlag){
          this.computeWidthAndHeight();
          if (this.$refs.subtext.getBBox().width + this.padding.subtext > this.maxTextWidth) {
            this._truncateSubtext();
          }
        } else if (this.showFullTextFlag()){
          this.computeWidthAndHeight();
        }
      });
    }

    get rawWidth() {
      return this.computedTotalWidth;
    }

    @Watch("subtext")
    onSubtextChanged() {
      this.truncatedSubtext = this.subtext;
      this.fitSubtext();
      this.updateText();
    }

    @Watch("textSize")
    onTextSizeChange() {
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
