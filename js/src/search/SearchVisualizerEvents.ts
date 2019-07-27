/** Events that can be received from the backend. */

import { Events, IEvent } from "../Events";

export interface ISearchHighlightNodeEvent extends IEvent {
  action: "highlightNodes";
  // The ID of the nodes to highlight
  nodeIds: string[];
  // A HTML colour string that will be used as the stroke of the node
  colour: string;
}

export interface ISearchHighlightPathEvent extends IEvent {
  action: "highlightPath";
  // A list of edge IDs that make up the path
  path: string[];
  // A HTML colour string that will be used as the stroke along the path
  colour: string;
}

export interface ISearchClearEvent extends IEvent {
  action: "clear";
}

export interface ISearchUpdateFrontierEvent extends IEvent {
  action: "setFrontier";
  // The string representing the new frontier
  frontier: string;
}

export interface ISearchSetPreSolutionEvent extends IEvent {
  action: "setPreSolution";
  // The string representing the new solution
  solution: string;
  // The cost of the solution
  cost: number;
}

export interface ISearchShowPositionsEvent extends IEvent {
  action: "showPositions";
  // The string representing the node positions
  positions: string;
}

// Search Visualizer Events
export type Events =
  | ISearchHighlightNodeEvent
  | ISearchHighlightPathEvent
  | ISearchClearEvent
  | ISearchUpdateFrontierEvent
  | ISearchSetPreSolutionEvent
  | ISearchShowPositionsEvent
  | Events;
