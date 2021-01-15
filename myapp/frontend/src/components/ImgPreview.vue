<template>
    <div>
    <v-img
        lazy-src="../../public/static/img/wait.png"
        max-height="500"
        max-width="500"
        src="../../public/static/img/test.jpg">
    </v-img>
    <v-btn v-on:click="ImgUpdate">更新</v-btn>
</template>



<script>
const axios = require('axios').create()
export default {
  name: 'TimeInput',
  data() {
      return{
          timeData: {
              time: ""
          }
      }
  },
//   mounted: async function() {
//       await axios.get('/api/img')
//       .then(response => {
//           this.results = response.data;
//           console.log(this.results)
//       })
//       .catch(error => {
//           console.log(error)
//       })
//   },
  methods:{
      async ImgUpdate(){
          await axios.get('/api/img')
          .then(response => {
              this.results = response.data;
              console.log(this.results);
          })
          .catch(error => {
              console.log(error);
          })
      }
  }
}
</script>