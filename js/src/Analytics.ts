/**
 * Uses Google Analytics (loaded in index.ts) to track user events.
 */
declare let ga: any;

/**
 * Tracks the use of an applet.
 * 
 * @param applet The name of the applet being tracked.
 */
export function trackApplet(applet: string) {
  // The "page" is the title of the notebook, plus the applet
  // For example, someone using the CSP applet inside a "Planning as CSP" notebook has page
  // "planning_as_csp.ipynb/csp". This is obviously not foolproof.
  ga("set", "page", `${window.location.href.split("/").pop()}/${applet}`);
  ga("send", "pageview");
}

/**
 * Tracks an event.
 * 
 * Note that Google Analytics has tracking limits (roughly 1 event per second).
 * 
 * @param category The applet being used - e.g. "Search Visualizer"
 * @param action The action being tracked - e.g. "Arc Clicked"
 * @param label Additional information to distinguish the category/action pair.
 */
export function trackEvent(
  category: string,
  action: string,
  label: string = ""
) {
  ga("send", "event", category, action, label);
}
