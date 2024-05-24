<template>
    <div class="product-list" v-loading="loading">
        <div class="list-top">
            <span class="page-title">科</span>
            <el-input placeholder="按科名或目名查询" v-model="filter.query" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
        </div>
        <div class="list-table">
            <el-table ref="multipleTable" :data="table.data">
                <el-table-column prop="id" label="ID" width="60px"></el-table-column>
                <el-table-column prop="name" label="名称"></el-table-column>
                <el-table-column prop="alias" label="别名"></el-table-column>
                <el-table-column prop="latin" label="拉丁学名"></el-table-column>
                <el-table-column label="目">
                    <template #default="scope">
                        {{scope.row.parentName}} {{scope.row.parentLatin}}
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="list-bottom">
            <el-pagination background @current-change="fetchList" v-model:current-page="page.currentPage"
                           :page-size="20" layout="total, prev, pager, next" :total="page.totalCount">
            </el-pagination>
        </div>
    </div>
</template>

<script>
    export default {
        components: {
        },
        data() {
            return {
                loading: false,
                filter: {
                    query: ''
                },
                table: {
                    data: []
                },
                page: {
                    totalCount: 0,
                    currentPage: 1
                }
            }
        },
        computed: {},
        watch: {},
        methods: {
            search() {
                this.page.currentPage = 1;
                this.fetchList();
            },
            fetchList() {
                this.loading = true;
                this.$axios({
                    method: "get",
                    url: this.$basePath + "/mushroom/family",
                    params: {
                        pageSize: 20,
                        pageNum: this.page.currentPage,
                        search: this.filter.query
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
            }
        },
        mounted: function () {
            this.fetchList();
        }
    }
</script>

<style scoped lang="less">

</style>