<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="feature-card" @click="router.push('/templates')">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>提示词模板</span>
            </div>
          </template>
          <div class="card-content">
            管理和编辑提示词模板，支持 RTGO、SPAR 等多种框架
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="feature-card" @click="router.push('/scenes')">
          <template #header>
            <div class="card-header">
              <el-icon><Grid /></el-icon>
              <span>场景管理</span>
            </div>
          </template>
          <div class="card-content">
            管理不同的应用场景，针对性地配置提示词模板
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="feature-card" @click="router.push('/contents')">
          <template #header>
            <div class="card-header">
              <el-icon><Collection /></el-icon>
              <span>内容管理</span>
            </div>
          </template>
          <div class="card-content">
            管理生成的内容，包括历史记录和版本管理
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Document, Grid, Collection } from '@element-plus/icons-vue'

const router = useRouter()
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.feature-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 18px;
}

.card-header .el-icon {
  margin-right: 10px;
  font-size: 20px;
}

.card-content {
  color: #606266;
  line-height: 1.5;
}
</style>