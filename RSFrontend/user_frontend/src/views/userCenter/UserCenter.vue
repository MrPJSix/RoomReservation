<template>
  <div class="user-content">
    <profile-head></profile-head>
    <profile-credits></profile-credits>
    <profile-history></profile-history>
    <profile-other></profile-other>
  </div>
</template>

<script>
import ProfileCredits from './UcComps/ProfileCredits.vue'
import ProfileHead from './UcComps/ProfileHead.vue'
import ProfileHistory from './UcComps/ProfileHistory.vue'
import ProfileOther from './UcComps/ProfileOther.vue'
export default {
  components: { ProfileHead, ProfileCredits, ProfileHistory, ProfileOther },
    name: "UserCenter"
}
</script>

<style>
.user-content {
  position: fixed;
  width: 100%;
  background-color: rgba(206, 203, 203, 0.721);
  height: 87%;
}
</style>