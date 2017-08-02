/**
 * Webpack configuration for development.
 * 
 * Contains plugins and settings that make development a better experience.
 */

const webpack = require("webpack");
const merge = require("webpack-merge");
const fs = require("fs");
const { execSync } = require("child_process");
const path = require("path");
const argv = require("yargs").argv;

const commonConfig = require("./webpack.common.js");
const DashboardPlugin = require("webpack-dashboard/plugin");
const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");

if (!fs.existsSync(path.resolve(__dirname, "vendor", "vendor-manifest.json"))) {
  // This _should_ exist, since we run the command for you when you run `npm run dev`
  console.log(
    "Vendor files not found. Running 'npm run build:dev-dll' for you..."
  );
  execSync("npm run build:dev-dll");
  console.log("Done generating vendor files.");
}

const devConfig = {
  main: {
    devtool: "cheap-module-eval-source-map",
    plugins: [
      new webpack.DllReferencePlugin({
        context: ".",
        manifest: require("./vendor/vendor-manifest.json")
      }),
      new ForkTsCheckerWebpackPlugin({
        tslint: true,
        async: false,
        silent: true
      })
    ]
  }
};

// Only enable the dashboard plugin if --watch is specified
// The dashboard plugin annoyingly doesn't allow webpack to exit,
// so we only enable it with --watch, which doesn't exit anyways
if (argv.watch) {
  devConfig.main.plugins.push(new DashboardPlugin());
}

module.exports = merge.multiple(commonConfig, devConfig);
