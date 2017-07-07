<template>
  <line :x1="x1" :y1="y1" :x2="x2" :y2="y2" :stroke="colour" :stroke-width="thickness" @mouseover="$emit('mouseover', $event)"
        @mouseout="$emit('mouseout', $event)" @click="$emit('click', $event)"></line>
</template>

<script>
  export default {
    name: 'node-link',
    props: {
      x1: {
        type: Number,
        required: true
      },
      y1: {
        type: Number,
        required: true
      },
      x2: {
        type: Number,
        required: true
      },
      y2: {
        type: Number,
        required: true
      },
      colour: {
        type: String,
        required: false,
        default: "black"
      },
      thickness: {
        type: Number,
        required: false,
        default: 4
      }
    }
  }
</script>
