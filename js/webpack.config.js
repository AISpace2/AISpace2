module.exports = function(env) {
  process.env.NODE_ENV = env;
  return require(`./webpack.${env}.js`);
};
