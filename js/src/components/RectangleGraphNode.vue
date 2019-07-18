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
    @Prop({default: 1}) detailLevel: number;
    /** The maximum width of the text, in pixels, before truncation occurs. */
    @Prop({default: 100}) maxWidth: number;
    /** The text, truncated to `maxWidth`. This text is displayed in the node. */
    truncatedText = "";
    /** The real width, in pixels, of the text. Updated by calling `computeWidthAndHeight()`. */
    textWidth = 0;
    /** The real height, in pixels, of the text. Updated by calling `computeWidthAndHeight()`. */
    textHeight = 0;
    // Minimum text width so that the node doesn't become too small when the text is short
    minTextWidth = 15;
    // Expansion toggle flag
    isExpanded = false;
    minHeight = 20;
    // since calculating node height is expensive, do it only when user change text size
    cache = {
      height: -1,
      subHeight: -1,
    };

    padding ={
      // fixed padding to change the width of the graph node
      // reduce padding by making the graph node width smaller or larger with negative or positive extra padding respectively
      // usage: width = width + padding for graph nodes
      // higher number means more width
      widthPadding: 30,
      height: 15,

      // extra invisible text size when considering truncating words so it doesn't overflow the graph node
      text: 2,
      subtext: 0,
    };

    // Constants: keys, flags, etc...
    // DO NOT CHANGE
    flag = {
      TEXT: 0,
      SUBTEXT: 1
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
      let finalWidth = 0;
      if (this.showNoTextFlag() || this.text === "{}") {
        return this.minTextWidth;
      } else if (this.showFullTextFlag()) {
        finalWidth = Math.max(this.rawWidth, this.minTextWidth);
      } else {
        if (this.rawWidth < this.minTextWidth) finalWidth = this.minTextWidth;
        else if (this.rawWidth > this.maxWidth) finalWidth = this.maxWidth;
        else finalWidth = this.rawWidth;
      }

      return finalWidth + this.padding.widthPadding;
    }
    /** Height of the rectangle. */
    height() {
      this.computeWidthAndHeight();
      if (this.showNoTextFlag() || this.text === "{}") {
        return this.minHeight;
      }
      return Math.max(this.textHeight, this.minHeight) + this.padding.height;
    }
    /**
     * Computes the width and height of the rendered text elements and updates the following:
     * - `textHeight`
     * - `textWidth`
     *
     * You should call this whenever you change the text.
     */
    computeWidthAndHeight() {
      if (this.$refs.text === null || this.$refs.text === undefined) {
        this.textHeight = 0;
      } else if (this.cache.height != -1) {
        this.textHeight = this.cache.height;
      } else {
        this.textHeight = this.$refs.text.getBoundingClientRect().height;
      }

      this.textWidth = this.measureTextWidth(this.text);
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

    /*
    Format text for display purposes
    * Similar to Java data structure's toString methods
    * Effect: remove ' characters from this.text
    * Effect: remove prefix { and postfix } from string
    */
    format(str: string) {
      let characters = str.split("");
      let charsToRemove = ["'"];
      let result = without(characters, ...charsToRemove).join("");

      if (result.charAt(0) === '{') result = result.substr(1);
      if (result.charAt(result.length - 1) === '}') result = result.substr(0, result.length - 1);

      return result;
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
      this.measureTextHeight(this.text, this.flag.TEXT);
      this.updateText();
    }

    @Watch("hover")
    onHoverChanged() {
      this.updateText();
    }

    @Watch("detailLevel")
    onDetailLevelChanged() {
      this.updateText();
    }

    @Watch("maxWidth")
    onMaxWidthChanges() {
      this.updateText();
    }

    updateText() {
      this.truncatedText = this.text;
      this.fitText();
    }

    measureTextWidth(text: string) {
      let canvas = document.createElement('canvas');
      let context = canvas.getContext("2d");
      context!.font = this.textSize.toString() + "px serif";
      if(text){
      var splitText : string[] = text.split('\n');
      var measureText : string = splitText[0];
      for(var key of splitText){
          if(measureText.length <= key.length){
              measureText = key;
          }
      }
      }
      return context!.measureText(measureText).width;
    }

    // src: https://stackoverflow.com/questions/16816071/calculate-exact-character-string-height-in-javascript
    measureTextHeight(text: string, flag: number) {
      let width: number = 1500;
      let height: number = 500;

      let canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      let ctx=canvas.getContext("2d");
      if (ctx != null) {
        ctx.save();
        ctx.font = this.textSize.toString() + "px serif";

        ctx.clearRect(0, 0, width, height);
        "ctx.fillText(text, width * 0.1, height / 2);"
        ctx.restore();

        document.body.appendChild(canvas);

        let data = ctx.getImageData(0, 0, width, height).data;
        let topMost = 0;
        let bottomMost = 0;
        let leftMost = 0;
        let rightMost = 0;
        for (let x: number = 0; x < width; x++) {
          for (let y:number = 0; (y < height) && (!leftMost); y++) {
            if (data[this.getAlphaIndexForCoordinates(x, y, width, height)] != 0) {
              leftMost = x;
            }
          }
        }
        for (let y:number = 0; y < height; y++) {
          for (let x:number = 0; (x < width) && (!topMost); x++) {
            if (data[this.getAlphaIndexForCoordinates(x, y, width, height)] != 0) {
              topMost = y;
            }
          }
        }
        for (let x:number = width - 1; x >= 0; x--) {
          for (let y:number = height - 1; (y >= 0) && (!rightMost); y--) {
            if (data[this.getAlphaIndexForCoordinates(x, y, width, height)] != 0) {
              rightMost = x;
            }
          }
        }
        for (let y:number = height - 1; y >= 0; y--) {
          for (let x:number = width - 1; (x >= 0) && (!bottomMost); x--) {
            if (data[this.getAlphaIndexForCoordinates(x, y, width, height)] != 0) {
              bottomMost = y;
            }
          }
        }

        height = bottomMost - topMost + 1;
          
          
        if (flag === this.flag.TEXT) {
          this.cache.height = height;
        } else if (flag === this.flag.SUBTEXT) {
          this.cache.subHeight = height;
        }
      } else {
        return -1;
      }
    }

    getAlphaIndexForCoordinates(x: number, y:number, width:number, height:number) {
      return (((width*4*y)+4*x)+3);
    }
  }
</script>
