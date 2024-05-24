<template>
    <div class="merchant-list" v-loading="loading">
        <div class="list-top">
            <span class="page-title">代理</span>
            <el-button type="primary" icon="el-icon-plus" class="add-btn" @click="add">新增</el-button>
            <el-input placeholder="按代理昵称、实名查询" v-model="filter.query" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
        </div>
        <div class="list-filter">
            <el-select v-model="filter.status" placeholder="所有状态" clearable filterable @change="filterChange">
                <el-option v-for="item in filter.statusList" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>
        </div>
        <div class="list-table">
            <el-table :data="table.data">
                <el-table-column prop="id" label="ID" width="50px"></el-table-column>
                <el-table-column prop="nickname" label="昵称" width="100px"></el-table-column>
                <el-table-column prop="realName" label="实名" width="100px"></el-table-column>
                <el-table-column prop="idNum" label="身份证号" width="200px"></el-table-column>
                <el-table-column prop="bankNum" label="银行卡号" width="200px"></el-table-column>
                <el-table-column prop="phoneNum" label="手机号" width="120px"></el-table-column>
                <el-table-column prop="code" label="Code" width="250px"></el-table-column>
                <el-table-column prop="volumeTotal" label="总销售额"></el-table-column>
                <el-table-column prop="volumeSurplus" label="新销售额"></el-table-column>
                <el-table-column prop="takeTotal" label="总提成"></el-table-column>
                <el-table-column prop="takeSurplus" label="未提现的提成"></el-table-column>
                <el-table-column prop="takePercent" label="当前提成百分比"></el-table-column>
                <el-table-column label="状态">
                    <template #default="scope">
                        {{displayStatus(scope.row.status)}}
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="text" @click="enable(scope.row)" v-if="scope.row.status == 'forbidden'">启用
                        </el-button>
                        <el-button type="text" @click="disable(scope.row)" v-if="scope.row.status == 'normal'">禁用
                        </el-button>
                        <el-button type="text" @click="edit(scope.row)">编辑</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="list-bottom">
            <el-pagination background @current-change="fetchList" v-model:current-page="page.currentPage"
                           :page-size="10" layout="total, prev, pager, next" :total="page.totalCount">
            </el-pagination>
        </div>
        <el-dialog title="新增" v-model="addDialog.visible" width="500px" :close-on-click-modal="false">
            <el-form :model="addDialog" ref="addForm" :rules="rules" label-width="100px">
                <el-form-item label="昵称：" prop="nickname">
                    <el-input v-model="addDialog.nickname" placeholder="请输入"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="addDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="addConfirm" v-loading="addDialog.loading">确 认</el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="编辑" v-model="editDialog.visible" width="500px" :close-on-click-modal="false">
            <el-form :model="editDialog" ref="editForm" :rules="rules" label-width="100px">
                <el-form-item label="昵称：" prop="nickname">
                    <el-input v-model="editDialog.nickname" placeholder="请输入"></el-input>
                </el-form-item>
                <el-form-item label="真名：" prop="realName">
                    <el-input v-model="editDialog.realName" placeholder="请输入"></el-input>
                </el-form-item>
                <el-form-item label="身份证号：" prop="idNum">
                    <el-input v-model="editDialog.idNum" placeholder="请输入"></el-input>
                </el-form-item>
                <el-form-item label="银行卡号：" prop="bankNum">
                    <el-input v-model="editDialog.bankNum" placeholder="请输入"></el-input>
                </el-form-item>
                <el-form-item label="手机号：" prop="phoneNum">
                    <el-input v-model="editDialog.phoneNum" placeholder="请输入"></el-input>
                </el-form-item>
            </el-form>
            <div class="dialog-footer">
                <el-button @click="editDialog.visible = false">取 消</el-button>
                <el-button type="primary" @click="editConfirm">确 认</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
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
                            label: '正常'
                        },
                        {
                            value: 'forbidden',
                            label: '禁用'
                        }
                    ]
                },
                table: {
                    data: []
                },
                page: {
                    totalCount: 0,
                    currentPage: 1
                },
                editDialog: {
                    visible: false,
                    id: '',
                    nickname: '',
                    realName: '',
                    idNum: '',
                    bankNum: '',
                    phoneNum: ''

                },
                addDialog: {
                    visible: false,
                    loading: false,
                    nickname: ''
                },
                rules: {
                    nickname: [
                        {required: true, message: '请填写', trigger: "blur"}
                    ]
                }
            }
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
                this.filter.query = "";
                this.fetchList();
            },
            displayStatus(status) {
                let item = this.filter.statusList.find((item) => {
                    return item.value === status;
                });
                return item && item.label;
            },
            fetchList() {
                this.loading = true;
                this.$axios({
                    method: "get",
                    url: this.$basePath + "/agent",
                    params: {
                        pageSize: 10,
                        pageNum: this.page.currentPage,
                        search: this.filter.query,
                        status: this.filter.status
                    },
                    data: {}
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if (response) {
                        this.table.data = response.data.list || [];
                        this.page.totalCount = response.data.total;
                    }
                }).catch(() => {
                    this.loading = false;
                });
            },
            enable(row) {
                this.$confirm('确认启用该用户?', '确认', {
                    confirmButtonText: '确认',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.operateAjax("/agent/enable", [row.id]);
                }).catch(() => {
                });
            },
            disable(row) {
                this.$confirm('确认禁用该用户?', '确认', {
                    confirmButtonText: '确认',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.operateAjax("/agent/forbid", [row.id]);
                }).catch(() => {
                });
            },
            operateAjax(url, ids) {
                this.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + url,
                    data: ids
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if (response.code == 0) {
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.loading = false;
                });
            },
            /*******  编辑 对话框  *******/
            edit(row) {
                this.editDialog.id = row.id;
                this.editDialog.nickname = row.nickname;
                this.editDialog.realName = row.realName;
                this.editDialog.idNum = row.idNum;
                this.editDialog.bankNum = row.bankNum;
                this.editDialog.phoneNum = row.phoneNum;
                this.editDialog.visible = true;
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
                    method: "put",
                    url: this.$basePath + "/agent/" + this.editDialog.id,
                    data: this.editDialog
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.editDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.loading = false;
                });
            },
            /*******  新增 对话框  *******/
            add() {
                this.addDialog.visible = true;
                this.addDialog.nickname = '';
                this.$nextTick(function () {
                    this.$refs.addForm.clearValidate();
                });
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
                this.addDialog.loading = true;
                this.$axios({
                    method: "post",
                    url: this.$basePath + "/agent",
                    data: {
                        nickname: this.addDialog.nickname
                    }
                }).then((response) => {
                    this.addDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.addDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.addDialog.loading = false;
                });
            }
        },
        mounted: function () {
            this.fetchList();
        }
    }
</script>

<style scoped lang="less">
</style>