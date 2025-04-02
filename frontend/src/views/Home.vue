<template>
  <div class="home-container">
    <!-- 英雄区域 -->
    <div class="hero-section ai-card">
      <div class="hero-content">
        <h1 class="title">PromptMaster</h1>
        <p class="subtitle">企业级提示词工程管理平台</p>
        <p class="description">
          专注提升AI对话质量，为企业提供专业的提示词工程解决方案。
          通过标准化管理、智能优化和数据分析，
          帮助您的团队构建高质量的AI对话体系。
        </p>
        <div class="action-buttons">
          <el-button type="primary" size="large" @click="$router.push('/templates')">
            立即开始
          </el-button>
          <el-button size="large" @click="$router.push('/docs')">
            技术文档
          </el-button>
        </div>
        <div class="stats">
          <div class="stat-item">
            <h3>500+</h3>
            <p>模板数量</p>
          </div>
          <div class="stat-item">
            <h3>50+</h3>
            <p>企业用户</p>
          </div>
          <div class="stat-item">
            <h3>99.9%</h3>
            <p>服务可用性</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 核心优势 -->
    <div class="advantages-section">
      <h2>为什么选择 PromptMaster？</h2>
      <div class="advantage-cards">
        <el-card class="advantage-card ai-card">
          <template #header>
            <div class="card-header">
              <el-icon><Monitor /></el-icon>
              <span>专业的提示词工程管理</span>
            </div>
          </template>
          <div class="card-content">
            <ul>
              <li>支持RTGO、SPAR等主流提示词框架</li>
              <li>完整的版本控制和历史追踪</li>
              <li>灵活的模板复用和继承机制</li>
              <li>严格的质量控制和审核流程</li>
            </ul>
          </div>
        </el-card>

        <el-card class="advantage-card ai-card">
          <template #header>
            <div class="card-header">
              <el-icon><Connection /></el-icon>
              <span>智能场景配置系统</span>
            </div>
          </template>
          <div class="card-content">
            <ul>
              <li>场景化模板组织和管理</li>
              <li>智能场景识别和匹配</li>
              <li>动态参数配置和验证</li>
              <li>场景效果实时监控</li>
            </ul>
          </div>
        </el-card>

        <el-card class="advantage-card ai-card">
          <template #header>
            <div class="card-header">
              <el-icon><DataAnalysis /></el-icon>
              <span>全方位数据分析</span>
            </div>
          </template>
          <div class="card-content">
            <ul>
              <li>提示词性能评估指标</li>
              <li>使用情况统计和分析</li>
              <li>效果对比和优化建议</li>
              <li>自定义报表和导出</li>
            </ul>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 功能特性 -->
    <div class="features-section">
      <h2>强大的功能特性</h2>
      <div class="feature-list">
        <div class="feature-item ai-card">
          <div class="feature-icon">
            <el-icon><Document /></el-icon>
          </div>
          <div class="feature-content">
            <h3>多框架支持</h3>
            <p>原生支持RTGO、SPAR等主流提示词框架，可扩展自定义框架，轻松应对不同场景需求</p>
          </div>
        </div>

        <div class="feature-item ai-card">
          <div class="feature-icon">
            <el-icon><Share /></el-icon>
          </div>
          <div class="feature-content">
            <h3>团队协作</h3>
            <p>支持团队成员协同编辑、审核和管理，内置完整的权限控制，确保工作流程顺畅</p>
          </div>
        </div>

        <div class="feature-item ai-card">
          <div class="feature-icon">
            <el-icon><Timer /></el-icon>
          </div>
          <div class="feature-content">
            <h3>版本管理</h3>
            <p>自动记录所有更改，支持版本比较和回滚，让每一次修改都可追溯</p>
          </div>
        </div>

        <div class="feature-item ai-card">
          <div class="feature-icon">
            <el-icon><Refresh /></el-icon>
          </div>
          <div class="feature-content">
            <h3>实时验证</h3>
            <p>提供在线测试环境，支持多种模型接入，快速验证提示词效果</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 应用案例 -->
    <div class="cases-section">
      <h2>客户案例</h2>
      <div class="case-list">
        <el-card class="case-card ai-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h3>智能客服升级</h3>
              <span class="case-tag">金融行业</span>
            </div>
          </template>
          <div class="case-content">
            <p class="case-description">
              某大型银行通过PromptMaster管理超过200个客服场景的提示词模板，
              将客服回复准确率提升40%，用户满意度提升35%。
            </p>
            <ul class="case-points">
              <li>场景化模板管理</li>
              <li>多轮对话优化</li>
              <li>准确率持续提升</li>
            </ul>
          </div>
        </el-card>

        <el-card class="case-card ai-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h3>内容创作助手</h3>
              <span class="case-tag">媒体行业</span>
            </div>
          </template>
          <div class="case-content">
            <p class="case-description">
              某新媒体平台使用PromptMaster管理内容创作提示词，
              将内容生产效率提升60%，创作质量显著提高。
            </p>
            <ul class="case-points">
              <li>创作模板库</li>
              <li>质量评估体系</li>
              <li>团队协作管理</li>
            </ul>
          </div>
        </el-card>

        <el-card class="case-card ai-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h3>研发效能提升</h3>
              <span class="case-tag">科技行业</span>
            </div>
          </template>
          <div class="case-content">
            <p class="case-description">
              某互联网公司将PromptMaster应用于代码生成和优化场景，
              研发效率提升30%，代码质量显著改善。
            </p>
            <ul class="case-points">
              <li>代码生成模板</li>
              <li>最佳实践沉淀</li>
              <li>效果评估分析</li>
            </ul>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 开始使用 -->
    <div class="cta-section ai-card">
      <h2>开始使用 PromptMaster</h2>
      <p>立即体验专业的提示词工程管理平台，提升您的AI应用效果</p>
      <el-button type="primary" size="large" @click="$router.push({ name: 'Register' })">
        免费注册
      </el-button>
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

