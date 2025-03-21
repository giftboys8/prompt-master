<template>
  <div class="preview-modes">
    <div class="preview-header">
      <el-radio-group v-model="currentMode" size="large">
        <el-radio-button v-for="mode in previewModes" :key="mode.value" :label="mode.value">
          <el-icon>
            <component :is="mode.icon" />
          </el-icon>
          {{ mode.label }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <!-- 基础预览模式 -->
    <div v-if="currentMode === 'basic'" class="preview-content basic-preview">
      <div class="content-section">
        <template v-if="template?.framework_type === 'RTGO'">
          <div class="content-item">
            <h5>角色 (Role)</h5>
            <p>{{ template?.content.role }}</p>
          </div>
          <div class="content-item">
            <h5>任务 (Task)</h5>
            <p>{{ template?.content.task }}</p>
          </div>
          <div class="content-item">
            <h5>目标 (Goal)</h5>
            <p>{{ template?.content.goal }}</p>
          </div>
          <div class="content-item">
            <h5>输出 (Output)</h5>
            <p>{{ template?.content.output }}</p>
          </div>
        </template>

        <template v-else-if="template?.framework_type === 'SPAR'">
          <div class="content-item">
            <h5>情境 (Situation)</h5>
            <p>{{ template?.content.situation }}</p>
          </div>
          <div class="content-item">
            <h5>目的 (Purpose)</h5>
            <p>{{ template?.content.purpose }}</p>
          </div>
          <div class="content-item">
            <h5>行动 (Action)</h5>
            <p>{{ template?.content.action }}</p>
          </div>
          <div class="content-item">
            <h5>结果 (Result)</h5>
            <p>{{ template?.content.result }}</p>
          </div>
        </template>

        <template v-else>
          <div class="content-item">
            <h5>自定义内容</h5>
            <p>{{ template?.content.custom }}</p>
          </div>
        </template>
      </div>
    </div>

    <!-- 对话预览模式 -->
    <div v-else-if="currentMode === 'chat'" class="preview-content chat-preview">
      <div class="chat-container">
        <div class="message system">
          <el-avatar :size="40" src="/ai-avatar.png" />
          <div class="message-content">
            <p>我是您的AI助手，我将按照以下方式为您服务：</p>
            <template v-if="template?.framework_type === 'RTGO'">
              <p><strong>作为：</strong>{{ template?.content.role }}</p>
              <p><strong>任务：</strong>{{ template?.content.task }}</p>
              <p><strong>目标：</strong>{{ template?.content.goal }}</p>
              <p><strong>输出：</strong>{{ template?.content.output }}</p>
            </template>
            <template v-else-if="template?.framework_type === 'SPAR'">
              <p><strong>情境：</strong>{{ template?.content.situation }}</p>
              <p><strong>目的：</strong>{{ template?.content.purpose }}</p>
              <p><strong>行动：</strong>{{ template?.content.action }}</p>
              <p><strong>结果：</strong>{{ template?.content.result }}</p>
            </template>
            <template v-else>
              <p>{{ template?.content.custom }}</p>
            </template>
          </div>
        </div>
        <div class="message user">
          <div class="message-content">
            <p>好的，我明白了。让我们开始吧！</p>
          </div>
          <el-avatar :size="40" :src="userAvatar" />
        </div>
      </div>
    </div>

    <!-- 格式化文本预览模式 -->
    <div v-else-if="currentMode === 'format'" class="preview-content format-preview">
      <el-card class="format-card">
        <div class="format-header">
          <el-tag>{{ template?.framework_type }}</el-tag>
          <el-button type="primary" text @click="copyFormatted">
            <el-icon><CopyDocument /></el-icon>
            复制
          </el-button>
        </div>
        <pre><code>{{ formattedContent }}</code></pre>
      </el-card>
    </div>

    <!-- 交互式预览模式 -->
    <div v-else-if="currentMode === 'interactive'" class="preview-content interactive-preview">
      <div class="variables-form" v-if="template?.variables?.length">
        <h4>填写变量</h4>
        <el-form :model="variableValues" label-position="top">
          <el-form-item
            v-for="variable in template.variables"
            :key="variable.name"
            :label="variable.description"
          >
            <el-input
              v-model="variableValues[variable.name]"
              :placeholder="variable.default_value"
            />
          </el-form-item>
        </el-form>
      </div>
      <div class="preview-result">
        <h4>预览结果</h4>
        <el-card class="result-card">
          <pre><code>{{ processedContent }}</code></pre>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Document,
  ChatRound,
  Reading,
  Edit,
  CopyDocument
} from '@element-plus/icons-vue'
import type { Template } from '@/types'

