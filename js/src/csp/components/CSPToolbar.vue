<template>
    <span>
        <input type="radio" id="zero" value="select" v-model="picked">
        <label for="zero">Select</label>
        <input type="radio" id="one" value="variable" v-model="picked">
        <label for="one">Variable</label>
        <input type="radio" id="two" value="constraint" v-model="picked">
        <label for="two">Constraint</label>
        <input type="radio" id="three" value="edge" v-model="picked">
        <label for="three">Edge</label>
    </span>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

type Mode = "select" | "variable" | "constraint" | "edge";

/**
 * Toolbar to switch between modes while creating a CSP.
 */
@Component
export default class CSPToolbar extends Vue {
  picked: Mode = "select";

  @Watch("picked")
  onPickedChanged() {
    this.$emit("modechanged", this.picked);
  }
}
</script>

<style scoped>
</style>
