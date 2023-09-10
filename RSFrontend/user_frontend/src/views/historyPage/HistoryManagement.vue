<template>
  <div id="history-management">
    <van-nav-bar :title="$t('historyPage.title')" left-arrow @click-left="onClickLeft">
      <template #right>
        <van-icon name="replay" size="18" @click="refresh" />
      </template>
    </van-nav-bar>
    <scroll-com ref="scroll">
      <div>
        <div
          class="res-detail-body"
          v-for="(reservation, index) in reservations"
          :key="index"
        >
          <!-- <van-divider :style="{ borderColor: 'black' }" /> -->
          <van-row>
            <van-col class="col1" span="4">{{$t('historyPage.res.id')}}</van-col>
            <van-col class="col2" span="12">{{
              reservation.reservation_id
            }}</van-col>
          </van-row>
          <van-row>
            <van-col class="col1" span="4">{{$t('historyPage.res.name')}}</van-col>
            <van-col class="col2" span="12"
              >{{ user.user_id }} {{ user.user_name }}</van-col
            >
          </van-row>
          <van-row>
            <van-col class="col1" span="4">{{$t('historyPage.res.seat')}}</van-col>
            <van-col class="col2" span="16"
              >
              <!-- {{ reservation.campus_name }} / {{ reservation.building_name }} / -->
              {{ reservation.room_name }} /
              {{ reservation.seat_number }}</van-col
            >
          </van-row>
          <van-row>
            <van-col class="col1" span="4">{{$t('historyPage.res.date')}}</van-col>
            <van-col class="col2" span="12"
              >{{ reservation.date }}
              {{ reservation.reservation_time }}</van-col
            >
          </van-row>
          <van-row>
            <van-col class="col1" span="4">{{$t('historyPage.res.duration')}}</van-col>
            <van-col class="col2" span="12"
              >{{ reservation.reservation_hours }}h</van-col
            >
          </van-row>
          <van-row>
            <van-col class="col1" span="4">{{$t('historyPage.res.statusTitle')}}</van-col>
            <van-col class="col2" span="12">{{
              reservationStatus(reservation.reservation_status)
            }}</van-col>
          </van-row>
        </div>
      </div>
    </scroll-com>
  </div>
</template>

<script>
import user from "@/api/user";
import ScrollCom from "@/components/scroll/ScrollCom.vue";
import { Notify } from 'vant';
export default {
  components: { ScrollCom },
  name: "HistoryManagement",
  data() {
    return {
      reservations: [],
    };
  },
  created() {
    user
      .getAllReservations({ user_id: this.$store.state.userData.user_id })
      .then((res) => {
        if (res.data.success === true) {
          console.log(res.data);
          this.reservations = res.data.data;
          this.$nextTick(() => {
            this.$refs.scroll.refresh()
          })
        } else {
          Notify({ type: 'danger', message: '获取历史信息失败!' });
        }
      });
  },
  methods: {
    reservationStatus(v) {
      let ch = v
      if (ch === '0') {
        return this.$t('historyPage.res.status.notCheckedIn')
      } else if (ch === '1') {
        return this.$t('historyPage.res.status.checkedIn')
      } else if (ch === '2') {
        return this.$t('historyPage.res.status.canceled')
      } else if (ch === '3') {
        return this.$t('historyPage.res.status.defaulted')
      } else {
        return this.$t('historyPage.res.status.ended')
      }
    },
    onClickLeft() {
      this.$router.push("reservationsManagement");
    },
    refresh() {
      Notify({ type: 'primary', message: '刷新...' });
    },
  },
  computed: {
    user() {
      return this.$store.state.userData;
    },
  },
};
</script>

<style lang="less" scoped>
.van-nav-bar {
  background-color: #409eff;
}
/deep/.van-nav-bar__title {
  max-width: 60%;
  margin: 0 auto;
  color: #fff;
  font-weight: 500;
  font-size: 16px;
}
/deep/.van-nav-bar .van-icon {
  color: #fff !important;
}
/deep/.van-nav-bar__text {
  color: #fff;
}
.col1 {
  text-align: left;
  margin-left: 20px;
  font-size: 13px;
  /* background-color: red; */
  line-height: 25px;
}
.col2 {
  text-align: left;
  margin-left: 0px;
  font-size: 13px;
  line-height: 25px;
}
.res-detail-body {
    border-bottom-color: #409eff;
    border-width: 1px;
    border: solid;
}
.wrapper {
    height: calc(100vh - 46px - 49px - 60px);
    overflow: hidden;
    background-color: rgb(235, 249, 249);
}
</style>