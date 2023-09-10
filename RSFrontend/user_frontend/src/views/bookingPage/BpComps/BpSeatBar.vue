<template>
  <div id="bp-seat-bar">
    <div class="tips">
      <ul class="seat-intro">
        <li><span class="seat active"></span>{{$t('bookingPage.seatBar.vacant')}}</li>
        <li><span class="seat selected"></span>{{$t('bookingPage.seatBar.chosen')}}</li>
        <li><span class="seat disable"></span>{{$t('bookingPage.seatBar.disable')}}</li>
        <li><span class="seat flash"></span>{{$t('bookingPage.seatBar.charge')}}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
    name: "BpSeatBar",
}
</script>

<style>
#bp-seat-bar {
    background-color: rgb(236, 235, 235);
}
.seat {
    /* display: flex; */
    /* display: inline-block; */
    /* display: inline-table; */
    width: 30px;
    height: 30px;
    line-height: 30px;
    /* margin: 0 .04rem .04rem 0; */
    background-size: 30px 30px;
}
.active {
  background-image: url('/src/assets/seats/choose_uncharge.png');
}
.selected {
  background-image: url('/src/assets/seats/chosen_uncharge.png');
}
.disable {
  background-image: url('/src/assets/seats/unchoose_uncharge.png');
}
.flash {
  background-image: url('/src/assets/seats/flash.png');
}
.tips {
  min-height: 30px;
  line-height: 10px;
  /* border-top: 1px solid #d6d6d6; */
  background: #f8f8f8;
}
.tips .seat-intro {
  padding-right: .5em;
  text-align: center;
}
.tips .seat-intro li {
  display: flex;
  float: left;
  width: 25%;
  font-size: 13px;
  justify-content: center;
  align-items: center;
}
.tips .seat-intro .seat {
  margin: 0 .06rem;
  vertical-align: -.04rem;
}
</style>