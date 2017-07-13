<template>
    <g>
        <ellipse rx="40" ry="30" cx="0" cy="0" fill="gold" :stroke="focus ? 'deeppink' : 'black'"></ellipse>
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
      focus: {
        type: Boolean,
        required: false,
        default: false
      }
    }
  }
</script>
