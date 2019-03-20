<style>

</style>

<template>

<div id="app">
    <nav-bar></nav-bar>
    <router-view></router-view>
    <footer></footer>
</div>

</template>

<script>
/* eslint-disable */

import Map from './components/Map.vue'
import NavBar from './components/NavBar.vue'
import Stats from './components/Stats.vue'
import Foot from './components/Foot.vue'
export default {
    name: "app",
    components: {
        Map,
        NavBar,
        Stats,
        Foot
        // Leaderboard,
        // Live,
        // Maintenance
    }
}

</script>
