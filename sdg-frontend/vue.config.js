module.exports = {
	devServer: {
		proxy: {
			'/': {
				// target: 'http://172.16.111.153:8000',
				target: 'http://172.16.111.78:8000', // test 
				changeOrigin: true,
			},
		},
	},
	pages: {
		login: {
			entry: 'src/login/main.js', // page 的入口
			template: 'public/index.html', // html 模板
			filename: 'login.html', // 在 dist里 的输出
			title: '自驾保 登录', // html 模板 里用到的变量
		},
		operation: {
			entry: 'src/console/main.js',
			template: 'public/index.html',
			filename: 'index.html',
			title: '自驾保 控制台',
		},
	}
};
