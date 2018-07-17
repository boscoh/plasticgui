<template>
  <v-toolbar dense
             dark
             color="indigo">
    <v-avatar :tile=true
              :size=24
              color="indigo">
      <img src="/static/logo.png" />
    </v-avatar>
    <v-toolbar-title style="cursor: pointer;"
                     @click="home()">
      {{ title }}
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-tabs dark
            color="indigo">
      <v-tab id="tab-home"
             to="/"
             router>Home
      </v-tab>
      <v-tab v-show="user.authenticated"
             id="tab-search"
             to="/private"
             router>Private
      </v-tab>
      <v-tab id="tab-about"
             to="/about"
             router>About
      </v-tab>
    </v-tabs>
    <v-spacer></v-spacer>
    <div v-if="isUser">
      <v-menu bottom
              left
              open-on-hover
              v-if="user.authenticated">
        <v-btn slot="activator"
               color="indigo">
          {{user.name}}
          <v-icon>arrow_drop_down</v-icon>
        </v-btn>
        <v-list>
          <v-list-tile @click="editUser">
            <v-list-tile-title>Edit User</v-list-tile-title>
          </v-list-tile>
          <v-list-tile @click="logout">
            <v-list-tile-title>Logout</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <v-btn v-else
             dark
             color="indigo"
             to='/login'>
        Login
      </v-btn>
    </div>
  </v-toolbar>
</template>

<script>
import auth from '../modules/auth'
import config from '../config'

export default {
  name: 'navbar',
  data () {
    return {
      title: config.title,
      isUser: config.isUser
    }
  },
  computed: {
    user: function () {
      return this.$store.state.user
    }
  },
  methods: {
    editUser () {
      this.$router.push('/edit-user')
    },
    home () {
      this.$router.push('/')
    },
    async logout () {
      await auth.logout()
      this.$router.push('/login')
    }
  }
}
</script>
<style scoped>
@font-face {
  font-family: Clip;
  src: url("/static/assets/Clip.ttf");
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
.tabs {
  width: 50%;
}
</style>
