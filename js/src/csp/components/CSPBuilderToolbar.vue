<template>
  <span>
    <input type="radio" id="setRadio" value="select" name="set-radio" v-model="picked">
    <label for="setRadio">Set Property</label>
    <input type="radio" id="variableRadio" value="variable" name="variable-radio" v-model="picked">
    <label for="variableRadio">Create Variable</label>
    <input
      type="radio"
      id="constraintRadio"
      value="constraint"
      name="constraint-radio"
      v-model="picked"
    >
    <label for="constraintRadio">Create Constraint</label>
    <input type="radio" id="edgeRadio" value="edge" name="edge-radio" v-model="picked">
    <label for="edgeRadio">Create Edge</label>
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
