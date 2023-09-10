<template>
    <div class="RmNavBar">
        <p>{{$t('rmPage.myReservations')}}</p>
    </div>
</template>

<script>
export default {
    name: "RmNavBar"
}
</script>

<style>
.RmNavBar {
    background-color: rgb(70, 156, 241);
    position: fixed;
    width: 100%;
    height: 5%;
    color: white;
    line-height: 15px;
}
</style>