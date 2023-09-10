export default {
    //添加campus数据至vuex
    addCampus(context, value) {
        context.commit('ADDCAMPUS', value)
        sessionStorage.setItem("campusData", JSON.stringify(value))
    },

    //添加building数据至vuex
    addBuilding(context, value) {
        context.commit('ADDBUILDING', value)
        sessionStorage.setItem("buildingData", JSON.stringify(value))
    },

    //添加room数据至vuex
    addRoom(context, value) {
        context.commit('ADDROOM', value)
        sessionStorage.setItem("roomData", JSON.stringify(value))
    },

    //修改seatStatus
    updateSeatStatus(context, value) {
        context.commit('UPDATESEATSTATUS', value)
        sessionStorage.setItem("seatStatus", JSON.stringify(value))
    },

    //添加user数据至vuex
    addUser(context, value) {
        context.commit('ADDUSER', value)
        sessionStorage.setItem("userData", JSON.stringify(value))
    },

    //添加用户未生效的reservation数据至vuex
    addInvalidReservation(context, value) {
        let v
        if (value.success === true) {
            v = value.data
        } else {
            v = {}
        }
        context.commit('ADDINVALIDRESERVATION', v)
        sessionStorage.setItem("invalidReservation", JSON.stringify(v))
    },

    //修改startTime
    updateStartTime(context, value) {
        context.commit('UPDATESTARTTIME', value)
        sessionStorage.setItem("startTime", JSON.stringify(value))
    }
}