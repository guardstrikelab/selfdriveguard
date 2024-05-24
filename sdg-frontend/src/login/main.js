import '../assets/mixin.less'
import { createApp } from 'vue'
import ElementPlus from 'element-plus';
import '../../theme/index.css'
import App from './App'
import qs from 'qs'
import axios from 'axios'
import Moment from 'moment'
import validation from '../components/validation'
import '../assets/icon/iconfont.css'
const app = createApp(App);
app.use(ElementPlus);
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$qs = qs;  // 用于将 json格式 转换为 表单格式
app.config.globalProperties.$moment = Moment;
app.config.globalProperties.$validation = validation;
app.config.globalProperties.$basePath = 'http://172.16.111.78:8000';

app.mount('#app');