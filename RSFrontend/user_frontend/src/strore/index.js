import Vue from "vue";
import Vuex from "vuex";

import mutations from "./mutations";
import actions from "./actions";
import getters from "./getters";
import moment from "moment";

Vue.use(Vuex)

const state = {
    //选中的校区数据
    campus: JSON.parse(sessionStorage.getItem("campusData")) ? JSON.parse(sessionStorage.getItem("campusData")) : {},
    //选中的教学楼数据
    building: JSON.parse(sessionStorage.getItem("buildingData")) ? JSON.parse(sessionStorage.getItem("buildingData")) : {},
    //选中的自习室数据
    room: JSON.parse(sessionStorage.getItem("roomData")) ? JSON.parse(sessionStorage.getItem("roomData")) : {},
    //按时间的自习室座位状态
    seatStatus: JSON.parse(sessionStorage.getItem("seatStatus")) ? JSON.parse(sessionStorage.getItem("seatStatus")) : "",
    //用户数据
    userData: JSON.parse(sessionStorage.getItem("userData")) ? JSON.parse(sessionStorage.getItem("userData")) : {},
    //预约数据
    invalidReservation: JSON.parse(sessionStorage.getItem("invalidReservation")) ? JSON.parse(sessionStorage.getItem("invalidReservation")) : {},
    //自习开始时间
    startTime: JSON.parse(sessionStorage.getItem("startTime")) ? JSON.parse(sessionStorage.getItem("startTime")) : parseInt(moment().format("HH")),
}

export default new Vuex.Store({
    state,
    mutations,
    actions,
    getters,
})