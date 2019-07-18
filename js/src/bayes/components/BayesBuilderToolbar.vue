<template>
  <span>
    <input type="radio" id="zero" value="select" v-model="picked" />
    <label for="zero">Select</label>
    <input type="radio" id="one" value="variable" v-model="picked" />
    <label for="one">Variable</label>
    <input type="radio" id="two" value="edge" v-model="picked" />
    <label for="two">Edge</label>
    <input type="radio" id="three" value="delete" v-model="picked" />
    <label for="three">Delete</label>
    <input type="radio" id="four" value="set_prob" v-model="picked" />
    <label for="four">Set Probability Table</label>
  </span>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

type Mode = "select" | "variable" | "edge" | "delete" | "set_prob";

/**
 * Toolbar to switch between modes while creating a CSP.
 */
@Component
export default class BayesToolbar extends Vue {
  picked: Mode = "select";

  @Watch("picked")
  onPickedChanged() {
    this.$emit("modechanged", this.picked);
  }
}
</script>

<style scoped>
</style>

