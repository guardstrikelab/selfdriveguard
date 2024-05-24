<template>
	<div class="task-edit">
		<el-breadcrumb separator-class="el-icon-arrow-right">
			<el-breadcrumb-item :to="{path: '/op/task/list'}"
				>任务管理</el-breadcrumb-item
			>
			<el-breadcrumb-item v-if="$route.query.id">任务编辑</el-breadcrumb-item>
			<el-breadcrumb-item v-else>新建任务</el-breadcrumb-item>
		</el-breadcrumb>
		<div class="form-container" v-show="sectionShow == 'form'">
			<div class="menu-container">
				<div class="menu-title">基本信息</div>
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
					type="primary"
					v-loading="loading"
					@click="create"
				>
					保存
				</div>
			</div>
			<div class="task-form">
				<el-form :model="form" ref="form" :rules="rules" label-width="130px">
					<!-- <el-row> -->
					<el-form-item label="受测系统：">
						<div class="menu-item" style="width: 160px;">
							{{ form.ads }}
						</div>
					</el-form-item>
					<!-- <div class="menu-btn pointer" style="width: 90px;">修改</div> -->
					<!-- </el-row> -->

					<el-row>
						<el-form-item label="场景：">
							<div
								class="menu-item"
								style="width: 160px;"
								:title="allScenarios"
							>
								<!-- <label
									class="label"
									v-for="item in form.scenarios"
									:key="item.id"
									>{{ item.name + ' ' }}</label
								> -->
								{{ allScenarios }}
							</div>
						</el-form-item>
						<div
							class="menu-btn pointer"
							@click="showSelect"
							style="width: 90px;"
						>
							{{ allScenarios ? '修改' : '选择' }}
						</div>
					</el-row>
					<el-form-item label="测试时间（秒）：" prop="time_limit">
						<el-input
							type="number"
							v-model="form.time_limit"
							placeholder="请输入"
						></el-input>
					</el-form-item>
				</el-form>
			</div>
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
					确定
				</div>
			</div>
			<div class="scene-select">
				<div class="list-top scene-lib " style="width:100%">
					<div class="title">场景库</div>
					<div class="menu">
						<div
							class="menu-item"
							style="width: 300px;display: flex;align-items: center;justify-content: start;"
						>
							<i class="el-icon-folder" style="margin-right: 10px;"></i>
							<el-breadcrumb separator="/" class="breadcrumb">
								<el-breadcrumb-item
									v-for="folder in folderChain"
									:key="folder.id"
									@click="changeFolder(folder)"
									class="breadcrumb-item"
								>
									<el-button
										type="text"
										:disabled="true"
										v-if="folder == curFolder"
										>{{ folder.name }}</el-button
									>
									<el-button v-else type="text">{{ folder.name }}</el-button>
								</el-breadcrumb-item>
							</el-breadcrumb>
						</div>

						<div
							class="menu-item pointer"
							style="width: 42px;text-overflow: clip;"
							@click="search"
						>
							<i class="el-icon-refresh"></i>
						</div>
						<div class="menu-item" style="width: 150px;">
							<el-select
								style="width:100%"
								v-model="filter.level"
								placeholder="层级"
								@change="filterChange"
							>
								<el-option label="当前层级" value="cur"></el-option>
								<el-option label="所有层级" value="all"></el-option>
							</el-select>
						</div>
					</div>
					<div class="list-table singlepick">
						<el-table
							style="width: 100%"
							max-height="500"
							:header-cell-style="{
								'background-color': '#2A2F3F',
								color: '#ffffff',
							}"
							:cell-style="tableCellStyle"
							:data="table_0.data"
							@selection-change="selectionChange_0"
							@current-change="currentChanfe_0"
							ref="table_0"
						>
							<el-table-column
								type="selection"
								:selectable="selectable"
								width="50"
							></el-table-column>
							<el-table-column label="名称">
								<template #default="scope">
									<div v-if="scope.row.type == 'scenario'">
										{{ scope.row.name }}
									</div>
									<div
										type="text"
										v-else
										@click="changeFolder(scope.row)"
										class="pointer"
									>
										<i class="el-icon-folder" style="margin-right: 10px;"></i
										>{{ scope.row.name }}
									</div>
								</template>
							</el-table-column>
							<el-table-column prop="desc" label="描述备注">
								<template #default="scope">
									<div v-if="scope.row.desc">
										{{ scope.row.desc }}
									</div>
									<div v-else>-</div>
								</template>
							</el-table-column>
							<el-table-column prop="language" label="语言">
								<template #default="scope">
									<div v-if="scope.row.language">
										{{ scope.row.language }}
									</div>
									<div v-else>-</div>
								</template>
							</el-table-column>
							<el-table-column prop="map_name" label="地图">
								<template #default="scope">
									<div v-if="scope.row.map_name">
										{{ scope.row.map_name }}
									</div>
									<div v-else>-</div>
								</template>
							</el-table-column>
						</el-table>
					</div>
				</div>
			</div>
			<!-- <div class="scene-select">
				<div class="list-top scene-lib ">
					<div class="title">场景库</div>
					<div class="menu">
						<div
							class="menu-item"
							style="width: 300px;display: flex;align-items: center;justify-content: start;"
						>
							<i class="el-icon-folder" style="margin-right: 10px;"></i>
							<el-breadcrumb separator="/" class="breadcrumb">
								<el-breadcrumb-item
									v-for="folder in folderChain"
									:key="folder.id"
									@click="changeFolder(folder)"
									class="breadcrumb-item"
								>
									<el-button
										type="text"
										:disabled="true"
										v-if="folder == curFolder"
										>{{ folder.name }}</el-button
									>
									<el-button v-else type="text">{{ folder.name }}</el-button>
								</el-breadcrumb-item>
							</el-breadcrumb>
						</div>

						<div
							class="menu-item pointer"
							style="width: 42px;text-overflow: clip;"
							@click="search"
						>
							<i class="el-icon-refresh"></i>
						</div>
						<div class="menu-item" style="width: 150px;">
							<el-select
								style="width:100%"
								v-model="filter.level"
								placeholder="层级"
								@change="filterChange"
							>
								<el-option label="当前层级" value="cur"></el-option>
								<el-option label="所有层级" value="all"></el-option>
							</el-select>
						</div>
					</div>
					<div class="list-table">
						<el-table
							style="width: 100%"
							max-height="500"
							:header-cell-style="{
								'background-color': '#2A2F3F',
								color: '#ffffff',
							}"
							:cell-style="tableCellStyle"
							:data="table_0.data"
							@selection-change="selectionChange_0"
							ref="table_0"
						>
							<el-table-column
								
								type="selection"
								:selectable="selectable"
								width="50"
							></el-table-column>
							<el-table-column label="名称"  >
								<template #default="scope">
									<div v-if="scope.row.type == 'scenario'">
										{{ scope.row.name }}
									</div>
									<div
										type="text"
										v-else
										@click="changeFolder(scope.row)"
										class="pointer"
									>
										<i class="el-icon-folder" style="margin-right: 10px;"></i
										>{{ scope.row.name }}
									</div>
								</template>
							</el-table-column>
							<el-table-column prop="desc" label="描述备注">
								<template #default="scope">
									<div v-if="scope.row.desc">
										{{ scope.row.desc }}
									</div>
									<div v-else>-</div>
								</template>
							</el-table-column>
							<el-table-column prop="language" label="语言">
								<template #default="scope">
									<div v-if="scope.row.language">
										{{ scope.row.language }}
									</div>
									<div v-else>-</div>
								</template>
							</el-table-column>
							<el-table-column prop="map_name" label="地图">
								<template #default="scope">
									<div v-if="scope.row.map_name">
										{{ scope.row.map_name }}
									</div>
									<div v-else>-</div>
								</template>
							</el-table-column>
						</el-table>
					</div>
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
				<div class="scene-selected">
					<div class="title">已选场景</div>

					<div class="list-table">
						<el-table
							style="width: 100%"
							max-height="500"
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
							<el-table-column label="名称" prop="name"></el-table-column>
							<el-table-column prop="desc" label="描述"></el-table-column>
							<el-table-column prop="language" label="语言"></el-table-column>
							<el-table-column prop="map_name" label="地图"></el-table-column>
						</el-table>
					</div>
				</div>
			</div> -->
		</div>
	</div>
