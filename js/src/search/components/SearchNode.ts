import Vue, { ComponentOptions } from "vue";

interface ISearchNode extends Vue {
  /// Props
  /** The name of the node to display. */
  name: string;
  /** A HTML colour string used to outline the node. */
  stroke: string;
  /** The width of the stroke to draw around the node. */
  strokeWidth: number;

  /// Data
  /** The final width, in pixels, of the text element containing the (truncated) name. */
  computedTextWidth: number;
  /** The maximum width of the text, in pixels, before truncation occurs.
   *  `computedTextWidth` should always be less than this.
   */
  maxWidth: number;
  /** The radius along the x-axis of the ellipse. Will be updated whenever the text changes. */
  rx: number;
  /** The radius along the y-axis of the ellipse. Will be updated whenever the text changes. */
  ry: number;
  /** The name, truncated to `maxWidth`. You should use this for displaying the node's name. */
  truncatedName: string;

  /// Computed
  /** The size of the node, in terms of it's radius along the x, y axis. */
  size: { rx: number; ry: number };

  /// Misc
  $refs: {
    /** A reference to the text element where the name is drawn. */
    text: SVGTextElement
  }

  /// Events
  /* 'updateBounds': The bounds have been updated. Passes a size object {rx: number, ry: number} as an argument.
   *                 To correctly implement automatic node sizing, you should listen for this event and update
   *                 the edges to use this information.
   */
}

const SearchNode = {
  mounted() {
    this.truncatedName = this.name;
  },
  computed: {
    size() {
      // Scale size based off text width
      this.rx = Math.min(Math.max(this.computedTextWidth, 30), 45);
      this.ry = this.rx / 1.6;
      const bounds = { rx: this.rx, ry: this.ry };
      this.$emit("updateBounds", bounds);
      return bounds;
    }
  },
  data() {
    return {
      computedTextWidth: 0,      
      maxWidth: 75,      
      rx: 0,
      ry: 0,
      truncatedName: '',
    };
  },
  props: {
    name: {
      required: true,
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
  watch: {
    name() {
      // Optimization: We can guess that if the new name is too long,
      // we can chop it off around the previous truncation length
      // Note: we can't just keep track of the index where the truncation happened,
      // and use that to bail out of re-truncating,
      // because if the user edits the beginning of the name, it won't update
      const subStrIndexEstimate = this.truncatedName.length;

      // Update name now so we can test to see if it is too long after re-render
      this.truncatedName = this.name;

      // DOM changes aren't available until next tick
      Vue.nextTick(() => {
        if (this.$refs.text.getBoundingClientRect().width > this.maxWidth) {
          // Too long. Begin truncation recursion
          this.truncatedName = `${this.name.substr(0, subStrIndexEstimate)}…`;
        }
      });
    },
    truncatedName(oldVal, newVal) {
      Vue.nextTick(() => {
        this.computedTextWidth = this.$refs.text.getBoundingClientRect().width;

        if (this.computedTextWidth > this.maxWidth) {
          // Setting truncatedName again will cause recursion, chopping off one character at a time
          // until we hit the desired width
          this.truncatedName = `${this.truncatedName.substr(0, this.truncatedName.length - 2)}…`;
        }
      });
    }
  },
} as ComponentOptions<ISearchNode>;

/** Common props and data for search nodes.  */
export default function() {
  return Object.assign({}, SearchNode);
}
