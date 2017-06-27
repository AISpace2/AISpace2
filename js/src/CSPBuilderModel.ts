import * as Backbone from "backbone";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";
import { IEvent } from "./CSPViewerEvents";
import { IGraph } from "./Graph";

export default class CSPBuilderModel extends widgets.DOMWidgetModel {
    public defaults() {
        return {
            ...super.defaults(),
            _model_module: "aispace",
            _model_module_version: "0.1.0",
            _model_name: "CSPBuilderModel",
            _view_module: "aispace",
            _view_module_version: "0.1.0",
            _view_name: "CSPBuilder",
            graphJSON: ({} as IGraph),
        };
    }

    public initialize(attrs: any, opts: any) {
        super.initialize(attrs, opts);

        this.listenTo(this, "msg:custom", (event: IEvent) => {
            this.trigger("view:msg", event);
        });
    }

    get graphJSON(): IGraph {
        return this.get("graphJSON");
    }

    set graphJSON(val) {
        this.set("graphJSON", val);
    }
}
