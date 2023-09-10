<template>
  <div class="condition-search">
    <div>
        <van-search class="search-box" v-model="searchValue" placeholder="请输入搜索关键词" />
    </div>
    <div class="condition-search-menu">
        <van-dropdown-menu overlay class="test">
            <van-dropdown-item v-model="type" :options="types" />
            <van-dropdown-item v-model="is_all_night" :options="is_all_night_choices" />
        </van-dropdown-menu>
    </div>
  </div>
</template>

<script>
export default {
    name: "ConditionSearch",
    components: {
        
    },
    data() {
        return {
            searchValue: "",
            type: 0,
            is_all_night: 0,
            types: [
                { text: '所有类型', value: 0},
                { text: '图书馆', value: 1},
                { text: '教室', value: 2},
                { text: '其他', value: 3},
            ],
            is_all_night_choices: [
                { text: "通宵与否都可", value: 0},
                { text: "非通宵",value: 1},
                { text: "通宵", value: 2},
            ]
        }
    }
}
</script>

<style>
.condition-search {
    position: relative;
    height: 13%;
    width: 100%;
    background-color: bisque;
}
.serach-box {
    position: absolute;
    top: 0%;
}
.test {
    overflow: auto;
    position: relative;
}

</style>