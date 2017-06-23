import * as Backbone from "backbone";
import * as d3 from "d3";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";

import CSPBuilderModel from "./CSPBuilderModel";
import GraphBuilder from "./GraphBuilder";

export default class CSPBuilder extends widgets.DOMWidgetView {
    public model: CSPBuilderModel;
    private visualizer: GraphBuilder;

    public initialize(opts: any) {
        super.initialize(opts);

        this.visualizer = new GraphBuilder();
    }

    public render() {
        this.$el.html("<div id='svg' tabindex='0'></div>");
        d3.timeout(() => {
            this.visualizer.render(this.model.get("csp"), this.$("#svg")[0]);
        });
        return this;
    }
}
