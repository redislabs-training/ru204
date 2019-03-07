<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view></router-view>
  </div>
</template>

<script>
  import Map from './components/Map.vue'
  import NavBar from './components/NavBar.vue'
  import Stats from './components/Stats.vue'
  export default {
    name: "app",
	  components: {
  	  Map,
      NavBar,
      Stats
      // Leaderboard,
      // Live,
      // Maintenance
	  }
}
</script>

<style>
</style>
