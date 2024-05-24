<template>
	<div
		class="operator-list"
		v-loading="loading"
		style="min-height: calc(100vh - 100px);"
		element-loading-text="加载中"
		element-loading-spinner="el-icon-loading"
		element-loading-background="rgba(0, 0, 0, 0.8)"
	>
		<div class="list-top">
			<div class="menu">
				<!-- <span class="page-title">作业</span> -->
				<!-- <el-input placeholder="" v-model="filter.query" class="input-with-select" clearable @keyup.enter="search"></el-input>
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
				<div style="flex:1"></div>
				<div class="menu-item pointer" style="width: 38px;" @click="fetchList">
						<i class="el-icon-refresh"></i>
					</div>
				<div class="menu-item pointer" style="width: 118px;" @click="add">
					新建作业
				</div>
				<button class="menu-item pointer" style="width: 118px;" @click="run(0)">
					执行作业
				</button>
			</div>
		</div>
		<el-card class="table-container" shadow="never">
			<div class="list-table">
				<el-table
					ref="table"
					:height="tableHeight"
					:data="table.data"
					@selection-change="selectionChange"
					:border="false"
					:header-cell-style="{'background-color': '#2A2F3F', color: '#ffffff'}"
					:cell-style="tableCellStyle"
				>
					<el-table-column
						type="selection"
						width="50"
						:selectable="checkSelect"
					></el-table-column>
					<el-table-column prop="id" label="任务ID"></el-table-column>
					<el-table-column prop="desc" label="任务名称"></el-table-column>
					<el-table-column label="执行情况">
						<template #default="scope">
							{{
								scope.row.status == 'Running'
									? '运行中'
									: scope.row.status == 'Ready'
									? '未运行'
									: '已完成'
							}}
						</template>
					</el-table-column>
					<el-table-column label="操作" width="150">
						<template #default="scope">
							<el-button type="text" @click="edit(scope.row)">
								{{ scope.row.status == 'Ready' ? '修改' : '详情' }}
							</el-button>
							<el-button
								type="text"
								@click="remove(scope.row)"
								:disabled="scope.row.status == 'Running'"
								>删除</el-button
							>
						</template>
					</el-table-column>
				</el-table>
			</div>
			<div class="list-bottom">
				<!-- <el-button type="text" @click="run" :disabled="!targets.length">执行</el-button> -->
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
			title="新增人员"
			v-model="addDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<!-- 用ref.prop 去 校验 model.prop -->
			<el-form :model="form" ref="addForm" :rules="rules" label-width="100px">
				<el-form-item label="姓名：" prop="name">
					<el-input
						v-model="form.name"
						maxlength="8"
						placeholder="请输入"
					></el-input>
				</el-form-item>
				<el-form-item label="身份证号：" prop="idNumber">
					<el-input
						v-model="form.idNumber"
						maxlength="20"
						placeholder="请输入"
					></el-input>
				</el-form-item>
				<el-form-item label="手机号：" prop="username">
					<el-input
						v-model="form.username"
						maxlength="11"
						placeholder="请输入"
					></el-input>
				</el-form-item>
				<el-form-item label="角色：" prop="roles">
					<el-select
						v-model="form.roles"
						filterable
						placeholder="请选择"
						multiple
					>
						<el-option
							v-for="item in allRoles"
							:key="item.id"
							:value="item.id"
							:label="item.label"
						></el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="登录密码：" prop="password">
					<el-input
						v-model="form.password"
						maxlength="16"
						placeholder="请输入"
						type="password"
					></el-input>
				</el-form-item>
				<el-form-item label="重复密码：" prop="repeatPwd">
					<el-input
						v-model="form.repeatPwd"
						maxlength="16"
						placeholder="请输入"
						type="password"
						@keyup.enter="addConfirm"
					></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="addDialog.visible = false">取 消</el-button>
					<el-button type="primary" @click="addConfirm">确 认</el-button>
				</div>
			</template>
		</el-dialog>
		<el-dialog
			title="编辑人员"
			v-model="editDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<!-- 用ref.prop 去 校验 model.prop -->
			<el-form :model="form" ref="editForm" :rules="rules" label-width="100px">
				<el-form-item label="手机号：" prop="username">
					<el-input
						v-model="form.username"
						maxlength="11"
						placeholder="请输入"
					></el-input>
				</el-form-item>
				<el-form-item label="角色：" prop="roles">
					<el-select
						v-model="form.roles"
						filterable
						placeholder="请选择"
						multiple
						@keyup.enter="editConfirm"
					>
						<el-option
							v-for="item in allRoles"
							:key="item.id"
							:value="item.id"
							:label="item.label"
						></el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="editDialog.visible = false">取 消</el-button>
					<el-button type="primary" @click="editConfirm">确 认</el-button>
				</div>
			</template>
		</el-dialog>

		<el-dialog
			title="重置密码"
			v-model="resetDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<!-- 用ref.prop 去 校验 model.prop -->
			<el-form :model="form" ref="resetForm" :rules="rules" label-width="120px">
				<el-form-item label="新密码：" prop="password">
					<el-input
						v-model="form.password"
						maxlength="16"
						placeholder="请输入"
						type="password"
					></el-input>
				</el-form-item>
				<el-form-item label="重复新密码：" prop="repeatPwd">
					<el-input
						v-model="form.repeatPwd"
						maxlength="16"
						placeholder="请输入"
						type="password"
						@keyup.enter.="resetConfirm"
					></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="resetDialog.visible = false">取 消</el-button>
					<el-button type="primary" @click="resetConfirm">确 认</el-button>
				</div>
			</template>
		</el-dialog>
	</div>
