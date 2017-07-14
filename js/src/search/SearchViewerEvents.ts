import { IEvent } from "../Events";

export interface IHighlightNodeEvent extends IEvent {
  action: "highlightNode";
  /** The ID of the node to highlight. */
  nodeId: string;
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

export function isHighlightNodeEvent(
  event: IEvent
): event is IHighlightNodeEvent {
  return event.action === "highlightNode";
}

export function isHighlightPathEvent(
  event: IEvent
): event is IHighlightPathEvent {
  return event.action === "highlightPath";
}

export function isClearEvent(event: IEvent): event is IClearEvent {
  return event.action === "clear";
}
