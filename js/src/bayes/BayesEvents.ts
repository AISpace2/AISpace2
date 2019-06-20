/** Events that can be received from the backend. */

import { Events, IEvent } from "../Events";

export interface IBayesObserveEvent extends IEvent {
  action: "observe";
  /** The name of the selected node */
  name: string;
  /** The observation value made */
  value: any;
}

export interface IBayesQueryEvent extends IEvent {
  action: "query";
  name: string;
  prob: any;
}

/** CSP Visualizer Events. */
export type Events =
  | IBayesObserveEvent
  | IBayesQueryEvent
  | Events;
