const path = require('path');
const notifier = require('node-notifier');
const webpack = require('webpack');
const merge = require('webpack-merge');
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin');
const portfinder = require('portfinder');
const webpackBase = require('./webpack.base.config');
const pkg = require('../package.json');

const config = {
  // Paths
  assetsSubDirectory: 'static',
  assetsPublicPath: 'http://localhost:8080/static/',
  proxyTable: {},

  // Various Dev Server settings
  host: 'localhost', // can be overwritten by process.env.HOST
  port: 8080, // if port is in use, a free one will be determined
  autoOpenBrowser: false,
  errorOverlay: true,
  notifyOnErrors: true,
  poll: false,

  // Use Eslint Loader?
  // If true, your code will be linted during bundling and
  // linting errors and warings will be shown in the console.
  useEslint: true,
  // If true, eslint errors and warings will also be shown in the error overlay
  // in the browser.
  showEslintErrorsInOverlay: false,

  /**
   * Source Maps
  */
  // If you have problems debugging vue-files in devtools,
  // set this to false - it *may* help
  // https://vue-loader.vuejs.org/en/options.html#cachebusting
  cacheBusting: true,

  // CSS Sourcemaps off by default because relative paths are "buggy"
  // with this option, according to the CSS-Loader README
  // (https://github.com/webpack/css-loader#sourcemaps)
  // In our experience, they generally work as expected,
  // just be aware of this issue when enabling this option.
  cssSourceMap: false,
};

function createNotifierCallback() {
  return (severity, errors) => {
    if (severity !== 'error') {
      return;
    }
    const error = errors[0];

    const filename = error.file.split('!').pop();
    notifier.notify({
      title: pkg.name,
      message: `${severity}:${error.name}`,
      subtitle: filename || '',
      icon: path.join(__dirname, 'logo.png'),
    });
  };
}

const webpackDev = {
  mode: 'development',
  devtool: 'inline-source-map',

  output: {
    publicPath: config.assetsPublicPath,
  },
  // these devServer options should be customized in /config/index.js
  devServer: {
    historyApiFallback: true,
    hot: true,
    host: process.env.HOST || config.host,
    port: process.env.PORT || config.port,
    open: config.autoOpenBrowser,
    overlay: config.errorOverlay ? {
      warnings: false,
      errors: true,
    } : false,
    publicPath: config.assetsPublicPath,
    proxy: config.proxyTable,
    quiet: true, // necessary for FriendlyErrorsPlugin
    watchOptions: {
      poll: config.poll,
    },
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization',
    },
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    // new webpack.NoEmitOnErrorsPlugin()
  ],
};
const webpackDevMerged = merge(webpackBase, webpackDev);

module.exports = new Promise((resolve, reject) => {
  portfinder.basePort = process.env.PORT || config.port;
  portfinder.getPort((err, port) => {
    if (err) {
      reject(err);
    } else {
      // publish the new Port, necessary for e2e tests
      process.env.PORT = port;
      // add port to devServer config
      webpackDevMerged.devServer.port = port;

      // Add FriendlyErrorsPlugin
      webpackDevMerged.plugins.push(new FriendlyErrorsPlugin({
        compilationSuccessInfo: {
          messages: [`Your application is running here: http://${config.host}:${port}`],
        },
        onErrors: config.notifyOnErrors
          ? createNotifierCallback()
          : undefined,
      }));

      resolve(webpackDevMerged);
    }
  });
});
