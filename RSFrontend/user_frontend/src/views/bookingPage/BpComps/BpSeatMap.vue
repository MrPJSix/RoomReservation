<template>
  <div id="bp-seat-map" ref="seatMap">
    <p
      v-for="(rowInfo, rowIndex) in seats"
      :key="rowIndex"
      @click="select_seat"
    >
      <template v-for="(cell, colIndex) in rowInfo">
        <div class="seat-item" :key="colIndex">
          <van-badge :content="hour_able(cell)">
            <div
              v-if="
                cell === 'B' || cell === 'C' || cell === 'D' || cell === 'E'
              "
              class="seat active-charge"
              :data-row="rowIndex"
              :data-col="colIndex"
            ></div>
            <div
              v-else-if="
                cell === 'b' || cell === 'c' || cell === 'd' || cell === 'e'
              "
              class="seat active"
              :data-row="rowIndex"
              :data-col="colIndex"
            ></div>
            <div
              v-else-if="cell === 'a'"
              class="seat disable"
              :data-row="rowIndex"
              :data-col="colIndex"
            ></div>
            <div
              v-else-if="cell === 'A'"
              class="seat disable-charge"
              :data-row="rowIndex"
              :data-col="colIndex"
            ></div>
            <!-- <div style="font-size: 1px">{{rowIndex*cols + colIndex}}</div> -->
          </van-badge>
          <a class="seat-num">{{ rowIndex * cols + colIndex + 1 }}</a>
        </div>
      </template>
    </p>
    <van-popup
      v-model="show_submit_pannel"
      position="bottom"
      :style="{ height: '30%' }"
      @close="cancel_submit"
    >
      <div class="affirm_popup">
        <h4>{{$t('bookingPage.bookingDialogue.resDateTitle')}}: {{ resDate }}</h4>
        <van-cell>
          <span slot="title">{{$t('bookingPage.bookingDialogue.durationTitle')}}</span>
          <van-stepper
            slot="default"
            v-model="res_hours_affirm"
            min="1"
            :max="maxHours"
          />
        </van-cell>
        <!-- <van-tabbar active-color="#07c160" inactive-color="#000">已选座位 {{selected_seat_num}}</van-tabbar>
            <p></p> -->
        <van-button class="affirm-btn" type="info" @click="booking"
          >{{$t('bookingPage.bookingDialogue.chosenSeatTitle')}} {{ selected_seat_num }}</van-button
        >
        <van-button
          class="cancel-btn"
          plain
          hairline
          type="info"
          @click="cancel_submit"
          >{{$t('bookingPage.bookingDialogue.cancel')}}</van-button
        >
      </div>
    </van-popup>
  </div>
</template>

