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
        if (this.startDrag && !this.moved) {
          this.moved = true;
          this.$emit('dragstart')
        }
      },
      mouseup: function (e) {
        // Warning: this method is not guaranteed to be called!
        // For example, if you click on a node, then tab out, mouseup is not called here.
        // For the parent component, you should use the mouseleave DOM event to determine this case,
        // and call the same thing as when you receive the dragend event.
        if (this.startDrag) {
          if (!this.moved) {
            this.$emit("click", e);
          } else {
            this.$emit("dragend");
          }
        }

        this.startDrag = false;
        this.moved = false;
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
