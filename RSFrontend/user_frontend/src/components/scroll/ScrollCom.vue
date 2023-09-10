<template>
    <div class="wrapper" ref="wrapper">
        <div class="content">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import BScroll from '@better-scroll/core'

export default {
    name: "ScrollCom",
    data() {
        return {
            scroll: null
        }
    },
    mounted() {
        this.scroll = new BScroll(this.$refs.wrapper, {
            click: true,
        })
    },
    methods: {
        refresh() {
            this.scroll = new BScroll(this.$refs.wrapper)
        }
    },
}
</script>

<style scoped>
.content {
    background-color: white;
}
</style>

