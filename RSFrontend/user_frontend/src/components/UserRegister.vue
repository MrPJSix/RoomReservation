<template>
  <div>
    <van-nav-bar
      :title="$t('registerPage.title')"
      left-arrow
      @click-left="onClickLeft"
    >
    </van-nav-bar>
    <van-form ref="RegisterFormRef" :model="RegisterForm" @submit="onSubmit">
      <van-field
        v-model="RegisterForm.user_id"
        :label="$t('registerPage.id')"
        :placeholder="$t('registerPage.id')"
        :rules="[{ required: true, message: $t('registerPage.idMessage') }]"
      />
      <van-field
        v-model="RegisterForm.user_name"
        type="text"
        :label="$t('registerPage.username')"
        :placeholder="$t('registerPage.username')"
        :rules="[{ required: true, message: $t('registerPage.usernameMessage') }]"
      />
      <van-field
        v-model="RegisterForm.email"
        type="email"
        :label="$t('registerPage.email')"
        :placeholder="$t('registerPage.emailPlaceholder')"
        :rules="[
          { required: true, message: $t('registerPage.emailMessage') },
        ]"
        
      />
      <van-field
        v-model="RegisterForm.password"
        type="password"
        :label="$t('registerPage.password')"
        :placeholder="$t('registerPage.password')"
        :rules="[{ required: true, message: $t('registerPage.passwordMessage') }]"
      />
      <div style="margin: 16px;">
        <van-button round block type="info" native-type="submit">{{$t('registerPage.submit')}}</van-button>
      </div>
    </van-form>
  </div>
</template>

<script>
import user from '@/api/user'
import { Notify } from 'vant'
export default {
  data(){
    return {
      RegisterForm: {
        user_id: "",
        user_name: "",
        email: "",
        password: "",
      },
    }
  },
  methods: {
    onSubmit() {
      user.register({
        user_id: this.RegisterForm.user_id,
        user_name: this.RegisterForm.user_name,
        password: this.RegisterForm.password,
        email: this.RegisterForm.email
      }).then(
        res => {
          if(res.data.success == true) {
            Notify({ type: 'success', message: '注册成功！' });
            this.$router.push("/login")
          } else {
            Notify({ type: 'danger', message: '注册失败！' });
          }
        }
      )
    },
    onClickLeft() {
      this.$router.push("/login")
    }
  }
}
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