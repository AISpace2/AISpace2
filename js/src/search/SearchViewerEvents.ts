import {IEvent} from "../Events";

export interface IHighlightPathEvent extends IEvent {
    action: "highlightPath";
    /** A list of edge IDs that make up the path. */
    path: string[];
}

export function isHighlightPathEvent(event: IEvent): event is IHighlightPathEvent {
    return event.action === "highlightPath";
}
