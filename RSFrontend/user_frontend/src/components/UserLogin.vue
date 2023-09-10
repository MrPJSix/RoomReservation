<template>
  <div>
    <van-nav-bar
      :title="$t('loginPage.title')"
    >
      <template #right>
        <van-icon name="exchange" size="18" @click="translate" />
      </template>
    </van-nav-bar>
    <van-form @submit="onSubmit" ref="form">
      <van-field
        v-model="user_id"
        :label="$t('loginPage.id')"
        :placeholder="$t('loginPage.id')"
        :rules="[{ required: true, message: $t('loginPage.idMessage') }]"
      />
      <van-field
        v-model="password"
        type="password"
        :label="$t('loginPage.password')"
        :placeholder="$t('loginPage.password')"
        :rules="[{ required: true, message: $t('loginPage.passwordMessage') }]"
      />
      <div style="margin: 16px">
        <van-button round block type="info" native-type="submit">{{
          $t('loginPage.login')
        }}</van-button>
      </div>
    </van-form>
    <div style="margin: 16px">
      <van-button round block type="primary" to="/register">{{
        $t('loginPage.register')
      }}</van-button>
    </div>
  </div>
</template>

<script>
import user from "@/api/user";
import { Notify } from 'vant';
export default {
  data() {
    return {
      user_id: "",
      password: "",
    };
  },
  methods: {
    onSubmit(values) {
      console.log("submit", values);
      user
        .login({ user_id: this.user_id, password: this.password })
        .then((res) => {
          if (res.data.success == true) {
            Notify({type: 'success', message: '登陆成功！' })
            this.$store.dispatch("addUser", res.data.data);
            // user.getInvalidReservations({user_id: this.user_id}).then(
            //   res => {
            //     this.$store.dispatch("addInvalidReservation", res.data)
            //   }
            // )
            user.getInvalidReservations({ user_id: this.user_id });
            this.$router.push("/campus");
          } else {
            Notify({ type: 'danger', message: '登陆失败！' });
          }
        });
    },
    translate() {
      this.$i18n.locale = (this.$i18n.locale === 'zh' ? 'en' : 'zh')
      this.$refs.form.resetValidation()
      sessionStorage.setItem("lang", this.$i18n.locale)
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
