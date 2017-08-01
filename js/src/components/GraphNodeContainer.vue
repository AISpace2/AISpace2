<template>
  <g :transform="transform"
     @mousedown="mousedown($event)"
     @mousemove="mousemove($event)"
     @mouseup="mouseup($event)"
     @mouseover="$emit('mouseover', $event)"
     @mouseout="$emit('mouseout', $event)"
     :class="{transitions}">
    <slot></slot>
  </g>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

/**
 * A container for nodes with a slot where the actual node is drawn.
 * This container places the node in the correct place and handles mouse events.
 */
@Component
export default class GraphNodeContainer extends Vue {
  /** The x-coordinate, in pixels, where the node is drawn. */
  @Prop() x: number;
  /** The y-coordinate, in pixels, where the node is drawn.*/
  @Prop() y: number;
  /** If true, animates positional changes and other properties of this node. */
  @Prop({default: false})
  transitions: boolean;

  /** True if the user is holding mouse down. */
  mouseDown = false;
  /** True if the mouse has moved since the user has held mouse down. */
  moved = false;

  /** Events Emitted */
  /**
   * 'dragstart': The mouse is down over the node and has moved since.
   * 'dragend': The mouse has been up since the drag started.
   * 'click': The user has clicked on the node. Receives MouseEvent as the first argument.
   * 'mouseover': The mouse is over the node. Receives MouseEvent as the first argument.
   * 'mouseout': The mouse has left the node. Receives MouseEvent as the first argument.
   * 'canTransition': Notifies its parent if it wants transitions enabled.
   *                  Receives a boolean as the first argument.
   *                  If false, requests its parent disables transitions on itself and edges (e.g. for dragging);
   *                  If true, allows the parent to set its transition prop to whatever it wants.
   */

  /** Returns the translation to move this node to the right position. */
  get transform() {
    return `translate(${this.x}, ${this.y})`;
  }

  mousedown(e: MouseEvent) {
    this.mouseDown = true;
    this.moved = false;
    e.preventDefault();
  }

  mousemove(e: MouseEvent) {
    if (this.mouseDown && !this.moved) {
      this.moved = true;
      this.$emit("dragstart");
      this.$emit("canTransition", false);
    }
  }

  mouseup(e: MouseEvent) {
    // Warning: this method is not guaranteed to be called!
    // For example, if you click on a node, then tab out, mouseup is not called here.
    // For the parent component, you should use the mouseleave DOM event to determine this case,
    // and call the same thing as when you receive the dragend event.
    if (this.mouseDown) {
      if (!this.moved) {
        this.$emit("click", e);
      } else {
        this.$emit("dragend");
      }
    }

    this.mouseDown = false;
    this.moved = false;
    this.$emit("canTransition", true);
  }
}
</script>

<style scoped>
  text {
    cursor: default;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
</style>
