<template>
  <div>
    <van-nav-bar
      :title="$t('buildingPage.title')"
      left-arrow
      @click-left="onClickLeft"
    >
      <template #right>
        <van-icon name="replay" size="18" @click="refresh" />
      </template>
    </van-nav-bar>
    <div id="building-page">
      <van-cell
        v-for="building in buildings"
        :key="building.building_id"
        :title="building.building_name"
        is-link
        to="room"
        @click="click(building)"
      />
    </div>
  </div>
</template>

<script>
import campus from "@/api/campus";
import { Notify } from 'vant';
export default {
  name: "BuildingPage",
  data() {
    return {
      buildings: [],
    };
  },
  created() {
    campus
      .getBuildingsByCampus({ campus_id: this.$store.state.campus.campus_id })
      .then((res) => {
        this.buildings = res.data.data;
        if (this.$i18n.locale === "en") {
          for (let i = 0; i < this.buildings.length; i++) {
            if (this.buildings[i].building_name === "第一教学楼")
              this.buildings[i].building_name += " (No.1 Teaching Building)";
            if (this.buildings[i].building_name === "第二教学楼")
              this.buildings[i].building_name += " (No.2 Teaching Building)";
            if (this.buildings[i].building_name === "第三教学楼")
              this.buildings[i].building_name += " (No.3 Teaching Building)";
            if (this.buildings[i].building_name === "第四教学楼")
              this.buildings[i].building_name += " (No.4 Teaching Building)";
            if (this.buildings[i].building_name === "第五教学楼")
              this.buildings[i].building_name += " (No.5 Teaching Building)";
            if (this.buildings[i].building_name === "第六教学楼")
              this.buildings[i].building_name += " (No.6 Teaching Building)";
            if (this.buildings[i].building_name === "文科图书馆")
              this.buildings[i].building_name += " (Liberal Arts Library)";
            if (this.buildings[i].building_name === "理科图书馆")
              this.buildings[i].building_name += " (Science Library)";
            if (this.buildings[i].building_name === "光华楼")
              this.buildings[i].building_name += " (Guanghua Tower)";
            if (this.buildings[i].building_name === "A教学楼")
              this.buildings[i].building_name += " (A Teaching Building)";
            if (this.buildings[i].building_name === "智华楼")
              this.buildings[i].building_name += " (ZhiHua Building)";
            if (this.buildings[i].building_name === "1号教学楼")
              this.buildings[i].building_name += " (Academic Building 1)";
            if (this.buildings[i].building_name === "2号教学楼")
              this.buildings[i].building_name += " (Academic Building 2)";
            if (this.buildings[i].building_name === "李兆基图书馆")
              this.buildings[i].building_name += " (Lee Shau Kee Library)";
            if (this.buildings[i].building_name === "康泉图书馆")
              this.buildings[i].building_name += " (KangQuan Library)";
            if (this.buildings[i].building_name === "张江校区图书馆")
              this.buildings[i].building_name += " (ZhangJiang Campus Library)";
          }
        }
      });
  },
  methods: {
    click(building) {
      this.$store.dispatch("addBuilding", building);
    },
    onClickLeft() {
      this.$router.push('/campus')
    },
    refresh() {
      Notify({type: 'primary', message: '刷新...'})
    }
  },
};
</script>

<style lang="less" scoped>
.van-nav-bar {
  background-color: #409eff;
}
/deep/.van-nav-bar__title {
  max-width: 60%;
  margin: 0 auto;
  color: #fff;
  font-weight: 500;
  font-size: 16px;
}
/deep/.van-nav-bar .van-icon {
  color: #fff !important;
}
/deep/.van-nav-bar__text {
  color: #fff;
}
</style>