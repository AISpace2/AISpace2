import { IEvent } from "../Events";

export interface ICSPHighlightArcsEvent extends IEvent {
  action: "highlightArcs";
  /** The IDs of the arc to highlight. If null, all arcs are highlighted. */
  arcIds: string[] | null;
  /** The thickness of the highlight. */
  style: "normal" | "bold";
  /** The colour of the highlight. */
  colour: string;
}

export interface ICSPSetDomainEvent extends IEvent {
  action: "setDomain";
  /** The ID of the variable node whose domain is to be set. */
  nodeId: string;
  /** The new domain of the node. */
  domain: string[];
}

export interface ICSPHighlightNodesEvent extends IEvent {
  action: "highlightNodes";
  /** The IDs of the nodes to highlight. */
  nodeIds: string[];
  /** The colour of the highlight. */
  colour: string;
}

export interface ICSPChooseDomainSplitEvent extends IEvent {
  action: "chooseDomainSplit";
  /** The domain to choose a split from. */
  domain: string[];
}

export function isHighlightArcsEvent(
  event: IEvent
): event is ICSPHighlightArcsEvent {
  return event.action === "highlightArcs";
}

export function isSetDomainEvent(event: IEvent): event is ICSPSetDomainEvent {
  return event.action === "setDomain";
}

export function isHighlightNodesEvent(
  event: IEvent
): event is ICSPHighlightNodesEvent {
  return event.action === "highlightNodes";
}

export function isChooseDomainSplitEvent(
  event: IEvent
): event is ICSPChooseDomainSplitEvent {
  return event.action === "chooseDomainSplit";
}
