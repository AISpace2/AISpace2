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
    "todo arc": COLOR.BLUE,
    "consistent arc": COLOR.GREEN,
    "inconsistent arc": COLOR.RED
  },

  search: {
    "nodes along path": COLOR.GREY,
    "current path": COLOR.RED,
    "neighbor nodes": COLOR.BLUE,
    "frontier nodes": COLOR.GREEN,
    "start node": COLOR.PURPLE,
    "goal node": COLOR.YELLOW
  }
};

export const cspLabelText = Object.keys(label.csp);
export const cspLabelColor = Object.values(label.csp);

export const searchLabelText = Object.keys(label.search);
export const searchLabelColor = Object.values(label.search);
