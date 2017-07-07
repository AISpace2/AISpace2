<template>
  <g :transform="transform"
     @mousedown="mousedown($event)"
     @mousemove="mousemove($event)"
     @mouseup="mouseup($event)"
     @mouseover="$emit('mouseover', $event)"
     @mouseout="$emit('mouseout', $event)"
  >
    <!--
      <ellipse v-if="type === 'csp:variable'" rx="40" ry="30" cx="0" cy="0" :fill="fill" stroke="black"></ellipse>
      <rect v-if="type === 'csp:constraint'" width="70" height="50" stroke="black" :fill="fill" x="-35" y="-25"></rect>
      <text x="0" y="0" text-anchor="middle" alignment-baseline="middle" :fill="textColor">{{text}}</text> -->
    <slot></slot>
  </g>
</template>

<script>
  export default {
    name: 'circle-node',
    props: ['text', 'x', 'y', 'fill', 'type', 'textColor'],
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
