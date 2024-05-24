<template>
  <el-select v-model="selected" :clearable="clearable" filterable :placeholder="placeholder"
             :filter-method="filterMethod" @change="valueChange" @visible-change="visibleChange">
    <el-option v-for="item in resultList" :key="item.id" :value="item.id" :label="item.name"></el-option>
  </el-select>
</template>

<script>
import $Pinyin from 'js-pinyin'
$Pinyin.setOptions({checkPolyphone: false, charCase: 0});
export default {
    props: ['value','list','placeholder', 'clearable'],  // value即上层传进来的model
    data(){
        return {
            selected: this.value,   // 不能直接拿prop的value去作为model
            resultList: this.list
        }
    },
    watch:{
        list: function(){
            this.resultList = this.list;
        },
        value: function (val) {
            this.selected = val;
        }
    },
    methods: {
        filterMethod(key){
            let regStr = key.split('').join(".*");
            let regExp = new RegExp(regStr.toLowerCase());
            this.resultList = this.list.filter((item)=>{
                let pinyin = $Pinyin.getFullChars(item.name).toLowerCase();
                return regExp.test(item.name) || regExp.test(pinyin);
            });
        },
        valueChange(){
            this.$emit('input', this.selected); // 发出input事件，用于改变上层的model
            this.$emit('change');
        },
        visibleChange(visible){
            if(visible){
                this.resultList = this.list;
            }
        }
    }
}
</script>

<style scoped>

</style>
