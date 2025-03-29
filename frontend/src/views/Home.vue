<template>
  <div class="home-container">
    <!-- 欢迎区域 -->
    <div class="welcome-section ai-card">
      <h1 class="title">Welcome to PromptMaster</h1>
      <p class="subtitle">智能提示词管理系统</p>
      <p class="description">
        专业的提示词工程管理平台，让AI对话更智能、更高效
      </p>
      <div class="action-buttons">
        <el-button
          type="primary"
          size="large"
          @click="$router.push('/templates')"
        >
          开始使用
        </el-button>
        <el-button size="large" @click="$router.push('/docs')">
          查看文档
        </el-button>
      </div>
    </div>

    <!-- 系统介绍 -->
    <div class="intro-section">
      <h2>系统介绍</h2>
      <div class="intro-cards">
        <el-card class="intro-card ai-card">
          <template #header>
            <div class="card-header">
              <el-icon><Monitor /></el-icon>
              <span>智能管理</span>
            </div>
          </template>
          <div class="card-content">
            <p>
              提供专业的提示词模板管理功能，支持多种框架，让AI对话更加规范和高效。
            </p>
          </div>
        </el-card>

        <el-card class="intro-card ai-card">
          <template #header>
            <div class="card-header">
              <el-icon><Connection /></el-icon>
              <span>场景联动</span>
            </div>
          </template>
          <div class="card-content">
            <p>
              灵活的场景配置系统，针对不同应用场景快速调用合适的提示词模板。
            </p>
          </div>
        </el-card>

        <el-card class="intro-card ai-card">
          <template #header>
            <div class="card-header">
              <el-icon><DataAnalysis /></el-icon>
              <span>数据分析</span>
            </div>
          </template>
          <div class="card-content">
            <p>
              完整的数据分析功能，帮助您了解提示词使用情况，持续优化对话效果。
            </p>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 亮点功能 -->
    <div class="features-section">
      <h2>亮点功能</h2>
      <div class="feature-list">
        <div class="feature-item ai-card">
          <div class="feature-icon">
            <el-icon><Document /></el-icon>
          </div>
          <div class="feature-content">
            <h3>多框架支持</h3>
            <p>支持RTGO、SPAR等多种提示词框架，满足不同场景需求</p>
          </div>
        </div>

        <div class="feature-item ai-card">
          <div class="feature-icon">
            <el-icon><Share /></el-icon>
          </div>
          <div class="feature-content">
            <h3>一键导入导出</h3>
            <p>支持模板批量导入导出，轻松实现团队共享和备份</p>
          </div>
        </div>

        <div class="feature-item ai-card">
          <div class="feature-icon">
            <el-icon><Timer /></el-icon>
          </div>
          <div class="feature-content">
            <h3>版本管理</h3>
            <p>完整的版本历史记录，随时回溯和恢复历史版本</p>
          </div>
        </div>

        <div class="feature-item ai-card">
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
      <div class="case-list">
        <el-card
          v-for="i in 3"
          :key="i"
          class="case-card ai-card"
          shadow="hover"
        >
          <template #header>
            <div class="card-header">
              <h3>案例 {{ i }}</h3>
            </div>
          </template>
          <div class="case-content">
            <p>
              这里是案例描述内容，展示如何使用提示词管理系统优化AI对话效果。
            </p>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Monitor,
  Connection,
  DataAnalysis,
  Document,
  Share,
  Timer,
  Refresh,
} from "@element-plus/icons-vue";
</script>

<style scoped lang="scss">
@use "../styles/variables" as *;

.home-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  padding: 4rem 2rem;
  margin-bottom: 4rem;
  border-radius: 16px;
  @include glass-morphism;

  .title {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .subtitle {
    font-size: 1.5rem;
    color: var(--text-secondary);
    margin-bottom: 1rem;
  }

  .description {
    font-size: 1.1rem;
    color: var(--text-muted);
    margin-bottom: 2rem;
  }

  .action-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }
}

.intro-section,
.features-section,
.cases-section {
  margin-bottom: 4rem;

  h2 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 2rem;
  }
}

.intro-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;

  .intro-card {
    .card-header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 1.25rem;
      color: var(--text-primary);
    }

    .card-content {
      p {
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.6;
      }
    }
  }
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;

  .feature-item {
    padding: 1.5rem;
    border-radius: 12px;
    @include glass-morphism;

    .feature-icon {
      font-size: 2rem;
      color: var(--primary-color);
      margin-bottom: 1rem;
    }

    .feature-content {
      h3 {
        font-size: 1.25rem;
        margin-bottom: 0.5rem;
      }

      p {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
      }
    }
  }
}

.case-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;

  .case-card {
    .card-header {
      h3 {
        margin: 0;
        font-size: 1.25rem;
      }
    }

    .case-content {
      p {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
      }
    }
  }
}

// 响应式调整
@media (max-width: 768px) {
  .welcome-section {
    padding: 2rem 1rem;

    .title {
      font-size: 2rem;
    }

    .subtitle {
      font-size: 1.25rem;
    }
  }

  .action-buttons {
    flex-direction: column;
  }

  .intro-cards,
  .feature-list,
  .case-list {
    grid-template-columns: 1fr;
  }
}
</style>
