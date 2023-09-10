<template>
  <div>
    <van-nav-bar
      :title="$t('campusPage.title')"
      left-arrow
      @click-left="onClickLeft"
    >
      <template #right>
        <van-icon name="replay" size="18" @click="refresh" />
      </template>
    </van-nav-bar>
    <div id="campus-page">
      <van-cell
        v-for="c in campus"
        :key="c.campus_id"
        :title="c.campus_name"
        is-link
        to="building"
        @click="click(c)"
      />
    </div>
  </div>
</template>

<script>
import campus from "@/api/campus";
import { Notify } from 'vant';
export default {
  name: "CampusPage",
  data() {
    return {
      campus: [],
    };
  },
  created() {
    campus.getAllCampus().then((res) => {
      this.campus = res.data.data;
      if (this.$i18n.locale === "en") {
        for (let i = 0; i < this.campus.length; i++) {
          if (this.campus[i].campus_name == "邯郸校区")
            this.campus[i].campus_name += " (HanDan Campus)";
          if (this.campus[i].campus_name == "枫林校区")
            this.campus[i].campus_name += " (FengLin Campus)";
          if (this.campus[i].campus_name == "江湾校区")
            this.campus[i].campus_name += " (JiangWan Campus)";
          if (this.campus[i].campus_name == "张江校区")
            this.campus[i].campus_name += " (ZhangJiang Campus)";
        }
      }
    });
  },
  methods: {
    click(c) {
      console.log(c);
      this.$store.dispatch("addCampus", c)
    },
    onClickLeft() {
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