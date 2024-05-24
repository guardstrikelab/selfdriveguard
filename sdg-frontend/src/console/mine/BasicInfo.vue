<template>
    <div class="basic-information" v-loading="loading">
        <div class="add-top">
            基本信息
        </div>
        <div class="add-form">
            <el-form :label-position="'left'" label-width="130px">
                <el-form-item label="ID：">
                    {{myDetail.id}}
                </el-form-item>
                <el-form-item label="email：">
                    {{myDetail.email}}
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                loading: false
            }
        },
        computed: {
            myDetail: function () {
                return this.$store.state.myDetail || {};
            },
            roles: function () {
                let roles = this.myDetail.roles || [];
                let roleLabels = roles.map((item) => {
                    return item.label;
                });
                return roleLabels.join(',');
            }
        },
        watch: {},
        methods: {},
        mounted: function () {
        }
    }
</script>

<style scoped lang="less">
</style>