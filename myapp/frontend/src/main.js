import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import router from './router'
import Toasted from 'vue-toasted';

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  const axios = require('axios').create()
  axios.get('/api/islogin')
      .then(response => {
        const flag = response.data;
        const withoutLogin = ["/signin", "/signup"];  // ログインなしで閲覧できるページ
        if (withoutLogin.includes(to.path)) {
          // 認証している場合は、トップページに飛ばす
          if (flag == 'ok') {
              next("/");
          } else {
            next();
          }
        } else {
          // 認証されていない場合、ログインページに飛ばす
          if (flag == 'ok') {
            next();
          } else {
            next("/signin");
          }
        }
      })
      .catch(error => {
          console.log(error);
      })
});


import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';
import vuetify from './plugins/vuetify';

Vue.component('VueCtkDateTimePicker', VueCtkDateTimePicker);
Vue.component('vue-ctk-date-time-picker', VueCtkDateTimePicker);

// import { Datetime } from 'vue-datetime';
// Vue.component('datetime', Datetime);

Vue.use(Toasted, {
  duration: 3000,
  singleton: true
});

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
