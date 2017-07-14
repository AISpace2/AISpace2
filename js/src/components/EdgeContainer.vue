<template>
  <g @mouseover="$emit('mouseover', $event)" @mouseout="$emit('mouseout', $event)" @click="$emit('click', $event)">
    <slot></slot>
  </g>
</template>
