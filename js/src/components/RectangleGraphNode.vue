<template>
  <g @click="isExpanded = !isExpanded" :id="id">
    <rect :width="size.width" :height="size.height" :x="-size.width / 2" :y="-size.height / 2" :fill="fill" :stroke="stroke" :stroke-width="strokeWidth"></rect>
    <text ref="text" x="0" :y="0" :fill="textColour" text-anchor="middle" :font-size="textSize" alignment-baseline="middle">
      {{displayText}}
    </text>
  </g>
</template>

<script lang="ts">
  import Vue, { ComponentOptions } from "vue";
  import Component from "vue-class-component";
  import { Prop, Watch } from "vue-property-decorator";
  import { without } from "underscore";
  /**
   * A rectangular node that supports one line of text, with automatic truncation and resizing.
   *
   * This is not as robust as EllipseGraphNode. In particularly, it doesn't report size changes,
   * and only supports one line of text.
   */
  @Component
  export default class RectangleGraphNode extends Vue {
    @Prop() id: string;
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
    // Check if this node is hovered by mouse
    @Prop({default: false}) hover: boolean;
    // Display setting for text
    // 0 is hide all text
    // 1 is show truncated version
    // 2 is show all text
    @Prop({default: 0}) detailLevel: number;
    /** The maximum width of the text, in pixels, before truncation occurs. */
    maxWidth = 100;
    /** The text, truncated to `maxWidth`. This text is displayed in the node. */
    truncatedText = "";
    /** The real width, in pixels, of the text. Updated by calling `computeWidthAndHeight()`. */
    textWidth = 0;
    /** The real height, in pixels, of the text. Updated by calling `computeWidthAndHeight()`. */
    textHeight = 0;
    // Minimum text width so that the node doesn't become too small when the text is short
    minTextWidth = 50;
    // Expansion toggle flag
    isExpanded = false;
    padding ={
      // fixed padding to change the width of the graph node
      // reduce padding by making the graph node width smaller or larger with negative or positive extra padding respectively
      // usage: width = width + padding for graph nodes
      // higher number means more width
      widthPadding: 25,

      // extra invisible text size when considering truncating words so it doesn't overflow the graph node
      text: 30,
      subtext: 50,
    };


    $refs: {
      /** A reference to the primary text element where the text is drawn. */
      text: SVGTextElement;
    };
    mounted() {
      this.truncatedText = this.text;
      this.fitText();
    }
    get size() {
      let bounds = {
        width: this.width(),
        height: this.height()
      };
      this.$emit("updateBounds", bounds);
      return bounds;
    }
    get displayText() {
      let text = this.showFullTextFlag() ? this.text : this.truncatedText;
      return this.format(text);
    }
    /* Width of the rounded rectangle */
    width() {
      this.computeWidthAndHeight();
      let widthWithPadding = this.rawWidth + this.padding.widthPadding;

      if (this.showNoTextFlag()) return this.minTextWidth;
      else if (this.showFullTextFlag()) {
        return Math.max(widthWithPadding, this.minTextWidth);
      } else {
        if (widthWithPadding < this.minTextWidth) return this.minTextWidth;
        else if (widthWithPadding > this.maxWidth) return this.maxWidth;
        else return widthWithPadding;
      }
    }
    /** Height of the rectangle. */
    height() {
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
        if (this.$refs.text.getBoundingClientRect().width + this.padding.text > this.maxWidth) {
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
        if (this.showNoTextFlag()) {
          this.truncatedText = "";
        } else if(this.showTruncatedTextFlag()) {
          this.computeWidthAndHeight();
          if (this.$refs.text.getBoundingClientRect().width + this.padding.text > this.maxWidth) {
            this._truncateText();
          }
        }});
    }
    // measure text width in pixels
    measureText(text: string) {
      let canvas = document.createElement('canvas');
      let context = canvas.getContext("2d");
      context!.font = this.textSize.toString() + "px serif";
      return context!.measureText(text).width;
    }
    /* Format text for display purposes
    * Similar to Java data structure's toString methods
    * Effect: remove {, }, ' characters from this.text */
    format(str: string) {
      let characters = str.split("");
      let charsToRemove = ['{', '}', "'"];
      return without(characters, ...charsToRemove).join("");
    }
    showNoTextFlag() {
      return this.detailLevel == 0 && !this.hover && !this.isExpanded;
    }

    showTruncatedTextFlag() {
      return this.detailLevel == 1 && !this.hover && !this.isExpanded;
    }

    showFullTextFlag() {
      return this.detailLevel == 2 || this.hover || this.isExpanded;
    }

    get rawWidth() {
      return this.textWidth;
    }

    @Watch("text")
    onTextChanged() {
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
    }
  }
</script>
