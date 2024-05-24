<template>
	<div
		class="role-list"
		v-loading="loading"
		style="min-height: calc(100vh - 100px);"
		element-loading-text="加载中"
		element-loading-spinner="el-icon-loading"
		element-loading-background="rgba(0, 0, 0, 0.8)"
	>
		<div class="list-top">
			<div class="menu">
				<!-- <el-input placeholder="" v-model="filter.query" class="input-with-select" clearable
                        @keyup.enter="search">
                </el-input>
                <div class="menu-item pointer" style="width: 38px;" @click="search">
                    <i class="el-icon-search"></i>
                </div> -->
				<el-select
					v-model="filter.status"
					placeholder="所有状态"
					clearable
					filterable
					@change="filterChange"
				>
					<el-option
						v-for="item in filter.statusList"
						:key="item.value"
						:label="item.label"
						:value="item.value"
					>
					</el-option>
				</el-select>
				<div style="flex: 1;"></div>
				<div class="menu-item pointer" style="width: 38px;" @click="fetchList">
						<i class="el-icon-refresh"></i>
					</div>
				<div class="menu-item pointer" style="width: 118px;" @click="add">
					新增任务
				</div>
				<button
					class="menu-item pointer"
					style="width: 118px;"
					@click="createJobDialog"
				>
					生成作业
				</button>
			</div>
		</div>

		<el-card class="table-container" shadow="never">
			<div class="list-table">
				<el-table
					ref="table"
					:height="tableHeight"
					:border="false"
					:header-cell-style="{'background-color': '#2A2F3F', color: '#ffffff'}"
					:cell-style="tableCellStyle"
					:data="table.data"
					@selection-change="selectionChange"
				>
					<el-table-column
						type="selection"
						width="50"
						:selectable="taskSelectable"
					></el-table-column>
					<el-table-column prop="id" label="ID"></el-table-column>
					<el-table-column prop="by_job_id" label="作业ID"></el-table-column>
					<el-table-column
						prop="use_scenario.name"
						label="场景"
					></el-table-column>
					<el-table-column label="受测系统" prop="ads"></el-table-column>
					<el-table-column
						label="测试时间（秒）"
						prop="time_limit"
					></el-table-column>
					<el-table-column label="状态">
						<template #default="scope">
							{{ displayStatus(scope.row.status) }}
						</template>
					</el-table-column>
					<el-table-column label="操作">
						<template #default="scope">
							<!-- <el-button type="text" @click="editTask(scope.row)">编辑
                            </el-button> -->
							<!-- <el-popconfirm
								title="确定删除任务吗？"
								confirmButtonText="确定"
								cancelButtonText="取消"
								@confirm="remove(scope.row)"
							>
								<template #reference>
									<el-button
										:disabled="
											scope.row.status == 'isRunning' || scope.row.by_job_id
										"
										type="text"
										>删除</el-button
									>
								</template>
							</el-popconfirm> -->

							<el-button
								type="text"
								@click="remove(scope.row)"
								>删除</el-button
							>
						</template>
					</el-table-column>
				</el-table>
			</div>
			<div class="list-bottom">
				<!-- <batch-operation :operations="batch.operations" :targets="batch.targets"
                                 @batchDone="fetchList"></batch-operation> -->
				<el-pagination
					background
					@current-change="fetchPageList"
					v-model:current-page="page.currentPage"
					:page-size="20"
					layout="total, prev, pager, next"
					:total="page.totalCount"
				>
				</el-pagination>
			</div>
		</el-card>
		<el-dialog
			center
			title="新增角色"
			v-model="addDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<!-- 用ref.prop 去 校验 model.prop -->
			<el-form :model="form" ref="addForm" :rules="rules" label-width="100px">
				<el-form-item label="名称：" prop="label">
					<el-input
						v-model="form.label"
						maxlength="8"
						placeholder="请输入"
					></el-input>
				</el-form-item>
				<el-form-item label="权限：" prop="authorities">
					<el-select
						v-model="form.authorities"
						filterable
						placeholder="请选择"
						multiple
					>
						<el-option
							v-for="item in allAuthorities"
							:key="item.id"
							:value="item.id"
							:label="item.label"
						></el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button type="primary" @click="addDialog.visible = false"
						>取 消</el-button
					>
					<el-button type="primary" @click="addConfirm">确 认</el-button>
				</div>
			</template>
		</el-dialog>
		<el-dialog
			center
			title="编辑角色"
			v-model="editDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<!-- 用ref.prop 去 校验 model.prop -->
			<el-form :model="form" ref="editForm" :rules="rules" label-width="100px">
				<el-form-item label="名称：" prop="label">
					<el-input
						v-model="form.label"
						maxlength="11"
						placeholder="请输入"
					></el-input>
				</el-form-item>
				<el-form-item label="角色：" prop="authorities">
					<el-select
						v-model="form.authorities"
						filterable
						placeholder="请选择"
						multiple
						@keyup.enter="editConfirm"
					>
						<el-option
							v-for="item in allAuthorities"
							:key="item.id"
							:value="item.id"
							:label="item.label"
						></el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button type="primary" @click="editDialog.visible = false"
						>取 消</el-button
					>
					<el-button type="primary" @click="editConfirm">确 认</el-button>
				</div>
			</template>
		</el-dialog>

		<el-dialog
			center
			title="生成作业"
			v-model="jobDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<el-form label-width="100px">
				<el-form-item label="名称：">
					<el-input v-model="jobDialog.name" placeholder="请输入"></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button type="primary" @click="jobDialog.visible = false"
						>取 消</el-button
					>
					<el-button type="primary" @click="createJob">确 认</el-button>
				</div>
			</template>
		</el-dialog>
	</div>
