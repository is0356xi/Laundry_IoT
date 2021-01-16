<template>
  <section class="today-weather">
    <h3 class="left-style">
      {{tableData.today}}
    </h3>
    <div class="indexes-weather-wrap clearfix">
      <div class="clearfix">
        <div class="indexes-icon-box">
          <img :src="'/static/img/laundry/0'+ tableData.laundry_index + '.png'"
          width="60"
          height="60"
          />
          <span class="indexes-telop-0">{{tableData.laundry_telop}}</span>
        </div>
        <div class="weather-icon-box">
          <img
            :src="'/static/img/weatherIcon/' + tableData.weather + '.png'"
            width="47"
            heigt="30"
            />
          <span class="weather_">{{tableData.weather}}</span>
          <p class="indexes-weather-date-value">
            <span>{{tableData.temperature}}℃</span>
            <span class="precip">{{tableData.rainfall}} mm/h</span>
          </p>
        </div>
      </div>
      <p class="indexes-telop-1">⭐︎⭐️おすすめ干し時間：〜{{tableData.laundry_optimaly}}:00〜⭐️⭐️</p>
    </div>
  </section>
</template>

<script>
const axios = require('axios').create()
export default {
  name: 'weather_today',
  data () {
    return {
      tableData: []
    }
  },
  mounted () {
    this.getWeatherToday()
  },
  methods: {
    getWeatherToday: async function () {
      const response = await axios.get('/api/weather_today')
      this.tableData = response.data
      console.log(this.tableData)
    }
  },
  computed: {
  }
}
</script>

<style scoped>
.weather_{
  font-size: 0.875em;
}
h3.left-style {
    border-left: 10px solid #0061ca;
    padding: 5px 0 0 10px;
    border-bottom: 0;
    text-align: left;
}
.today-weather, .two-box li {
    width: 400px;
    float: left;
    margin-right: 20px;
}
.clearfix {
    display: block;
    min-height: 1%;
}
.indexes-weather-wrap {
  background-color: #edf6ff;
  position: relative;
  text-align: center;
  margin-bottom: 10px;
}
.indexes-icon-box {
    float: left;
    width: 50%;
    padding: 15px 0 0;
}
.indexes-telop-0 {
    display: block;
    margin-top: 5px;
}
.indexes-weather-wrap
.weather-icon-box {
    position: absolute;
    top: 13px;
    right: 20px;
    background-color: #FFF;
    padding: 5px 20px;
    border-radius: 4px;
    width: 130px;
}
.indexes-weather-wrap .weather-icon-box p.weather-telop {
    display: inline-block;
    font-size: 0.875em;
}
p.indexes-weather-date-value{
  margin: 0;
  padding: 0;
  border: 0;
  outline: 0;
  font-size: 1em;
}
p.indexes-telop-1 {
    clear: both;
    font-size: 0.875em;
    background-color: #FFF;
    margin: 20px 20px 10px;
}
.indexes-weather-wrap .weather-icon-box .precip {
    display: block;
}
.forecast-days-wrap .weather-telop {
    margin-top: 5px;
}
.indexes-weather-wrap .weather-icon-box img {
    vertical-align: middle;
}
</style>