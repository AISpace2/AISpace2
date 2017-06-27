import * as Backbone from "backbone";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";

import { IEvent } from "./CSPViewerEvents";
import { IGraph } from "./Graph";

export default class CSPViewerModel extends widgets.DOMWidgetModel {
    public defaults() {
        return {
            ...super.defaults(),
            _model_module: "aispace",
            _model_module_version: "0.1.0",
            _model_name: "CSPViewerModel",
            _view_module: "aispace",
            _view_module_version: "0.1.0",
            _view_name: "CSPViewer",
            initial_render: true,
        };
    }

    public initialize(attrs: any, opts: any) {
        super.initialize(attrs, opts);

        // Forward message to views
        this.listenTo(this, "msg:custom", (event: IEvent) => {
            // We don't register a listener for Python messages (which go to the model) in the view,
            // because each new view would attach a new listener.
            // Instead, we register it once here, and broadcast it to views.
            this.trigger("view:msg", event);
        });
    }

    /** True if this model has not been rendered in any cell yet.
     *
     * This is used to work around timing issues: when the model is initialized,
     * the views may not be created, so sending a re-render message (to trigger the initial state)
     * doesn't work. Neither does sending a message from Python, for the same reason.
     * Instead, check if a view has rendered this model yet. If not, render the initial state.
     */
    get initial_render(): boolean {
        return this.get("initial_render");
    }

    set initial_render(val: boolean) {
        this.set("initial_render", val);
    }

    /** The base line width of the graph to draw. Bold arcs will be several pixels thicker than this. */
    get lineWidth(): number {
        return this.get("line_width");
    }

    /** The JSON representing the CSP graph. */
    get graphJSON(): IGraph {
        return this.get("graphJSON");
    }
}
