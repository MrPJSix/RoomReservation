<template>
  <div class="profile-history">
    <van-cell class="cell-history" :title="$t('userPage.history')" is-link to="history" icon="orders-o" />
  </div>
</template>

<script>
export default {
    name: "ProfileHistory",
}
</script>

<style>
.profile-history {
    position: fixed;
    width: 100%;
    top: 37%;
}
.cell-history {
    text-align: left;
}
</style>