/**
 * Base, shared webpack configuration used by development and production configurations.
 */
const webpack = require("webpack");
const version = require("./package.json").version;
const path = require("path");

const babelLoader = {
  loader: "babel-loader",
  options: {
    cacheDirectory: true
  }
};

const tsLoader = [
  babelLoader,
  {
    loader: "ts-loader",
    options: {
      appendTsSuffixTo: [/\.vue$/],
      silent: true,
      transpileOnly: process.env.NODE_ENV !== "production"
    }
  }
];

module.exports = {
  notebookExtension: {
    // Notebook extension
    //
    // This bundle only contains the part of the JavaScript that is run on
    // load of the notebook. This section generally only performs
    // some configuration for requirejs, and provides the legacy
    // "load_ipython_extension" function which is required for any notebook
    // extension.
    //
    entry: "./src/extension.js",
    output: {
      filename: "extension.js",
      path: path.resolve(__dirname, "..", "aispace2", "static"),
      libraryTarget: "amd"
    }
  },
  main: {
    // Bundle for the notebook containing the custom widget views and models
    //
    // This bundle contains the implementation for the custom widget views and
    // custom widget.
    // It must be an amd module
    //
    entry: ["babel-polyfill", "./src/index.ts"],
    output: {
      filename: "index.js",
      path: path.resolve(__dirname, "..", "aispace2", "static"),
      libraryTarget: "amd"
    },
    module: {
      rules: [
        {
          test: /\.ts$/,
          include: [path.join(__dirname, "./src")],
          use: tsLoader
        },
        {
          test: /\.js$/,
          include: [path.join(__dirname, "./src")],
          use: [babelLoader]
        },
        {
          test: /\.vue$/,
          include: [path.join(__dirname, "./src")],
          use: [
            {
              loader: "vue-loader",
              options: {
                loaders: {
                  ts: tsLoader
                }
              }
            }
          ]
        },
        {
          test: /\.html$/,
          include: [path.join(__dirname, "./src")],
          use: [
            {
              loader: "html-loader"
            }
          ]
        },
        {
          test: /\.css$/,
          include: [path.join(__dirname, "./src")],
          use: [
            "style-loader",
            { loader: "css-loader", options: { importLoaders: 1 } },
            {
              loader: "postcss-loader",
              options: {
                plugins: loader => [require("autoprefixer")()]
              }
            }
          ]
        },
        {
          test: /\.json$/,
          include: [path.join(__dirname, "./src")],
          loader: "json-loader"
        }
      ]
    },
    resolve: {
      extensions: [".vue", ".ts", ".js"],
      alias: {
        vue$: "vue/dist/vue.esm.js"
      }
    },
    externals: ["@jupyter-widgets/base", "underscore"]
  },
  embeddable: {
    // Embeddable aispace2 bundle
    //
    // This bundle is generally almost identical to the notebook bundle
    // containing the custom widget views and models.
    //
    // The only difference is in the configuration of the webpack public path
    // for the static assets.
    //
    // It will be automatically distributed by unpkg to work with the static
    // widget embedder.
    //
    // The target bundle is always `dist/index.js`, which is the path required
    // by the custom widget embedder.
    //
    entry: "./src/embed.js",
    output: {
      filename: "index.js",
      path: path.resolve(__dirname, "dist"),
      libraryTarget: "amd",
      publicPath: "https://unpkg.com/aispace2@" + version + "/dist/"
    },
    externals: ["@jupyter-widgets/base"]
  }
};
