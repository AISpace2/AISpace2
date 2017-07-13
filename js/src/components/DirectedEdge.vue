<template>
    <g>
        <path :d="path" stroke="black" stroke-width="5" marker-end="url(#marker-end)" :stroke="stroke != null ? stroke : 'black'" :stroke-width="strokeWidth != null ? strokeWidth : 4">
        </path>
        <rect v-if="text" :x="rectX" :y="rectY" :width="rectWidth" :height="rectHeight" fill="white"></rect>
        <text v-if="text" ref="text" :x="centerX" :y="centerY" text-anchor="middle" dominant-baseline="central">{{text}}</text>
    </g>
</template>

<script>
export default {
    computed: {
        centerX() {
            return this.x1 + (this.x2 - this.x1) / 2;
        },
        centerY() {
            return this.y1 + (this.y2 - this.y1) / 2
        },
        rectX() {
            return this.centerX - (this.rectWidth / 2);
        },
        rectY() {
            return this.centerY - (this.rectHeight / 2);
        },
        rectWidth() {
            // Hack: the check for this.text forces the bbox to be recomputed (refs aren't reactive!)
            if (this.isMounted && this.text) {
                return this.$refs.text.getBBox().width + this.rectHorizontalPadding;
            }
            return 0;
        },
        rectHeight() {
            // Hack: the check for this.text forces the bbox to be recomputed (refs aren't reactive!)            
            if (this.isMounted && this.text) {
                return this.$refs.text.getBBox().height + this.rectVerticalPadding;
            }
            return 0;
        },
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
    data() {
        return {
            /** Used to track with this.$refs.text is available. */
            isMounted: false,
            /** The horizontal padding of the rect behind the text. */
            rectHorizontalPadding: 8,
            /** The vertical padding of the rect behind the text. */
            rectVerticalPadding: 2
        };
    },
    mounted() {
        this.isMounted = true;
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
        },
        text: {
            type: [String, Number],
            required: false
        }
    }
}
</script>
