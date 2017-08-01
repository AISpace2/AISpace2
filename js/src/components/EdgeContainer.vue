<template>
  <g @mouseover="$emit('mouseover', $event)" @mouseout="$emit('mouseout', $event)" @click="$emit('click', $event)"
     :class="{transition}">
    <slot></slot>
  </g>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";

/** Events Emitted */
/**
 * All of the below events receive MouseEvent as the first argument.
 * 'mouseover'
 * 'mouseout'
 * 'click'
 */
@Component
export default class EdgeContainer extends Vue {
  /** If true, animates positional changes and other properties of the edge. */
  @Prop({default: true})
  transition: boolean;
}
</script>
