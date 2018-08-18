import Vue from 'vue'
import Router from 'vue-router'

import Home from './components/tabs/Home'
import About from './components/tabs/About'
import Private from './components/tabs/Private'
import Login from './components/user/Login'
import Register from './components/user/Register'
import EditUser from './components/user/EditUser'
import AdminUsers from './components/user/AdminUsers'
import ForgotPassword from './components/user/ForgotPassword'
import ResetPassword from './components/user/ResetPassword'

Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
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
  ]
})

export default router
