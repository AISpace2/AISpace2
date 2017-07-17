<template>
  <line
    :x1="x1" :y1="y1" :x2="x2" :y2="y2" :stroke="stroke"
    :stroke-width="strokeWidth">
  </line>
</template>

<script>
  export default {
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
      stroke: {
        type: String,
        required: false,
        default: "black"
      },
      strokeWidth: {
        type: Number,
        required: false,
        default: 4
      },
      hover: {
        type: Boolean,
        required: false,
        default: false
      }
    }
  }
</script>
