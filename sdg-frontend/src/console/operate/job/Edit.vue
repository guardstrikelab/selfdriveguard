<template>
	<div class="job-edit">
		<el-breadcrumb separator-class="el-icon-arrow-right">
			<el-breadcrumb-item :to="{path: '/op/job/list'}"
				>作业管理</el-breadcrumb-item
			>
			<el-breadcrumb-item v-if="$route.query.id">作业编辑</el-breadcrumb-item>
			<el-breadcrumb-item v-else>新建作业</el-breadcrumb-item>
		</el-breadcrumb>
		<div v-show="sectionShow == 'form'">
			<div class="list-top">
				<div class="menu">
					<div style="flex:1"></div>

					<div
						class="menu-item pointer"
						style="width: 38px;border: 1px solid #CDCED4;"
						@click="fetchDetail"
					>
						<i class="el-icon-refresh"></i>
					</div>
					<div
						class="menu-item pointer"
						style="width: 90px;border: 1px solid #CDCED4;"
						@click="back"
					>
						返回
					</div>
					<div
						class="menu-item pointer"
						style="width: 90px;border: 1px solid #CDCED4;"
						v-loading="loading"
						@click="create"
					>
						保存
					</div>
				</div>
			</div>
			<div
				:style="
					$route.query.id ? 'display:flex;justify-content:space-between' : ''
				"
			>
				<div
					class="form-container"
					:style="$route.query.id ? 'width:49%;' : 'min-height: 493px;'"
				>
					<div class="menu-container">
						<div class="menu-title">基本信息</div>
					</div>
					<div class="task-form">
						<el-form :model="form" ref="form" :rules="rules" label-width="50">
							<el-form-item label="名称：" prop="desc">
								<el-input
									class="menu-item"
									style="width: 160px;"
									v-model="form.desc"
									placeholder="请输入"
								></el-input>
							</el-form-item>
							<!-- <el-form-item label="结果：" prop="desc">
							<div
								class="menu-item"
								style="width: 160px;"
							></div>
						</el-form-item> -->
							<el-form-item label="任务：" v-show="!$route.query.id">
								<div
									class="menu-btn pointer"
									@click="showSelect"
									style="width: 90px;margin-left: 5px;"
								>
									{{ form.tasks.length > 0 ? '编辑' : '选择' }}
								</div>
								<div class="list-table" style="margin-top:20px;">
									<el-table
										style="width: 100%"
										:header-cell-style="{
											'background-color': '#2A2F3F',
											color: '#ffffff',
										}"
										:cell-style="tableCellStyle"
										:data="form.tasks"
										ref="table"
										max-height="300"
										v-if="form.tasks.length"
									>
										<el-table-column prop="id" label="ID"></el-table-column>
										<el-table-column
											prop="use_scenario.name"
											label="场景"
										></el-table-column>
										<el-table-column
											label="受测系统"
											prop="ads"
										></el-table-column>
										<el-table-column
											label="测试时间（秒）"
											prop="time_limit"
										></el-table-column>
									</el-table>
								</div>
							</el-form-item>
						</el-form>
					</div>
				</div>
				<div class="form-container" v-show="$route.query.id" style="width:49%;">
					<div class="menu-container">
						<div class="menu-title">完成进度</div>
					</div>
					<div class="chart-pie" ref="chartPie"></div>
				</div>
			</div>
			<div
				class="form-container"
				style="margin-top: 20px"
				v-show="$route.query.id"
			>
				<div class="menu-container">
					<div class="menu-title">任务列表</div>
					<div
						v-show="!$route.query.run"
						class="menu-item pointer"
						style="width: 90px;background: #41475e;"
						@click="showSelect"
					>
						增加
					</div>
					<!-- <div
						class="menu-item pointer"
						style="width: 90px;background: #41475e;"
						type="primary"
						@click="create"
					>
						删除
					</div> -->
				</div>
				<div class="task-form">
					<div class="list-table">
						<el-table
							style="width: 100%"
							:header-cell-style="{
								'background-color': '#2A2F3F',
								color: '#ffffff',
							}"
							:cell-style="tableCellStyle"
							:data="form.tasks"
							ref="table"
							max-height="400"
							v-if="form.tasks.length"
						>
							<el-table-column prop="id" label="ID"></el-table-column>
							<el-table-column
								prop="use_scenario.name"
								label="场景"
							></el-table-column>
							<el-table-column label="受测系统" prop="ads"></el-table-column>
							<el-table-column label="执行情况">
								<template #default="scope">
									<div v-if="scope.row.status">
										{{ taskStatus[scope.row.status] }}
									</div>
									<div v-else>-</div>
								</template>
							</el-table-column>
							<!-- <el-table-column label="执行结果">
								<template #default="scope">
									<div v-if="scope.row.result">{{ scope.row.result }}</div>
									<div v-else>-</div>
								</template>
							</el-table-column> -->
							<el-table-column
								label="测试时间（秒）"
								prop="time_limit"
							></el-table-column>
							<el-table-column label="得分">
								<template #default="scope">
									<div
										v-if="scope.row.result && scope.row.result.score"
										class="score pointer"
										title="得分"
										@click="showResult(scope.row)"
									>
										{{ scope.row.result.score.toFixed(2) }}
									</div>
									<div v-else>-</div>
								</template>
							</el-table-column>
							<el-table-column
								label="操作"
								width="80"
								v-if="$route.query.run == 'false'"
							>
								<template #default="scope">
									<!-- <el-button size="mini" @click="PlayBack(scope.row)"
										>查看回放</el-button
									> -->
									<el-button type="text" @click="removeTask(scope.row)"
										>删除</el-button
									>
								</template>
							</el-table-column>
						</el-table>
					</div>
				</div>
			</div>
			<!-- DEBUG 结果样式暂定 -->
			<!-- <el-dialog
				center
				title="结果列表"
				v-model="resultDialog.visible"
				width="500px"
				:close-on-click-modal="true"
			> -->
			<!-- v-if="$route.query.id && taskResult" -->
			<!-- <div class="form-container" style="margin-top: 20px"> -->
			<!-- <div class="menu-container"> -->
			<!-- <div class="menu-title">结果列表</div> -->
			<!-- <div style="color: white;">
							得分:{{ taskResult.score.toFixed(2) }}
						</div>
					</div>
					<div class="task-form">
						<div class="list-table" style="margin-top:20px;">
							<el-table
								style="width: 100%"
								:header-cell-style="{
									'background-color': '#2A2F3F',
									color: '#ffffff',
								}"
								:cell-style="tableCellStyle"
								:data="taskResult.list"
								ref="table_res"
								max-height="400"
							>
								<el-table-column
									prop="criterion"
									label="criterion"
								></el-table-column>
								<el-table-column
									label="penalty"
									prop="penalty"
								></el-table-column>
								<el-table-column label="result" prop="result"></el-table-column>
							</el-table>
						</div>
					</div>
				</div>
			</el-dialog> -->
		</div>
		<div v-show="sectionShow == 'select'">
			<div class="menu-container">
				<div style="flex:1"></div>
				<div
					class="menu-item pointer"
					style="width: 90px;border: 1px solid #CDCED4;"
					@click="selectCancel"
				>
					返回
				</div>
				<div
					class="menu-item pointer"
					style="width: 90px;border: 1px solid #CDCED4;"
					type="primary"
					v-loading="loading"
					@click="selectConfirm"
				>
					保存
				</div>
			</div>
			<div class="task-select">
				<div class="task-lib list-table">
					<el-table
						style="width: 100%"
						:height="tableHeight"
						:header-cell-style="{
							'background-color': '#2A2F3F',
							color: '#ffffff',
						}"
						:cell-style="tableCellStyle"
						ref="table_0"
						:data="table_0.data"
						@selection-change="selectionChange_0"
					>
						<el-table-column
							type="selection"
							width="50"
							:selectable="selectable"
						></el-table-column>
						<el-table-column prop="id" label="ID"></el-table-column>
						<el-table-column
							prop="use_scenario.name"
							label="场景"
						></el-table-column>
						<el-table-column label="受测系统" prop="ads"></el-table-column>
						<el-table-column
							label="测试时间（秒）"
							prop="time_limit"
						></el-table-column>
					</el-table>
				</div>
				<div class="middle-menu">
					<button class="btn" :disabled="!table_0.targets.length" @click="add">
						增加
					</button>
					<button
						class="btn"
						:disabled="!table_1.targets.length"
						@click="remove"
					>
						移除
					</button>
				</div>
				<div class="task-selected list-table">
					<el-table
						:height="tableHeight"
						:header-cell-style="{
							'background-color': '#2A2F3F',
							color: '#ffffff',
						}"
						:cell-style="tableCellStyle"
						:data="table_1.data"
						@selection-change="selectionChange_1"
						ref="table_1"
					>
						<el-table-column type="selection" width="50"></el-table-column>
						<el-table-column prop="id" label="ID"></el-table-column>
						<el-table-column
							prop="use_scenario.name"
							label="场景"
						></el-table-column>
						<el-table-column label="受测系统" prop="ads"></el-table-column>
						<el-table-column
							label="测试时间（秒）"
							prop="time_limit"
						></el-table-column>
					</el-table>
				</div>
			</div>
		</div>

		<task-edit v-if="sectionShow == 'task'"></task-edit>
		<!-- <div v-if="showPlayBack">
			<video
				autoplay
				controls="controls"
			>
				<source src="https://qrs21.techconf.org/assets/videos/hainan.mp4" type="video/mp4" />
			</video>
		</div> -->
		<el-dialog
			center
			title="结果列表"
			v-model="resultDialog.visible"
			width="700px"
			:close-on-click-modal="true"
		>
			<!-- v-if="$route.query.id && taskResult" -->
			<div class="form-container">
				<div class="menu-container">
					<div style="color: white;">
						得分:{{ resultDialog.data.score.toFixed(2) }}
					</div>
				</div>
				<div class="task-form">
					<div class="list-table" style="margin-top:20px;">
						<el-table
							style="width: 100%"
							:header-cell-style="{
								'background-color': '#2A2F3F',
								color: '#ffffff',
							}"
							:cell-style="tableCellStyle"
							:data="resultDialog.data.list"
							ref="table_res"
							max-height="400"
						>
							<el-table-column
								prop="criterion"
								label="criterion"
							></el-table-column>
							<el-table-column label="penalty" prop="penalty"></el-table-column>
							<el-table-column label="result" prop="result"></el-table-column>
						</el-table>
					</div>
				</div>
			</div>
		</el-dialog>
	</div>
