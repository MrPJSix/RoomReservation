<template>
  <div>
    <bp-nav-bar></bp-nav-bar>
    <bp-room-info></bp-room-info>
    <bp-detail></bp-detail>
    <bp-seat-bar></bp-seat-bar>
    <bp-seat-map></bp-seat-map>
    <!-- BookingPage...... -->
  </div>
</template>

<script>
import BpDetail from './BpComps/BpDetail.vue'
import BpNavBar from './BpComps/BpNavBar.vue'
import BpRoomInfo from './BpComps/BpRoomInfo.vue'
import BpSeatBar from './BpComps/BpSeatBar.vue'
import BpSeatMap from './BpComps/BpSeatMap.vue'
export default {
  components: { BpNavBar, BpDetail, BpRoomInfo, BpSeatBar, BpSeatMap },
    name: "BookingPage",
}
</script>

<style>

</style>