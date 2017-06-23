import * as Backbone from "backbone";
import * as widgets from "jupyter-js-widgets";
import * as _ from "underscore";

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
            csp: {},
        };
    }

    public initialize(attrs: any, opts: any) {
        super.initialize(attrs, opts);
    }
}
