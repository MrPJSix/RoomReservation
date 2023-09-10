<template>
  <div class="profile-head">
    <div class="profile-head-icon">
      <img height="80px" src="../../../assets/1.png" />
    </div>
    <div class="profile-head-name">{{ name }} {{ id }}</div>
    <div class="profile-head-email">
      {{ email }}
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileHead",
  data() {
    return {
      name: this.$store.state.userData.user_name,
      id: this.$store.state.userData.user_id,
      email: this.$store.state.userData.email,
    };
  },
};
</script>

<style>
.profile-head {
  position: fixed;
  height: 15%;
  width: 100%;
  background-color: rgb(87, 183, 235);
}
.profile-head-icon {
  position: fixed;
  top: 10%;
  left: 5%;
}
.profile-head-name {
  /* background-color: rgb(2, 22, 22); */
  position: fixed;
  top: 11.5%;
  left: 30%;
  font-size: 16px;
  color: white;
}
.profile-head-email {
  /* background-color: rgb(150, 150, 214); */
  position: fixed;
  font-size: 16px;
  top: 15%;
  left: 30%;
  color: white;
}
</style>