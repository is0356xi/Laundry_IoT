<template>
  <div class="about">
    <h1>This is an about page</h1>
</template>



<script>
const axios = require('axios').create()
export default {
  name: 'about',
  data () {
    return {
      tableData: []
    }
  },
  mounted () {
    this.getWeather()
  },
  methods: {
    getWeather: async function () {
      const response = await axios.get('/api/weather')
      this.tableData = response.data
      console.log(this.tableData)
    }
  }
}
</script>