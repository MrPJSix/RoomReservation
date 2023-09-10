<template>
  <div class="bp-room-detail">
    <p>{{ $t("bookingPage.roomInfo.openTimeTitle") }}: {{ openTime }}</p>
    <!-- <p>目前座位状况: 22/50, 3/25</p> -->
    <p>
      {{ $t("bookingPage.roomInfo.typeTitle") }}:
      {{
        roomType == "1"
          ? $t("bookingPage.roomInfo.type.room")
          : room.type == "2"
          ? $t("bookingPage.roomInfo.type.library")
          : $t("bookingPage.roomInfo.type.other")
      }}
    </p>
  </div>
</template>

<script>
export default {
  name: "BpRoomInfo",
  computed: {
    openTime() {
      let arr1 = this.$store.state.room.open_time.split(":");
      let arr2 = this.$store.state.room.close_time.split(":");
      return arr1[0] + ":00 - " + arr2[0] + ":00";
    },
    roomType() {
      return this.$store.state.room.type;
    },
  },
};
</script>

<style>
.bp-room-detail {
  background-color: rgb(248 247 247);
  margin: 0;
  display: table;
  width: 100%;
  font-size: 13px;
}
</style>