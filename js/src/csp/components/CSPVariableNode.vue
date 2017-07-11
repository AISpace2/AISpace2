<template>
    <g>
        <ellipse rx="40" ry="30" cx="0" cy="0" :fill="ellipseFill" stroke="black"></ellipse>
        <text x="0" y="-8" text-anchor="middle" alignment-baseline="middle" :fill="textFill">{{name}}</text>
        <text class="domain" x="0" y="7" text-anchor="middle" alignment-baseline="middle" :fill="textFill">
            {{domainText}}
        </text>
    </g>
</template>

<script>
  export default {
    props: {
      name: {
        type: String,
        required: true
      },
      domain: {
        type: Array,
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
      domainText: function () {
        return `{${this.domain.join(',')}}`
      },
      ellipseFill: function () {
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