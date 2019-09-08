<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import BaseEdge from "./BaseEdge.vue";


/**
 * An edge with an arrow pointing to the target, with support for text.
 */
@Component
export default class DirectedEllipseEdge extends BaseEdge {
  /** The radius along the x-axis of the source node. Defaults to 0 (i.e. drawn at origin of node at x1). */
  @Prop({ default: 0 })
  sourceRx: number;
  /** The radius along the y-axis of the source node. Defaults to 0 (i.e. drawn at origin of node at y1). */
  @Prop({ default: 0 })
  sourceRy: number;
  /** The radius along the x-axis of the target node. Defaults to 0 (i.e. drawn at origin of node at x2). */
  @Prop({ default: 0 })
  targetRx: number;
  /** The radius along the y-axis of the target node. Defaults to 0 (i.e. drawn at origin of node at y2). */
  @Prop({ default: 0 })
  targetRy: number;

  /** The x-coordinate to place the start of the path. It is adjusted to be on the edge of the node. */
  get adjustedX1() {
    //if (this.pathLength === 0) return 0;
    let offsetX = this.deltaX * this.sourceRx / this.pathLength;
    return this.x1 + offsetX;
  }

  /** The y-coordinate to place the start of the path. It is adjusted to be on the edge of the node. */
  get adjustedY1() {
    //if (this.pathLength === 0) return 0;
    let offsetY = this.deltaY * this.sourceRy / this.pathLength;
    return this.y1 + offsetY;
  }

  /** The x-coordinate to place the end of the path. It is adjusted to be on the edge of the node. */
  get adjustedX2() {
    //if (this.pathLength === 0) return 0;
    let offsetX = this.deltaX * this.targetRx / this.pathLength;
    return this.x2 - offsetX;
  }

  /** The y-coordinate to place the end of the path. It is adjusted to be on the edge of the node. */
  get adjustedY2() {
    //if (this.pathLength === 0) return 0;
    let offsetY = this.deltaY * this.targetRy / this.pathLength;
    return this.y2 - offsetY;
  }
}

</script>