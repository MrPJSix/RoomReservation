// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true,
// })

module.exports = {
  transpileDependencies: true,
  devServer: {
      host: '0.0.0.0', // 设置为 '0.0.0.0' 可以监听所有可用网络接口
      port: 8080, // 设置端口号
      proxy: {
          '/api': {
              target: 'http://django-backend:8000',
          // ws: true,
              changOrigin: true,//允许跨域
              pathRewrite: {
                  '^/api': '/'
              }
          },
      }
  }
}