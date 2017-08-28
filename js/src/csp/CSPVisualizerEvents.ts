/** Events that can be received from the backend. */

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

export interface ICSPSetDomainsEvent extends IEvent {
  action: "setDomains";
  /** The IDs of the variable node whose domains are to be set. */
  nodeIds: string[];
  /** The new domains of the nodes. */
  domains: string[][];
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

export function isSetDomainsEvent(event: IEvent): event is ICSPSetDomainsEvent {
  return event.action === "setDomains";
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
