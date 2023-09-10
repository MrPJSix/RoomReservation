<template>
  <div class="user-booking">
    <van-nav-bar
      :title="$t('roomPage.title')"
      left-arrow
      @click-left="onClickLeft"
    >
      <template #right>
        <van-icon name="replay" size="18" @click="refresh" />
      </template>
    </van-nav-bar>
    <!-- <condition-search></condition-search> -->
    <ri-content></ri-content>
  </div>
</template>

<script>
import { Notify } from 'vant'
// import ConditionSearch from './RiComps/ConditionSearch.vue'
import RiContent from './RiComps/RiContent.vue'
export default {
  components: { RiContent},
    name: "RoomInfo",
    methods: {
      onClickLeft() {
        this.$router.push("/building")
    },
      refresh() {
        Notify({ type: 'primary', message: '刷新...' });
    }
    }
}
</script>


<style lang="less" scoped>
.van-nav-bar {
  background-color: #409eff;
}
/deep/.van-nav-bar__title {
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
.user-booking {
  position: fixed;
  width: 100%;
  /* background-color: aquamarine; */
  height: 100%;
}
</style>