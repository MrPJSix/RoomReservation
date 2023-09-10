export default {
    loginPage: {
        title: "自习室座位预约系统",
        id: "学号",
        password: "密码",
        login: "登录",
        register: "注册",
        idMessage: "请填写学号",
        passwordMessage: "请填写密码",
    },
    registerPage: {
        title: "注  册",
        id: "学号",
        username: "姓名",
        email: "邮箱",
        emailPlaceholder: "邮箱如xxx@yy.zz",
        password: "密码",
        idMessage: "请填写学号",
        usernameMessage: "请填写姓名",
        emailMessage: "请填写邮箱",
        passwordMessage: "请填写密码",
        submit: "提交",
    },
    userPage: {
        credits: "信誉值",
        defaultTimes: "违约次数",
        history: "历史记录",
        help: "使用帮助",
        questions: "常见问题",
        feedback: "留言反馈",
        nowLang: "系统语言"
    },
    campusPage: {
        title: "校区选择",
    },
    mainTabBar: {
        rm: "预约管理",
        home: "首页",
        uc: "个人中心"
    },
    buildingPage: {
        title: "教学楼选择"
    },
    roomPage: {
        title: "自习室选择",
        type: {
            room: "教室",
            library: "图书馆",
            other: "其他",
        },
    },
    bookingPage: {
        roomInfo: {
            openTimeTitle: "当时开放时间",
            typeTitle: "自习室类型",
            type: {
                room: "教室",
                library: "图书馆",
                other: "其他",
            },
        },
        bookingDetail: {
            bookingDateTitle: "预约日期",
            startTimeTitle: "开始时间",
            now: "当前时间"
        },
        seatBar: {
            vacant: "可预约",
            chosen: "已选",
            disable: "不可选",
            charge: "充电标志",
        },
        bookingDialogue: {
            resDateTitle: "预约时间",
            durationTitle: "自习时长",
            chosenSeatTitle: "已选座位",
            cancel: "取消",
        }
    },
    rmPage: {
        noReservations: "暂无预约",
        myReservations: "我的预约",
        history: "历史预约",
        resDetail: {
            title: "预约信息",
            id: "预约号",
            name: "预约人",
            seat: "座位",
            date: "预约日期",
            duration: "预约时长",
            statusTitle: "预约状态",
            status: {
                notCheckedIn: "未签到",
                checkedIn: "已签到",
                canceled: "已取消",
                defaulted: "已违约",
                ended: "已结束"
            },
            cancel: "取消",
            cancelMes: "是否取消预约？",
            cancelSuc: "取消预约成功!",
            cancelDef: "取消预约失败!",
            signIn: "签到",
            signInSuc: "签到成功!",
            signInDef: "签到失败!",
        }
    },
    historyPage: {
        title: "历史预约记录",
        res: {
            id: "预约号",
            name: "预约人",
            seat: "座位",
            date: "预约日期",
            duration: "预约时长",
            statusTitle: "预约状态",
            status: {
                notCheckedIn: "未签到",
                checkedIn: "已签到",
                canceled: "已取消",
                defaulted: "已违约",
                ended: "已结束"
            }
        }
    },
}