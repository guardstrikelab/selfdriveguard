<template>
	<div class="login">
		<el-row align="middle" class="header">
			<el-col :span="3">
				<img
					style="height: 20px;margin-left: 20px;vertical-align: middle;"
					src="@/assets/images/logo_cn.png"
					alt=""
				/>
			</el-col>
			<el-col :span="20"></el-col>
			<el-col :span="1">
				<span class="iconfont iconyingwen pointer"></span>
				<!-- <span class="iconfont iconzhongwen pointer"></span> -->
			</el-col>
		</el-row>
		<main>
			<img class="login-bg" src="../assets/images/login_bg.png" alt="" />
			<el-card class="login-box" shadow="never">
				<div class="sys-name">欢迎来到自驾保！</div>
				<el-form ref="form" :model="form" :rules="validate" class="form">
					<el-form-item label="" prop="j_username">
						<el-input
							v-model="form.j_username"
							placeholder="请输入用户名"
							class="input-item"
						></el-input>
					</el-form-item>
					<el-form-item label="" prop="j_password">
						<el-input
							class="input-item"
							type="password"
							v-model="form.j_password"
							placeholder="请输入密码"
						></el-input>
					</el-form-item>
					<el-form-item>
						<el-checkbox
							label="记住密码"
							name="type"
							v-model="pwdSave"
						></el-checkbox>
					</el-form-item>
					<el-form-item>
						<el-button type="primary" class="login-btn" @click="validateForm"
							>登录</el-button
						>
					</el-form-item>
					<el-form-item>
						<!-- <div class="service-email">客服邮箱：152@guardstrike.com</div> -->
					</el-form-item>
				</el-form>
			</el-card>
		</main>
	</div>
</template>

<script>
export default {
	data() {
		return {
			form: {
				j_username: '',
				j_password: '',
			},
			validate: {
				j_username: this.$validation.email,
				j_password: this.$validation.password,
			},
			pwdSave: false,
		};
	},
	computed: {},
	methods: {
		validateForm() {
			this.$refs.form.validate((valid) => {
				if (valid) {
					this.submit();
				}
			});
		},
		submit() {
			if (this.pwdSave) {
				this.setCookie(this.form.j_username, this.form.j_password, 7);
			} else {
				this.clearCookie();
			}
			this.$axios({
				method: 'post',
				url: this.$basePath + '/auth/jwt/login',
				data: this.$qs.stringify({
					grant_type: 'password',
					username: this.form.j_username,
					password: this.form.j_password,
				}),
			})
				.then((response) => {
					response = response.data;
					if (response.access_token) {
						localStorage.setItem('access_token', response.access_token);
						window.location.href = 'index.html';
					}
				})
				.catch((error) => {
					if (error.response) {
						// 请求已发出，但服务器响应的状态码不在 2xx 范围内
						console.log(error.response);
						this.$message({
							message: '用户名或密码错误',
							type: 'error',
						});
					} else {
						console.log('Error', error.message);
						this.$message({
							message: '网络连接失败',
							type: 'error',
						});
					}
					console.log('config', error.config);
				});
		},
		setCookie(c_name, c_pwd, exdays) {
			var exdate = new Date();
			exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * exdays); //保存的天数
			window.document.cookie =
				'userName' + '=' + c_name + ';path=/;expires=' + exdate.toGMTString();
			window.document.cookie =
				'password' + '=' + c_pwd + ';path=/;expires=' + exdate.toGMTString();
		},
		getCookie() {
			if (document.cookie.length > 0) {
				var arr = document.cookie.split('; ');
				this.pwdSave = true;
				for (var i = 0; i < arr.length; i++) {
					var arr2 = arr[i].split('=');
					if (arr2[0] == 'userName') {
						this.form.j_username = arr2[1];
					} else if (arr2[0] == 'password') {
						this.form.j_password = arr2[1];
					}
				}
			}
		},
		clearCookie() {
			this.setCookie('', '', -1);
		},
	},
	mounted: function() {
		// 请求拦截器
		this.$axios.interceptors.request.use(function(config) {
			return config;
		}, null);
		// 响应拦截器
		this.$axios.interceptors.response.use(
			(response) => {
				return response;
			},
			(error) => {
				return Promise.reject(error);
			}
		);
		this.getCookie();
	},
};
</script>

<style scoped lang="less">
.login {
	// background-image: url('../assets/images/supplier-background.jpeg');
	background-color: #141926;
	// background-size: cover;
	height: 100%;
	position: relative;
}
.header {
	height: 38px;
	background-color: #353a4c;
}

main {
	display: flex;
	align-items: center;
	position: absolute;
	left: 40%;
	top: 50%;
	transform: translate(-50%, -50%);
}
.login-bg {
	width: 962px;
	height: 488px;
}
:deep(.login-box) {
	border: none;
}
.login-box {
	// position: absolute;
	width: 390px;
	height: 360px;
	background: #2a2f3f;
	margin-left: -100px;
	// left: 50%;
	// top: 50%;
	// margin: -235px 0 0 -200px;

	.logo {
		margin: 0 auto;
		display: block;
	}

	.sys-name {
		text-align: center;
		color: white;
		font-size: 24px;
		font-weight: 600;
		margin-top: 20px;
	}
}

.form {
	width: 330px;
	margin: 30px auto 0;
	&:deep(.el-form-item:nth-of-type(1)) {
		margin-bottom: 18px;
	}
	&:deep(.el-form-item:nth-of-type(3)) {
		margin-bottom: 0;
	}
	&:deep(.el-form-item:nth-of-type(2)),
	&:deep(.el-form-item:nth-of-type(4)) {
		margin-bottom: 10px;
	}

	.input-item :deep(.el-input__inner) {
		color: white;
		height: 38px;
		background: #202533;
		border: 1px solid #4d536b;
		&::placeholder {
			color: #8d8e9b;
		}
	}

	& :deep(.el-checkbox__inner) {
		background-color: #202533;
		border-style: dashed;
		border-color: #4d536b;
	}

	& :deep(.el-checkbox__label) {
		font-size: 14px;
		color: #c1c1c8;
	}
	.login-btn {
		width: 100%;
	}
	.service-email {
		font-size: 12px;
		font-weight: 400;
		color: #8d8e9b;
		line-height: 18px;
	}
}
</style>
<style lang="less">
html,
body,
#app {
	height: 100%;
}

.login .form .el-input input {
	height: 46px;
}
</style>
