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

<template>

<div id="app">
    <div class="container">
        <form id="search" @submit.prevent="onSubmit">
            <div class="form-row m-1">
                <div class="col px-1">
                    <input id="search_address" name="address" type="text" class="form-control" placeholder="Address (e.g., 1452 55th Avenue B
  Oakland, CA)">
                </div>
                <div class="col2 px-1">
                    <input name="radius" type="text" class="form-control" placeholder="Radius">
                </div>
                <div class="col2 px-1">
                    <select class="custom-select">
                        <option selected>Units (e.g, KM, M, FT)</option>
                        <option value="1">KM (Kilometers)</option>
                        <option value="2">Two</option>
                        <option value="3">Three</option>
                    </select>
                </div>
                <div class="col2 px-1">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
            </div>
        </form>
    </div>
    <div class="container" id="mapid"></div>
</div>

</template>

<script>
import {
  L, LMap, LTileLayer, LMarker
}
  from 'vue2-leaflet'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  mounted () {
    this.submitForm()
    this.createMap()
    this.getData(this)
  },
  methods: {
    submitForm () {},
    getData (self) {
      axios.get('http://localhost:8081/api/sites')
        .then(function (response) {
          response.data.forEach(function (site) {
            self.addMarker(site)
          })
        })
        .catch(function (error) {
          console.log(error)
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
