import * as Backbone from "backbone";
import * as d3 from "d3";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";

import CSPBuilderModel from "./CSPBuilderModel";
import { IEvent } from "./CSPViewerEvents";
import GraphBuilder from "./GraphBuilder";

declare let Jupyter: any;

export default class CSPBuilder extends widgets.DOMWidgetView {
    private static readonly SHOW_PYTHON_CODE = "python-code";

    public model: CSPBuilderModel;
    private visualizer: GraphBuilder;

    public initialize(opts: any) {
        super.initialize(opts);

        this.visualizer = new GraphBuilder();
        this.visualizer.onUpdate = (graph) => {
            // Must copy CSP to bypass reference check shortcircuiting update
            const cspCopy = JSON.parse(JSON.stringify(graph));
            this.model.graphJSON = cspCopy;
            this.touch();
        };

        this.listenTo(this.model, "view:msg", (event: IEvent) => {
            if (event.action === CSPBuilder.SHOW_PYTHON_CODE) {
                // Replace cell contents with the code
                Jupyter.notebook.get_selected_cell().set_text((event as any).code);
            }
        });
    }

    public render() {
        this.$el.html("<div id='svg' tabindex='0'></div>");
        d3.timeout(() => {
            this.visualizer.render(this.model.graphJSON, this.$("#svg")[0]);
        });
        return this;
    }
}
