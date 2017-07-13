<template>
    <path :d="path" stroke="black" stroke-width="5" marker-end="url(#marker-end)"></path>
</template>

<script>
export default {
    computed: {
        path() {
            let diffX = this.x2 - this.x1;
            let diffY = this.y2 - this.y1;

            let pathLength = Math.sqrt((diffX * diffX) + (diffY * diffY));

            let offsetX = (diffX * 50) / pathLength;
            let offsetY = (diffY * 40) / pathLength;

            let offsetXSource = (diffX * 40) / pathLength;
            let offsetYSource = (diffY * 30) / pathLength;

            return "M" + (this.x1 + offsetXSource) + "," + (this.y1 + offsetYSource) + "L" + (this.x2 - offsetX) + "," + (this.y2 - offsetY);
        }
    },
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
