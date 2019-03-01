<template>
  <v-container>
    <v-layout
      justify-center
      row
    >
      <v-flex
        xs8
        md4
        lg4
      >
        <v-card class="mt-5">
          <v-card-title
            primary-title
            class="headline"
          >
            {{ title }}
          </v-card-title>

          <v-card-text>
            <form
              novalidate
              class="login-screen"
              @submit.prevent="submit"
            >
              <v-text-field
                v-model="name"
                v-validate="'required'"
                :error-messages="errors.collect('name')"
                label="User name"
                data-vv-name="name"
              ></v-text-field>

              <v-text-field
                v-model="email"
                v-validate="'email'"
                :error-messages="errors.collect('email')"
                label="E-mail address"
                data-vv-name="email"
              ></v-text-field>

              <v-text-field
                v-model="rawPassword"
                v-validate="'required|min:6'"
                :append-icon="passwordHidden ? 'visibility' : 'visibility_off'"
                :append-icon-cb="() => (passwordHidden = !passwordHidden)"
                :type="passwordHidden ? 'password' : 'text'"
                :error-messages="errors.collect('Password')"
                hint="At least 6 characters"
                counter
                label="New Password"
                data-vv-name="Password"
              ></v-text-field>

              <v-text-field
                v-model="rawConfirmPassword"
                v-validate="'required|confirmed:Password'"
                :append-icon="
                  confirmPasswordHidden ? 'visibility' : 'visibility_off'
                "
                :append-icon-cb="
                  () => (confirmPasswordHidden = !confirmPasswordHidden)
                "
                :type="confirmPasswordHidden ? 'password' : 'text'"
                :error-messages="errors.collect('Confirm_Password')"
                hint="At least 6 characters"
                counter
                label="Confirm New Password"
                data-vv-name="Confirm_Password"
              ></v-text-field>

              <v-btn
                type="submit"
                class="v-accent"
              >
                Save
              </v-btn>

              <div
                v-if="error"
                style="color: red"
              >
                {{ error }}
              </div>
            </form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import auth from '../../modules/auth'
import _ from 'lodash'

export default {
  data () {
    let result = {}
    _.assign(result, this.$store.state.user)
    _.assign(result, {
      title: 'Edit Your Details',
      rawPassword: '',
      passwordHidden: true,
      rawConfirmPassword: '',
      confirmPasswordHidden: true,
      error: ''
    })
    return result
  },
  methods: {
    async submit () {
      this.error = ''

      let payload = {}
      const keys = ['id', 'name', 'email', 'rawPassword', 'rawPasswordConfirm']
      for (let key of keys) {
        if (this.$data[key]) {
          payload[key] = this.$data[key]
        }
      }

      let response = await auth.update(payload)
      if (response.result) {
        this.error = 'User updated'
      } else {
        console.log('> EditUser.submit fail', response)
        this.error = response.error.message
      }
    }
  }
}
</script>
