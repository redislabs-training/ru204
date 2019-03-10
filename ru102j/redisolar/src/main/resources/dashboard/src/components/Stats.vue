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
    this.createChart()
    this.getData(this)
  },
  methods: {
    getData (self) {
      axios.get('http://localhost:8081/api/metrics/99')
        .then(function (response) {
          self.chart.data.datasets.push({
            label: 'kWH Generated',
            borderColor: 'rgb(66, 134, 234)',
            data: response.data.map(function (point) {
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
