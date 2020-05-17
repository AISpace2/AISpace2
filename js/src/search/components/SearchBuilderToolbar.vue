<template>
    <span>
        <input type="radio" id="zero" value="select" v-model="picked">
        <label for="zero">Select</label>
        <input type="radio" id="one" value="create" v-model="picked">
        <label for="one">Create</label>
        <input type="radio" id="two" value="delete" v-model="picked">
        <label for="two">Delete</label>

    </span>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

type Mode = "select" | "create" | "delete";

/**
 * Toolbar to switch between modes while creating a Search.
 */
@Component
export default class SearchToolbar extends Vue {
  picked: Mode = "select";

  @Watch("picked")
  onPickedChanged() {
    this.$emit("modechanged", this.picked);
  }
}

</script>

<style scoped>
</style>
