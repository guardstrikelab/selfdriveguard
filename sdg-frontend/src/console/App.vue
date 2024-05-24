<template>
	<el-container class="main">
        <el-header class="top" height="38px">
			<div  class="name" @click="$router.replace({path: '/'})">
				<img
					style="height: 20px;"
					src="@/assets/images/logo_cn.png"
					alt=""
				/>
			</div>
			<el-col style="flex: 1;"> </el-col>
			<div class="pay-btn pointer">
					购买
				</div>
			<!-- <span class="iconfont iconzhongwen pointer"></span> -->
			<span class="iconfont iconyingwen pointer"></span>
			
			<!-- <div  class="user-info pointer" style="width: fit-content;" @click="goToMine">
                <span class="iconfont iconuser"></span>
			</div> -->
			<div  class="user-info pointer" style="width: fit-content;">
                <span class="iconfont iconuser"></span>
			</div>
        </el-header>
        <el-container>
			<el-aside class="level_two_menu">
				<el-menu
					text-color="#C1C1C8"
					active-text-color="#ffffff"
					:default-active="$route.path"
					router
					v-if="$route.path.startsWith('/op') || $route.path == '/'"
				>
					<el-menu-item index="/op/scene/list"
						><span class="iconfont iconchangjingku"></span>
						<template #title> 场景管理</template></el-menu-item
					>

					<el-menu-item index="/op/task/list">
						<span class="iconfont iconchangjingku"></span>
						<template #title> 任务管理</template></el-menu-item
					>
					<el-menu-item index="/op/job/list">
						<span class="iconfont iconchangjingku"></span>
						<template #title> 作业管理</template>
					</el-menu-item>
				</el-menu>
				<el-menu
					:default-active="$route.path"
					router
					v-if="$route.path.startsWith('/mine')"
				>
					<el-menu-item index="/mine/basic">基本信息</el-menu-item>
				</el-menu>
			</el-aside>
			<el-main class="right">
				<router-view></router-view>
			</el-main>


        </el-container>
	</el-container>
</template>

<script>
export default {
	data() {
		return {};
	},
	computed: {
		myDetail: function() {
			return this.$store.state.myDetail;
		},
	},
	watch: {},
	methods: {
		goToMine() {
			this.$router.push({path: '/mine/basic'});
		},
		fetchMe() {
			this.$axios({
				method: 'get',
				url: this.$basePath + '/users/me',
			})
				.then((response) => {
					response = response.data;
					if (response.id) {
						this.$store.state.myDetail = response;
						this.$store.commit('change');
					}
				})
				.catch(() => {
					window.location.href = '/login.html';
				});
		},
	},
	created() {
		let access_token = localStorage.getItem('access_token');
		this.$store.state.access_token = access_token;
		this.$store.commit('change');
		// 请求拦截器
		this.$axios.interceptors.request.use(function(config) {
			config.headers = {
				Authorization: `Bearer ${access_token}`,
			};
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
	},
	mounted() {
		setTimeout(() => {
			this.fetchMe();
		}, 100);
	},
};
</script>

<style scoped lang="less">
.top {
	color: #fff;
	line-height: 38px;
	background: #353a4c;
    display: flex;
    align-items: center;
	border-bottom: 1px solid #141926;
	.logo {
		height: 40px;
		vertical-align: middle;
	}

	.name {
		font-size: 24px;
		cursor: pointer;
	}
	.pay-btn {
		width: 90px;
		height: 100%;
		background: #4f5deb;
		text-align: center;
		color: white;
        margin: 0 20px;
	}
	.user-info {
        height: 38px;
        margin: 0 20px;
		.el-button--text {
			font-size: 16px;
		}

	}
}
.level_two_menu  {
    width: 220px;
    min-height: calc(100vh - 38px);
	background-color: #353a4c;
}
.level_two_menu .el-menu {
	border-right: 0;

	& :deep(.el-menu-item) {
        height: 38px;
        line-height: 38px;
		background-color: #353a4c;
		&:hover {
			background-color: #141926;
		}
	}
	& :deep(.el-menu-item.is-active) {
		background-color: #141926;
	}
}

.right {
	background-color: #141926;
}
</style>
