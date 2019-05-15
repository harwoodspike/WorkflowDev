const path = require('path');
const webpack = require('webpack');
// const safeParser = require('postcss-safe-parser');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
// const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const devMode = process.env.NODE_ENV !== 'production';
module.exports = {
  mode: 'none',
  context: path.resolve(__dirname, '../'),

  entry: {
    app: './src/main.js',
  },

  output: {
    path: path.resolve(__dirname, '../static'),
    filename: '[name].js',
  },

  resolve: {
    symlinks: false,
    extensions: ['.js', '.vue', '.json'],
    alias: {
      '@': path.join(__dirname, '..', 'src'),
    },
  },

  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          devMode ? 'vue-style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
        ],
      },
      {
        test: /\.scss$/,
        use: [
          devMode ? 'vue-style-loader' : MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },
      {
        enforce: 'pre',
        test: /\.vue$/,
        include: path.join(__dirname, '..', 'src'),
        loader: 'eslint-loader',
        options: {
          emitWarning: true,
        },
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      {
        enforce: 'pre',
        test: /\.js$/,
        include: path.join(__dirname, '..', 'src'),
        loader: 'eslint-loader',
        options: {
          emitWarning: true,
        },
      },
      {
        test: /\.js$/,
        include: path.join(__dirname, '..', 'src'),
        loader: 'babel-loader',
        options: {
          presets: [
            ['env', {
              modules: false,
              targets: {
                browsers: ['> 1%', 'last 2 versions', 'not ie <= 8'],
              },
            }],
            'stage-2',
          ],
          plugins: ['transform-vue-jsx', 'transform-runtime'],
          env: {
            test: {
              presets: ['env', 'stage-2'],
              plugins: ['transform-vue-jsx', 'transform-es2015-modules-commonjs', 'dynamic-import-node'],
            },
          },
        },
      },
    ],
  },

  plugins: [
    new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /en/),
    new VueLoaderPlugin(),
    new BundleTracker({ filename: './webpack-stats.json' }),
  ],
};
