<template>
  <nav id="main" class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
    <a class="navbar-brand" href="#">RediSolar</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link class="nav-link" to="/map">Map</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/stats">Stats</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/leaderboard">Leaderboard</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/live">Live</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/maintenance">Maintenance</router-link>
        </li>
      </ul>
    </div>
  </div>
  </nav>
</template>

<script>
</script>

<style scoped>
#main {
}
</style>
