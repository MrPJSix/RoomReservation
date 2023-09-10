<template>
  <div class="res-detail">
    <p id="title">{{$t('rmPage.resDetail.title')}}</p>
    <van-divider :style="{ borderColor: 'black' }" />
    <div class="res-detail-body">
      <van-row>
        <van-col class="col1" span="4">{{$t('rmPage.resDetail.id')}}</van-col>
        <van-col class="col2" span="12">{{
          invalidReservation.reservation_id
        }}</van-col>
      </van-row>
      <van-row>
        <van-col class="col1" span="4">{{$t('rmPage.resDetail.name')}}</van-col>
        <van-col class="col2" span="12"
          >{{ user.user_id }} - {{ user.user_name }}</van-col
        >
      </van-row>
      <van-row>
        <van-col class="col1" span="4">{{$t('rmPage.resDetail.seat')}}</van-col>
        <van-col class="col2" span="16"
          >
          <!-- {{ invalidReservation.campus_name }} /
          {{ invalidReservation.building_name }} / -->
          {{ invalidReservation.room_name }} /
          {{ invalidReservation.seat_number }}</van-col
        >
      </van-row>
      <van-row>
        <van-col class="col1" span="4">{{$t('rmPage.resDetail.date')}}</van-col>
        <van-col class="col2" span="12"
          >{{ invalidReservation.date }}
          {{ invalidReservation.reservation_time }}</van-col
        >
      </van-row>
      <van-row>
        <van-col class="col1" span="4">{{$t('rmPage.resDetail.duration')}}</van-col>
        <van-col class="col2" span="12"
          >{{ invalidReservation.reservation_hours }}h</van-col
        >
      </van-row>
      <van-row>
        <van-col class="col1" span="4">{{$t('rmPage.resDetail.statusTitle')}}</van-col>
        <van-col class="col2" span="12">{{resStatus}}</van-col>
      </van-row>
    </div>
    <span v-if="buttonShow">
      <van-button
        type="danger"
        hairline
        size="small"
        style="height: 25px"
        @click="cancelRes"
        >{{$t('rmPage.resDetail.cancel')}}</van-button
      >
      <van-dialog
        v-model="show"
        :title="$t('rmPage.resDetail.cancelMes')"
        show-cancel-button
        @confirm="confirm"
      >
      </van-dialog>
    </span>
    <span v-if="buttonShow">{{ }}
    </span>
    <span v-if="buttonShow">
      <van-button
        type="info"
        hairline
        size="small"
        style="height: 25px"
        @click="signin"
        >{{$t('rmPage.resDetail.signIn')}}</van-button
      >
    </span>
  </div>
</template>

<script>
import user from "@/api/user";
import { Notify } from 'vant';
export default {
  name: "ReservationDetail",
  components: {},
  data() {
    return {
      show: false,
      
    };
  },
  computed: {
    invalidReservation() {
      return this.$store.state.invalidReservation;
    },
    user() {
      return this.$store.state.userData;
    },
    resStatus() {
      let ch = this.$store.state.invalidReservation.reservation_status
      if (ch === '0') {
        return this.$t('rmPage.resDetail.status.notCheckedIn')
      } else if (ch === '1') {
        return this.$t('rmPage.resDetail.status.checkedIn')
      } else if (ch === '2') {
        return this.$t('rmPage.resDetail.status.canceled')
      } else if (ch === '3') {
        return this.$t('rmPage.resDetail.status.defaulted')
      } else {
        return this.$t('rmPage.resDetail.status.ended')
      }
    },
    // 当未签到时才显示“取消”，“签到”按钮， 已签到则不显示
    buttonShow() {
      let ch = this.$store.state.invalidReservation.reservation_status
      if (ch === '0') {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    cancelRes() {
      this.show = true;
    },
    confirm() {
      user
        .cancelReservation({
          reservation_id: this.$store.state.invalidReservation.reservation_id,
        })
        .then((res) => {
          // 取消预约成功
          if (res.data.success === true) {
            Notify({ type: 'success', message: this.$t('rmPage.resDetail.cancelSuc') });
            user.getInvalidReservations({
              user_id: this.$store.state.userData.user_id,
            });
          } else {
            // 取消预约失败
            Notify({ type: 'danger', message: this.$t('rmPage.resDetail.cancelDef') });
          }
        });
    },
    signin() {
        user.signIn({reservation_id: this.invalidReservation.reservation_id}).then(
            res => {
                if (res.data.success === true) {
                  // 签到成功
                    Notify({ type: 'success', message: this.$t('rmPage.resDetail.signInSuc') });
                    user.getInvalidReservations({
                        user_id: this.$store.state.userData.user_id,
                    })
                } else {
                  // 签到失败
                    Notify({ type: 'danger', message: this.$t('rmPage.resDetail.signInDef') });
                }
            }
        )
    },
  },
};
</script>

<style>
#title {
  position: relative;
  text-align: left;
  margin-left: 15px;
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
</style>