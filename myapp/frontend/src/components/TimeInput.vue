<template>
  <div>
    <vue-ctk-date-time-picker 
        label="日時を選択" 
        v-model="timeData.time" 
        formatted="MM月DD日 HH時mm分" format="YYYY-MM-DD HH:mm"
        minute-interval="5">
    </vue-ctk-date-time-picker>

    <v-form @submit.prevent="reserve">
        <!-- <v-input type="text" name="" :value="timeData.time"> -->
        <v-btn type="submit">予約する</v-btn>
        <!-- <button type="cancel">予約のキャンセル</button> -->
    </v-form>

    <v-btn v-on:click="cancel">予約のキャンセル</v-btn>

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