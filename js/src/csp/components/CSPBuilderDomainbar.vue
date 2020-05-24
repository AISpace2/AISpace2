<template>
    <span>
        <input type="radio" id="zero" value="number" v-model="picked">
        <label for="zero">Number</label>
        <input type="radio" id="one" value="string" v-model="picked">
        <label for="one">String</label>
        <input type="radio" id="two" value="boolean" v-model="picked">
        <label for="two">Boolean</label>
    </span>
</template>

<script lang="ts">
import Vue, { ComponentOptions } from "vue";
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";

type DomainType = "number" | "string" | "boolean";

/**
 * Toolbar to switch between DomainTypes while creating a CSP.
 */
@Component
export default class CSPToolbar extends Vue {
  picked: DomainType = "number";

  @Watch("picked")
  onPickedChanged() {
    this.$emit("domainTypechanged", this.picked);
  }
}

</script>

<style scoped>
</style>