</template>

<script>
// import BatchOperation from "../../../components/BatchOperation"

export default {
	components: {
		// 'batch-operation': BatchOperation
	},
	data() {
		return {
			loading: false,
			filter: {
				query: '',
				status: '',
				statusList: [
					{
						value: 'Ready',
						label: '未运行',
					},
					{
						value: 'isRunning',
						label: '运行中',
					},
					{
						value: 'notRunning',
						label: '已完成',
					},
				],
			},
			table: {
				data: [],
			},
			page: {
				totalCount: 0,
				currentPage: 1,
			},
			batch: {
				operations: [
					{
						label: '启用',
						url: '/role/enable',
						method: 'put',
					},
					{
						label: '停用',
						url: '/role/disable',
						method: 'put',
					},
				],
				targets: [],
			},
			addDialog: {
				visible: false,
			},
			editDialog: {
				visible: false,
			},
			jobDialog: {
				visible: false,
				name: '',
			},
			allAuthorities: [],
			form: {
				id: '',
				label: '',
				authorities: [],
			},
			rules: {
				label: this.$validation.fullName,
			},
			tableHeight: 600,
			resizeFlag: null,
		};
	},
	watch: {},
	computed: {},
	methods: {
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
				url: this.$basePath + '/tasks',
				params: {
					status: this.filter.status,
				},
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response) {
						this.table.data =
							response.slice(
								(this.page.currentPage - 1) * 20,
								this.page.currentPage * 20
							) || [];
						this.page.totalCount = response.length;
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		fetchPageList(page) {
			this.page.currentPage = page;
			this.fetchList();
		},
		displayAuthorities(authorities) {
			let labels = authorities.map((item) => {
				return item.label;
			});
			return labels.join(',');
		},
		displayStatus(status) {
			let item = this.filter.statusList.find((item) => {
				return item.value === status;
			});
			return item && item.label;
		},
		selectionChange(selection) {
			this.batch.targets = selection.map((item) => {
				return item.id;
			});
		},
		remove(row) {
			if(row.status == 'isRunning' || row.by_job_id){
				this.$message({
						message: '请先在对应作业中删除该任务',
						type: 'warning',
					});
				return;
			}
			this.loading = true;
			this.$axios({
				method: 'delete',
				url: this.$basePath + `/tasks/${row.id}`,
			})
				.then(() => {
					this.loading = false;
					this.$message({
						message: '操作成功',
						type: 'success',
					});
					this.fetchList();
				})
				.catch(() => {
					this.loading = false;
				});
		},
		fetchAuthorities() {
			this.loading = true;
			this.$axios({
				method: 'get',
				url: this.$basePath + '/role/authority',
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response) {
						this.allAuthorities = response.data;
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		/*******  新增 对话框  *******/
		add() {
			this.$router.replace({path: '/op/task/edit'});
		},
		createJobDialog() {
			if (!this.batch.targets.length) {
				this.$message({
					message: '请选择任务',
					type: 'error',
				});
				return;
			}
			this.jobDialog.visible = true;
		},
		createJob() {
			this.$axios({
				method: 'post',
				url: this.$basePath + '/jobs',
				data: {
					desc: this.jobDialog.name || '',
					tasks_id: this.batch.targets,
				},
			})
				.then((response) => {
					response = response.data;
					if (response) {
						this.jobDialog.visible = false;
						this.$message({
							message: '操作成功',
							type: 'success',
						});
						setTimeout(() => {
							// this.fetchList();
							this.$router.replace({path: '/op/job/list'});
						}, 1000);
					}
				})
				.catch(() => {});
		},
		addConfirm() {
			this.$refs.addForm.validate((valid) => {
				if (valid) {
					this.addSubmit();
				} else {
					return false;
				}
			});
		},
		addSubmit() {
			this.loading = true;
			this.$axios({
				method: 'post',
				url: this.$basePath + '/role',
				data: {
					label: this.form.label,
					authorityIds: this.form.authorities,
				},
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response.code == '0') {
						this.addDialog.visible = false;
						this.$message({
							message: '操作成功',
							type: 'success',
						});
						this.fetchList();
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		/*******  编辑 对话框  *******/
		edit(row) {
			this.form.id = row.id;
			this.form.label = row.label;
			this.form.authorities = row.authorities.map((item) => {
				return item.id;
			});
			this.editDialog.visible = true;
			this.fetchAuthorities();
		},
		editConfirm() {
			this.$refs.editForm.validate((valid) => {
				if (valid) {
					this.editSubmit();
				} else {
					return false;
				}
			});
		},
		editSubmit() {
			this.loading = true;
			this.$axios({
				method: 'put',
				url: this.$basePath + '/role/' + this.form.id,
				data: {
					label: this.form.label,
					authorityIds: this.form.authorities,
				},
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response.code == '0') {
						this.editDialog.visible = false;
						this.$message({
							message: '操作成功',
							type: 'success',
						});
						this.fetchList();
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		tableCellStyle({row, columnIndex}) {
			return Object.assign(
				{color: '##C1C1C8', 'font-size': '14px'},
				{'background-color': row.type == 'subfolder' ? '#141926' : '#202533'},
				columnIndex < 6 ? {color: '#C1C1C8'} : {}
			);
		},
		taskSelectable(row) {
			return !row.by_job_id;
		},
		editTask(row) {
			this.$router.replace({path: '/op/task/edit', query: {id: row.id}});
		},
		getTableHeight() {
			this.tableHeight = window.innerHeight - 188 - 150;
			// console.log(this.tableHeight,window.innerHeight,this.$refs.table.$el.offsetTop)
		},
	},
	mounted: function() {
		this.fetchList();
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
	beforeRouteLeave(to, from, next) {
		window.onresize = null;
		next();
	},
};
</script>

<style scoped lang="less">
.role-list {
	.el-dialog {
		.el-select {
			width: 360px;
		}
	}
}
</style>
