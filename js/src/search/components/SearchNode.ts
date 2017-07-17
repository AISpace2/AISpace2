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
  /** The radius along the x-axis of the ellipse. Will be updated whenever the text changes. */
  rx: number;
  /** The radius along the y-axis of the ellipse. Will be updated whenever the text changes. */
  ry: number;

  /// Computed
  /** The size of the node, in terms of it's radius along the x, y axis. */
  size: { rx: number; ry: number };

  /// Events
  /* 'updateBounds': The bounds have been updated. Passes a size object {rx: number, ry: number} as an argument.
   *                 To correctly implement automatic node sizing, you should listen for this event and update
   *                 the edges to use this information.
   */
}

const SearchNode = {
  computed: {
    size() {
      this.rx = Math.min(Math.max(6 * this.name.length, 30), 45);
      this.ry = this.rx / 1.6;
      const bounds = { rx: this.rx, ry: this.ry };
      this.$emit("updateBounds", bounds);
      return bounds;
    }
  },
  data() {
    return {
      rx: 0,
      ry: 0
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
  }
} as ComponentOptions<ISearchNode>;

/** Common props and data for search nodes.  */
export default function() {
  return Object.assign({}, SearchNode);
}
