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
    }),
    initialize: function() {
        DisplayModel.__super__.initialize.apply(this, arguments);
        this.on('change:value', this.value_changed, this);
        this.listenTo(this, 'msg:custom', data => {
            if (data.action === 'highlightArc') {
                Backbone.trigger('action:highlightArc', data)
            } else if (data.action === 'reduceDomain') {
                Backbone.trigger('action:reduceDomain', data);
            } else if (data.action === 'output') {
                Backbone.trigger('action:output', {text: data.result, process_id: data.process_id});
            }
        });
    }
});

module.exports = {
    DisplayModel : DisplayModel,
};
