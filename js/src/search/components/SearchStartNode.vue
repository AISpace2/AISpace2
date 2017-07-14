<template>
  <g>
    <ellipse rx="40" ry="30" cx="0" cy="0" fill="orchid" :stroke="stroke" :stroke-width="strokeWidth"></ellipse>
    <text x="0" y="0" text-anchor="middle" alignment-baseline="middle">{{name}}</text>
  </g>
</template>

<script>
  export default {
    props: {
      name: {
        type: String,
        required: true
      },
      stroke: {
        type: String,
        default: "black"
      },
      strokeWidth: {
        type: Number,
        default: 1
      }
    },
  }
</script>
