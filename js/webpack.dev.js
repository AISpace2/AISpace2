const webpack = require("webpack");
const merge = require("webpack-merge");
const commonConfig = require("./webpack.common.js");
const DashboardPlugin = require("webpack-dashboard/plugin");

module.exports = merge.multiple(commonConfig, {
  main: {
    devtool: "eval-source-map",
    // The dashboard plugin annoyingly doesn't allow webpack to exit
    // This is "ok" for development since you'll usually use --watch
    plugins: [new DashboardPlugin()]
  }
});
