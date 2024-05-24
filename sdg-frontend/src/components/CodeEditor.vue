<template>
	<div class="in-coder-panel">
		<textarea ref="textarea" v-model="code"></textarea>
	</div>
</template>

<script>
import _CodeMirror from 'codemirror/lib/codemirror';
import 'codemirror/lib/codemirror.css';
import 'codemirror/addon/hint/show-hint.css';
import 'codemirror/addon/display/autorefresh.js';
import 'codemirror/mode/javascript/javascript.js';
const codemirrorThemList = [];
const requireModules = require.context('codemirror/theme/', false, /\.css$/);
requireModules.keys().forEach((value) => {
	const newValue = value.replace(/^\.\//, '').replace(/\.css$/, '');
	codemirrorThemList.push(newValue);
});

const CodeMirror = window.CodeMirror || _CodeMirror;
let coder = null; // 编辑器实例

import {
	reactive,
	defineComponent,
	toRefs,
	getCurrentInstance,
	onMounted,
	onBeforeUnmount,
	watch,
} from 'vue';
export default defineComponent({
	name: 'codeEditor',
	props: {
		value: {
			type: String,
			default: 'edit',
		},
		scene: {
			type: String,
			default: 'look', // add: 新增； edit: 编辑； look: 查看
		},
		eventType: {
			type: String,
			default: 'change', // 可用事件'change', 'blur'等
		},
		theme: {
			type: String,
			default: 'base16-dark',
		},
	},
	setup(props, {emit}) {
		const {proxy} = getCurrentInstance();
		const data = reactive({
			code: props.value,
			options: {
				mode: 'javascript',
				// 使setValue立刻显示，而不是聚焦后才显示.
				// 使用code.refresh() 和 proxy.$refs.textarea.focus() 失效，是由于此时codemirror还未显示导致，因此官方提供了autoRefresh插件。
				// https://codemirror.net/doc/manual.html#addon_autorefresh
				// 参考：https://stackoverflow.com/questions/8349571/codemirror-editor-is-not-loading-content-until-clicked
				autoRefresh: true,
				tabSize: 2,
				theme: props.theme,
				// 显示行号
				lineNumbers: false,
				readOnly:
					props.scene === 'add' || props.scene === 'edit' ? false : 'nocursor', // true: 不可编辑  false: 可编辑 'nocursor' 失焦,不可编辑
			},
			initialize: () => {
				coder = CodeMirror.fromTextArea(proxy.$refs.textarea, data.options);
				coder.on(props.eventType, (coder) => {
					emit('update:value', coder.getValue());
				});
			},

			importThemDynamic: () => {
				return new Promise((resolve) => {
					codemirrorThemList.forEach((value) => {
						if (props.theme === value) {
							import(`codemirror/theme/${props.theme}.css`);
							resolve();
						}
					});
				});
			},
		});
		watch(
			() => props.value,
			(val) => {
				coder.setValue(val);
				// setTimeout(() => {
				// 	coder.refresh()
				// }, 4);
			}
		);
		onMounted(() => {
			data.importThemDynamic().then(() => {
				data.initialize();
			});
		});
		onBeforeUnmount(() => {
			coder.off(props.eventType);
		});
		return {
			...toRefs(data),
		};
	},
});
</script>

<style>
.in-coder-panel {
	flex-grow: 1;
	display: flex;
	position: relative;
	height: 100%;
}
.in-coder-panel .CodeMirror {
	flex-grow: 1;
	text-align: left !important;
	z-index: 1;
	width: 100%;
	min-width: 750px;
	height: 100%;
	background: #1a1f2c;
	border: 1px solid #353a4c;
}
.in-coder-panel .CodeMirror .CodeMirror-code {
	line-height: 19px;
}
</style>
