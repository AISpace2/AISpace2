<template>
    <g :transform="transform"
       @mousedown="mousedown($event)"
       @mousemove="mousemove($event)"
       @mouseup="mouseup($event)"
       @mouseover="$emit('mouseover', $event)"
       @mouseout="$emit('mouseout', $event)">
        <slot></slot>
    </g>
</template>

<script>
  export default {
    props: ['x', 'y'],
    computed: {
      transform: function () {
        return `translate(${this.x}, ${this.y})`;
      },
    },
    data () {
      return {
        startDrag: false,
        startPos: [],
        moved: false
      }
    },
    methods: {
      mousedown: function (e) {
        this.startDrag = true;
        this.moved = false;
      },
      mousemove: function (e) {
        if (this.startDrag) {
          this.$emit("dragstart", e);
          this.moved = true;
        }
      },
      mouseup: function (e) {
        this.startDrag = false;
        if (!this.moved) {
          this.$emit("click", e);
        } else {
          this.$emit("dragend");
        }
      }
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
