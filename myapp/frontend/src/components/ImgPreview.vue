<template>
    <!-- <div>
    <v-img
        lazy-src="../../public/static/img/wait.png"
        max-height="200"
        max-width="250"
        src="../../public/static/img/test.jpg">

    </v-img>
    <v-btn v-on:click="ImgUpdate">更新</v-btn>
    </div> -->
    <div class="gallery">
    <v-row>
    <v-col
      v-for="n in 9"
      :key="n"
      class="d-flex child-flex"
      cols="4"
    >
      <v-img
        :src="`/static/img/gallery/test${n}.jpg`"
        :lazy-src="random_m(n)"
        aspect-ratio="1"
        max-height="200"
        max-width="250"
        class="grey lighten-2"
      >
        <template v-slot:placeholder>
          <v-row
            class="fill-height ma-0"
            align="center"
            justify="center"
          >
            <v-progress-circular
              indeterminate
              color="grey lighten-5"
            ></v-progress-circular>
          </v-row>
        </template>
      </v-img>
    </v-col>
  </v-row>
  <v-btn v-on:click="ImgUpdate">更新</v-btn>
  </div>
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
      },
      random_m(n) {
          var random_num = Math.floor( Math.random() * 6 );
          var filename = `/static/img/wait/wait${Math.abs(n-random_num)}.png`
          return filename
      }
  },
  computed:{
      random_c: function() {
          var random_num = Math.floor( Math.random() * 6 );
          var filename = `/static/img/wait/wait${random_num}.png`
          return filename
      }
  }
}
</script>

<style scoped>
.gallery{
  width: 800px;
  margin: auto;
}
</style>