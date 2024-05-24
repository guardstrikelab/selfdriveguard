<template>
    <el-dialog v-model="show" width="900px" :append-to-body="true" :close-on-click-modal="false">
        <el-carousel ref="carousel" :autoplay="false" arrow="always" height="500px" @change="change">
            <el-carousel-item v-for="(item,index) in images" :key="index" :label="item.label">
                <img :src="item.src"/>
            </el-carousel-item>
        </el-carousel>
    </el-dialog>
</template>

<script>
    export default {
        props: ['value', 'images', 'activeIndex'],  // value即上层传进来的model
        data() {
            return {
                show: this.value
            }
        },
        watch: {
            show: function (val) {
                this.$emit('update:value', val);
            },
            activeIndex: function (val) {
                this.$refs.carousel && this.$refs.carousel.setActiveItem(val);
            }
        },
        methods: {
            change(index) {
                this.$emit('update:activeIndex', index);
            }
        }
    }
</script>

<style lang="less">
    .el-carousel__item {
        img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
    }
</style>
