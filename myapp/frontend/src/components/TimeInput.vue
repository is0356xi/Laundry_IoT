<template>
  <div class="about">
    <vue-ctk-date-time-picker label="日時を選択" v-model="timeData.time" formatted="MM月DD日 HH時mm分" format="YYYY-MM-DD HH:mm"></vue-ctk-date-time-picker>

    <form @submit.prevent="submit">
        <input type="text" name="" :value="timeData.time">
        <button type="submit">予約する</button>
    </form>
</template>



<script>
const axios = require('axios').create()
export default {
  name: 'about',
  data() {
      return{
          timeData: {
              time: ""
          }
      }
  },
  methods: {
    async submit() {
      console.log(this.timeData);
      await axios.post('/api/reserve', this.timeData)
      .then(response => {
          this.results = response.data.results;
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