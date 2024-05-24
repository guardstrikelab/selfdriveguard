<template>
    <div class="scene-edit">
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/op/scene/list' }">场景管理</el-breadcrumb-item>
            <el-breadcrumb-item v-if="$route.query.id">编辑场景</el-breadcrumb-item>
            <el-breadcrumb-item v-else>新建场景</el-breadcrumb-item>
        </el-breadcrumb>
        <div class="menu-container">
            <el-menu
            :default-active="menuSelectIndex"
            class="el-menu-demo"
            style="flex: 1;"
            mode="horizontal"
            @select="handleSelect"
            background-color="#141926"
            text-color="#fff"
            active-text-color="#4F5DEB">
                <el-menu-item index="1">状态</el-menu-item>
                <el-menu-item index="2">代码</el-menu-item>
                <!-- <el-menu-item index="3">预览</el-menu-item> -->
            </el-menu>
            <div class="menu-item pointer" style="width: 90px;border: 1px solid #CDCED4;" @click="back">返回</div>
            <div class="menu-item pointer" style="width: 90px;border: 1px solid #CDCED4;" type="primary" v-loading="loading" @click="create">保存</div>
        </div>
        <div class="form-container" v-show="menuSelectIndex == 1">
            <el-form :model="form" ref="form" :rules="rules" label-width="90px">
                <el-row>
                    <el-form-item label="名称：" prop="name"  >
                        <el-input class="menu-item" style="width:260px" v-model="form.name" maxlength="8" placeholder="请输入"></el-input>
                    </el-form-item>
                    <el-form-item label="存储位置：" style="margin-left: 100px;">
                        <div class="menu-item" style="width:100px">{{form.folder.name == 'root' ? '根目录' : form.folder.name}}</div>
                        <!-- <el-popover  placement="bottom-start" title="" :width="200" trigger="click" v-loading="loading">
                            <template #reference>
                                <el-button  class="menu-item" style="width:100px">{{form.folder.name}}</el-button>
                            </template>
                            <el-tree :data="folderTree" :props="treeProps" @node-click="treeNodeClick" :highlight-current="true"
                                    :expand-on-click-node="false" :lazy="true" node-key="id" :current-node-key="form.folder.id"
                                    :load="treeLoad"></el-tree>
                        </el-popover> -->
                    </el-form-item>
                </el-row>
                <el-row>
                    <el-form-item label="地图：" prop="map_name" required>
                        <el-select class="menu-item" style="width:260px" v-model="form.map_name" placeholder="请选择">
                            <el-option :label="map" :value="map" v-for="map in maps" :key="map"></el-option>
                        </el-select>
                    </el-form-item>
                    <!-- <el-form-item label="创建时间：">
                        <el-button type="text"></el-button>
                    </el-form-item> -->
                </el-row>
                <!-- <el-form-item label="代码：" prop="script" required="">
                    <el-input type="textarea" v-model="form.script" placeholder="请输入"></el-input>
                </el-form-item> -->
                <el-form-item label="描述：" prop="desc">
                    <div class="menu-item" style="min-height:100px;height:auto;max-width: 623px;">
                        <el-input width="60%"  type="textarea" :autosize="{ minRows: 4, maxRows: 4}" v-model="form.desc" placeholder=""></el-input>
                    </div>
                </el-form-item>
                <el-form-item label="标签：" prop="tags">
                    <div class="tag tag-dialog">
                        <el-tag :key="tag" v-for="(tag,index) in form.tags" closable :disable-transitions="false"
                                @close="removeTag(index)">
                            {{tag}}
                        </el-tag>
                        <el-input class="input-new-tag" v-if="tag.inputVisible" v-model="tag.inputValue"
                                size="small" @keyup.enter="tagInputConfirm" @blur="tagInputConfirm" ref="tagInput">
                        </el-input>
                        <el-button v-else class="button-new-tag" size="small" @click="showTagInput">+</el-button>
                    </div>
                </el-form-item>

            </el-form>
        </div>
        <div class="edit-container" v-show="menuSelectIndex == 2">
            <CodeEditor v-model:value="form.script" :scene="type" theme="base16-dark"></CodeEditor>
        </div>
        <div v-show="menuSelectIndex == 3">

        </div>
    </div>
</template>

