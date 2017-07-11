// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
declare let __webpack_public_path__: any;
__webpack_public_path__ = document.querySelector("body")!.getAttribute("data-base-url") + "nbextensions/aispace/";

import "./style.css";

import * as packageJSON from "../package.json";
import CSPBuilder from "./csp/CSPBuilder";
import CSPBuilderModel from "./csp/CSPBuilderModel";
import CSPViewer from "./csp/CSPViewer";
import CSPViewerModel from "./csp/CSPViewerModel";

// Export widget models and views, and the npm package version number.
module.exports = {
    CSPBuilder,
    CSPBuilderModel,
    CSPViewer,
    CSPViewerModel,
    version: (packageJSON as any).version,
};
