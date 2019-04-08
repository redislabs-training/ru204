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
                        <option value="2">M (Miles)</option>
                        <option value="3">FT (Feet)</option>
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
                    ', ' + site.state + ' ' + site.postalCode + '<br>' +
                    '<a href="#/stats/' + site.id + '">Stats</a>')
    },
    createMap () {
      this.mymap = L.map('mapid').setView([37.715732, -122.027342], 11)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?',
        { attribution: 'Map and Image data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors. <a href="https://www.openstreetmap.org/copyright">License</a>.' }
      ).addTo(this.mymap)
    }
  }
}

</script>