</template>

<script>
import Md5 from 'md5';

export default {
	components: {},
	data() {
		return {
			loading: false,
			filter: {
				query: '',
				status: 'normal',
				statusList: [
					{
						value: 'normal',
						label: '正常',
					},
					{
						value: 'disabled',
						label: '停用',
					},
				],
			},
			table: {
				data: [],
				selection: [],
			},
			page: {
				totalCount: 0,
				currentPage: 1,
			},
			targets: [],
			allRoles: [],
			addDialog: {
				visible: false,
			},
			editDialog: {
				visible: false,
			},
			resetDialog: {
				visible: false,
			},
			form: {
				id: '',
				name: '',
				idNumber: '',
				username: '',
				roles: [],
				password: '',
				repeatPwd: '',
			},
			rules: {
				name: this.$validation.fullName,
				idNumber: this.$validation.idNumber,
				username: this.$validation.mobile,
				password: this.$validation.password,
				repeatPwd: this.$validation.repeatPwd.call(this, 'form.password'),
				roles: [{required: true, message: '请选择角色'}],
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
		displayRoles(roles) {
			let roleLabels = roles.map((item) => {
				return item.label;
			});
			return roleLabels.join(',');
		},
		displayStatus(status) {
			let item = this.filter.statusList.find((item) => {
				return item.value === status;
			});
			return item && item.label;
		},
		selectionChange(selection) {
			this.targets = selection.map((item) => {
				return item.id;
			});
		},
		fetchList() {
			this.loading = true;
			this.$axios({
				method: 'get',
				url: this.$basePath + '/jobs',
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
		fetchRoles() {
			this.loading = true;
			this.$axios({
				method: 'get',
				url: this.$basePath + '/operator/role',
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response) {
						this.allRoles = response.data;
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		/*******  新增 对话框  *******/
		add() {
			this.$router.replace({path: '/op/job/edit'});
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
				url: this.$basePath + '/operator',
				data: {
					name: this.form.name,
					idNumber: this.form.idNumber,
					username: this.form.username,
					roleIds: this.form.roles,
					pwd: Md5(this.form.password),
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
			this.$router.replace({
				path: '/op/job/edit',
				query: {id: row.id, run: row.status == 'Running'},
			});
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
		remove(row) {
			this.loading = true;
			this.$axios({
				method: 'delete',
				url: this.$basePath + `/jobs/${row.id}`,
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					try {
						this.$message({
							message: '操作成功',
							type: 'success',
						});
						this.fetchList();
					} catch (e) {}
					if (response) {
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		run(index) {
			if (index == 0) {
				if (!this.targets[index]) {
					if (!this.targets.length) {
						this.$message({
							message: '请选择作业',
							type: 'error',
						});
						return;
					}
				}
				this.loading = true;
			}
			if (!this.targets[index]) {
				this.loading = false;
				this.$message({
					message: '操作成功',
					type: 'success',
				});
				setTimeout(() => {
					this.fetchList();
				}, 1000);
				return;
			}
			this.$axios({
				method: 'post',
				url: this.$basePath + `/jobs/${this.targets[index]}/run`,
				data: {
					pwd: Md5(this.form.password),
				},
			})
				.then((response) => {
					response = response.data;
					if (response) {
						this.run(index + 1);
					}
				})
				.catch(() => {
					this.loading = false;
				});
		},
		checkSelect(row) {
			return row.status != 'Running';
		},
		tableCellStyle({row, columnIndex}) {
			return Object.assign(
				{color: '##C1C1C8', 'font-size': '14px'},
				{'background-color': row.type == 'subfolder' ? '#141926' : '#202533'},
				columnIndex < 8 ? {color: '#C1C1C8'} : {}
			);
		},
		getTableHeight() {
			this.tableHeight = window.innerHeight - 188 - 150;
		},
		resetConfirm(){}
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
};
</script>

<style scoped lang="less">
.operator-list {
	.el-dialog {
		.el-select {
			width: 360px;
		}
	}
}
</style>
