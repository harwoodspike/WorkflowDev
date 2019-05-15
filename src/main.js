import axios from 'axios';
import Vue from 'vue';
import router from './router';

axios.defaults.baseURL = window.location.origin;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
Vue.prototype.$http = axios;

const mvm = new Vue({
  name: 'RouteView',
  router,
  render(createElement) {
    return createElement(
      'router-view',
      { key: this.$route.fullPath },
    );
  },
});
mvm.$mount('#app');
