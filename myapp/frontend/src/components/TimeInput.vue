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
        <v-btn color="red" class="ma-2" type="submit">
          予約する
          <v-icon right>
          mdi-checkbox-marked-circle
        </v-icon></v-btn>
      </v-form>
      <v-btn class="ma-2" dark v-on:click="cancel">
        <v-icon dark left>mdi-minus-circle</v-icon>
        キャンセル</v-btn>

        <p v-if="flag">{{timeData.pref_time}}の予約があるよ</p>
        <p v-else>予約は無いよ</p>

    </div>
  </section>

</template>



<script>
const axios = require('axios').create()
export default {
  name: 'TimeInput',
  data() {
      return{
          timeData:{
            time : "",
            pref_time: ""
            },
            flag: true
      }
  },
  methods: {
    async reserve() {
      await axios.post('/api/reserve', this.timeData)
      .then(response => {
          this.results = response.data;
          //   this.seen = true;
        //   console.log(this.results)
        //   this.timeData.time = this.results.resv_time
          // 予約に成功したら予約フラグを反転

          if(this.results.resv_flag == true && this.flag == false){
            this.change_flag(this.results.resv_time)
          }else{
              this.timeData.pref_time = this.results.resv_time
          }
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
          this.change_flag("")
        })
      .catch(error => {
          console.log(error);
      })
    },
    change_flag(time){
        this.timeData.pref_time = time
        this.flag = !this.flag
        return this.flag
    }
  },
  created: async function check() {
          await axios.get('/api/check_resv')
          .then(response => {
              this.flag = response.data.resv_flag;
              this.timeData.pref_time = response.data.resv_time;
              console.log(response.data)
          })
          .catch(error => {
              console.log(error);
          })
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