<template>
  <div class="bp-nav-bar">
    <van-nav-bar
        :title="room_name"
        left-arrow
        @click-left="onClickLeft"
    >
        <template #right>
            <van-icon name="replay" size="18" @click="refresh"/>
        </template>
    </van-nav-bar>
  </div>
</template>

<script>
import { Notify } from 'vant';
export default {
    name: "BpNavBar",
    data() {
        return {
            room_name: this.$store.state.room.room_name
        }
    },
    methods: {
        onClickLeft() {
            this.$router.push("/room");
        },
        refresh() {
            Notify({type: 'primary', message: '刷新...'})
        }
    }
}
</script>

<style lang="less" scoped>
.van-nav-bar {
    background-color: #409eff;
}
/deep/.van-nav-bar__title{
    max-width: 60%;
    margin: 0 auto;
    color: #fff;
    font-weight: 500;
    font-size: 16px;
}
/deep/.van-nav-bar .van-icon {
    color: #fff !important;
}
/deep/.van-nav-bar__text {
    color: #fff;
}
</style>