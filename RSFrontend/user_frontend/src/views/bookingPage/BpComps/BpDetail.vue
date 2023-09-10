<template>
    <div>
        <van-row class="bp-detail-row">
            <van-col class="bp-detail-col1" span="7">{{$t('bookingPage.bookingDetail.bookingDateTitle')}}</van-col>
            <van-col class="bp-detail-col2" span="7">{{res_day}}</van-col>
            <van-col class="bp-detail-col3" span="8">
                <van-icon size="medium" class-prefix="icon" class="iconfont" name="calender" @click="showDateChoosePicker = true"></van-icon>
                <van-popup v-model="showDateChoosePicker" round position="bottom">
                    <van-picker
                        show-toolbar
                        :columns="dates"
                        @cancel="showDateChoosePicker = false"
                        @confirm="onConfirm"
                    />
                </van-popup>
            </van-col>
        </van-row>
        <van-divider></van-divider>
        <van-row class="bp-detail-row">
            <van-col class="bp-detail-col1" span="7">{{$t('bookingPage.bookingDetail.startTimeTitle')}}</van-col>
            <van-col class="bp-detail-col2" span="7">{{res_start_time}}</van-col>
            <van-col class="bp-detail-col3" span="8">
                <van-icon size="medium" name="clock-o" @click="show_start_time_choose_picker=true"></van-icon>
                <van-popup v-model="show_start_time_choose_picker" round position="bottom">
                    <van-picker
                        show-toolbar
                        :columns="start_time_options"
                        @cancel="show_start_time_choose_picker = false"
                        @confirm="onConfirmStartTime"
                    />
                </van-popup>
            </van-col>
        </van-row>
        <van-divider></van-divider>
    </div>
</template>

<script>
import moment from 'moment'
import room from '@/api/room'
export default {
    name: "BpDetail",
    data() {
        return {
            close_time: 22,
            res_day: moment().format("YYYY/MM/DD"),
            
            dates: [moment().format('MM/DD')+" 今天", moment().add(1, 'days').format('MM/DD')+" 明天"],
            
            showDateChoosePicker: false,
            show_start_time_choose_picker: false,
            
        }
    },
    computed: {
        // van-picker绑定值
        start_time_options() {
            var time_now = parseInt(moment().format("HH"))
            var list = [this.$t('bookingPage.bookingDetail.now')]
            for(var i = time_now + 1; i < this.close_time; i++) {
                list.push(i)
            }
            return list
        },
        // 当前时间框 显示值 经过处理后的 为string
        res_start_time() {
            if (this.$store.state.startTime === parseInt(moment().format("HH"))) {
                return this.$t('bookingPage.bookingDetail.now')
            } else {
                return this.$store.state.startTime + ":00"
            }
        },
    },
    methods: {
        onConfirm(value, index) {
            console.log(value)
            console.log(index)
            if (index === 1) {
                this.res_day = moment().add(1, 'days').format("YYYY/MM/DD")
            }
            this.showDateChoosePicker = false
        },
        // 确定开始时间
        onConfirmStartTime(value, index) {
            if (index === 0) {
                this.res_start_time_temp = parseInt(moment().format("HH"))
            } else {
                this.res_start_time_temp = this.start_time_options[index]
            }
            this.show_start_time_choose_picker = false
            // 将 确定的 开始时间 存放在vuex中
            this.$store.dispatch('updateStartTime', this.res_start_time_temp)
            room.getSeatStatus({
                room_id: this.$store.state.room.room_id,
                time_start: this.res_start_time_temp
            }).then(
                res => {
                    this.$store.dispatch('updateSeatStatus', res.data.data)
                }
            )
        },
    }
}
</script>

<style lang="less" scoped>
.bp-detail-row {
    height: 40px;
}
.bp-detail-col1 {
    text-align: left;
    line-height: 40px;
    height: 40px;
    margin-left: 10px;
}
.bp-detail-col2 {
    text-align: left;
    line-height: 40px;
    height: 40px;
    margin-left: 20px;
}
.bp-detail-col3 {
    text-align: right;
    line-height: 40px;
    height: 40px;
}
/deep/ .van-divider {
    margin: 0px 0;
    border-color: black;
}
/deep/ .van-icon {
    margin-right: 10%;
}
</style>