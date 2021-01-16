<template>
<v-row justify="center">
  <v-card width="400px" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">新規登録</h1>
    </v-card-title>
    <v-card-text>
      <v-form @submit.prevent="signup">
        <v-text-field prepend-icon="mdi-email" label="メールアドレス" v-model="userData.mail"/>
        <v-text-field v-bind:type="showPassword ? 'text' : 'password'" prepend-icon="mdi-lock" v-bind:append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" label="パスワード" @click:append="showPassword = !showPassword" v-model="userData.password"/>
        <v-text-field prepend-icon="mdi-account-circle" label="ユーザ名" v-model="userData.name"/>
        <v-card-actions>
          <v-btn type="submit">登録</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</v-row>
</template>

<script>
const axios = require('axios').create()
export default {
  name: 'Signup',
  data () {
      return{
        showPassword : false,
        userData: {
            mail: "",
            password: "",
            name: "",
        }
      }
  },
  methods: {
    async signup() {
      await axios.post('/api/signup', this.userData)
      .then(response => {
          const results = response.data;
          if (results.status_code == '201') {
            this.$router.push('/')
          } else {
            this.$toasted.error(`登録に失敗しました。(${results.message})`);
          }
        })
      .catch(error => {
          console.log(error);
      })
    }
  }
};
</script>
