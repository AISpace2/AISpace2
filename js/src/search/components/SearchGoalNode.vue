<template>
  <g>
    <ellipse :rx="size.rx" :ry="size.ry" cx="0" cy="0" fill="gold" :stroke="stroke" :stroke-width="strokeWidth"></ellipse>
    <text ref="text" x="0" y="0" text-anchor="middle" alignment-baseline="middle">{{truncatedName}}</text>
  </g>
</template>

<script>
  import SearchNode from './SearchNode';
  export default new SearchNode();
</script>
