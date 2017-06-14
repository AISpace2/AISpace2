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
var DisplayModel = widgets.WidgetModel.extend({
    defaults: _.extend(_.result(this, 'widgets.WidgetModel.prototype.defaults'), {
        _model_name : 'DisplayModel',
        _model_module : 'aispace',
        _model_module_version : '0.1.0',
    })
});

module.exports = {
    DisplayModel : DisplayModel,
};
