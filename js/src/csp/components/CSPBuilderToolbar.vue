<template>
  <span>
    <span class="radioInputGroup">
      <input type="radio" id="one" value="create" v-model="picked" />
      <label for="one">Create</label>
    </span>
    <span class="radioInputGroup">
      <input type="radio" id="zero" value="select" v-model="picked" />
      <label for="zero">Select</label>
    </span>
    <span class="radioInputGroup">
      <input type="radio" id="three" value="set_prob" v-model="picked" />
      <label for="three">Set Probability Table</label>
    </span>
    <span class="radioInputGroup">
      <input type="radio" id="two" value="delete" v-model="picked" />
      <label for="two">Delete</label>
    </span>
  </span>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

type Mode = "select" | "create" | "delete" | "set_prob";

/**
 * Toolbar to switch between modes while creating a CSP.
 */
@Component
export default class BayesToolbar extends Vue {
  picked: Mode = "create";

  @Watch("picked")
  onPickedChanged() {
    this.$emit("modechanged", this.picked);
  }
}
</script>
