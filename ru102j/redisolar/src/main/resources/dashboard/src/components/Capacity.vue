<style>

</style>

<template>

<div id="app">
    <div class="container">
        <canvas id="myChart"></canvas>
    </div>
    <div class="container">
      <table class="table">
        <thead>
          <tr>
            <td scope="col">ID</td>
            <td scope="col">Capacity</td>
          </tr>
        </thead>
        <tr v-for="item in capacityTable" :key="item.siteId">
          <td><router-link :to="{ name: 'stats', params: { id: item.siteId }}">{{ item.siteId }}</router-link></td>
          <td>{{ item.capacity }}</td>
        </tr>
      </table>
    </div>
</div>

</template>

<script>

import axios from 'axios'
import Chart from 'chart.js'
export default {
  name: 'Chart',
  data: function () {
    return {
      capacityTable: []
    }
  },
  mounted () {
    this.resetColor()
    this.createChart()
    this.getData(this)
  },
  watch: {
    $route (to, from) {
      this.clearChartData(this)
      this.resetColor()
      this.getData(this)
    }
  },
  methods: {
    resetColor () {
      this.currentColor = {
        r: 66,
        g: 134,
        b: 234
      }
    },
    cycleRGBColor (color) {
      if (color + 20 <= 255) {
        return color + 20
      } else {
        return 20 + (255 - color)
      }
    },
    getBorderColor () {
      this.currentColor.r = this.cycleRGBColor(this.currentColor.r)
      this.currentColor.g = this.cycleRGBColor(this.currentColor.g)
      this.currentColor.b = this.cycleRGBColor(this.currentColor.b)
      return 'rgb(' + this.currentColor.r + ', ' + this.currentColor.g +
        ', ' + this.currentColor.b + ')'
    },
    clearChartData (self) {
      self.chart.data.datasets = []
      self.chart.update()
    },
    getData (self) {
      axios.get('http://localhost:8081/api/capacity/')
        .then(function (response) {
          console.log(response)
          var items = []
          var ids = []
          response.data.highestCapacity.forEach(function (item) {
            items.push({x: item.siteId, y: item.capacity})
            ids.push('' + item.siteId)
            self.capacityTable.push(item)
          })
          console.log(items)
          self.chart.data.labels = ids
          self.chart.data.datasets.push({
            labels: ids,
            backgroundColor: '#94c635',
            borderColor: '#709628',
            borderWidth: 1,
            data: items
          })
          self.chart.update()
        })
        .catch(function (error) {
          console.log('Got error')
          console.log(error)
        })
    },
    createChart () {
      var ctx = document.getElementById('myChart').getContext('2d')
      this.chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'bar',

        // The data for our dataset
        data: {
          datasets: []
        },

        // Configuration options go here
        options: {
          legend: {display: false},
          title: {
            display: true,
            text: 'Top 10 Capacity'
          },
          scales: {
            xAxes: [{
              labelString: 'Site ID',
              barPercentage: 10,
              maxBarThickness: 60,
              minBarLength: 2,
              gridLines: {
                offsetGridLines: true
              },
              scaleLabel: {labelString: 'Site ID', display: true}
            }],
            yAxes: [{scaleLabel: {labelString: 'Watt-Hours', display: true}}]
          }
        }
      })
    }
  }
}

</script>
