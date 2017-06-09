var widgets = require('jupyter-js-widgets');
var _ = require('underscore');
var Backbone = require('backbone');
// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.
// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var DFSModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'), {
        _model_name : 'DFSModel',
        _view_name : 'DFSView',
        _model_module : 'aispace',
        _view_module : 'aispace',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        value : 'Hello World!!!!'
    })
});

// Custom View. Renders the widget model.
var DFSView = widgets.DOMWidgetView.extend({
    initialize: function() {
        widgets.DOMWidgetView.prototype.initialize.apply(this, arguments);
    },
    render: function() {
        this.$el.html('KING KONG');

        return this;
    }
});

module.exports = {
    DFSModel: DFSModel,
    DFSView: DFSView,
};
