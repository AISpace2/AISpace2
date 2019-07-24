const COLOR = {
  BLUE: "#0000FF",
  GREEN: "#008300",
  RED: "#ff0000",
  GREY: "#A8A8A8",
  GOLD: "#FFD700",
  ORCHID: "#DA70D6"
};

const label = {
  csp: {
    "To-do arc": COLOR.BLUE,
    "Consistent arc": COLOR.GREEN,
    "Inconsistent arc": COLOR.RED,
    "Domain-splittable variable": COLOR.ORCHID
  },

  search: {
    "Start node": COLOR.ORCHID, // when you change this key, you need also to change in ./search/SearchUtils.ts
    "Goal node": COLOR.GOLD, // when you change this key, you need also to change in ./search/SearchUtils.ts
    "Frontier node": COLOR.GREEN,
    "Current path": COLOR.RED,
    "Neighbour node": COLOR.BLUE
  },
};

export const cspLabelText = Object.keys(label.csp);
export const cspLabelColor = Object.values(label.csp);

export const searchLabelText = Object.keys(label.search);
export const searchLabelColor = Object.values(label.search);

export const searchLegend = label.search;
export const cspLegend = label.csp;