<script>
    // import CodeMirror from 'codemirror/lib/codemirror.js';
    // import 'codemirror/lib/codemirror.css';

    // import 'codemirror/keymap/sublime'; 
    // import 'codemirror/theme/base16-dark.css';
    //     CodeMirror(document.querySelector("#codemirror"), {
    // value: "function myScript(){return 100;}\n",
    // mode:  "javascript"
    // });

    import CodeEditor from '@/components/CodeEditor.vue'
    export default {
        components:{
            CodeEditor
        },
        data() {
            return {
                loading: false,
                treeProps: {
                    children: 'children',
                    label: 'name',
                    isLeaf: 'isLeaf'
                },
                folderTree: [],
                maps: [],
                form: {
                    name: '',
                    language: "cartel",
                    folder: {
                        name: ''
                    },
                    map_name: '',
                    script: '',
                    desc: '',
                    tags: []
                },
                tag: {
                    inputVisible: false,
                    inputValue: ''
                },
                rules: {
                    name: this.$validation.fullName
                },
                menuSelectIndex:1,
                type:'edit'
            }
        },
        watch: {
            myDetail: {
                handler() {
                    this.initTree();
                    // this.form.folder.id = this.myDetail.rootfolder;
                    this.form.folder.id = this.$route.query.folder;
                },
                immediate: true
            }
        },
        computed: {
            myDetail() {
                return this.$store.state.myDetail || {};
            }
        },
        methods: {
            back() {
                this.$router.replace({path: '/op/scene/list'});
            },
            treeNodeClick(node) {
                this.form.folder = node;
            },
            treeLoad(node, resolve) {
                if (node.level === 0) {
                    return resolve([]);
                }
                this.$axios({
                    method: "get",
                    url: this.$basePath + `/scen-folders/${node.key}`
                }).then((response) => {
                    response = response.data;
                    if (response) {
                        let children = response.subfolders.map((item) => {
                            item.isLeaf = false;
                            return item;
                        });
                        resolve(children);
                    }
                }).catch(() => {
                });
            },
            initTree(){
                if(!this.myDetail.rootfolder){
                    return;
                }
                this.$axios({
                    method: "get",
                    // url: this.$basePath + `/scen-folders/${this.myDetail.rootfolder}`
                    url: this.$basePath + `/scen-folders/${this.$route.query.folder}`
                }).then((response) => {
                    response = response.data;
                    if (response) {
                        this.folderTree = response.subfolders.map((item) => {
                            item.isLeaf = false;
                            return item;
                        });
                        this.form.folder = response
                    }
                }).catch(() => {
                });
            },
            fetchDetail() {
                if (!this.$route.query.id) {
                    return;
                }
                this.loading = true;
                this.$axios({
                    method: "get",
                    url: this.$basePath + `/scenarios/${this.$route.query.id}`
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if (response) {
                        this.form.name = response.name;
                        this.form.desc = response.desc;
                        this.form.tags = response.tags;
                        this.form.script = response.script;
                        this.form.map_name = response.map_name;
                    }
                }).catch(() => {
                    this.loading = false;
                });
            },
            create() {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.submit();
                    } else {
                        return false;
                    }
                });
            },
            submit() {
                if(!this.form.script) {
                    this.$message({
						message: '请输入代码',
						type: 'warning',
					});
                    return;
                }
                this.loading = true;
                // console.log(this.form.folder.id)
                this.$axios({
                    method:this.$route.query.id?'update': "post",
                    // url: this.$basePath + `/scen-folders/${this.form.folder.id}/scenarios`,
                    url: this.$basePath + `/scen-folders/${this.$route.query.id?this.$route.query.id :this.form.folder.id}/scenarios`,
                    data: this.form
                }).then(() => {
                    this.loading = false;
                    this.$message({
                        message: '操作成功',
                        type: 'success'
                    });
                    this.$router.replace({path: '/op/scene/list'});
                }).catch(() => {
                    this.loading = false;
                });
            },
            fetchMap() {
                this.$axios({
                    method: "get",
                    url: this.$basePath + `/maps`
                }).then((response) => {
                    response = response.data;
                    if (response) {
                        this.maps = response;
                    }
                }).catch(() => {
                });
            },
            /*******  编辑 Tag 对话框  *******/
            removeTag(index) {
                this.form.tags.splice(index, 1);
            },
            showTagInput() {
                this.tag.inputVisible = true;
                this.$nextTick(() => {
                    this.$refs.tagInput.$refs.input.focus();
                });
            },
            tagInputConfirm() {
                if (this.tag.inputValue) {
                    if (this.form.tags.includes(this.tag.inputValue)) {
                        this.$message({
                            message: 'Tag 重复'
                        });
                        return;
                    } else {
                        this.form.tags.push(this.tag.inputValue);
                    }
                }
                this.tag.inputVisible = false;
                this.tag.inputValue = '';
            },
            tagConfirm() {
                this.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/scen-folders/${this.curFolder.id}/scenarios/${this.tagDialog.row.id}`,
                    data: this.tagDialog.row
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if (response.id) {
                        this.tagDialog.visible = false;
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
            handleSelect(key) {
                this.menuSelectIndex = key
            }
        },
        mounted() {
            this.fetchDetail();
            this.fetchMap();
        },

    }
</script>

<style scoped lang="less">
    .scene-edit {
        padding: 10px;
        width: 100%;
        .el-input {
            width: 300px;
        }

        .el-textarea {
            width: 100%;
        }

        .el-select {
            width: 300px;
        }

        .tag {
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
        .menu-container{
            display: flex;
            align-items: center;
        }
        .form-container{
            width: 100%;
            min-height: 493px;
            background: #202533;
            margin-top: 20px;
            padding: 20px 30px;
        }
        .edit-container{
            width: 100%;
            height: 696px;
            background: #202533;
            padding: 30px;
            margin-top: 20px;
        }
    }
</style>
<style lang="less">
.menu-container,
.el-form-item{
    .menu-item{
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
        background: #1A1F2C;
        border: 1px solid #353A4C;
        user-select: none;
      
    }
.el-textarea .el-textarea__inner,
    .el-input .el-input__inner{
        background-color: #1A1F2C;
    }
}

.el-tag{
    min-width: 70px;
    height: 24px;
    min-height: 24px;
    line-height: 23px;
    color: #C1C1C8;
    background: #353A4C;
    border: none;
    // margin-top: 10px;
} 
</style>