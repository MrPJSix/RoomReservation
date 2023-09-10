import axios from "./api";
import qs from "qs"
import store from "@/strore"

const user = {
    
    //登录
    login(params) {
        return axios.post('/login/', qs.stringify(params))
    },

    //注册
    register(params) {
        console.log(params)
        return axios.post('/register/', qs.stringify(params))
    },

    //预定座位
    booking(params) {
        return axios.post('/studyroom/booking', qs.stringify(params))
    },

    //取消预约
    cancelReservation(params) {
        return axios.put('/reservations/cancel', qs.stringify(params))
    },

    //获取所有的预约记录
    getAllReservations(params) {
        return axios.get('/reservations/info', {params: params})
    },

    //获取未生效的预约记录
    getInvalidReservations(params) {
        axios.get('/reservations/invalid', {params: params}).then(
            res => {
                store.dispatch("addInvalidReservation", res.data)
            }
        )
    },

    //签到
    signIn(params) {
        return axios.get('reservations/sign', {params: params})
    },

    //查询用户信息
    getUserInfo(params) {
        axios.get('userInfo/', {params: params}).then(
            res => {
                store.dispatch("addUser", res.data.data)
            }
        )
    }
}

export default user;