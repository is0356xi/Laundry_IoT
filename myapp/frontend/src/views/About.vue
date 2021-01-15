<template>
  <div class="about">
    <h1>This is an about page</h1>
    <ImgPreview/>
    <TimeInput/>
</template>



<script>
import TimeInput from '../components/TimeInput'
import ImgPreview from '../components/ImgPreview'
export default {
  components:{
      TimeInput,
      ImgPreview
  }
}
</script>