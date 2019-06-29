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

export interface IBayesShowPositionsEvent extends IEvent {
  action: "showPositions";
  // The string representing the node positions
  positions: string;
}

/** CSP Visualizer Events. */
export type Events =
  | IBayesObserveEvent
  | IBayesQueryEvent
  | IBayesShowPositionsEvent
  | Events;
