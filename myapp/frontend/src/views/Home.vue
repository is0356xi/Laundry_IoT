<template>
  <div class="home">
    <br>
    <div class="title">
      今日の洗濯指数
    </div>
    <br>
    <div class="forecast-days">
      <WeatherToday/>
      <TimeInput/>
    </div>
    <br>
    <div class="title">
      1時間ごとの洗濯指数
    </div>
    <br>
    <WeatherTable/>
    <br>
    <div class="title">
      外干し状況
    </div>
    <br>
    <ImgPreview/>
  </div>
</template>



<script>
import WeatherTable from '../components/weather/WeatherTable'
import WeatherToday from '../components/weather/WeatherToday'
import TimeInput from '../components/TimeInput'
import ImgPreview from '../components/ImgPreview'
export default {
  components:{
    WeatherTable,
    WeatherToday,
    TimeInput,
    ImgPreview
  }
}
</script>

<style scoped>
.title {
  text-align: left;
  font-size: 1.259em;
  border-bottom: 4px solid #0061ca
}
.forecast-days {
  margin: 20px 0 40px;
  width:100%;
  height:180px;
}

</style>