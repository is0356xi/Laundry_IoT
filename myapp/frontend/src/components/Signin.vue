<template>
  <v-card width="400px" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">ログイン</h1>
    </v-card-title>
    <v-card-text>
      <v-form @submit.prevent="signin">
        <v-text-field prepend-icon="mdi-account-circle" label="メールアドレス" :value="userData.mail"/>
        <v-text-field v-bind:type="showPassword ? 'text' : 'password'" prepend-icon="mdi-lock" v-bind:append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" label="パスワード" @click:append="showPassword = !showPassword" :value="userData.password"/>
        <v-card-actions>
          <v-btn type="submit">ログイン</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
// const axios = require('axios').create()
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
      console.log(this.userData.mail);
      console.log(this.userData.password);
      /*await axios.post('/api/reserve', this.timeData)
      .then(response => {
          this.results = response.data;
          //   this.seen = true;
          console.log(this.results)
        })
      .catch(error => {
          console.log(error);
      })*/
    }
  }
};
</script>