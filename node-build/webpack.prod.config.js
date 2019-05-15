const webpack = require('webpack');
const merge = require('webpack-merge');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
// const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
const webpackBase = require('./webpack.base.config');

const webpackProd = {
  mode: 'production',
  devtool: false,
  output: {
    filename: 'js/[name].[chunkhash].js',
    chunkFilename: 'js/[name].[chunkhash].js',
    publicPath: '/static/',
  },

  plugins: [
    // keep module.id stable when vender modules does not change
    new webpack.HashedModuleIdsPlugin(),
    new MiniCssExtractPlugin({
      filename: 'styles/[name].[hash].css',
      chunkFilename: 'styles/[id].[hash].css',
    }),
    // new BundleAnalyzerPlugin({
    //     analyzerMode: 'static',
    //     generateStatsFile: true,
    // }),
  ],
};
module.exports = merge(webpackBase, webpackProd);
