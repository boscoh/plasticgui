import Vue from 'vue'
import Router from 'vue-router'

import config from './config.js'

import Home from './components/Home'

import About from './components/tabs/About'
import Private from './components/tabs/Private'

import Login from './components/user/Login'
import Register from './components/user/Register'
import EditUser from './components/user/EditUser'
import AdminUsers from './components/user/AdminUsers'
import ForgotPassword from './components/user/ForgotPassword'
import ResetPassword from './components/user/ResetPassword'

Vue.use(Router)
let routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    name: 'about',
    component: About
  }
]

if (config.isUser) {
  routes = routes.concat([
    {
      path: '/private',
      name: 'private',
      component: Private
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/edit-user',
      name: 'editUser',
      component: EditUser
    },
    {
      path: '/admin-users',
      name: 'adminUsers',
      component: AdminUsers
    },
    {
      path: '/forgot-password',
      name: 'forgotPassword',
      component: ForgotPassword
    },
    {
      path: '/reset-password/:tokenId',
      name: 'resetPassword',
      component: ResetPassword
    }
  ])
}

let router = new Router({ routes })

export default router
