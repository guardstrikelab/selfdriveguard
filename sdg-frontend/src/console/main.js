import '../assets/mixin.less'
import {createApp} from 'vue'
import {createRouter, createWebHashHistory} from 'vue-router'
import routes from './routes'
import ElementPlus from 'element-plus';
import Vuex from 'vuex'
import App from './App'
import qs from 'qs'
import axios from 'axios'
import Moment from 'moment'
import validation from '../components/validation'
import '../../theme/index.css'
import '../assets/icon/iconfont.css';
import locale from 'element-plus/lib/locale/lang/zh-cn'
import * as echarts from 'echarts';

const app = createApp(App);
app.use(ElementPlus, { locale });
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$qs = qs;  // 用于将 json格式 转换为 表单格式
app.config.globalProperties.$moment = Moment;
app.config.globalProperties.$validation = validation;
app.config.globalProperties.$basePath = 'http://172.16.111.78:8000';
app.config.globalProperties.$echarts = echarts;

app.config.globalProperties.$copyFields = function (fields, source, target, fill) {
    source = source || {};
    target = target || {};
    for(let field of fields){
        target[field] = source[field] || fill;
    }
    return target;
};
const router = createRouter({
    history: createWebHashHistory(),
    routes
});
router.afterEach((to) => {  
    if(to.fullPath == "/") router.push("/op/scene/list")
})
app.use(router);
const store = new Vuex.Store({
    state: {
        myDetail: {},
        access_token: ''
    },
    mutations: {
        change () {}
    }
});
app.use(store);
app.mount('#app');