const COLOR = {
  BLUE: "#0000FF",
  GREEN: "#008300",
  RED: "#ff0000",
  GREY: "#A8A8A8",
  YELLOW: "#FFD700",
  PURPLE: "#dc7cf4"
};

const label = {
  csp: {
    "To-do arc": COLOR.BLUE,
    "Consistent arc": COLOR.GREEN,
    "Inconsistent arc": COLOR.RED,
    "Domain-splittable nodes": COLOR.PURPLE
  },

  search: {
    "Current path": COLOR.RED,
    "Neighbor nodes": COLOR.BLUE,
    "Frontier nodes": COLOR.GREEN,
    "Start node": COLOR.PURPLE,
    "Goal nodes": COLOR.YELLOW
  },
};

export const cspLabelText = Object.keys(label.csp);
export const cspLabelColor = Object.values(label.csp);

export const searchLabelText = Object.keys(label.search);
export const searchLabelColor = Object.values(label.search);
