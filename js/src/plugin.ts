// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import * as packageJSON from "../package.json";

import { Application, IPlugin } from "@phosphor/application";

import { Widget } from "@phosphor/widgets";

import { IJupyterWidgetRegistry } from "@jupyter-widgets/base";

import BayesBuilder from "./bayes/BayesBuilder";
import BayesBuilderModel from "./bayes/BayesBuilderModel";
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

const EXTENSION_SPEC_VERSION = (packageJSON as any).version;
const EXTENSION_ID = (packageJSON as any).jlab_extension_id;

/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default examplePlugin;

/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  app: Application<Widget>,
  registry: IJupyterWidgetRegistry
): void {
  registry.registerWidget({
    name: (packageJSON as any).name,
    version: EXTENSION_SPEC_VERSION,
    exports: {
      BayesBuilder,
      BayesBuilderModel,
      BayesVisualizer,
      BayesVisualizerModel,
      CSPBuilder,
      CSPBuilderModel,
      CSPViewer,
      CSPViewerModel,
      SearchBuilder,
      SearchBuilderModel,
      SearchViewer,
      SearchViewerModel
    }
  });
}

/* tslint:enable */
