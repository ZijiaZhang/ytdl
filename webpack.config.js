path = require('path');

module.exports = {
    mode: "development",
    devtool: "source-map",
    entry: {
        main: './frontend/index.jsx',
    },
    resolve: {
        extensions: [".jsx", ".js"]
    },
    module: {
        rules: [{
            test: /\.scss$/,
            use: ["style-loader", "css-loader", "sass-loader"]
        },
            {
                test: /\.jsx$/,
                exclude: /node_modules/,
                use: ["babel-loader"]
            }]
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'public/js'),
    },
};