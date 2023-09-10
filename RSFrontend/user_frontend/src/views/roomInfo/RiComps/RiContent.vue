<template>
  <div class="booking-content">
    <van-cell
      v-for="room in rooms"
      :key="room.room_id"
      icon="star-o"
      is-link
      to="/booking"
      class="cell-room"
      @click="click(room)"
    >
      <template #title>
        <span class="custom-title"
          >{{ room.room_name }} ({{ room.number_of_seats }}/50)</span
        >
        <van-tag type="primary">{{
          room.type == "1"
            ? $t("roomPage.type.room")
            : room.type == "2"
            ? $t("roomPage.type.library")
            : $t("roomPage.type.other")
        }}</van-tag>
      </template>
    </van-cell>
  </div>
</template>

<script>
import room from "@/api/room";
export default {
  name: "RiContent",
  data() {
    return {
      activeName: "1",
      rooms: [],
    };
  },
  created() {
    room
      .getAllRooms({ building_id: this.$store.state.building.building_id })
      .then((res) => {
        console.log(res.data);
        this.rooms = res.data.data;
      });
  },
  methods: {
    click(room) {
      console.log(room);
      this.$store.dispatch("addRoom", room);
    },
  },
};
</script>

<style>
.booking-content {
  position: relative;
  top: 0%;
  width: 100%;
  height: 87%;
  background-color: rgb(235, 233, 233);
}
.booking-contents {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.cell-room {
  text-align: left;
}
.custom-title {
  margin-right: 4px;
  vertical-align: middle;
}
</style>