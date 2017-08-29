/** Events that can be received from the backend. */

export interface IEvent {
  action: string;
}

export interface IOutputEvent extends IEvent {
  action: "output";
  text: string;
}

export type Events = IOutputEvent;
