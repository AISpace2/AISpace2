// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
declare let __webpack_public_path__: any;
__webpack_public_path__ =
  document.querySelector("body")!.getAttribute("data-base-url") +
  "nbextensions/aispace2/";

declare let ga: any;

import "./style.css";

import * as packageJSON from "../package.json";
import BayesVisualizer from "./bayes/BayesVisualizer";
import BayesVisualizerModel from "./bayes/BayesVisualizerModel";
import CSPBuilder from "./csp/CSPBuilder";
import CSPBuilderModel from "./csp/CSPBuilderModel";
import CSPViewer from "./csp/CSPVisualizer";
import CSPViewerModel from "./csp/CSPVisualizerModel";
import SearchBuilder from "./search/SearchBuilder";
import SearchBuilderModel from "./search/SearchBuilderModel";
import SearchViewer from "./search/SearchVisualizer";
import SearchViewerModel from "./search/SearchVisualizerModel";

// Export widget models and views, and the npm package version number.
module.exports = {
  BayesVisualizer,
  BayesVisualizerModel,
  CSPBuilder,
  CSPBuilderModel,
  CSPViewer,
  CSPViewerModel,
  SearchBuilder,
  SearchBuilderModel,
  SearchViewer,
  SearchViewerModel,
  version: (packageJSON as any).version
};

/** Google Analytics */
/* tslint:disable */
if (process.env.NODE_ENV !== "development") {
  // Only track in production mode
  (function(i, s, o, g, r, a, m) {
    i["GoogleAnalyticsObject"] = r;
    (i[r] =
      i[r] ||
      function() {
        (i[r].q = i[r].q || []).push(arguments);
      }),
      (i[r].l = 1 * <any>new Date());
    (a = <any>s.createElement(o)), (m = <any>s.getElementsByTagName(o)[0]);
    (<any>a).async = 1;
    (<any>a).src = g;
    (<any>m).parentNode.insertBefore(a, m);
  })(
    window,
    document,
    "script",
    "https://www.google-analytics.com/analytics.js",
    "ga"
  );

  ga("create", "UA-105176225-2", "auto");
  ga("set", "page", window.location.href.split("/").pop());
  ga("send", "pageview");
} else {
  window.ga = (...args: any[]) => {
    console.groupCollapsed("Google Analytics");
    console.log(args);
    console.groupEnd();
  };
}
/* tslint:enable */
