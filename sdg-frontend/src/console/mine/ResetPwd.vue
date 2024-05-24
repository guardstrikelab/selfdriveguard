<template>
    <div class="basic-information" v-loading="loading">
        <div class="add-top">
            修改密码
        </div>
        <div class="add-form">
            <div class="add-tip"><span>*</span>为必填项</div>
            <el-form ref="form" :model="form" :rules="validate" :label-position="'left'" label-width="130px">
                <el-form-item label="新密码：" prop="newPassword">
                    <el-input type="password" v-model="form.newPassword" maxlength="16" placeholder="请输入新密码"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="validateForm">保存</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>

    export default {
        data () {
            return {
                loading: false,
                form: {
                    newPassword: ''
                },
                validate: {
                    newPassword: this.$validation.password
                }
            }
        },
        computed: {},
        watch: {},
        methods: {
            validateForm(){
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.submit();
                    }
                });
            },
            submit(){
                this.loading = true;
                this.$axios({
                    method: "post",
                    url: this.$basePath + "/auth/reset-password",
                    data: {
                        "token": this.$store.state.access_token,
                        "password": this.form.newPassword
                    }
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if(response.code == "0"){
                        this.$message({
                            message: "修改成功",
                            type: 'success'
                        });
                        this.form.oldPassword= '';
                        this.form.newPassword= '';
                        this.form.repeatPwd= '';
                        this.$nextTick(function () {
                            this.$refs.form.clearValidate();
                        });
                    }
                }).catch(()=>{
                    this.loading = false;
                });
            }
        },
        mounted: function () {
        }
    }
</script>

<style scoped lang="less">
    .el-input,.el-select{
        width: 400px;
    }
    .form-tip{
        color: #B7B7B7;
        margin: 0 0 30px;
    }
</style>