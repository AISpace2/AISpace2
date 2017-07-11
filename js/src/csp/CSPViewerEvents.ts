import {IEvent} from "../Events";

export interface ICSPHighlightArcEvent extends IEvent {
    action: "highlightArc";
    /** The ID of the arc to highlight. If null, all arcs are highlighted. */
    arcId: string | null;
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

export interface IOutputEvent extends IEvent {
    action: "output";
    text: string;
}

export function isHighlightArcEvent(event: IEvent): event is ICSPHighlightArcEvent {
    return event.action === "highlightArc";
}

export function isSetDomainEvent(event: IEvent): event is ICSPSetDomainEvent {
    return event.action === "setDomain";
}

export function isOutputEvent(event: IEvent): event is IOutputEvent {
    return event.action === "output";
}
