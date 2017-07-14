<template>
  <g>
    <rect width="70" height="50" stroke="black" :fill="rectFill" x="-35" y="-25"></rect>
    <text x="0" y="0" text-anchor="middle" alignment-baseline="middle" :fill="textFill">A {{constraint}} 0</text>
  </g>
</template>

<script>
  export default {
    props: {
      name: {
        type: String,
        required: true
      },
      constraint: {
        type: String,
        required: true
      },
      focus: {
        type: Boolean,
        default: false,
        required: false
      },
      hover: {
        type: Boolean,
        default: false,
        required: false,
      }

    },
    computed: {
      rectFill: function () {
        if (this.focus) {
          return 'pink';
        }

        if (this.hover) {
          return 'black';
        }

        return 'white';
      },
      textFill: function () {
        if (this.hover) {
          return 'white';
        }

        return 'black';
      }
    }
  }
</script>
