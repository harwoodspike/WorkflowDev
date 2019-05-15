<template>
  <div class="main-element">
    <div>This is VueJS text.</div>
    <div>API TEXT: {{ api_data }}</div>
  </div>
</template>

<script>
export default {
  name: 'CatchAll',
  data() {
    return {
      api_data: '',
    };
  },
  created() {
    this.$http.get('/api/test/').then((resp) => {
      this.api_data = resp.data.msg;
    }).catch((err) => {
      this.api_data = 'API FAILED';
      console.log(err);
    });
  },
};
</script>
