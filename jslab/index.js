var aispace = require('aispace');

var jupyterlab_widgets = require('@jupyterlab/nbwidgets');

/**
 * The widget manager provider.
 */
module.exports.default = {
  id: 'jupyter.extensions.aispace',
  requires: [jupyterlab_widgets.INBWidgetExtension],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'aispace',
          version: aispace.version,
          exports: aispace
      });
    },
  autoStart: true
};