<script>
import room from "@/api/room";
import moment from "moment";
import user from "@/api/user";
import { Notify } from 'vant';
export default {
  name: "BpSeatMap",
  data() {
    return {
      // a 不可选 b 可选
      // seat_status: this.$store.state.seatStatus,
      rows: 10,
      cols: 5,
      selected_seat_num: -1,
      show_submit_pannel: false,
      res_hours_affirm: 1,
      target: null,
    };
  },
  computed: {
    seats() {
      var lst = [];
      for (var i = 0; i < this.rows; i++) {
        var row = [];
        for (var j = 0; j < this.cols; j++) {
          row.push(this.$store.state.seatStatus[i * this.cols + j]);
        }
        lst.push(row);
      }
      return lst;
    },
    // 预约具体开始时间
    resDate() {
      return moment()
        .add(this.$store.state.startTime - parseInt(moment().format("HH")), "h")
        .format("YYYY/MM/DD HH:00");
    },
    maxHours() {
      console.log(this.$store.state.room.close_time);
      let t = parseInt(this.$store.state.room.close_time.substring(0, 2));
      return t - this.$store.state.startTime <= 4 ? t - this.$store.state.startTime : 4;
    },
  },
  created() {
    room
      .getSeatStatus({
        room_id: this.$store.state.room.room_id,
        time_start: this.$store.state.startTime,
      })
      .then((res) => {
        this.$store.dispatch("updateSeatStatus", res.data.data);
      });
  },
  methods: {
    hour_able(cell) {
      if (cell === "a" || cell === "A") {
        return 0;
      } else if (cell === "b" || cell === "B") {
        return 1;
      } else if (cell === "c" || cell === "C") {
        return 2;
      } else if (cell === "d" || cell === "D") {
        return 3;
      }
      return 4;
    },
    select_seat(e) {
      var target = e.target;
      if (target.tagName === "DIV") {
        const row = parseInt(target.dataset.row);
        const col = parseInt(target.dataset.col);
        if (target.classList.contains("active")) {
          target.classList.remove("active");
          target.classList.add("selected");
          this.selected_seat_num = row * 5 + col + 1;
          this.show_submit_pannel = true;
          this.target = target;
        }
        if (target.classList.contains("active-charge")) {
          target.classList.remove("active-charge");
          target.classList.add("selected-charge");
          this.selected_seat_num = row * 5 + col + 1;
          this.show_submit_pannel = true;
          this.target = target;
        }
      }
    },
    cancel_submit() {
      this.show_submit_pannel = false;
      var target = this.target;
      if (target.classList.contains("selected")) {
        target.classList.remove("selected");
        target.classList.add("active");
      }
      if (target.classList.contains("selected-charge")) {
        target.classList.remove("selected-charge");
        target.classList.add("active-charge");
      }
    },
    booking() {
      console.log(this.$store.state.userData.user_id);
      user
        .booking({
          user_id: this.$store.state.userData.user_id,
          room_id: this.$store.state.room.room_id,
          seat_number: this.selected_seat_num,
          reservation_time: this.$store.state.startTime,
          reservation_hours: this.res_hours_affirm,
        })
        .then((res) => {
          if (res.data.success == 1) {
            Notify({ type: 'success', message: '预约成功！' });
            this.show_submit_pannel = false;
            // user.getInvalidReservations({user_id: this.$store.state.userData.user_id}).then(
            //   res => {
            //     this.$store.dispatch("addInvalidReservation", res.data)
            //   }
            // )
            user.getInvalidReservations({user_id: this.$store.state.userData.user_id})
          } else {
            if (res.data.code == 401) {
              Notify({ type: 'danger', message: '信用值不及格，预约失败！' });
            } else if (res.data.code == 402) {
              Notify({ type: 'danger', message: '座位已被预定，预约失败！' });
            } else if (res.data.code == 403) {
              Notify({ type: 'danger', message: '预约时间过长，预约失败！' });
            } else if (res.data.code == 405) {
              Notify({ type: 'danger', message: '存在未生效预约，没办法再次预约！' });
            }
          }
          room
            .getSeatStatus({
              room_id: this.$store.state.room.room_id,
              time_start: parseInt(this.$store.state.startTime),
            })
            .then((res) => {
              this.$store.dispatch("updateSeatStatus", res.data.data);
            });
        });
    },
  },
};
</script>

<style lang="less" scoped>
#bp-seat-map {
  z-index: 3;
  //   display: inline-block;
  background: #f0f0f0;
  text-align: center;
  overflow: hidden;
  border-top: 1px solid silver;
  min-width: 100%;
  //   height: 430px;
  //   top: 10px;
  position: relative;
}
#bp-seat-map p {
  white-space: nowrap;
  display: flex;
  min-width: 100%;
  margin: 0;
  padding: 0;
  line-height: 0;
  justify-content: center;
}
.seat-item {
  display: flex;
  height: 45px;
  flex-direction: column;
}
.seat-num {
  font-size: 1px;
}
.seat {
  width: 40px;
  height: 40px;
  line-height: 40px;
  background-size: 40px 40px;
}
.active-charge {
  background-image: url("/src/assets/seats/choose_charge.png");
}
.active {
  background-image: url("/src/assets/seats/choose_uncharge.png");
}
.disable {
  background-image: url("/src/assets/seats/unchoose_uncharge.png");
}
.disable-charge {
  background-image: url("/src/assets/seats/unchoose_charge.png");
}
.selected {
  background-image: url("/src/assets/seats/chosen_uncharge.png");
}
.selected-charge {
  background-image: url("/src/assets/seats/chosen_charge.png");
}
/deep/.van-badge--fixed {
  top: 10px;
  right: 7px;
}
/deep/.van-button {
  height: 40px;
  width: 90%;
  margin: 5px;
}
/deep/.van-cell__title,
.van-cell__value {
  -webkit-box-flex: 1;
  -webkit-flex: 1;
  flex: 1;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>