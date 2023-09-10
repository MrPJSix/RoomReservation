<template>
  <div class="rmbtn">
    <van-button class="button-box" size="small" plain type="info" to="history">{{$t('rmPage.history')}}</van-button>
  </div>
</template>

<script>
export default {
    name: "RmButton",
}
</script>

<style>
.rmbtn {
  position: fixed; 
  width: 100%;
  top: 12%;
  height: 42px;
  background-color: rgb(244, 244, 244);
}
.button-box {
  position: fixed;
  top: 110px;
  height: 25px;
  right: 7px;
}
</style>