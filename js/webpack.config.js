// Entry point webpack config that delegates to different environments depending on the --env passed in.
module.exports = function(env) {
  // env is set under webpack.labExtension.js under "mode." If you're a developer ensure it is set to "development" if you're a user of AISpace2 just set to "production"
  process.env.NODE_ENV = env;
  return require(`./webpack.${env}.js`);
};
