<template>
    <div class="withdraw-list" v-loading="loading">
        <div class="list-top">
            <span class="page-title">提现记录</span>
            <el-button type="primary" icon="el-icon-plus" class="add-btn" @click="add">新增</el-button>
            <el-input placeholder="按代理真名或昵称查询" v-model="filter.query" class="input-with-select" clearable
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
                <el-table-column prop="id" label="ID"></el-table-column>
                <el-table-column prop="agentId" label="代理ID"></el-table-column>
                <el-table-column prop="realName" label="代理真名"></el-table-column>
                <el-table-column prop="nickname" label="代理昵称"></el-table-column>
                <el-table-column prop="volume" label="提现金额"></el-table-column>
                <el-table-column prop="createTime" label="创建时间"></el-table-column>
                <el-table-column prop="createTime" label="完成时间"></el-table-column>
                <el-table-column label="状态">
                    <template #default="scope">
                        {{displayStatus(scope.row.status)}}
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="text" @click="paid(scope.row)" v-if="scope.row.status == 'handling'">改为已支付
                        </el-button>
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
                <el-form-item label="代理ID：" prop="agentId">
                    <el-input v-model="addDialog.agentId" placeholder="请输入" type="number"></el-input>
                </el-form-item>
                <el-form-item label="提现额：" prop="volume">
                    <el-input v-model="addDialog.volume" placeholder="请输入" type="number"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="addDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="addConfirm" v-loading="addDialog.loading">确 认</el-button>
                </div>
            </template>
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
                    status: '',
                    statusList: [
                        {
                            value: 'handling',
                            label: '支付中'
                        },
                        {
                            value: 'paid',
                            label: '已支付'
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
                addDialog: {
                    visible: false,
                    loading: false,
                    agentId: '',
                    volume: ''
                },
                rules: {

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
                    url: this.$basePath + "/withdraw",
                    params: {
                        pageSize: 10,
                        pageNum: this.page.currentPage,
                        search: this.filter.query,
                        status: this.filter.status
                    }
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
            /*******  新增 对话框  *******/
            add() {
                this.addDialog.visible = true;
                this.addDialog.agentId = '';
                this.addDialog.volume = '';
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
                    url: this.$basePath + "/withdraw",
                    data: {
                        agentId: this.addDialog.agentId,
                        volume: this.addDialog.volume
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
            },
            /** 已支付 对话框 **/
            paid(row) {
                this.$confirm('确认已支付?', '确认', {
                    confirmButtonText: '确认',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.operateAjax("/withdraw/" + row.id + "/paid");
                }).catch(() => {
                });
            },
            operateAjax(url) {
                this.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + url
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
            }
        },
        mounted: function () {
            this.fetchList();
        }
    }
</script>

<style scoped lang="less">
</style>