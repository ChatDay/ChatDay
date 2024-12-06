const webpack = require('webpack');

module.exports = {
configureWebpack: {
    output: {
      filename: '[name].[contenthash].js', // 파일 이름에 해시 추가
      chunkFilename: '[name].[contenthash].js', // 청크 파일에도 해시 추가
    },
    plugins: [
    new webpack.DefinePlugin({
        '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': JSON.stringify(false),
    }),
    ],
},
};
