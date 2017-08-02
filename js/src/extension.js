// This file contains the javascript that is run when the notebook is loaded.
// It contains some requirejs configuration and the `load_ipython_extension`
// which is required for any notebook extension.

// Configure requirejs
if (window.require) {
  window.require.config({
    map: {
      "*": {
        aispace2: "nbextensions/aispace2/index",
        "jupyter-js-widgets": "nbextensions/jupyter-js-widgets/extension",
        vendor_lib: "nbextensions/aispace2/vendor_lib" // Only applicable for development
      }
    }
  });
}

// Export the required load_ipython_extention
module.exports = {
  // tslint:disable-next-line:no-empty
  load_ipython_extension: function() {}
};
