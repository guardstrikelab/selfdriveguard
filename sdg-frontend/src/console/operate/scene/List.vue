<template>
	<div
		v-loading="loading"
		style="min-height: calc(100vh - 100px);"
		element-loading-text="加载中"
		element-loading-spinner="el-icon-loading"
		element-loading-background="rgba(0, 0, 0, 0.8)"
	>
		<div class="list-top">
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

				<div class="menu-item pointer" style="width: 38px;" @click="fetchList">
					<i class="el-icon-refresh"></i>
				</div>
				<!-- <div class="menu-item" style="width: 118px;">全部遍历</div> -->
				<div class="menu-item" style="width: 150px;">
					<el-select
						class="level-select"
						v-model="filter.level"
						placeholder="层级"
						@change="filterChange"
					>
						<el-option label="当前层级" value="cur"></el-option>
						<el-option label="所有层级" value="all"></el-option>
					</el-select>
				</div>
				<div class="menu-item pointer" style="width: 132px;" @click="addFolder">
					新建文件夹
				</div>
			</div>

			<div class="menu">
				<!-- <el-input class="menu-item"  style="width: 300px;" placeholder=""  v-model="filter.query"  clearable 
                      @keyup.enter="search">
                </el-input>
                <div class="menu-item pointer"  style="width: 38px;" @click="search">
                    <i class="el-icon-search"></i>
                </div> -->
				<div style="flex: 1;"></div>
				<div
					class="menu-item pointer"
					style="width: 132px;border: 1px solid #CDCED4;"
					@click="addScene"
				>
					新建场景
				</div>
				<!-- <div class="menu-item" style="width: 132px;border: 1px solid #CDCED4;">删除</div> -->
			</div>
		</div>
		<el-card class="table-container" shadow="never">
			<div class="list-table scene-table">
				<el-table
					ref="table"
					:height="tableHeight"
					:border="false"
					:header-cell-style="{'background-color': '#2A2F3F', color: '#ffffff'}"
					:cell-style="tableCellStyle"
					:data="table.data"
					@selection-change="selectionChange"
				>
					<!-- <el-table-column type="selection" width="50"></el-table-column> -->
					<el-table-column label="名称">
						<template #default="scope">
							<div v-if="scope.row.type == 'scenario'">
								{{ scope.row.name }}
							</div>
							<div v-else @click="changeFolder(scope.row)" class="pointer">
								<i class="el-icon-folder" style="margin-right: 5px;"></i>
								{{ scope.row.name }}
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
					<el-table-column label="标签">
						<template #default="scope">
							<el-button
								type="text"
								@click="editTag(scope.row)"
								icon="el-icon-view"
								v-if="scope.row.tags"
							>
								点击查看
							</el-button>
							<div v-else style="color: #C1C1C8;">-</div>
						</template>
					</el-table-column>
					<el-table-column label="操作">
						<template #default="scope">
							<el-button
								type="text"
								@click="editFolder(scope.row)"
								v-if="scope.row.type == 'subfolder'"
								>修改
							</el-button>
							<el-button
								type="text"
								@click="editScenario(scope.row)"
								v-if="scope.row.type == 'scenario'"
								>详情
							</el-button>
							<el-popconfirm
								title="确定删除目录吗？"
								v-if="scope.row.type == 'subfolder'"
								confirmButtonText="确定"
								cancelButtonText="取消"
								@confirm="deleteFolder(scope.row)"
							>
								<template #reference>
									<el-button type="text">删除</el-button>
								</template>
							</el-popconfirm>
							<el-popconfirm
								title="确定删除场景吗？"
								v-if="scope.row.type == 'scenario'"
								confirmButtonText="确定"
								cancelButtonText="取消"
								@confirm="deleteScenario(scope.row)"
							>
								<template #reference>
									<el-button type="text">删除</el-button>
								</template>
							</el-popconfirm>
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
			title="新增目录"
			v-model="addFolderDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<el-form
				:model="addFolderDialog"
				ref="addFolderForm"
				:rules="rules"
				label-width="100px"
			>
				<el-form-item label="名称：" prop="name">
					<el-input
						v-model="addFolderDialog.name"
						maxlength="8"
						placeholder="请输入"
					></el-input>
				</el-form-item>
				<el-form-item label="描述：" prop="desc">
					<el-input
						type="textarea"
						v-model="addFolderDialog.desc"
						placeholder="请输入"
					></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button type="primary" @click="addFolderDialog.visible = false"
						>取 消</el-button
					>
					<el-button type="primary" @click="addFolderConfirm">确 认</el-button>
				</div>
			</template>
		</el-dialog>
		<el-dialog
			center
			title="修改目录"
			v-model="editFolderDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<el-form
				:model="editFolderDialog"
				ref="editFolderForm"
				:rules="rules"
				label-width="100px"
			>
				<el-form-item label="名称：" prop="name">
					<el-input
						v-model="editFolderDialog.name"
						maxlength="8"
						placeholder="请输入"
					></el-input>
				</el-form-item>
				<el-form-item label="描述：" prop="desc">
					<el-input
						type="textarea"
						v-model="editFolderDialog.desc"
						placeholder="请输入"
					></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<div class="dialog-footer">
					<el-button type="primary" @click="editFolderDialog.visible = false"
						>取 消</el-button
					>
					<el-button type="primary" @click="editFolderConfirm">确 认</el-button>
				</div>
			</template>
		</el-dialog>
		<el-dialog
			center
			title="场景标签"
			v-model="tagDialog.visible"
			width="500px"
			:close-on-click-modal="false"
		>
			<div class="tag-dialog">
				<el-tag
					:key="tag"
					v-for="(tag, index) in tagDialog.row.tags"
					closable
					:disable-transitions="false"
					@close="removeTag(index)"
				>
					{{ tag }}
				</el-tag>
				<el-input
					class="input-new-tag"
					v-if="tagDialog.inputVisible"
					v-model="tagDialog.inputValue"
					size="small"
					@keyup.enter="tagInputConfirm"
					@blur="tagInputConfirm"
					ref="tagInput"
				>
				</el-input>
				<el-button
					v-else
					class="button-new-tag"
					size="small"
					@click="showTagInput"
				>
					+</el-button
				>
			</div>
			<template #footer>
				<div class="dialog-footer">
					<!-- <el-button @click="tagDialog.visible = false">取 消</el-button>、 -->
					<el-button type="primary" @click="tagConfirm">确 认</el-button>
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
			folderChain: [],
			filter: {
				query: '',
				level: 'cur',
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
						label: '删除',
						url: '/authority',
						method: 'delete',
					},
				],
				targets: [],
			},
			addFolderDialog: {
				visible: false,
				name: '',
				desc: '',
			},
			editFolderDialog: {
				visible: false,
				name: '',
				desc: '',
			},
			tagDialog: {
				visible: false,
				inputVisible: false,
				inputValue: '',
				row: {},
			},
			rules: {
				name: this.$validation.fullName,
			},
			tableHeight: 600,
			resizeFlag: null,
		};
	},
	watch: {
		myDetail: {
			handler() {
				this.folderChain = [
					{
						id: this.myDetail.rootfolder,
						name: '全部场景',
					},
				];
				this.fetchList();
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
	},
	methods: {
		search() {
			if (!this.filter.query) return;
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
						let data = response.subfolders.concat(response.scenarios);
						this.table.data = data.slice(
							(this.page.currentPage - 1) * 20,
							this.page.currentPage * 20
						);
						this.page.totalCount = data.length;
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
						// this.table.data = response;
						// this.page.totalCount = this.table.data.length;
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
		selectionChange(selection) {
			this.batch.targets = selection.map((item) => {
				return item.id;
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
		deleteFolder(row) {
			this.loading = true;
			this.$axios({
				method: 'delete',
				url:
					this.$basePath +
					`/scen-folders/${this.curFolder.id}/sub-folders/${row.id}`,
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
		deleteScenario(row) {
			this.loading = true;
			this.$axios({
				method: 'delete',
				url:
					this.$basePath +
					`/scen-folders/${this.curFolder.id}/scenarios/${row.id}`,
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
		editScenario(row) {
			this.$router.replace({path: '/op/scene/edit', query: {id: row.id}});
		},
		addScene() {
			this.$router.replace({path: '/op/scene/edit', query: {folder: this.curFolder.id || ''}});
		},
		/*******  新增目录 对话框  *******/
		addFolder() {
			this.addFolderDialog.visible = true;
			this.addFolderDialog.name = '';
			this.addFolderDialog.desc = '';
			this.$nextTick(() => {
				this.$refs.addFolderForm.clearValidate();
			});
		},
		addFolderConfirm() {
			this.$refs.addFolderForm.validate((valid) => {
				if (valid) {
					this.addFolderSubmit();
				} else {
					return false;
				}
			});
		},
		addFolderSubmit() {
			this.loading = true;
			this.$axios({
				method: 'post',
				url: this.$basePath + `/scen-folders/${this.curFolder.id}/sub-folders`,
				data: {
					name: this.addFolderDialog.name,
					desc: this.addFolderDialog.desc,
				},
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response.id) {
						this.addFolderDialog.visible = false;
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
		/*******  修改目录 对话框  *******/
		editFolder(row) {
			this.editFolderDialog.visible = true;
			this.editFolderDialog.id = row.id;
			this.editFolderDialog.name = row.name;
			this.editFolderDialog.desc = row.desc;
			this.$nextTick(() => {
				this.$refs.editFolderForm.clearValidate();
			});
		},
		editFolderConfirm() {
			this.$refs.editFolderForm.validate((valid) => {
				if (valid) {
					this.editFolderSubmit();
				} else {
					return false;
				}
			});
		},
		editFolderSubmit() {
			this.loading = true;
			this.$axios({
				method: 'put',
				url: this.$basePath + `/scen-folders/${this.editFolderDialog.id}`,
				data: {
					name: this.editFolderDialog.name,
					desc: this.editFolderDialog.desc,
				},
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response.id) {
						this.editFolderDialog.visible = false;
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
		/*******  编辑 Tag 对话框  *******/
		editTag(row) {
			this.tagDialog.visible = true;
			this.tagDialog.row = JSON.parse(JSON.stringify(row));
		},
		removeTag(index) {
			this.tagDialog.row.tags.splice(index, 1);
		},
		showTagInput() {
			this.tagDialog.inputVisible = true;
			this.$nextTick(() => {
				this.$refs.tagInput.$refs.input.focus();
			});
		},
		tagInputConfirm() {
			if (this.tagDialog.inputValue) {
				if (this.tagDialog.row.tags.includes(this.tagDialog.inputValue)) {
					this.$message({
						message: 'Tag 重复',
					});
					return;
				} else {
					this.tagDialog.row.tags.push(this.tagDialog.inputValue);
				}
			}
			this.tagDialog.inputVisible = false;
			this.tagDialog.inputValue = '';
		},
		tagConfirm() {
			this.loading = true;
			this.$axios({
				method: 'put',
				url:
					this.$basePath +
					`/scen-folders/${this.curFolder.id}/scenarios/${this.tagDialog.row.id}`,
				data: this.tagDialog.row,
			})
				.then((response) => {
					this.loading = false;
					response = response.data;
					if (response.id) {
						this.tagDialog.visible = false;
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
		// 样式
		tableCellStyle({row, columnIndex}) {
			return Object.assign(
				{color: '##C1C1C8', 'font-size': '14px'},
				{'background-color': row.type == 'subfolder' ? '#141926' : '#202533'},
				columnIndex < 5 ? {color: '#C1C1C8'} : {}
			);
		},
		getTableHeight() {
			this.tableHeight =
				window.innerHeight - this.$refs.table.$el.offsetTop - 120;
			//    console.log(window.innerHeight,this.$refs.table.$el.offsetTop)
		},
	},
	mounted() {
		this.fetchList();
		this.getTableHeight();
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
	updated() {},
};
</script>

<style scoped lang="less">
.breadcrumb {
	// padding: 0 20px;
	.breadcrumb-item {
		cursor: pointer;
	}
}

.tag-dialog {
	width: 439px;
	height: 182px;
	background: #202533;
	border: 1px solid #353a4c;
	padding: 20px;
	.el-tag {
		min-width: 70px;
		height: 24px;
		line-height: 23px;
		color: #c1c1c8;
		background: #353a4c;
		border: none;
		margin-top: 10px;
	}
	.el-tag + .el-tag {
		margin-left: 10px;
	}

	.button-new-tag {
		text-align: right;
		margin-left: 10px;
		// height: 32px;
		// line-height: 30px;
		padding-top: 0;
		padding-bottom: 0;
	}

	.input-new-tag {
		width: 90px;
		margin-left: 10px;
		// vertical-align: bottom;
	}
}
</style>
