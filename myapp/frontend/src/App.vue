<template>
  <div id="app">
    <el-menu :default-active="activeIndex" mode="horizontal" router @select="handleSelect">
      <el-menu-item index="home" :route="{ name:'home' }" target="_blank">Home</el-menu-item>
      <el-menu-item index="token">Token</el-menu-item>
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
      } else if (index == 'token') {
        const axios = require('axios').create()
        axios.get('/api/islogin')
            .then(response => {
              const flag = response.data;
              if(flag == "ok") {
                window.open('/token/token.html', 'newtab');
                this.$router.push('/');
              }
            })
            .catch(error => {
                console.log(error);
            })
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