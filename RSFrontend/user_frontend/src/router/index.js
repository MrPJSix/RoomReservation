import Vue from "vue"
import VueRouter from "vue-router"

// 解决同路由跳转时的报错
const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err);
};

//1.安装插件
Vue.use(VueRouter)

const UserLogin = () => import("../components/UserLogin.vue")
const UserRegister = () => import("../components/UserRegister.vue")
const UserMain = () => import("../components/UserMain.vue")
const ReservationsManagement = () => import("../views/reservationsManagement/ReservationsManagement.vue")
const RoomInfo = () => import("../views/roomInfo/RoomInfo.vue")
const UserCenter = () => import("../views/userCenter/UserCenter.vue")
const BookingPage = () => import("../views/bookingPage/BookingPage.vue")
const CampusPage = () => import("../views/campusPage/CampusPage.vue")
const BuildingPage = () => import("../views/campusPage/BuildingPage.vue")
const historyPage = () => import("../views/historyPage/HistoryManagement.vue")

const routes = [
    { path: "", redirect: "/login"},
    { path: "/login", component: UserLogin},
    { path: "/register", component: UserRegister},
    { path: "/apphome", 
      component: UserMain,
      children: [
        { path: "/room", component: RoomInfo},
        { path: "/campus", component: CampusPage},
        { path: "/building", component: BuildingPage},
        { path: "/reservationsManagement", component: ReservationsManagement},
        { path: "/userCenter", component: UserCenter},
        { path: "/booking", component: BookingPage},
        { path: "/history", component: historyPage},
      ]
    },
]

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
})

export default router