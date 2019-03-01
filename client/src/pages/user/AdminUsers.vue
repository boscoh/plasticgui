<template>
  <v-container>
    <v-layout
      justify-center
      row
    >
      <v-flex
        xs6
        md4
        lg4
      >
        <h2
          class="display-2 pt-5 pb-4"
          style="text-align: center"
        >
          Admin - Users
        </h2>

        <v-card>
          <v-card-text>
            <v-list>
              <template v-for="(user, i) in users">
                <v-divider
                  v-if="i > 0"
                  :key="i"
                ></v-divider>
                <v-list-tile :key="i">
                  {{ user.name }}
                  <v-spacer></v-spacer>
                  {{ user.email }}
                  <v-btn
                    flat
                    icon
                    @click="deleteUser(user.id)"
                  >
                    <v-icon>
                      delete
                    </v-icon>
                  </v-btn>
                </v-list-tile>
              </template>
            </v-list>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import rpc from '../../modules/rpc'
import config from '../../config'

export default {
  data () {
    return {
      title: config.title,
      users: []
    }
  },
  async mounted () {
    let response = await rpc.rpcRun('adminGetUsers')
    console.log('AdminUsers.mounted', response)
    if (response.result) {
      console.log('> AdminUsers.mounted users', response.result.users)
      this.users = response.result.users
    }
  },
  methods: {
    async deleteUser (userId) {
      let response = await rpc.rpcRun('adminDeleteUser', userId)
      if (response.result) {
        console.log('> AdminUsers.deleteUser remaining', response.result.users)
        this.users = response.result.users
      }
    }
  }
}
</script>
