// Entry point webpack config that delegates to different environments depending on the --env passed in.
module.exports = function(env) {
  process.env.NODE_ENV = env;
  return require(`./webpack.${env}.js`);
};
