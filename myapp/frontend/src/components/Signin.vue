<template>
<v-row justify="center">
  <v-card width="400px" class="mx-auto mt-5" justify="center" >
    <v-card-title>
      <h1 class="display-1">ログイン</h1>
    </v-card-title>
    <v-card-text>
      <v-form @submit.prevent="signin">
        <v-text-field prepend-icon="mdi-email" label="メールアドレス" v-model="userData.mail"/>
        <v-text-field v-bind:type="showPassword ? 'text' : 'password'" prepend-icon="mdi-lock" v-bind:append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" label="パスワード" @click:append="showPassword = !showPassword" v-model="userData.password"/>
        <v-card-actions>
          <v-btn type="submit">ログイン</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
    <v-card-text>
      <v-col class="text-right">
        <v-btn elevation="2" href="/signup">新規登録</v-btn>
      </v-col>
    </v-card-text>
  </v-card>
</v-row>
</template>

<script>
const axios = require('axios').create()
export default {
  name: 'Signin',
  data () {
      return{
        showPassword : false,
        userData: {
            mail: "",
            password: ""
        }
      }
  },
  methods: {
    async signin() {
      await axios.post('/api/signin', this.userData)
      .then(response => {
          const results = response.data;
          if (results.status_code == '201') {
            this.$router.push('/')
          } else {
            this.$toasted.error(`ログインに失敗しました。(${results.message})`);
          }
        })
      .catch(error => {
          console.log(error);
      })
    }
  }
};
</script>