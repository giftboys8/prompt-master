<template>
  <div class="about">
    <h1>关于 PromptMaster</h1>
    
    <el-card class="about-card">
      <template #header>
        <div class="card-header">
          <h3>我们的使命</h3>
        </div>
      </template>
      <div class="content">
        <p>PromptMaster 致力于为AI创作者提供最专业的提示词管理解决方案。我们的目标是通过简化提示词的管理和优化过程，帮助用户更好地发挥AI的潜力。</p>
      </div>
    </el-card>
    
    <el-card class="about-card">
      <template #header>
        <div class="card-header">
          <h3>核心功能</h3>
        </div>
      </template>
      <div class="content">
        <ul>
          <li>提示词库管理：系统化管理您的提示词集合</li>
          <li>智能优化：基于数据分析的提示词优化建议</li>
          <li>版本控制：追踪提示词的修改历史</li>
          <li>团队协作：支持多人协作和权限管理</li>
          <li>性能分析：评估提示词效果的数据分析</li>
        </ul>
      </div>
    </el-card>
    
    <el-card class="about-card">
      <template #header>
        <div class="card-header">
          <h3>联系我们</h3>
        </div>
      </template>
      <div class="content">
        <p>如果您有任何问题或建议，欢迎联系我们：</p>
        <p>邮箱：support@promptmaster.com</p>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>

<style scoped>
.about {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 2em;
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.about-card {
  margin-bottom: 20px;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
}

.content {
  padding: 10px 0;
}

p {
  margin: 10px 0;
  line-height: 1.6;
  color: #666;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 10px 0;
  padding-left: 20px;
  position: relative;
  color: #666;
}

li:before {
  content: "•";
  position: absolute;
  left: 0;
  color: #409EFF;
}
</style>