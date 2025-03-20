<template>
  <div class="home-container">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <h1 class="title">Welcome to PromptMaster</h1>
      <p class="subtitle">智能提示词管理系统</p>
      <p class="description">
        专业的提示词工程管理平台，让AI对话更智能、更高效
      </p>
    </div>

    <!-- 系统介绍 -->
    <div class="intro-section">
      <h2>系统介绍</h2>
      <div class="intro-cards">
        <el-card class="intro-card">
          <template #header>
            <div class="card-header">
              <el-icon><Monitor /></el-icon>
              <span>智能管理</span>
            </div>
          </template>
          <p style="color: #666666; font-size: 16px; font-weight: 500;">提供专业的提示词模板管理功能，支持多种框架，让AI对话更加规范和高效。</p>
        </el-card>

        <el-card class="intro-card">
          <template #header>
            <div class="card-header">
              <el-icon><Connection /></el-icon>
              <span>场景联动</span>
            </div>
          </template>
          <p style="color: #666666; font-size: 16px; font-weight: 500;">灵活的场景配置系统，针对不同应用场景快速调用合适的提示词模板。</p>
        </el-card>

        <el-card class="intro-card">
          <template #header>
            <div class="card-header">
              <el-icon><DataAnalysis /></el-icon>
              <span>数据分析</span>
            </div>
          </template>
          <p style="color: #666666; font-size: 16px; font-weight: 500;">完整的数据分析功能，帮助您了解提示词使用情况，持续优化对话效果。</p>
        </el-card>
      </div>
    </div>

    <!-- 亮点功能 -->
    <div class="features-section">
      <h2>亮点功能</h2>
      <div class="feature-list">
        <div class="feature-item">
          <div class="feature-icon">
            <el-icon><Document /></el-icon>
          </div>
          <div class="feature-content">
            <h3>多框架支持</h3>
            <p>支持RTGO、SPAR等多种提示词框架，满足不同场景需求</p>
          </div>
        </div>

        <div class="feature-item">
          <div class="feature-icon">
            <el-icon><Share /></el-icon>
          </div>
          <div class="feature-content">
            <h3>一键导入导出</h3>
            <p>支持模板批量导入导出，轻松实现团队共享和备份</p>
          </div>
        </div>

        <div class="feature-item">
          <div class="feature-icon">
            <el-icon><Timer /></el-icon>
          </div>
          <div class="feature-content">
            <h3>版本管理</h3>
            <p>完整的版本历史记录，随时回溯和恢复历史版本</p>
          </div>
        </div>

        <div class="feature-item">
          <div class="feature-icon">
            <el-icon><Refresh /></el-icon>
          </div>
          <div class="feature-content">
            <h3>实时测试</h3>
            <p>提供实时测试功能，快速验证提示词效果</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 经典案例 -->
    <div class="cases-section">
      <h2>经典案例</h2>
      <el-row :gutter="24">
        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="case-card" shadow="hover">
            <template #header>
              <div class="case-header">
                <h3>智能客服对话</h3>
                <el-tag size="small" type="success">RTGO框架</el-tag>
              </div>
            </template>
            <div class="case-content">
              <p>通过RTGO框架构建的客服对话模板，提供专业、亲切的服务体验</p>
              <ul>
                <li>准确理解用户意图</li>
                <li>个性化回答定制</li>
                <li>情感化表达优化</li>
              </ul>
            </div>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="case-card" shadow="hover">
            <template #header>
              <div class="case-header">
                <h3>营销文案生成</h3>
                <el-tag size="small" type="warning">SPAR框架</el-tag>
              </div>
            </template>
            <div class="case-content">
              <p>基于SPAR框架的营销文案模板，生成吸引力强的推广内容</p>
              <ul>
                <li>场景化文案构建</li>
                <li>目标受众分析</li>
                <li>转化率优化</li>
              </ul>
            </div>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="case-card" shadow="hover">
            <template #header>
              <div class="case-header">
                <h3>技术文档撰写</h3>
                <el-tag size="small" type="info">自定义框架</el-tag>
              </div>
            </template>
            <div class="case-content">
              <p>自定义框架支持的技术文档模板，提供专业规范的文档输出</p>
              <ul>
                <li>结构化内容组织</li>
                <li>专业术语规范</li>
                <li>示例代码生成</li>
              </ul>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 快速入口 -->
    <div class="quick-start">
      <h2>立即开始</h2>
      <div class="action-buttons">
        <el-button type="primary" size="large" @click="router.push('/templates')">
          <el-icon><Document /></el-icon>浏览模板
        </el-button>
        <el-button type="success" size="large" @click="router.push('/templates/create')">
          <el-icon><Plus /></el-icon>创建模板
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Document, Plus, Monitor, Connection, DataAnalysis, Share, Timer, Refresh } from '@element-plus/icons-vue'

const router = useRouter()
</script>

<style scoped>
.home-container {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 欢迎区域 */
.welcome-section {
  text-align: center;
  margin-bottom: 64px;
  animation: fadeInUp 0.8s ease;
}

.title {
  font-size: 48px;
  margin-bottom: 16px;
  background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 30px rgba(96, 165, 250, 0.3);
}

.subtitle {
  font-size: 24px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.description {
  font-size: 16px;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

/* 通用标题样式 */
h2 {
  font-size: 32px;
  margin-bottom: 32px;
  text-align: center;
  background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 系统介绍 */
.intro-section {
  margin-bottom: 64px;
}

.intro-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.intro-card {
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  transition: all 0.3s ease;
}

.intro-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  padding: 8px 0;
}

.card-header .el-icon {
  font-size: 24px;
  color: var(--primary-color);
}

/* 亮点功能 */
.features-section {
  margin-bottom: 64px;
  padding: 48px 0;
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid var(--glass-border);
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 32px;
  padding: 0 32px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.feature-icon {
  padding: 16px;
  border-radius: 12px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
}

.feature-icon .el-icon {
  font-size: 24px;
  color: var(--primary-color);
}

.feature-content h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.feature-content p {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

/* 经典案例 */
.cases-section {
  margin-bottom: 64px;
}

.case-card {
  height: 100%;
  background: var(--glass-bg);
  backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  transition: all 0.3s ease;
  margin-bottom: 24px;
}

.case-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.case-header h3 {
  margin: 0;
  font-size: 18px;
  color: var(--text-primary);
}

.case-content {
  color: var(--text-secondary);
}

.case-content ul {
  list-style: none;
  padding: 0;
  margin: 16px 0 0;
}

.case-content li {
  margin: 8px 0;
  padding-left: 20px;
  position: relative;
}

.case-content li::before {
  content: "•";
  color: var(--primary-color);
  position: absolute;
  left: 0;
}

/* 快速入口 */
.quick-start {
  text-align: center;
  margin-bottom: 32px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.action-buttons .el-button {
  min-width: 160px;
}

/* 动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .home-container {
    padding: 16px;
  }

  .title {
    font-size: 36px;
  }

  .subtitle {
    font-size: 20px;
  }

  h2 {
    font-size: 28px;
  }

  .feature-list {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .el-button {
    width: 100%;
  }
}
</style>