/** Events that can be received from the backend. */

import { Events, IEvent } from "../Events";

export interface IHighlightNodeEvent extends IEvent {
  action: "highlightNodes";
  /** The ID of the nodes to highlight. */
  nodeIds: string[];
  /** A HTML colour string that will be used as the stroke of the node. */
  colour: string;
}

export interface IHighlightPathEvent extends IEvent {
  action: "highlightPath";
  /** A list of edge IDs that make up the path. */
  path: string[];
  /** A HTML colour string that will be used as the stroke along the path. */
  colour: string;
}

export interface IClearEvent extends IEvent {
  action: "clear";
}

export interface IUpdateFrontierEvent extends IEvent {
  action: "setFrontier";
  /** The string representing the new frontier. */
  frontier: string;
}

/** Search Visualizer Events. */
export type Events =
  | IHighlightNodeEvent
  | IHighlightPathEvent
  | IClearEvent
  | IUpdateFrontierEvent
  | Events;
