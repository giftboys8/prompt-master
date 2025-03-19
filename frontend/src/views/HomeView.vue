<template>
  <div class="home">
    <h1>欢迎使用 PromptMaster</h1>
    <p>您的AI提示词管理专家</p>
    
    <el-row class="feature-list" :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>提示词管理</h3>
            </div>
          </template>
          <div class="text item">
            高效管理和组织您的AI提示词，让创作更加便捷。
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>智能优化</h3>
            </div>
          </template>
          <div class="text item">
            自动分析和优化提示词，提高AI响应的质量和准确性。
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>团队协作</h3>
            </div>
          </template>
          <div class="text item">
            支持团队共享和协作，提高团队工作效率。
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5em;
  color: #2c3e50;
  margin-bottom: 20px;
}

p {
  font-size: 1.2em;
  color: #666;
  margin-bottom: 40px;
}

.feature-list {
  margin-top: 40px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  color: #2c3e50;
}

.text {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.item {
  margin-bottom: 18px;
}
</style>