.hero-section {
  padding: 4rem 2rem;
  margin-bottom: 4rem;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--primary-color-light) 0%, var(--primary-color) 100%);
  color: white;
  text-align: center;
  @include glass-morphism;

  .title {
    font-size: 3.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
    background: linear-gradient(to right, #fff, #e0e0e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .subtitle {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    opacity: 0.9;
  }

  .description {
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto 2rem;
    line-height: 1.8;
    opacity: 0.8;
  }

  .action-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 3rem;
  }

  .stats {
    display: flex;
    justify-content: center;
    gap: 4rem;
    margin-top: 2rem;

    .stat-item {
      h3 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: bold;
      }

      p {
        margin: 0;
        opacity: 0.8;
      }
    }
  }
}

.advantages-section,
.features-section,
.cases-section {
  margin-bottom: 4rem;

  h2 {
    text-align: center;
    font-size: 2.2rem;
    margin-bottom: 2.5rem;
    color: var(--text-primary);
  }
}

.advantage-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;

  .advantage-card {
    .card-header {
      display: flex;
      align-items: center;
      gap: 0.8rem;
      font-size: 1.3rem;
      color: var(--primary-color);
    }

    .card-content {
      ul {
        padding-left: 1.2rem;
        margin: 0;

        li {
          color: var(--text-secondary);
          margin-bottom: 0.8rem;
          line-height: 1.6;
        }
      }
    }
  }
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;

  .feature-item {
    padding: 2rem;
    border-radius: 12px;
    transition: transform 0.3s ease;
    @include glass-morphism;

    &:hover {
      transform: translateY(-5px);
    }

    .feature-icon {
      font-size: 2.5rem;
      color: var(--primary-color);
      margin-bottom: 1.5rem;
    }

    .feature-content {
      h3 {
        font-size: 1.4rem;
        margin-bottom: 1rem;
        color: var(--text-primary);
      }

      p {
        color: var(--text-secondary);
        line-height: 1.6;
      }
    }
  }
}

.case-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;

  .case-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h3 {
        margin: 0;
        font-size: 1.3rem;
        color: var(--text-primary);
      }

      .case-tag {
        background: var(--primary-color-light);
        color: var(--primary-color);
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        font-size: 0.9rem;
      }
    }

    .case-content {
      .case-description {
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 1.5rem;
      }

      .case-points {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;

        li {
          background: var(--background-secondary);
          color: var(--text-secondary);
          padding: 0.4rem 0.8rem;
          border-radius: 4px;
          font-size: 0.9rem;
        }
      }
    }
  }
}

.cta-section {
  text-align: center;
  padding: 4rem 2rem;
  border-radius: 16px;
  @include glass-morphism;

  h2 {
    font-size: 2.2rem;
    margin-bottom: 1rem;
    color: var(--text-primary);
  }

  p {
    color: var(--text-secondary);
    font-size: 1.2rem;
    margin-bottom: 2rem;
  }
}

// 响应式调整
@media (max-width: 768px) {
  .hero-section {
    padding: 3rem 1rem;

    .title {
      font-size: 2.5rem;
    }

    .subtitle {
      font-size: 1.4rem;
    }

    .description {
      font-size: 1rem;
    }

    .stats {
      flex-direction: column;
      gap: 2rem;
    }
  }

  .action-buttons {
    flex-direction: column;
  }

  .advantage-cards,
  .feature-list,
  .case-list {
    grid-template-columns: 1fr;
  }

  h2 {
    font-size: 1.8rem !important;
  }
}
</style>