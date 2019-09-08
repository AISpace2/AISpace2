<template>
  <span>
    <span class="radioInputGroup">
      <input type="radio" id="zero" value="create" v-model="picked" />
      <label for="zero">Create</label>
    </span>
    <span class="radioInputGroup">
      <input type="radio" id="one" value="select" v-model="picked" />
      <label for="one">Select</label>
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

type Mode = "create" | "select" | "delete";

/**
 * Toolbar to switch between modes while creating a CSP.
 */
@Component
export default class SearchToolbar extends Vue {
  picked: Mode = "create";

  @Watch("picked")
  onPickedChanged() {
    this.$emit("modechanged", this.picked);
  }
}
</script>

<style scoped>
</style>
