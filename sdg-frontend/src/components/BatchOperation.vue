<template>
    <div class="batch-operations">
        <el-button type="text" v-for="(item,index) in operations" :key="index" @click="batchMsgBox(index)"
                   :disabled="!targets.length || item.disabled">批量{{item.label}}
        </el-button>
    </div>
</template>

<script>
    import {h} from 'vue'

    export default {
        props: ['value', 'operations', 'targets'],  // value即上层传进来的model
        data() {
            return {}
        },
        watch: {},
        methods: {
            batchMsgBox(index) {
                let operation = this.operations[index];

                this.$msgbox({
                    title: operation.title || operation.label + "提示",
                    message: h('p', null, [
                        h('span', null, operation.head || "确认" + operation.label + "?"),
                        h('div', null, operation.message)
                    ]),
                    showCancelButton: true,
                    beforeClose: (action, instance, done) => {
                        if (action === 'confirm') {
                            done();
                            this.batchAjax(operation);
                        } else {
                            done();
                        }
                    }
                });
            },
            batchAjax(operation) {
                let data = this.targets;
                if (operation.fieldName) {
                    data = {};
                    data[operation.fieldName] = this.targets;
                }
                this.$axios({
                    method: operation.method || "post",
                    url: this.$basePath + operation.url,
                    data: data
                }).then((response) => {
                    this.batchResult(response.data);
                });
            },
            batchResult(response) {
                if (response.code == '0') {
                    this.$message({
                        message: '操作成功',
                        type: 'success',
                        duration: 2000,
                        center: true,
                        onClose: () => {
                        }
                    });
                    this.$emit('batchDone');
                    this.$emit('batchSuccess');
                } else {
                    this.$emit('batchDone');
                    this.$emit('batchFail');
                }
            }
        }
    }
</script>

<style scoped>

</style>
