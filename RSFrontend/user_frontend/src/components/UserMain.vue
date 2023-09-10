<template>
    <div>
        <div>
            <router-view/>
        </div>
        <main-tab-bar/>
    </div>
</template>

<script>
import MainTabBar from './MainTabBar/MainTabBar.vue'
export default {
    components: {
        MainTabBar
    }
}
</script>

<style>

</style>