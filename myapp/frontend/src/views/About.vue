<template>
  <div class="about">
    <h1>This is an about page</h1>
    <WeatherTable/>
    <ImgPreview/>
    <TimeInput/>
</template>



<script>
import WeatherTable from '../components/weather/WeatherTable'
import TimeInput from '../components/TimeInput'
import ImgPreview from '../components/ImgPreview'
export default {
  components:{
    WeatherTable,
    TimeInput,
    ImgPreview
  }
}
</script>