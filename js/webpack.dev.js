const webpack = require("webpack");
const merge = require("webpack-merge");
const commonConfig = require("./webpack.common.js");

module.exports = merge.multiple(commonConfig, {
  main: {
    devtool: "eval-source-map"
  }
});
