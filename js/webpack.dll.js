/**
 * Generates DLL files (https://webpack.js.org/plugins/dll-plugin/) for this project.
 * 
 * This helps with build times during development. DLL files are *not* used during production,
 * as they prevent tree-shaking and other optimizations.
 * 
 * This configuration should be run before developing for the first time. 
 * It is automatically run for you by the development script
 * if it detects `vendor/vendor-manifest.json` does not exist.
 * 
 * You should re-run this any time any dependency listed in `vendor/vendor.js` has been updated,
 * by running `webpack --config webpack.dll.js`.
 */

const webpack = require("webpack");
const path = require("path");

module.exports = {
  devtool: "eval-source-map",  
  entry: {
    vendor: ["./vendor/vendor.js"]
  },
  output: {
    filename: "vendor_lib.js",
    path: path.resolve(__dirname, "..", "aispace2", "static"),
    library: "vendor_lib"
  },
  plugins: [
    new webpack.DllPlugin({
      name: "vendor_lib",
      path: "vendor/vendor-manifest.json"
    })
  ]
};
