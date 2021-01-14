import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import router from './router'

Vue.config.productionTip = false

import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';

Vue.component('VueCtkDateTimePicker', VueCtkDateTimePicker);
Vue.component('vue-ctk-date-time-picker', VueCtkDateTimePicker);

// import { Datetime } from 'vue-datetime';
// Vue.component('datetime', Datetime);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
