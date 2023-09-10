<template>
  <div class="proflie-other">
    <van-cell
      class="cell-other"
      :title="$t('userPage.help')"
      is-link
      to="index"
      icon="question-o"
    />
    <van-cell
      class="cell-other"
      :title="$t('userPage.questions')"
      is-link
      to="index"
      icon="more-o"
    />
    <van-cell
      class="cell-other"
      :title="$t('userPage.feedback')"
      is-link
      to="index"
      icon="chat-o"
    />
    <van-cell
      class="cell-other"
      :title="$t('userPage.nowLang')"
      center
      :label="nowLang"
    >
      <template #right-icon>
        <van-icon name="exchange" size="16px" class="exchange-icon" @click="translate"/>
      </template>
    </van-cell>
  </div>
</template>

<script>
export default {
  name: "ProfileOther",
    methods: {
    translate() {
      this.$i18n.locale = this.$i18n.locale === "zh" ? "en" : "zh";
      sessionStorage.setItem("lang", this.$i18n.locale);
    },
  },
  computed: {
    nowLang() {
      return this.$i18n.locale === "zh" ? "简体中文" : "English"
    }
  }
};
</script>

<style>
.proflie-other {
  position: fixed;
  width: 100%;
  top: 44%;
}
.cell-other {
  text-align: left;
}
.exchange-icon {
  height: 24px;
  top: 4px;
}
</style>