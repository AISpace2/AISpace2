<template>
  <g @mouseover="$emit('mouseover', $event)" @mouseout="$emit('mouseout', $event)" @click="$emit('click', $event)">
    <slot></slot>
  </g>
</template>

<script lang="ts">
/** Events Emitted */
/**
 * All of the below events receive MouseEvent as the first argument.
 * 'mouseover'
 * 'mouseout'
 * 'click'
 */
export default {};
</script>
