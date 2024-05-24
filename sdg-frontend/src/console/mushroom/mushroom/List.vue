<template>
    <div class="product-list" v-loading="loading">
        <div class="list-top">
            <span class="page-title">种</span>
            <el-button type="primary" icon="el-icon-plus" class="add-btn" @click="add">新增种</el-button>
            <el-upload ref="searchUploader" :action="`${$basePath}/mushroom/img/search`"
                       style="float: right;margin-left: 20px"
                       with-credentials accept=".jpg,.png,.jpeg,.bmp" name="image" :show-file-list="false"
                       :file-list="filter.imgList" :on-success="searchSuccess" :on-error="searchError"
                       :before-upload="searchChange">
                <el-button icon="el-icon-upload" circle></el-button>
            </el-upload>
            <el-input placeholder="种名、属名、描述" v-model="filter.search" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
            <el-select v-model="filter.toxicity" placeholder="毒性" clearable @change="filterChange">
                <el-option label="无有毒记载" value="isNull"></el-option>
                <el-option label="有有毒记载" value="isNotNull"></el-option>
                <el-option v-for="item in map2Options(toxicityMap)" :key="item.key" :label="item.label"
                           :value="item.key">
                </el-option>
            </el-select>
            <el-select v-model="filter.edibility" placeholder="可食性" clearable @change="filterChange">
                <el-option label="无可食记载" value="isNull"></el-option>
                <el-option label="有可食记载" value="isNotNull"></el-option>
                <el-option v-for="item in map2Options(edibilityMap)" :key="item.key" :label="item.label"
                           :value="item.key">
                </el-option>
            </el-select>
        </div>
        <div class="list-filter">
            <el-input placeholder="子实体（菌盖）" v-model="filter.cap" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
            <el-input placeholder="子实体（菌盖）中心" v-model="filter.center" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
            <el-input placeholder="子实体（菌盖）边缘" v-model="filter.edge" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
            <el-input placeholder="菌褶" v-model="filter.lamella" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
            <el-input placeholder="菌柄" v-model="filter.stipe" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
            <el-input placeholder="菌环" v-model="filter.ring" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
            <el-input placeholder="菌托" v-model="filter.volva" class="input-with-select" clearable
                      @clear="search" @keyup.enter="search">
                <template #append>
                    <el-button icon="el-icon-search" @click="search"></el-button>
                </template>
            </el-input>
        </div>
        <div class="list-table">
            <el-table ref="multipleTable" :data="table.data" :default-sort="table.sort"
                      @sort-change="sortChange" @selection-change="selectionChange">
                <el-table-column type="selection" width="50" fixed></el-table-column>
                <el-table-column prop="id" label="ID" width="60px" sortable="custom" fixed></el-table-column>
                <el-table-column prop="name" label="名称" width="140px" fixed>
                    <template #default="scope">
                        <div class="flex">
                            <div>{{scope.row.name}}</div>
                            <i class="el-icon-edit-outline" @click="nameEdit(scope.row)"></i>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="别名" width="140px">
                    <template #default="scope">
                        <div class="flex" v-if="scope.row.alias">
                            <div v-html="scope.row.alias.split(',').join('<br/>')"></div>
                            <i class="el-icon-edit-outline" @click="aliasEdit(scope.row)"></i>
                        </div>
                        <i class="el-icon-circle-plus-outline" v-else @click="aliasEdit(scope.row)"></i>
                    </template>
                </el-table-column>
                <el-table-column label="俗称" width="140px">
                    <template #default="scope">
                        <div class="flex" v-if="scope.row.vulgo">
                            <div v-html="scope.row.vulgo.split(',').join('<br/>')"></div>
                            <i class="el-icon-edit-outline" @click="vulgoEdit(scope.row)"></i>
                        </div>
                        <i class="el-icon-circle-plus-outline" v-else @click="vulgoEdit(scope.row)"></i>
                    </template>
                </el-table-column>
                <el-table-column label="拉丁学名" width="270px">
                    <template #default="scope">
                        <div class="flex">
                            <div v-html="scope.row.latin.split(',').join('<br/>')"></div>
                            <i class="el-icon-edit-outline" @click="latinEdit(scope.row)"></i>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="底库图片" width="60px">
                    <template #default="scope">
                        <el-button type="text" v-if="scope.row.bankImg"
                                   @click="showCarousel(scope.row.id,scope.row.bankImg.split(';'), 'hongo-bank')">
                            {{scope.row.bankImg.split(';').length}} 张
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column label="展示图片" width="60px">
                    <template #default="scope">
                        <el-button type="text" v-if="scope.row.img"
                                   @click="showCarousel(scope.row.id,scope.row.img.split(','), 'hongo')">
                            {{scope.row.img.split(',').length}} 张
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column label="相似种" width="140px">
                    <template #default="scope">
                        <div class="flex" v-if="scope.row.similarList">
                            <div v-html="displaySimilar(scope.row.similarList)"></div>
                            <i class="el-icon-edit-outline" @click="similarEdit(scope.row)"></i>
                        </div>
                        <i class="el-icon-circle-plus-outline" v-else @click="similarEdit(scope.row)"></i>
                    </template>
                </el-table-column>
                <el-table-column prop="parentName" label="属" width="100px"></el-table-column>
                <el-table-column label="可食性" width="100px">
                    <template #default="scope">
                        <div class="flex" v-if="scope.row.edibility">
                            <div>{{edibilityMap[scope.row.edibility]}}</div>
                            <i class="el-icon-edit-outline" @click="edibilityEdit(scope.row)"></i>
                        </div>
                        <i class="el-icon-circle-plus-outline" v-else @click="edibilityEdit(scope.row)"></i>
                    </template>
                </el-table-column>
                <el-table-column label="毒性" width="120px">
                    <template #default="scope">
                        <div class="flex" v-if="scope.row.toxicity">
                            <div>
                                <div v-for="item in scope.row.toxicity.split(',')" :key="item">{{toxicityMap[item]}}
                                </div>
                            </div>
                            <i class="el-icon-edit-outline" @click="toxicityEdit(scope.row)"></i>
                        </div>
                        <i class="el-icon-circle-plus-outline" v-else @click="toxicityEdit(scope.row)"></i>
                    </template>
                </el-table-column>
                <el-table-column label="鹅膏哥" width="70px">
                    <template #default="scope">
                        <el-button type="text" v-if="scope.row.desc_egaoge"
                                   @click="descEdit(scope.row, 'desc_egaoge')">
                            查看
                        </el-button>
                        <i class="el-icon-circle-plus-outline" v-else @click="descEdit(scope.row, 'desc_egaoge')"></i>
                    </template>
                </el-table-column>
                <el-table-column label="补充" width="50px">
                    <template #default="scope">
                        <el-button type="text" v-if="scope.row.desc_addition"
                                   @click="descEdit(scope.row, 'desc_addition')">
                            查看
                        </el-button>
                        <i class="el-icon-circle-plus-outline" v-else @click="descEdit(scope.row, 'desc_addition')"></i>
                    </template>
                </el-table-column>
                <el-table-column label="资源" width="50px">
                    <template #default="scope">
                        <el-button type="text" v-if="scope.row.desc_resource"
                                   @click="descEdit(scope.row, 'desc_resource')">
                            查看
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column label="世界" width="50px">
                    <template #default="scope">
                        <el-button type="text" v-if="scope.row.desc_world" @click="descEdit(scope.row, 'desc_world')">查看
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column label="毒菇" width="50px">
                    <template #default="scope">
                        <el-button type="text" v-if="scope.row.desc_poison" @click="descEdit(scope.row, 'desc_poison')">
                            查看
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column label="鹅膏" width="50px">
                    <template #default="scope">
                        <el-button type="text" v-if="scope.row.desc_amanita"
                                   @click="descEdit(scope.row, 'desc_amanita')">
                            查看
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column prop="hitCount" label="命中数" width="70px"></el-table-column>
                <el-table-column fixed="right" label="操作" width="120px">
                    <template #default="scope">
                        <el-button type="text" @click="uploadImg(scope.row)">上传</el-button>
                        <el-button type="text" @click="multiUpload(scope.row)">批量上传</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="list-bottom">
            <batch-operation :operations="batch.operations" :targets="batch.targets"
                             @batchDone="fetchList"></batch-operation>
            <el-pagination background @current-change="fetchList" v-model:current-page="page.currentPage"
                           v-model:page-size="page.pageSize" layout="total, sizes, prev, pager, next, jumper"
                           :total="page.totalCount" @size-change="fetchList">
            </el-pagination>
        </div>
        <el-dialog title="新增" v-model="addDialog.visible" width="500px" :close-on-click-modal="false">
            <el-form :model="addDialog" ref="addForm" :rules="rules" label-width="100px">
                <el-form-item label="名称：" prop="name">
                    <el-input v-model="addDialog.name" placeholder="请输入"></el-input>
                </el-form-item>
                <el-form-item label="拉丁学名：" prop="latin">
                    <el-input v-model="addDialog.latin" placeholder="请输入"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="addDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="addConfirm" v-loading="addDialog.loading">确 认</el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="编辑名称" v-model="nameDialog.visible" width="500px" :close-on-click-modal="false">
            <el-input placeholder="请输入内容" v-model="nameDialog.name"></el-input>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="nameDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="nameSubmit" :disabled="!nameDialog.name"
                               v-loading="nameDialog.loading">
                        确 认
                    </el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="编辑别名" v-model="aliasDialog.visible" width="1000px" :close-on-click-modal="false">
            <el-input placeholder="请输入内容" v-model="aliasDialog.alias"></el-input>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="aliasDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="aliasSubmit" v-loading="aliasDialog.loading">确 认</el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="编辑俗称" v-model="vulgoDialog.visible" width="1000px" :close-on-click-modal="false">
            <el-input placeholder="请输入内容" v-model="vulgoDialog.vulgo"></el-input>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="vulgoDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="vulgoSubmit" v-loading="vulgoDialog.loading">确 认</el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="编辑拉丁学名" v-model="latinDialog.visible" width="1000px" :close-on-click-modal="false">
            <el-input placeholder="请输入内容" v-model="latinDialog.latin"></el-input>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="latinDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="latinSubmit" v-loading="latinDialog.loading">确 认</el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="编辑相似种" v-model="similarDialog.visible" width="500px" :close-on-click-modal="false">
            <el-input placeholder="请输入内容" v-model="similarDialog.similar"></el-input>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="similarDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="similarSubmit" v-loading="similarDialog.loading">确 认</el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="编辑可食性" v-model="edibilityDialog.visible" width="500px" :close-on-click-modal="false">
            <el-select v-model="edibilityDialog.edibility" placeholder="请选择" clearable>
                <el-option value="null" label="无可食记载"></el-option>
                <el-option v-for="item in map2Options(edibilityMap)" :key="item.key" :value="item.key"
                           :label="item.label"></el-option>
            </el-select>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="edibilityDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="edibilitySubmit" v-loading="edibilityDialog.loading">确 认
                    </el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="编辑毒性" v-model="toxicityDialog.visible" width="500px" :close-on-click-modal="false">
            <el-select v-model="toxicityDialog.toxicity" placeholder="请选择" clearable multiple>
                <el-option v-for="item in map2Options(toxicityMap)" :key="item.key" :value="item.key"
                           :label="item.label"></el-option>
            </el-select>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="toxicityDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="toxicitySubmit" v-loading="toxicityDialog.loading">确 认</el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="上传图片" v-model="imgDialog.visible" width="600px" :close-on-click-modal="false"
                   @close="dialogClose">
            <el-form label-width="100px">
                <el-form-item label="图片：">
                    <el-upload ref="imgUploader" :action="`${$basePath}/mushroom/img/object`"
                               with-credentials accept=".jpg,.png,.jpeg,.bmp" name="image" :show-file-list="false"
                               :file-list="imgDialog.imgList" :on-remove="imgRemove" :on-change="imgChange"
                               :on-success="imgSuccess" :on-error="imgError">
                        <el-button type="text" v-if="!imgDialog.imgList.length">选择图片</el-button>
                        <div class="img-object" v-if="imgDialog.imgList.length">
                            <img ref="uploadImg" :src="imgDialog.imgList[0].src"/>
                            <div class="frame" :style="{left: (imgDialog.imgObject.left * imgDialog.imageScale + imgDialog.imageLocation.left)+'px',
                            top: (imgDialog.imgObject.top * imgDialog.imageScale + imgDialog.imageLocation.top)+'px',
                            width:imgDialog.imgObject.width * imgDialog.imageScale+'px',
                            height:imgDialog.imgObject.height * imgDialog.imageScale+'px'}"></div>
                        </div>
                    </el-upload>
                </el-form-item>
                <el-form-item label="入底库：">
                    <el-checkbox-group v-model="imgDialog.intoBank">
                        <el-checkbox label="origin">原图</el-checkbox>
                        <el-checkbox label="object">主体裁剪图</el-checkbox>
                    </el-checkbox-group>
                </el-form-item>
                <el-form-item label="入OSS：">
                    <el-checkbox-group v-model="imgDialog.intoOss">
                        <el-checkbox label="origin">原图</el-checkbox>
                        <el-checkbox label="object">主体裁剪图</el-checkbox>
                    </el-checkbox-group>
                </el-form-item>
                <el-form-item label="底库图片：">
                    <div v-if="imgDialog.row.bankImg">
                        <img :src="`https://hongo-bank.oss-cn-zhangjiakou.aliyuncs.com/${imgDialog.id}/${item}`"
                             :title="index+1"
                             v-for="(item,index) in imgDialog.row.bankImg.split(';')" :key="item"
                             @click="removeBankImg(imgDialog.row, item)"
                             style="width: 100px;height: 100px;object-fit: contain;">
                    </div>
                </el-form-item>
                <el-form-item label="展示图片：">
                    <div v-if="imgDialog.row.img">
                        <img :src="`https://hongo.oss-cn-zhangjiakou.aliyuncs.com/${imgDialog.id}/${item}`"
                             :title="index+1"
                             v-for="(item,index) in imgDialog.row.img.split(',')" :key="item"
                             @click="removeImg(imgDialog.row, item)"
                             style="width: 100px;height: 100px;object-fit: contain;">
                    </div>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="imgDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="imgSubmit" v-loading="imgDialog.loading"
                               :disabled="!imgDialog.imgList.length || (!imgDialog.intoBank.length && !imgDialog.intoOss.length)">
                        确 认
                    </el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog title="批量上传" v-model="multiDialog.visible" width="1300px" :close-on-click-modal="false"
                   @close="dialogClose">
            <el-upload ref="multiUploader" :action="`${$basePath}/mushroom/img/object`" multiple
                       with-credentials accept=".jpg,.png,.jpeg,.bmp" name="image" :show-file-list="false"
                       :file-list="multiDialog.imgList" :on-remove="multiRemove" :on-change="multiChange"
                       :on-success="multiSuccess" :on-error="multiError" :before-upload="beforeUpload">
                <el-button type="text" v-if="!multiDialog.imgList.length">选择图片</el-button>
            </el-upload>
            <div style="display: flex;flex-wrap: wrap;" class="multi-file">
                <div class="img-object" v-for="(img,index) in multiDialog.imgList" :key="index">
                    <img :ref="'uploadImg_'+index" :src="img.src" @dblclick="multiRemoveImg(index)"/>
                    <div class="frame" v-if="img.imgObject" :style="{left: (img.imgObject.left * img.imageScale + img.imageLocation.left)+'px',
                            top: (img.imgObject.top * img.imageScale + img.imageLocation.top)+'px',
                            width:img.imgObject.width * img.imageScale+'px',
                            height:img.imgObject.height * img.imageScale+'px'}" @dblclick.stop="removeFrame(img)"></div>
                </div>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="multiDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="multiSubmit" v-loading="multiDialog.loading"
                               :disabled="!multiDialog.imgList.length">
                        确 认
                    </el-button>
                </div>
            </template>
        </el-dialog>
        <dialog-carousel :images="imgCarousel.images" :activeIndex="imgCarousel.activeIndex"
                         v-model="imgCarousel.visible"></dialog-carousel>
        <el-dialog :title="'编辑描述 '+descDialog.field" v-model="descDialog.visible" width="1000px"
                   :close-on-click-modal="false">
            <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 20}"
                      placeholder="请输入内容" v-model="descDialog.desc">
            </el-input>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="descDialog.visible = false">取 消</el-button>
                    <el-button type="primary" @click="descSubmit" v-loading="descDialog.loading">确 认</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script>
    import BatchOperation from "../../../components/BatchOperation"
    import DialogCarousel from "../../../components/DialogCarousel"

    export default {
        components: {
            'batch-operation': BatchOperation,
            'dialog-carousel': DialogCarousel
        },
        data() {
            return {
                loading: false,
                filter: {
                    search: '',
                    edibility: '',
                    toxicity: '',
                    imgList: [],
                    cap: '', // 子实体 或 菌盖
                    center: '',  // 中心
                    edge: '',  // 边缘
                    lamella: '', // 菌褶
                    stipe: '',  // 菌柄
                    ring: '', // 菌环
                    volva: ''  // 菌托
                },
                edibilityMap: {
                    edible: '可食',
                    young: '幼时可食',
                    drink: '忌酒可食',  // 不能同时饮酒
                    cooked: '煮熟可食',
                    special: '特殊处理可食'
                },
                toxicityMap: {
                    liver: '肝损害', // 急性肝损害
                    kidney: '肾衰竭', // 急性肾衰竭
                    breathing: '呼吸衰竭', // 呼吸循环衰竭
                    central: '中枢中毒',// 中枢神经系统中毒
                    hemolysis: '溶血',
                    rhabdomyolysis: '肌溶解', // 横纹肌溶解
                    hypertoxic: '剧毒',
                    serious: '严重中毒',
                    nerve: '神经毒素',
                    stomach: '肠胃炎',
                    erythema: '肢痛', // 红斑性肢痛
                    dermitis: '皮炎', // 光过敏性皮炎
                    other: '有毒',
                    probably: '可能有毒',
                    excess: '过量中毒', // 过量食用会中毒
                    few: '个别中毒'  // 个别体质会中毒
                },
                table: {
                    data: [],
                    sort: {
                        prop: 'id',
                        order: 'ascending'
                    },
                    selection: []
                },
                batch: {
                    operations: [
                        {
                            label: "设为已订正",
                            url: "/mushroom/revised",
                            method: 'put'
                        }
                    ],
                    targets: []
                },
                page: {
                    pageSize: 10,
                    totalCount: 0,
                    currentPage: 1
                },
                addDialog: {
                    visible: false,
                    loading: false,
                    name: '',
                    latin: ''
                },
                nameDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    name: ''
                },
                aliasDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    latin: ''
                },
                vulgoDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    vulgo: ''
                },
                latinDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    latin: ''
                },
                similarDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    similar: ''
                },
                edibilityDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    edibility: ''
                },
                toxicityDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    toxicity: []
                },
                imgDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    row: {},
                    imgList: [],
                    imageSize: {
                        width: 0,
                        height: 0
                    },
                    imageScale: 1,
                    imageLocation: {
                        left: 0,
                        top: 0
                    },
                    imgObject: {},
                    intoBank: ["object"],  // 入底库
                    intoOss: ["origin"]   // 入 OSS
                },
                multiDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    imgList: []
                },
                imgCarousel: {
                    visible: false,
                    images: [],
                    activeIndex: 0
                },
                descDialog: {
                    visible: false,
                    loading: false,
                    id: '',
                    desc: '',
                    field: ''
                },
                rules: {
                    name: this.$validation.fullName,
                    latin: [
                        {required: true, message: '请填写', trigger: "blur"},
                        {pattern: /^[a-zA-Z \\-]+$/, message: '请输入英文字母', trigger: "blur"}
                    ]
                }
            }
        },
        computed: {},
        watch: {
            'imgDialog.imageSize': function () {
                let boxHeight = 400;  // 图片框高度
                let boxWidth = 400;  // 图片框宽度
                let size = this.imgDialog.imageSize;
                if (size.width / boxWidth >= size.height / boxHeight) {  // 横向贴边
                    this.imgDialog.imageScale = boxWidth / size.width;
                    this.imgDialog.imageLocation.left = 0;
                    this.imgDialog.imageLocation.top = (boxHeight - size.height * this.imgDialog.imageScale) / 2;
                } else {          // 纵向贴边
                    this.imgDialog.imageScale = boxHeight / size.height;
                    this.imgDialog.imageLocation.top = 0;
                    this.imgDialog.imageLocation.left = (boxWidth - size.width * this.imgDialog.imageScale) / 2;
                }
            }
        },
        methods: {
            search() {
                this.page.currentPage = 1;
                this.fetchList();
            },
            map2Options(map) {
                return Object.keys(map).map((key) => {
                    return {
                        key,
                        label: map[key]
                    }
                });
            },
            filterChange() {
                this.page.currentPage = 1;
                this.fetchList();
            },
            sortChange(e) {
                this.page.currentPage = 1;
                this.table.sort.prop = e.prop;
                this.table.sort.order = e.order;
                this.fetchList();
            },
            selectionChange(selection) {
                this.batch.targets = selection.map((item) => {
                    return item.id;
                });
            },
            searchChange() {
                this.loading = true;
            },
            searchSuccess(response) {
                this.loading = false;
                if (response.code == "0") {
                    this.table.data = response.data;
                    this.page.totalCount = response.data.length;
                } else {
                    this.filter.imgList = [];
                    this.$alert(response.msg);
                }
            },
            searchError() {
                this.loading = false;
                this.filter.imgList = [];
                this.$alert("检索失败");
            },
            fetchList() {
                this.loading = true;
                let params = {
                    pageSize: this.page.pageSize,
                    pageNum: this.page.currentPage,
                    sortProp: this.table.sort.prop || 'id',
                    sortOrder: this.table.sort.order == 'ascending' ? 'ASC' : 'DESC',
                };
                this.$copyFields(Object.keys(this.filter), this.filter, params);
                this.$axios({
                    method: "get",
                    url: this.$basePath + (this.filter.search == '缺陷' ? "/mushroom/defect" : "/mushroom"),
                    params: params
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if (response) {
                        this.table.data = this.filter.search == '缺陷' ? response.data : response.data.list || [];
                        this.page.totalCount = this.filter.search == '缺陷' ? response.data.length : response.data.total;
                    }
                }).catch(() => {
                    this.loading = false;
                });
            },
            displaySimilar(similarList) {
                let mushrooms = similarList.map((item) => {
                    return `<div title="${item.id}">${item.name}</div>`
                });
                return mushrooms.join('');
            },
            removeImg(row, img) {
                this.$msgbox({
                    title: "确定要删除该展示图片吗？",
                    showCancelButton: true,
                    beforeClose: (action, instance, done) => {
                        if (action === 'confirm') {
                            done();
                            this.removeImgSubmit(row.id, img);
                        } else {
                            done();
                        }
                    }
                });
            },
            removeBankImg(row, img) {
                this.$msgbox({
                    title: "确定要删除该底库图片吗？",
                    showCancelButton: true,
                    beforeClose: (action, instance, done) => {
                        if (action === 'confirm') {
                            done();
                            this.removeBankImgSubmit(row.id, img);
                        } else {
                            done();
                        }
                    }
                });
            },
            removeImgSubmit(id, img) {
                this.loading = true;
                this.$axios({
                    method: "delete",
                    url: this.$basePath + `/mushroom/${id}/img/${img}`,
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.imgDialog.row = response.data;
                    }
                }).catch(() => {
                    this.loading = false;
                });
            },
            removeBankImgSubmit(id, img) {
                this.loading = true;
                this.$axios({
                    method: "delete",
                    url: this.$basePath + `/mushroom/${id}/bankImg/${img}`,
                }).then((response) => {
                    this.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.imgDialog.row = response.data;
                    }
                }).catch(() => {
                    this.loading = false;
                });
            },
            showCarousel(id, imgs, bucket) {
                this.imgCarousel.visible = true;
                this.imgCarousel.images = imgs.map((item, index) => {
                    return {
                        src: `https://${bucket}.oss-cn-zhangjiakou.aliyuncs.com/${id}/${item}`,
                        label: index + 1
                    }
                });
                this.imgCarousel.activeIndex = 0;
            },
            /*******  新增 对话框  *******/
            add() {
                this.addDialog.visible = true;
                this.addDialog.name = '';
                this.addDialog.latin = '';
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
                    url: this.$basePath + "/mushroom",
                    data: {
                        name: this.addDialog.name,
                        latin: this.addDialog.latin,
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
            /*******  编辑名称 对话框  *******/
            nameEdit(row) {
                this.nameDialog.id = row.id;
                this.nameDialog.name = row.name;
                this.nameDialog.visible = true;
            },
            nameSubmit() {
                this.nameDialog.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/mushroom/${this.nameDialog.id}/name`,
                    data: {
                        name: this.nameDialog.name
                    }
                }).then((response) => {
                    this.nameDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.nameDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.nameDialog.loading = false;
                });
            },
            /*******  编辑别名 对话框  *******/
            aliasEdit(row) {
                this.aliasDialog.id = row.id;
                this.aliasDialog.alias = row.alias;
                this.aliasDialog.visible = true;
            },
            aliasSubmit() {
                this.aliasDialog.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/mushroom/${this.aliasDialog.id}/alias`,
                    data: {
                        alias: this.aliasDialog.alias
                    }
                }).then((response) => {
                    this.aliasDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.aliasDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.aliasDialog.loading = false;
                });
            },
            /*******  编辑俗称 对话框  *******/
            vulgoEdit(row) {
                this.vulgoDialog.id = row.id;
                this.vulgoDialog.vulgo = row.vulgo;
                this.vulgoDialog.visible = true;
            },
            vulgoSubmit() {
                this.vulgoDialog.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/mushroom/${this.vulgoDialog.id}/vulgo`,
                    data: {
                        vulgo: this.vulgoDialog.vulgo
                    }
                }).then((response) => {
                    this.vulgoDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.vulgoDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.vulgoDialog.loading = false;
                });
            },
            /*******  编辑拉丁学名 对话框  *******/
            latinEdit(row) {
                this.latinDialog.id = row.id;
                this.latinDialog.latin = row.latin;
                this.latinDialog.visible = true;
            },
            latinSubmit() {
                this.latinDialog.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/mushroom/${this.latinDialog.id}/latin`,
                    data: {
                        latin: this.latinDialog.latin
                    }
                }).then((response) => {
                    this.latinDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.latinDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.latinDialog.loading = false;
                });
            },
            /*******  编辑相似种 对话框  *******/
            similarEdit(row) {
                this.similarDialog.id = row.id;
                this.similarDialog.similar = row.similar;
                this.similarDialog.visible = true;
            },
            similarSubmit() {
                this.similarDialog.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/mushroom/${this.similarDialog.id}/similar`,
                    data: {
                        similar: this.similarDialog.similar
                    }
                }).then((response) => {
                    this.similarDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.similarDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.similarDialog.loading = false;
                });
            },
            /*******  编辑可食性 对话框  *******/
            edibilityEdit(row) {
                this.edibilityDialog.id = row.id;
                this.edibilityDialog.edibility = row.edibility;
                this.edibilityDialog.visible = true;
            },
            edibilitySubmit() {
                this.edibilityDialog.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/mushroom/${this.edibilityDialog.id}/edibility`,
                    data: {
                        edibility: this.edibilityDialog.edibility || null
                    }
                }).then((response) => {
                    this.edibilityDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.edibilityDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.edibilityDialog.loading = false;
                });
            },
            /*******  编辑毒性 对话框  *******/
            toxicityEdit(row) {
                this.toxicityDialog.id = row.id;
                this.toxicityDialog.toxicity = row.toxicity ? row.toxicity.split(',') : [];
                this.toxicityDialog.visible = true;
            },
            toxicitySubmit() {
                this.toxicityDialog.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/mushroom/${this.toxicityDialog.id}/toxicity`,
                    data: {
                        toxicity: this.toxicityDialog.toxicity.join(",") || null
                    }
                }).then((response) => {
                    this.toxicityDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.toxicityDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.toxicityDialog.loading = false;
                });
            },
            /*******  上传图片 对话框  *******/
            uploadImg(row) {
                this.imgDialog.id = row.id;
                this.imgDialog.visible = true;
                this.imgDialog.imgList = [];
                this.imgDialog.row = row;
            },
            imgChange(file) {   // 更换图片、上传成功、上传失败都会触发
                if (!file.src) {    // 更换图片
                    this.imgDialog.imgObject = {};
                    let that = this;
                    let reader = new FileReader();
                    reader.readAsDataURL(file.raw);
                    reader.onloadend = function () {
                        file.src = this.result;
                        that.imgDialog.imgList = [file];
                    }
                }
            },
            imgRemove(file, fileList) {
                this.imgDialog.imgList = fileList;
            },
            imgSuccess(response) {
                if (response.code == "0") {
                    this.imgDialog.imgObject = response.data.result;
                    this.imgDialog.imageSize = {
                        width: this.$refs.uploadImg.naturalWidth,
                        height: this.$refs.uploadImg.naturalHeight
                    }
                } else {
                    this.imgDialog.imgList = [];
                    this.$alert(response.msg);
                }
            },
            imgError() {
                this.imgDialog.loading = false;
                this.imgDialog.imgList = [];
                this.$alert("上传失败");
            },
            imgSubmit() {
                let form = new FormData();
                form.append("image", this.imgDialog.imgList[0].raw);
                let params = {
                    objectLeft: this.imgDialog.imgObject.left,
                    objectTop: this.imgDialog.imgObject.top,
                    objectWidth: this.imgDialog.imgObject.width,
                    objectHeight: this.imgDialog.imgObject.height,
                    originToBank: this.imgDialog.intoBank.includes('origin'),
                    originToOss: this.imgDialog.intoOss.includes('origin'),
                    objectToBank: this.imgDialog.intoBank.includes('object'),
                    objectToOss: this.imgDialog.intoOss.includes('object')
                };
                form.append('params', JSON.stringify(params));
                this.imgDialog.loading = true;
                this.$axios({
                    method: "post",
                    url: this.$basePath + `/mushroom/${this.imgDialog.id}/img`,
                    data: form
                }).then((response) => {
                    this.imgDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.imgDialog.imgList = [];
                        this.imgDialog.row = response.data;
                    }
                }).catch(() => {
                    this.imgDialog.loading = false;
                });
            },
            dialogClose() {
                this.fetchList();
            },
            /*******  批量上传 对话框  *******/
            multiUpload(row) {
                this.multiDialog.id = row.id;
                this.multiDialog.visible = true;
                this.multiDialog.imgList = [];
            },
            multiChange(file, fileList) {   // 更换图片、上传成功、上传失败都会触发
                if (!file.src) {    // 更换图片
                    let that = this;
                    that.multiDialog.imgList = fileList;
                    let reader = new FileReader();
                    reader.readAsDataURL(file.raw);
                    reader.onloadend = function () {
                        file.src = this.result;
                        that.multiDialog.imgList = [].concat(fileList);
                    }
                }
            },
            multiRemove(file, fileList) {
                this.multiDialog.imgList = fileList;
            },
            beforeUpload(file) {
                file = this.multiDialog.imgList.find((item) => {
                    return item.name === file.name;  // 此 file 对象 非 数组里的 file
                });
                return new Promise((resolve) => setTimeout(resolve, this.multiDialog.imgList.indexOf(file) * 1000));   // 使得 主体 检测请求 错开发送，避免触发限额
            },
            multiSuccess(response, file, fileList) {
                if (response.code == "0") {
                    file.imgObject = response.data.result;
                    file.imageSize = {
                        width: this.$refs['uploadImg_' + fileList.indexOf(file)].naturalWidth,
                        height: this.$refs['uploadImg_' + fileList.indexOf(file)].naturalHeight
                    };
                    let boxHeight = 200;  // 图片框高度
                    let boxWidth = 200;  // 图片框宽度
                    if (file.imageSize.width / boxWidth >= file.imageSize.height / boxHeight) {  // 横向贴边
                        file.imageScale = boxWidth / file.imageSize.width;
                        file.imageLocation = {
                            left: 0,
                            top: (boxHeight - file.imageSize.height * file.imageScale) / 2
                        }
                    } else {          // 纵向贴边
                        file.imageScale = boxHeight / file.imageSize.height;
                        file.imageLocation = {
                            top: 0,
                            left: (boxWidth - file.imageSize.width * file.imageScale) / 2
                        }
                    }
                    this.multiDialog.imgList = [].concat(fileList);
                } else {
                    this.$alert(response.msg);
                }
            },
            multiError() {
                this.multiDialog.loading = false;
                this.$alert("上传失败");
            },
            removeFrame(img) {
                img.imgObject = null;
                this.multiDialog.imgList = [].concat(this.multiDialog.imgList);
            },
            multiRemoveImg(index) {
                this.multiDialog.imgList.splice(index, 1);
                this.multiDialog.imgList = [].concat(this.multiDialog.imgList);
            },
            multiSubmit() {
                this.submitOne(0);
            },
            submitOne(){
                let img = this.multiDialog.imgList[0];
                if(!img){
                    return;
                }
                let form = new FormData();
                form.append("image", img.raw);
                let params = {
                    objectLeft: img.imgObject && img.imgObject.left,
                    objectTop: img.imgObject && img.imgObject.top,
                    objectWidth: img.imgObject && img.imgObject.width,
                    objectHeight: img.imgObject && img.imgObject.height,
                    originToBank: false,
                    originToOss: true,
                    objectToBank: !!img.imgObject,
                    objectToOss: false
                };
                form.append('params', JSON.stringify(params));
                this.multiDialog.loading = true;
                this.$axios({
                    method: "post",
                    url: this.$basePath + `/mushroom/${this.multiDialog.id}/img`,
                    data: form
                }).then((response) => {
                    this.multiDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.$message({
                            message: '操作成功 ',
                            type: 'success'
                        });
                        this.multiDialog.imgList.splice(0,1);
                        this.submitOne();
                    }
                }).catch(() => {
                    this.multiDialog.loading = false;
                });
            },
            /*******  编辑描述 对话框  *******/
            descEdit(row, field) {
                this.descDialog.id = row.id;
                this.descDialog.field = field;
                this.descDialog.desc = row[field];
                this.descDialog.visible = true;
            },
            descSubmit() {
                this.descDialog.loading = true;
                this.$axios({
                    method: "put",
                    url: this.$basePath + `/mushroom/${this.descDialog.id}/${this.descDialog.field}`,
                    data: {
                        desc: this.descDialog.desc
                    }
                }).then((response) => {
                    this.descDialog.loading = false;
                    response = response.data;
                    if (response.code == "0") {
                        this.descDialog.visible = false;
                        this.$message({
                            message: '操作成功',
                            type: 'success'
                        });
                        this.fetchList();
                    }
                }).catch(() => {
                    this.descDialog.loading = false;
                });
            }
        },
        mounted: function () {
            this.fetchList();
        }
    }
</script>

<style scoped lang="less">
    .list-table {
        .flex {
            display: flex;
            justify-content: space-between;
            align-items: center;
            word-break: normal;
        }

        i {
            cursor: pointer;
        }
    }

    .img-object {
        position: relative;

        img {
            width: 400px;
            height: 400px;
            object-fit: contain;
            vertical-align: top;
        }

        .frame {
            position: absolute;
            border: 1px solid #FFB204;
        }
    }

    .multi-file {
        display: flex;
        flex-wrap: wrap;

        .img-object {
            width: 200px;
            height: 200px;

            img {
                width: 200px;
                height: 200px;
            }
        }
    }

</style>