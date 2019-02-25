<template>
  <v-container>
    <v-flex
      xs8
      offset-xs2
      md4
      offset-md4
      lg4
      offset-lg4>
      <v-card class="mt-5">

        <v-card-title
          primary-title
          class="headline">
          Forgot your password to {{ title }}?
        </v-card-title>

        <v-card-text>
          <form
            novalidate
            @submit.prevent="submit">

            <v-text-field
              v-validate="'email'"
              v-model="user.email"
              :error-messages="errors.collect('email')"
              label="E-mail address"
              data-vv-name="email"></v-text-field>

            <v-btn
              type="submit"
              class="v-accent">Send password reset email</v-btn>

            <v-progress-linear
              v-if="isSending"
              :indeterminate="true">
            </v-progress-linear>

            <div
              v-if="error"
              style="color: red">
              {{ error }}
            </div>

            <div style="margin-top: 3em">
              New to {{ title }}? &nbsp;
              <router-link to="/register">Register</router-link>
            </div>

          </form>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-container>
</template>

<script>
import auth from '../../modules/auth'
import config from '../../config'

export default {
  data() {
    return {
      title: config.title,
      passwordHidden: true,
      rawPassword: '',
      error: '',
      isSending: false
    }
  },
  computed: {
    user: {
      get() {
        return this.$store.state.user
      },
      set(u) {
        this.$store.commit('setUser', u)
      }
    }
  },
  methods: {
    async submit() {
      let payload = this.user.email
      console.log('> ForgotPassword.submit', payload)
      this.isSending = true
      this.error = ''
      let response = await auth.forgotPassword(payload)
      console.log('> ForgotPassword.submit response', response)
      this.isSending = false

      if (response.result) {
        this.$router.push('/')
      } else {
        this.error = response.error.message
      }
    }
  }
}
</script>
