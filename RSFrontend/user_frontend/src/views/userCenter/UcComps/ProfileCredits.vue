<template>
  <div class="profile-credits"> 
    <van-cell-group>
      <van-cell class="cell-credits" :title="$t('userPage.credits')" :value="credits" icon="diamond-o"/>
      <van-cell class="cell-credits" :title="$t('userPage.defaultTimes') " :value="defaultTimes" icon="warning-o" />
    </van-cell-group>
  </div>
</template>

<script>
export default {
    name: "ProfileCredits",
    computed: {
      credits() {
        return this.$store.state.userData.credits
      },
      defaultTimes() {
        return this.$store.state.userData.default_times
      },
    }
}
</script>

<style>
.profile-credits {
    position: fixed;
    width: 100%;
    top: 25%;
}
.cell-credits {
    text-align: left;
}
</style>