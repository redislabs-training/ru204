<style>

</style>

<template>

<div id="app">
    <div class="container">
        <canvas id="myChart"></canvas>
    </div>
</div>

</template>

<script>

import axios from 'axios'
import Chart from 'chart.js'
export default {
  name: 'Chart',
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
      axios.get('http://localhost:8081/api/metrics/' + self.$route.params.id)
        .then(function (response) {
          response.data.forEach(function (plot) {
            self.chart.data.datasets.push({
              label: plot.name,
              borderColor: self.getBorderColor(),
              data: plot.measurements.map(function (point) {
                return {
                  t: new Date(point.dateTime[0],
                    point.dateTime[1] - 1,
                    point.dateTime[2],
                    point.dateTime[3],
                    point.dateTime[4]),
                  y: point.value
                }
              })
            })
            self.chart.update()
          })
        })
        .catch(function (error) {
          console.log('Got error')
          console.log(error)
        })
    },
    createChart () {
      var timeFormat = 'MM/DD/YYYY HH:mm'
      var ctx = document.getElementById('myChart').getContext('2d')
      this.chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
          datasets: []
        },

        // Configuration options go here
        options: {
          title: {
            text: 'Time Scale'
          },
          scales: {
            xAxes: [{
              type: 'time',
              time: {
                format: timeFormat,
                // round: 'day'
                tooltipFormat: 'll HH:mm'
              },
              scaleLabel: {
                display: true,
                labelString: 'Date'
              }
            }],
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'kWh'
              }
            }]
          }
        }
      })
    }
  }
}

</script>
