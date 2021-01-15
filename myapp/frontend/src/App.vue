<template>
  <div id="app">
    <el-menu :default-active="activeIndex" mode="horizontal" router @select="handleSelect">
      <el-menu-item index="home" :route="{ name:'home' }" target="_blank">Home</el-menu-item>
      <el-menu-item>
        <a href="http://0.0.0.0:5000/token">Token</a>
      </el-menu-item>
      <el-menu-item index="logout">Logout</el-menu-item>
    </el-menu>
    <router-view />
  </div>
</template>

<script>
const axios = require('axios').create()
export default {
  name: 'app',
  data () {
    return {
      activeIndex: this.$route.name
    }
  },
  methods: {
    handleSelect(index, indexPath) {
      console.log(indexPath);
      if (index == 'logout') {
        this.logout()
      }
    },
    async logout() {
      console.log(this.userData);
      await axios.get('/api/logout')
      .then(response => {
          this.results = response.data;
          console.log(this.results);
          this.$router.push('/signin');
        })
      .catch(error => {
          console.log(error);
      })
    }
  }
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
a {
  text-decoration: none;
}
</style>