import Vue from 'vue'
import Router from 'vue-router'

import Map from '@/components/Map'
import Stats from '@/components/Stats'
import Maintenance from '@/components/Maintenance'
import Live from '@/components/Live'
import Leaderboard from '@/components/Leaderboard'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Map',
      component: Map
    },
    {
      path: '/map',
      name: 'Map',
      component: Map
    },
    {
      path: '/stats',
      name: 'stats',
      component: Stats
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: Leaderboard
    },
    {
      path: '/live',
      name: 'live',
      component: Live
    },
    {
      path: '/maintenance',
      name: 'Maintenance',
      component: Maintenance
    }
  ]
})
