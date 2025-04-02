<!-- 403 Forbidden Page -->
<template>
  <div class="forbidden-page">
    <h1>403</h1>
    <h2>权限不足</h2>
    <p>抱歉，您没有权限访问此页面</p>
    <router-link to="/" class="back-home">返回首页</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Forbidden",
});
</script>

<style scoped>
.forbidden-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
}

h1 {
  font-size: 6rem;
  margin: 0;
  color: #f56c6c;
}

h2 {
  font-size: 2rem;
  margin: 1rem 0;
}

.back-home {
  margin-top: 2rem;
  padding: 0.8rem 1.6rem;
  color: #409eff;
  text-decoration: none;
  border: 1px solid #409eff;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.back-home:hover {
  color: #fff;
  background-color: #409eff;
}
</style>
