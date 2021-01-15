<template>

  <section class="reserve-form">
    <h3 class="left-style">
      洗濯機の予約
    </h3>
    <br>
    <div class="about">
      <vue-ctk-date-time-picker
          label="日時を選択"
          v-model="timeData.time"
          formatted="MM月DD日 HH時mm分" format="YYYY-MM-DD HH:mm"
          minute-interval="5">
      </vue-ctk-date-time-picker>




      <br>

      <v-form @submit.prevent="reserve">
        <!-- <v-input type="text" name="" :value="timeData.time"> -->
        <v-btn class="ma-2" red type="submit">
          予約する
          <v-icon right>
          mdi-checkbox-marked-circle
        </v-icon></v-btn>
        <!-- <button type="cancel">予約のキャンセル</button> -->

      </v-form>
      <v-btn v-on:click="cancel" class="ma-2" dark>
        <v-icon dark left>mdi-minus-circle</v-icon>
        キャンセル</v-btn>
    </div>
  </section>

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
  methods: {
    async reserve() {
      console.log(this.timeData);
      await axios.post('/api/reserve', this.timeData)
      .then(response => {
          this.results = response.data;
          //   this.seen = true;
          console.log(this.results)
        })
      .catch(error => {
          console.log(error);
      })
    },
    async cancel() {
      await axios.get('/api/cancel')
      .then(response => {
          this.results = response.data;
          //   this.seen = true;
          console.log(this.results)
        })
      .catch(error => {
          console.log(error);
      })
    }
  },
  props: {
    value: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
h3.left-style {
    border-left: 10px solid #0061ca;
    padding: 5px 0 0 10px;
    border-bottom: 0;
    text-align: left;
}
.reserve-form{
  margin-right: 0;
  width: 336px;
  float: left;
  margin-right: 20px;
}

</style>