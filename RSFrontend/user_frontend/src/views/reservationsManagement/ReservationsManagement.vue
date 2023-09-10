<template>
  <div>
    <rm-nav-bar></rm-nav-bar>
    <rm-button></rm-button>
    <div class="rm-content-body">
      <reservation-detail class="detail-box" v-if="haveInvalidReservation"></reservation-detail>
      <van-empty class="empty-box" v-else :description="$t('rmPage.noReservations')" />
    </div>
  </div>
</template>

<script>
import ReservationDetail from './comps/ReservationDetail.vue'
import RmButton from './comps/RmButton.vue'
import RmNavBar from './comps/RmNavBar.vue'
export default {
  components: { RmNavBar, ReservationDetail, RmButton },
    name: "ReservationsManagement",
    computed: {
      haveInvalidReservation() {
        return JSON.stringify(this.$store.state.invalidReservation) !== '{}'
      }
    }
}
</script>

<style>
.rm-content-body {
  position: fixed;
  width: 100%;
  top: 17%;
  height: 76.9%;
  background-color: rgb(244, 244, 244);
}
.empty-box {
  position: fixed;
  width: 100%;
  top: 18%;
  height: 75%;
  background-color: white;
}
.detail-box {
  position: fixed;
  width: 100%;
  height: 30%;
  top: 18%;
  background-color: #fff;
}
</style>