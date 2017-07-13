import * as Backbone from "backbone";
import * as widgets from "jupyter-js-widgets";
import Vue from "vue";
import { IEvent, isOutputEvent } from "../Events";
import { Graph, ICSPGraphNode } from "../Graph";
import { d3ForceLayoutEngine } from "../GraphLayout";
import * as StepEvents from "../StepEvents";
import CSPGraphInteractor from "./components/CSPGraphInteractor.vue";
import * as Events from "./CSPViewerEvents";
import CSPViewerModel from "./CSPViewerModel";

export default class CSPViewer extends widgets.DOMWidgetView {
  private static readonly ARC_CLICK = "arc:click";
  private static readonly VAR_CLICK = "var:click";

  public model: CSPViewerModel;

  private vue: any;
  private graph: Graph<ICSPGraphNode>;

  public initialize(opts: any) {
    super.initialize(opts);

    this.graph = Graph.fromJSON(this.model.graphJSON) as Graph<ICSPGraphNode>;

    // Functions called on the Python backend are queued until first render
    if (this.model.initial_render) {
      this.send({ event: "initial_render" });
      this.highlightArc({
        action: "highlightArc",
        arcId: null,
        colour: "blue",
        style: "normal"
      });
    }

    this.listenTo(this.model, "view:msg", (event: IEvent) => {
      // tslint:disable-next-line:no-console
      console.log(event);

      if (Events.isHighlightArcEvent(event)) {
        this.highlightArc(event);
      } else if (Events.isSetDomainEvent(event)) {
        this.setDomain(event);
      } else if (isOutputEvent(event)) {
        this.vue.output = event.text;
      }
    });
  }

  public render() {
    d3ForceLayoutEngine.setup(this.graph, { width: 800, height: 600 });

    const that = this;

    const App = Vue.extend({
      components: { CSPGraphInteractor },
      data() {
        return {
          graph: that.graph,
          output: ""
        };
      },
      methods: {
        autostep() {
          that.send({ event: StepEvents.AUTO_STEP_CLICK });
        },
        finestep() {
          that.send({ event: StepEvents.FINE_STEP_CLICK });
        },
        edge(l: any) {
          that.send({
            constId: l.target.idx,
            event: CSPViewer.ARC_CLICK,
            varId: l.source.name
          });
        },
        step() {
          that.send({ event: StepEvents.STEP_CLICK });
        }
      },
      template: `
                <div id="app">
                    <CSPGraphInteractor
                        :graph="graph"
                        @click:auto-step="autostep"
                        @click:step="step"
                        @click:fine-step="finestep"
                        @click:edge="edge"
                        :output="output">
                    </CSPGraphInteractor>
                </div>`
    });

    this.vue = new App().$mount();
    this.el.appendChild(this.vue.$el);

    return this;
  }

  /**
   * Highlights an arc (or all arcs), as described by the event object.
   */
  private highlightArc(event: Events.ICSPHighlightArcEvent) {
    const strokeWidth = event.style === "bold" ? 7 : 2;

    if (event.arcId == null) {
      for (const edge of this.graph.edges) {
        const stroke = event.colour ? event.colour : edge.styles.stroke;
        Vue.set(edge.styles, "stroke", stroke);
        Vue.set(edge.styles, "strokeWidth", strokeWidth);
      }
    } else {
      const i = this.graph.edges
        .map(a => a.id)
        .findIndex(a => a === event.arcId);
      if (i !== -1) {
        const stroke = event.colour
          ? event.colour
          : this.graph.edges[i].styles.stroke;
        Vue.set(this.graph.edges[i].styles, "stroke", stroke);
        Vue.set(this.graph.edges[i].styles, "strokeWidth", strokeWidth);
      }
    }
  }

  /**
   * Sets the domain of a variable node, as described by the event object.
   */
  private setDomain(event: Events.ICSPSetDomainEvent) {
    const i = this.graph.nodes
      .map(a => a.id)
      .findIndex(a => a === event.nodeId);

    if (i !== -1) {
      this.graph.nodes[i].domain = event.domain;
    }
  }
}