</template>

<script>
export default {
	components: {},
	data() {
		return {
			loading: false,
			sectionShow: 'form',
			form: {
				ads: 'autoware',
				time_limit: '',
				scenarios: [],
			},
			folderChain: [],
			filter: {
				query: '',
				level: 'cur',
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
		};
	},
	watch: {
		myDetail: {
			handler() {
				this.folderChain = [
					{
						id: this.myDetail.rootfolder,
						name: '根目录',
					},
				];
			},
			immediate: true,
		},
	},
	computed: {
		myDetail() {
			return this.$store.state.myDetail || {};
		},
		curFolder() {
			return this.folderChain[this.folderChain.length - 1];
		},
		allScenarios() {
			let str = [];
			this.form.scenarios.forEach((item) => {
				str.push(item.name);
			});
			return str.join('、');
		},
	},
	methods: {
		showSelect() {
			this.table_1.data = this.form.scenarios;
			this.table_1.targets = [];
			this.table_0.targets = [];
			this.fetchList();
			this.sectionShow = 'select';
			this.$refs.table_0.clearSelection();
			// 这里屏蔽的穿梭框
			// this.$refs.table_1.clearSelection();
		},
		back() {
			this.$router.replace({path: '/op/task/list'});
		},
		create() {
			if (!this.form.scenarios[0] || !this.form.time_limit) {
				// this.loading = false;
				this.$message({
					message: '请完整填写信息',
					type: 'warning',
				});
				// this.$router.replace({path: '/op/task/list'});
				return;
			}
			this.$refs.form.validate((valid) => {
				if (valid) {
					this.loading = true;
					this.submit(0);
				} else {
					return false;
				}
			});
		},
		submit(index) {
			// if (!this.table_1.data[index]) {
			// 	this.loading = false;
			// 	this.$message({
			// 		message: '操作成功',
			// 		type: 'success',
			// 	});
			// 	this.$router.replace({path: '/op/task/list'});
			// 	return;
			// }
			this.$axios({
				method: 'post',
				url: this.$basePath + `/tasks`,
				data: {
					ads: this.form.ads,
					time_limit: this.form.time_limit,
					use_scenario_id: this.form.scenarios[0].id,
				},
			})
				.then(() => {
					// this.submit(index + 1);
					this.loading = false;
					this.$message({
						message: '操作成功',
						type: 'success',
					});
					this.$router.replace({path: '/op/task/list'});
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
			if (!this.curFolder || !this.curFolder.id) {
				return;
			}
			if (this.filter.level == 'all') {
				this.fetchAll();
			} else {
				this.fetchCur();
			}
		},
		fetchCur() {
			this.loading = true;
			this.$axios({
				method: 'get',
				url: this.$basePath + `/scen-folders/${this.curFolder.id}`,
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response) {
						response.scenarios.forEach((item) => {
							item.type = 'scenario';
						});
						response.subfolders.forEach((item) => {
							item.type = 'subfolder';
						});
						this.table_0.data = response.subfolders.concat(response.scenarios);
						this.page.totalCount = this.table_0.data.length;
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		fetchAll() {
			this.loading = true;
			this.$axios({
				method: 'get',
				url:
					this.$basePath +
					`/scen-folders/${this.curFolder.id}/scenarios?recursive=true`,
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response) {
						response.forEach((item) => {
							item.type = 'scenario';
						});
						this.table_0.data = response;
						this.page.totalCount = this.table_0.data.length;
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		changeFolder(folder) {
			if (folder == this.curFolder) {
				return;
			}
			if (this.folderChain.includes(folder)) {
				this.folderChain = this.folderChain.slice(
					0,
					this.folderChain.indexOf(folder) + 1
				);
			} else {
				this.folderChain.push(folder);
			}
			this.fetchList();
		},
		selectable(row) {
			return (
				row.type === 'scenario' &&
				!this.table_1.data.find((item) => {
					return item.id === row.id;
				})
			);
		},
		selectionChange_0(selection) {
			// this.table_0.targets = selection;
			if (selection.length > 1) {
				this.$refs.table_0.clearSelection();
				this.$refs.table_0.toggleRowSelection(selection.pop());
				this.table_0.targets = selection;
			} else {
				this.table_0.targets = selection;
			}
		},
		currentChanfe_0(currentRow) {
			this.$refs.table_0.toggleRowSelection(currentRow);
		},
		selectionChange_1(selection) {
			this.table_1.targets = selection.map((item) => {
				return item.id;
			});
		},
		add() {
			this.table_1.data = this.table_1.data.concat(this.table_0.targets);
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
			// this.form.scenarios = this.table_1.data;
			this.form.scenarios = this.table_0.targets;
			this.sectionShow = 'form';
		},
		tableCellStyle({row, columnIndex}) {
			return Object.assign(
				{color: '##C1C1C8', 'font-size': '14px'},
				{'background-color': row.type == 'subfolder' ? '#141926' : '#202533'},
				columnIndex < 5 ? {color: '#C1C1C8'} : {}
			);
		},
	},
	mounted() {},
};
</script>

<style scoped lang="less">
.task-edit {
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
			// height: 32px;
			// line-height: 30px;
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

.scene-select {
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
	.scene-lib {
		width: 45%;
		padding: 30px;
		line-height: 1;
		background: #202533;
	}

	.scene-selected {
		width: 45%;
		padding: 30px;
		background: #202533;
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
}
.form-container {
	width: 100%;
	min-height: 493px;
	background: #202533;
	margin-top: 20px;
	padding: 20px 30px;
}
</style>
<style lang="less">
.form-container,
.el-form-item {
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

.el-tag {
	min-width: 70px;
	height: 24px;
	min-height: 24px;
	line-height: 23px;
	color: #c1c1c8;
	background: #353a4c;
	border: none;
	// margin-top: 10px;
}

.singlepick thead .el-table-column--selection .cell {
	display: none;
}
</style>
