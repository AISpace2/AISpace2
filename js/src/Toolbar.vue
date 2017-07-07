<template>
  <div>
    <input type="radio" id="one" value="variable" v-model="picked">
    <label for="one">Variable</label>
    <input type="radio" id="two" value="constraint" v-model="picked">
    <label for="two">Constraint</label>
    <input type="radio" id="three" value="edge" v-model="picked">
    <label for="three">Edge</label>
  </div>
</template>

<script>
  export default {
    name: 'toolbar',
    props: ['mode'],
    data() {
      return {
        picked: 'variable'
      }
    },
    watch: {
      'picked': function() {
        this.$emit('modechanged', this.picked);
      }
    }
  }
</script>

<style scoped>
</style>