const props = defineProps<{
  template?: Template
}>()

// 预览模式
const previewModes = [
  { label: '基础预览', value: 'basic', icon: 'Document' },
  { label: '对话预览', value: 'chat', icon: 'ChatRound' },
  { label: '格式化预览', value: 'Reading', icon: 'Reading' },
  { label: '交互预览', value: 'interactive', icon: 'Edit' }
]

const currentMode = ref('basic')
const userAvatar = ref('/user-avatar.png') // 用户头像，可以从用户状态获取
const variableValues = ref<Record<string, string>>({})

// 格式化内容
const formattedContent = computed(() => {
  if (!props.template) return ''

  if (props.template.framework_type === 'RTGO') {
    return `Role:
${props.template.content.role}

Task:
${props.template.content.task}

Goal:
${props.template.content.goal}

Output:
${props.template.content.output}`
  } else if (props.template.framework_type === 'SPAR') {
    return `Situation:
${props.template.content.situation}

Purpose:
${props.template.content.purpose}

Action:
${props.template.content.action}

Result:
${props.template.content.result}`
  } else {
    return props.template.content.custom || ''
  }
})

// 处理变量替换后的内容
const processedContent = computed(() => {
  let content = formattedContent.value
  if (props.template?.variables) {
    props.template.variables.forEach(variable => {
      const value = variableValues.value[variable.name] || variable.default_value
      content = content.replace(new RegExp(`{${variable.name}}`, 'g'), value)
    })
  }
  return content
})

// 复制格式化内容
const copyFormatted = async () => {
  try {
    await navigator.clipboard.writeText(formattedContent.value)
    ElMessage.success('复制成功')
  } catch (err) {
    ElMessage.error('复制失败')
  }
}
</script>

<style lang="scss" scoped>
@use '@/styles/tech-theme.scss' as *;

.preview-modes {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
  z-index: 10;
  background-color: var(--bg-card);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
}

.preview-header {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.preview-content {
  flex: 1;
  overflow-y: auto;
}

// 基础预览样式
.basic-preview {
  .content-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .content-item {
    @include glass-morphism;
    padding: 1.2rem;
    border-radius: 12px;
    @include hover-effect;

    h5 {
      font-family: 'Orbitron', sans-serif;
      background: var(--primary-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin: 0 0 0.75rem 0;
      font-size: 1.1rem;
    }

    p {
      color: var(--text-primary);
      line-height: 1.6;
      margin: 0;
      white-space: pre-wrap;
    }
  }
}

// 对话预览样式
.chat-preview {
  .chat-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 800px;
    margin: 0 auto;
  }

  .message {
    display: flex;
    gap: 1rem;
    align-items: flex-start;

    &.user {
      flex-direction: row-reverse;
      .message-content {
        background: rgba(14, 165, 233, 0.2);
        border: 1px solid rgba(14, 165, 233, 0.3);
      }
    }
  }

  .message-content {
    @include glass-morphism;
    padding: 1.2rem;
    border-radius: 12px;
    flex: 1;
    max-width: 80%;
    @include hover-effect;

    p {
      margin: 0.5rem 0;
      color: var(--text-primary);
      line-height: 1.6;

      strong {
        color: var(--neon-blue);
      }

      &:first-child {
        margin-top: 0;
      }

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

// 格式化预览样式
.format-preview {
  .format-card {
    @include glass-morphism;
    padding: 1.2rem;
    @include hover-effect;
  }

  .format-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  pre {
    margin: 0;
    white-space: pre-wrap;
    color: var(--text-primary);
    line-height: 1.6;
    font-family: 'Inter', monospace;
    font-size: 0.95rem;
  }
}

// 交互式预览样式
.interactive-preview {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }

  .variables-form {
    h4 {
      color: $primary-color;
      margin: 0 0 1rem 0;
      font-family: $header-font;
    }
  }

  .preview-result {
    h4 {
      color: $primary-color;
      margin: 0 0 1rem 0;
      font-family: $header-font;
    }

    .result-card {
      @include glass-morphism;
      // 已应用glass-morphism，不需要额外的背景和边框

      pre {
        margin: 0;
        white-space: pre-wrap;
        color: var(--text-primary);
        line-height: 1.6;
        font-family: 'Inter', monospace;
      }
    }
  }
}
</style>