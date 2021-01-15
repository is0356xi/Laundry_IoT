<template>
    <p v-if="flag">予約されているよ</p>
    <p v-else>予約は無いよ</p>
</template>



<script>
const axios = require('axios').create()
export default {
  name: 'ResvView',
  data() {
      return{
          flag: true
      }
  },
  created: function () {
    setInterval(() => {
      this.Check()
    }, 5000)
  },
  methods:{
      async Check(){
          await axios.get('/api/check')
          .then(response => {
              this.flag = response.data;
              console.log(response.data)
          })
          .catch(error => {
              console.log(error);
          })
      }
    }
}
</script>