</template>

<script>
import TaskEdit from '../task/Edit.vue';
export default {
	components: {
		TaskEdit,
	},
	data() {
		return {
			loading: false,
			sectionShow: 'form',
			form: {
				desc: '',
				tasks: [],
			},
			filter: {
				query: '',
			},
			table_0: {
				data: [],
				targets: [],
			},
			page: {
				totalCount: 0,
				currentPage: 1,
			},
			table_1: {
				data: [],
				targets: [],
			},
			rules: {
				name: this.$validation.fullName,
			},
			chart: {
				pie: {},
			},
			taskStatus: {
				isRunning: '运行中',
				Ready: '未运行',
				notRunning: '已完成',
			},
			resultDialog: {
				data: [],
				visible: false,
			},
			showPlayBack: false,
			taskResult: null,
			tableHeight: 600,
			resizeFlag: null,
		};
	},
	watch: {
		myDetail: {
			handler() {},
			immediate: true,
		},
	},
	computed: {
		myDetail() {
			return this.$store.state.myDetail || {};
		},
	},
	methods: {
		showSelect() {
			this.table_1.data = this.form.tasks;
			this.table_1.targets = [];
			this.table_0.targets = [];
			this.fetchList();
			this.sectionShow = 'select';
			// this.sectionShow = 'task';
			this.$refs.table_0.clearSelection();
			this.$refs.table_1.clearSelection();
		},
		back() {
			this.$router.replace({path: '/op/job/list'});
		},
		fetchDetail() {
			if (!this.$route.query.id) return;
			this.loading = true;
			this.$axios({
				method: 'get',
				url: this.$basePath + `/jobs/${this.$route.query.id}`,
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response) {
						this.form.desc = response.desc;
						this.form.tasks = response.tasks;
						// DEBUG
						this.taskResult = this.form.tasks[0].result || null;
						this.initChart();
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		showResult(row) {
			this.resultDialog.data = row.result || null;
			// if(!this.resultDialog.data){
			// 	this.$message
			// }
			this.resultDialog.visible = true;
		},
		initChart() {
			let pie = this.$echarts.init(this.$refs.chartPie);
			let pieOption = {
				legend: {
					orient: 'horizontal',
					left: 'center',
					top: 'bottom',
					data: ['已完成', '未完成'],
					textStyle: {
						color: '#C1C1C8',
					},
				},
				series: [
					{
						name: '任务完成进度',
						type: 'pie',
						radius: '60%',
						data: [
							{
								value: this.form.tasks.filter(
									(item) => item.status == 'notRunning'
								).length,
								name: '已完成',
							},
							{
								value: this.form.tasks.filter(
									(item) => item.status == 'Ready' || item.status == 'isRunning'
								).length,
								name: '未完成',
							},
						],
						color: ['#4F5DEB', '#2A2F3F'],
						center: ['50%', '50%'],
						emphasis: {
							label: false,
							lableLine: false,
						},
						label: {
							position: 'inner',
							show: false,
						},
						lableLine: {
							normal: {
								show: false,
							},
						},
					},
				],
			};
			pie.setOption(pieOption);
			this.$nextTick(() => {
				window.onresize = function() {
					pie.resize();
				};
			});
		},
		create() {
			if (!this.form.tasks.length) return;
			this.$refs.form.validate((valid) => {
				if (valid) {
					this.loading = true;
					this.submit();
				} else {
					return false;
				}
			});
		},
		removeTask(row) {
			this.form.tasks = this.form.tasks.filter((item) => item.id != row.id);
		},
		submit() {
			this.$axios({
				method: this.$route.query.id ? 'put' : 'post',
				url:
					this.$basePath +
					(this.$route.query.id ? `/jobs/${this.$route.query.id}` : '/jobs'),
				data: {
					desc: this.form.desc,
					tasks_id: this.form.tasks.map((item) => {
						return item.id;
					}),
				},
			})
				.then(() => {
					this.loading = false;
					this.$message({
						message: '操作成功',
						type: 'success',
					});
					this.$router.replace({path: '/op/job/list'});
				})
				.catch(() => {
					this.loading = false;
				});
		},
		search() {
			this.page.currentPage = 1;
			this.fetchList();
		},
		filterChange() {
			this.page.currentPage = 1;
			this.filter.query = '';
			this.fetchList();
		},
		fetchList() {
			this.loading = true;
			this.$axios({
				method: 'get',
				url: this.$basePath + `/tasks`,
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response) {
						this.table_0.data = response.filter((task) => !task.by_job_id);
						this.page.totalCount = this.table_0.data.length;
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		selectable(row) {
			return !this.table_1.data.find((item) => {
				return item.id === row.id;
			});
		},
		selectionChange_0(selection) {
			this.table_0.targets = selection;
		},
		selectionChange_1(selection) {
			this.table_1.targets = selection.map((item) => {
				return item.id;
			});
		},
		add() {
			this.table_1.data = this.table_1.data.concat(this.table_0.targets);
			// this.table_0.data = this.table_0.data.filter(item => !this.table_1.data.includes(item));
			this.table_0.targets = [];
			this.$refs.table_0.clearSelection();
		},
		remove() {
			this.table_1.data = this.table_1.data.filter((item) => {
				return !this.table_1.targets.includes(item.id);
			});
			this.$refs.table_1.clearSelection();
		},
		selectCancel() {
			this.sectionShow = 'form';
		},
		selectConfirm() {
			this.form.tasks = this.table_1.data;
			this.sectionShow = 'form';
		},
		tableCellStyle({row, columnIndex}) {
			return Object.assign(
				{color: '##C1C1C8', 'font-size': '14px'},
				{'background-color': row.type == 'subfolder' ? '#141926' : '#202533'},
				columnIndex < 5 ? {color: '#C1C1C8'} : {}
			);
		},
		// task回放
		PlayBack() {
			this.showPlayBack = true;
		},
		getTableHeight() {
			// 180 是 this.$refs.table_0.$el.offsetTop
			this.tableHeight = window.innerHeight - 180 - 100;
			// console.log(this.tableHeight,window.innerHeight,this.$refs.table_0.$el.offsetTop)
		},
	},
	mounted() {
		this.fetchDetail();
		setTimeout(() => {
			this.getTableHeight();
		}, 200);
		window.onresize = () => {
			if (this.resizeFlag) {
				clearTimeout(this.resizeFlag);
			}
			this.resizeFlag = setTimeout(() => {
				this.getTableHeight();
				this.resizeFlag = null;
			}, 100);
		};
	},
};
</script>

<style scoped lang="less">
.job-edit {
	padding: 20px;

	.el-input {
		width: 300px;
	}

	.el-textarea {
		width: 300px;
	}

	.el-select {
		width: 300px;
	}

	.tag {
		.el-tag + .el-tag {
			margin-left: 10px;
		}

		.button-new-tag {
			margin-left: 10px;
			height: 32px;
			line-height: 30px;
			padding-top: 0;
			padding-bottom: 0;
		}

		.input-new-tag {
			width: 90px;
			margin-left: 10px;
			vertical-align: bottom;
		}
	}
}

.task-form {
	margin-top: 20px;
	.label {
		margin-right: 10px;
	}
}

.task-select {
	display: flex;
	justify-content: space-between;
	margin-top: 20px;

	.title {
		font-size: 18px;
		color: #ffffff;
		margin-bottom: 20px;
		position: relative;
		&::before {
			content: '';
			width: 4px;
			height: 18px;
			background: #4f5deb;
			position: absolute;
			left: -30px;
		}
	}
	.task-lib {
		width: 45%;
		padding: 30px;
		line-height: 1;
		background: #202533;
	}

	.task-selected {
		width: 45%;
		padding: 30px;
		background: #202533;
	}
}
.list-top {
	padding: 30px 0;
}
.form-container {
	width: 100%;
	// min-height: 493px;
	background: #202533;
	padding: 20px 30px;
	.chart-pie {
		width: 100%;
		// height: 230px;
		height: 180px;
		margin-top: -25px;
	}
}
.menu-container,
.form-container {
	.menu-item {
		padding: 0 10px;
		margin: 0 5px;
		height: 38px;
		box-sizing: border-box;
		line-height: 38px;
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
		text-align: center;
		color: #ffffff;
		font-size: 14px;
		background: #1a1f2c;
		border: 1px solid #353a4c;
		user-select: none;
	}
	.el-textarea .el-textarea__inner,
	.el-input .el-input__inner {
		background-color: #1a1f2c;
	}

	.menu-btn {
		height: 38px;
		background: #41475e;
		font-size: 14px;
		text-align: center;
		color: #ffffff;
		line-height: 38px;
	}
}
.middle-menu {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	.btn {
		width: 68px;
		height: 38px;
		background: #41475e;
		outline: none;
		border: none;
		color: #ffffff;
		border-radius: 0;
		&:last-of-type {
			margin-top: 10px;
		}
		&:disabled {
			color: #c1c1c8;
		}
	}
}
.menu-container {
	display: flex;
	align-items: center;
	.menu-title {
		font-size: 18px;
		color: #ffffff;
		text-align: left;
		flex: 1;
		position: relative;
		&::before {
			content: '';
			width: 4px;
			height: 18px;
			background: #4f5deb;
			position: absolute;
			left: -30px;
		}
	}
}

.list-table .score {
	color: #4f5deb;
	&:hover {
		color: #c1c1c8;
	}
}
</style>
