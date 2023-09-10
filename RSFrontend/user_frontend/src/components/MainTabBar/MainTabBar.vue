<template>
    <tab-bar>
        <tab-bar-item path="/reservationsManagement" activeColor="DodgerBlue" >
            <van-icon slot="item-icon" name="todo-list" color="DarkGray" size="30px" @click="getInvalidRes"/>
            <van-icon slot="item-icon-active" name="todo-list" color="DodgerBlue" size="30px"/>
            <div slot="item-text">{{$t('mainTabBar.rm')}}</div>
        </tab-bar-item>
        <tab-bar-item path="/campus" activeColor="DodgerBlue">
            <van-icon slot="item-icon" name="wap-home" color="DarkGray" size="30px"/>
            <van-icon slot="item-icon-active" name="wap-home" color="DodgerBlue" size="30px"/>
            <div slot="item-text">{{$t('mainTabBar.home')}}</div>
        </tab-bar-item>
        <tab-bar-item path="/userCenter" activeColor="DodgerBlue">
            <van-icon slot="item-icon" name="manager" color="DarkGray" size="30px" @click="getUser"/>
            <van-icon slot="item-icon-active" name="manager" color="DodgerBlue" size="30px"/>
            <div slot="item-text">{{$t('mainTabBar.uc')}}</div>
        </tab-bar-item>
    </tab-bar>
</template>

<script>
import user from '@/api/user'
  import TabBar from "../tabBar/TabBar.vue"
  import TabBarItem from "../tabBar/TabBarItem.vue"

export default {
  name:'MainTabBar',
  components:{
      TabBar,
      TabBarItem
    },
    methods: {
        getInvalidRes() {
            user.getInvalidReservations({ user_id: this.$store.state.userData.user_id })
        },
        getUser() {
            user.getUserInfo({ user_id: this.$store.state.userData.user_id })
        }
    }
}
</script>

<style>

</style>