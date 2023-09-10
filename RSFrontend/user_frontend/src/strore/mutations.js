export default {
    //添加campus数据至vuex
    ADDCAMPUS(state, value) {
        state.campus = value
    },

    //添加building数据至vuex
    ADDBUILDING(state, value) {
        state.building = value
    },

    //添加room数据至vuex
    ADDROOM(state, value) {
        state.room = value
    },

    //修改seatStatus
    UPDATESEATSTATUS(state, value) {
        state.seatStatus = value
    },

    //添加user数据至vuex
    ADDUSER(state, value) {
        state.userData = value
    },

    //添加用户未生效的reservation数据至vuex
    ADDINVALIDRESERVATION(state, value) {
        state.invalidReservation = value
    },

    //修改startTime
    UPDATESTARTTIME(state, value) {
        state.startTime = value
    },
    
}