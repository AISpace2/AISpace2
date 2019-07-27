import * as widgets from "@jupyter-widgets/base";
import { timeout } from "d3";
import Vue from "vue";
import { IEvent } from "../Events";
import { Graph, IBayesGraphNode } from "../Graph";
import { d3ForceLayout, GraphLayout, relativeLayout } from "../GraphLayout";
import BayesGraphBuilder from "./components/BayesBuilder.vue";
import BayesBuilderModel from "./BayesBuilderModel";
declare let Jupyter: any;

/**
 * Creates a view to construct a Belief Network. Interfaces with Jupyter backend.
 *
 * See the accompanying backend file: `aispace2/jupyter/bayes/bayesbuilder.py`.
 */
export default class BayesBuilder extends widgets.DOMWidgetView {
  public model: BayesBuilderModel;
  public vue: Vue;

  public initialize(opts: any) {
    super.initialize(opts);
  }

  public render() {
    const initialGraph = this.model.graph;

    timeout(() => {
      this.vue = new BayesGraphBuilder({
        data: {
          graph: initialGraph,
          textSize: this.model.textSize,
          layout: new GraphLayout(d3ForceLayout(), relativeLayout()),
          detailLevel: this.model.detailLevel,
          decimalPlace: this.model.decimalPlace
        },
        watch: {
          graph: {
            handler: (val: Graph, oldVal: Graph) => {
              // Creating a copy is necessary as changes are detected by reference by traitlets
              this.model.graph = Graph.fromJSON(oldVal.toJSON()) as Graph<
                IBayesGraphNode
              >;
              this.touch();
            },
            deep: true
          }
        }
      }).$mount(this.el);
    });

    return this;
  }

  public remove() {
    if (this.vue != null) {
      this.vue.$destroy();
    }
  }
}
