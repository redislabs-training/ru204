<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">RediSolar</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <a class="nav-link" href="#">Map <span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Usage</a>
        </li>
      </ul>
    </div>
    </nav>
    <div class="container" id="mapid"></div>
   <br />
   <div class="container">
     <canvas id="myChart" width="400" height="400"></canvas>
   </div>
  </div>
</template>

<script>
import Chart from 'chart.js'
import {L, LMap, LTileLayer, LMarker} from 'vue2-leaflet'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  mounted () {
    this.createMap()
    this.getData(this)
  },
  methods: {
    getData (self) {
       axios.get('http://localhost:8081/api/sites')
       .then(function (response) {
          response.data.forEach(function(site) {
            self.addMarker(site)
          })
       })
       .catch(function (error) {
         console.log(error);
       })
    },
    addMarker (site) {
      var coordinate = site.coordinate
      var marker = L.marker([coordinate.lat, coordinate.lng]).addTo(this.mymap)
      marker.bindPopup('<b>' + site.address + '</b><br/>' + site.city +
        ', ' + site.state + ' ' + site.postalCode + '<br>')
    },
    createMap () {
      this.mymap = L.map('mapid').setView([37.715732, -122.027342], 11)
      L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia2JyZWRpcyIsImEiOiJjanMxeXZ1bTExemlyNDNvZDc2N2JyY20wIn0.onntwgLbKiGP9-rgZdssNA', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'your.mapbox.access.token'
      }).addTo(this.mymap)
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#mapid {
  height: 900px;
}
</style>
