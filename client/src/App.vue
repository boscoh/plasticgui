<template>
  <div id="app">
    <v-app>
      <navbar></navbar>
      <div
        style="
          margin-top: 10px;
          height: calc(100vh - 58px);
          overflow: auto">
        <router-view></router-view>
      </div>
    </v-app>
  </div>
</template>

<style>
@import 'vuetify/dist/vuetify.min.css';
@import 'http://fonts.googleapis.com/css?family=Roboto:300,400,500,700,400italic';
@import 'http://fonts.googleapis.com/icon?family=Material+Icons';
</style>

<script>
import Navbar from './components/Navbar.vue'
export default {
  name: 'App',
  components: { Navbar }
}
</script>
