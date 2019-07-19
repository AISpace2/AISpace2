const path = require("path");
const { VueLoaderPlugin } = require("vue-loader");

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
    /**
     * Bundle for the notebook containing the custom widget views and models.
     *
     * This bundle contains the implementation for the custom widget views and custom widget.
     * It must be an AMD module to work with Jupyter.
     */
    mode: "production",
    entry: ["babel-polyfill", "./src/index.ts"],
    output: {
      filename: "labExtension.js",
      path: path.resolve(__dirname),
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
    externals: ["@jupyter-widgets/base", "underscore"],
    performance: {
        hints: false
    },
    plugins: [new VueLoaderPlugin()]
};
