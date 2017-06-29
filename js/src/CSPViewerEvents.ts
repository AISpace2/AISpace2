export interface IEvent {
    action: string;
}

export interface ICSPHighlightArcEvent extends IEvent {
    action: "highlightArc";
    arcId: string;
    style: "normal" | "bold";
    colour: string;
}

export interface ICSPSetDomainEvent extends IEvent {
    action: "setDomain";
    nodeId: string;
    domain: string[];
}

export interface IOutputEvent extends IEvent {
    action: "output";
    result: string;
}

export interface IRerenderEvent extends IEvent {
    action: "rerender";
}

export interface IBeginFuncEvent extends IEvent {
    action: "begin_func";
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

export function isRerenderEvent(event: IEvent): event is IRerenderEvent {
    return event.action === "rerender";
}

export function isBeginFuncEvent(event: IEvent): event is IBeginFuncEvent {
    return event.action === "begin_func";
}
