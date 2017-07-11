export interface IEvent {
    action: string;
}

export interface IOutputEvent extends IEvent {
    action: "output";
    text: string;
}

export function isOutputEvent(event: IEvent): event is IOutputEvent {
    return event.action === "output";
}
