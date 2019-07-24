import { ISearchGraphNode } from "../Graph";
import * as labelDict from "../labelDictionary";

/** Returns a formatted string representing the search node's heuristic value. */
export function nodeHText(node: ISearchGraphNode) {
  // Ensures proper rounding for e.g. 8.45 -> 8.5, which fails just using toFixed (8.4)
  return "heur: " + (Math.round(10 * node.h) / 10).toFixed(1);
}

/** Returns the fill colour of a search node based on its type. */
export function nodeFillColour(node: ISearchGraphNode) {
  switch (node.type) {
    case "search:start":
      return labelDict.searchLegend["Start node"];
    case "search:goal":
      return labelDict.searchLegend["Goal node"];
    default:
      return "white";
  }
}
