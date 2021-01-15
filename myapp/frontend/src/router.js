import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Signin from './components/Signin.vue'
import Signup from './components/Signup.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/signin',
      name: 'Signin',
      component: Signin
    },
    {
      path: '/signup',
      name: 'Signup',
      component: Signup
    },
  ]
})
