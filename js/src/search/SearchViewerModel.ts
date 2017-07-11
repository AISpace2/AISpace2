import * as widgets from "jupyter-js-widgets";
import {IGraphJSON} from "../Graph";

export default class SearchViewerModel extends widgets.DOMWidgetModel {
    public defaults() {
        return {
            ...super.defaults(),
            _model_module: "aispace",
            _model_module_version: "0.1.0",
            _model_name: "SearchViewerModel",
            _view_module: "aispace",
            _view_module_version: "0.1.0",
            _view_name: "SearchViewer",
            graph_json: ({} as IGraphJSON),
        };
    }

    get graphJSON(): IGraphJSON {
        return this.get("graph_json");
    }

    set graphJSON(val) {
        this.set("graph_json", val);
    }
}
