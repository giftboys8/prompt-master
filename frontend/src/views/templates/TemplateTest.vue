<template>
  <div class="template-test">
    <h2>模板测试</h2>
    <el-form :model="testForm" @submit.prevent="runTest" label-position="top" class="test-form">
      <div class="form-header">
        <el-form-item label="选择模板" required>
          <el-select 
            v-model="testForm.template" 
            placeholder="请选择模板"
            @change="handleTemplateChange"
            filterable
          >
            <el-option
              v-for="template in templates"
              :key="template.id"
              :label="template.name"
              :value="template.id"
            >
              <div class="template-option">
                <div class="template-name">{{ template.name }}</div>
                <div class="template-description">{{ template.description }}</div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="选择模型" required>
          <el-select v-model="testForm.model" placeholder="请选择模型">
            <el-option label="GPT-3.5" value="GPT-3.5"></el-option>
            <el-option label="GPT-4" value="GPT-4"></el-option>
            <el-option label="Claude" value="CLAUDE"></el-option>
          </el-select>
        </el-form-item>
      </div>

      <!-- 变量输入表单 -->
      <template v-if="selectedTemplate">
        <div class="variables-section">
          <h3>变量设置</h3>
          <div class="variables-description">
            请填写以下变量的值，这些值将用于生成最终的提示词。
          </div>
          <el-form-item
            v-for="variable in selectedTemplate.variables"
            :key="variable.name"
            :required="true"
          >
            <template #label>
              <div class="variable-label">
                <span>{{ variable.name }}</span>
                <span class="variable-description-inline">({{ variable.description }})</span>
              </div>
            </template>
            <div class="variable-input">
              <el-input
                v-model="variableInputs[variable.name]"
                :placeholder="'请输入' + variable.name"
              >
                <template #append v-if="variable.default_value">
                  <el-button @click="useDefaultValue(variable.name, variable.default_value)">
                    使用默认值
                  </el-button>
                </template>
              </el-input>
            </div>
          </el-form-item>
        </div>

        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            :disabled="!isFormValid"
            :loading="isRunning"
          >
            运行测试
          </el-button>
        </el-form-item>
      </template>

        <!-- 预览区域 -->
        <div v-if="selectedTemplate" class="preview-section">
          <h3>模板预览</h3>
          <div class="template-preview">
            <div v-if="selectedTemplate.framework_type === 'RTGO'" class="framework-content">
              <div class="preview-item">
                <div class="preview-label">角色(Role)：</div>
                <div class="preview-text">{{ selectedTemplate.content.role }}</div>
              </div>
              <div class="preview-item">
                <div class="preview-label">任务(Task)：</div>
                <div class="preview-text">{{ selectedTemplate.content.task }}</div>
              </div>
              <div class="preview-item">
                <div class="preview-label">目标(Goal)：</div>
                <div class="preview-text">{{ selectedTemplate.content.goal }}</div>
              </div>
              <div class="preview-item">
                <div class="preview-label">输出(Output)：</div>
                <div class="preview-text">{{ selectedTemplate.content.output }}</div>
              </div>
            </div>
            <div v-else-if="selectedTemplate.framework_type === 'SPAR'" class="framework-content">
              <div class="preview-item">
                <div class="preview-label">情境(Situation)：</div>
                <div class="preview-text">{{ selectedTemplate.content.situation }}</div>
              </div>
              <div class="preview-item">
                <div class="preview-label">目的(Purpose)：</div>
                <div class="preview-text">{{ selectedTemplate.content.purpose }}</div>
              </div>
              <div class="preview-item">
                <div class="preview-label">行动(Action)：</div>
                <div class="preview-text">{{ selectedTemplate.content.action }}</div>
              </div>
              <div class="preview-item">
                <div class="preview-label">结果(Result)：</div>
                <div class="preview-text">{{ selectedTemplate.content.result }}</div>
              </div>
            </div>
            <div v-else class="framework-content">
              <div class="preview-item">
                <div class="preview-label">自定义内容：</div>
                <div class="preview-text">{{ selectedTemplate.content.custom }}</div>
              </div>
            </div>
          </div>
        </div>

      <!-- 测试结果 -->
      <div v-if="testResult" class="test-result">
        <h3>测试结果</h3>
        <div v-html="formattedTestResult" class="test-result-content"></div>
      </div>
    </el-form>

    <!-- 测试历史 -->
    <div class="test-history">
      <div class="section-header">
        <h3>测试历史</h3>
        <el-button 
          type="primary" 
          plain 
          size="small" 
          @click="fetchTestHistory" 
          :loading="isLoadingHistory"
        >
          <el-icon><Refresh /></el-icon> 刷新
        </el-button>
      </div>
      
      <el-table 
        :data="testHistory" 
        style="width: 100%" 
        v-loading="isLoadingHistory"
        border
        stripe
        :header-cell-style="{ background: 'var(--el-fill-color-light)', color: 'var(--el-text-color-primary)' }"
      >
        <el-table-column prop="created_at" label="测试时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="model" label="模型" width="120">
          <template #default="{ row }">
            <el-tag size="small" :type="getModelTagType(row.model)">
              {{ row.model }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="template_name" label="模板名称" show-overflow-tooltip />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button 
              @click="viewTestDetail(scope.row)" 
              type="primary" 
              link
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="testHistory.length === 0 && !isLoadingHistory" class="empty-history">
        <el-empty description="暂无测试历史记录" />
      </div>
    </div>

    <!-- 测试详情对话框 -->
    <el-dialog
      v-model="showTestDetail"
      title="测试详情"
      width="80%"
      :close-on-click-modal="false"
      destroy-on-close
      top="5vh"
      :modal-class="'template-test-modal'"
    >
      <template #header>
        <div class="dialog-header">
          <h3>测试详情</h3>
          <div class="test-meta" v-if="currentTestDetail">
            <el-tag size="small">{{ currentTestDetail.template_name }}</el-tag>
            <el-tag size="small" :type="getModelTagType(currentTestDetail.model)">{{ currentTestDetail.model }}</el-tag>
            <span class="test-time">{{ formatDate(currentTestDetail?.created_at) }}</span>
          </div>
        </div>
      </template>
      
      <div class="test-detail" v-if="currentTestDetail">
        <el-tabs type="border-card">
          <el-tab-pane label="输出结果">
            <div class="detail-content result-content" v-html="formatMarkdown(currentTestDetail?.output_content)" />
          </el-tab-pane>
          <el-tab-pane label="输入数据">
            <div class="input-data">
              <el-descriptions :column="1" border>
                <el-descriptions-item v-for="(value, key) in currentTestDetail.input_data" :key="key" :label="key">
                  {{ value }}
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { runTemplateTest, getTemplateTests } from '@/api/templateTest'
import { getTemplateList } from '@/api/templates'
import type { Template } from '@/types'
import MarkdownIt from 'markdown-it'
import { Refresh } from '@element-plus/icons-vue'

// 配置MarkdownIt
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true
})
const templates = ref<Template[]>([])
const selectedTemplate = ref<Template | null>(null)
const variableInputs = ref<Record<string, string>>({})
const testResult = ref('')
const testHistory = ref([])
const isRunning = ref(false)
const isLoadingHistory = ref(false)
const showTestDetail = ref(false)
const currentTestDetail = ref(null)

const testForm = ref({
  template: '',
  model: '',
})

// 计算表单是否有效
const isFormValid = computed(() => {
  if (!testForm.value.template || !testForm.value.model) {
    return false
  }
  
  // 如果有选中的模板，检查所有必填变量是否都已填写
  if (selectedTemplate.value) {
    return selectedTemplate.value.variables.every(
      variable => !!variableInputs.value[variable.name]
    )
  }
  
  return false
})

// 格式化测试结果
const formattedTestResult = computed(() => {
  return md.render(testResult.value)
})

// 处理模板选择变化
const handleTemplateChange = (templateId: number) => {
  selectedTemplate.value = templates.value.find(t => t.id === templateId) || null
  // 重置变量输入
  variableInputs.value = {}
  // 如果模板有变量，初始化变量输入对象
  if (selectedTemplate.value) {
    selectedTemplate.value.variables.forEach(variable => {
      variableInputs.value[variable.name] = ''
    })
  }
}

// 使用默认值
const useDefaultValue = (variableName: string, defaultValue: string) => {
  variableInputs.value[variableName] = defaultValue
}

// 获取模板列表
const fetchTemplates = async () => {
  try {
    const response = await getTemplateList()
    if (response && response.results) {
      templates.value = response.results
    }
  } catch (error: any) {
    ElMessage.error('获取模板列表失败：' + (error.message || '未知错误'))
  }
}

// 获取测试历史
const fetchTestHistory = async () => {
  isLoadingHistory.value = true
  try {
    const response = await getTemplateTests({})
    // 处理分页响应结构
    if (response && Array.isArray(response.results)) {
      testHistory.value = response.results
    } else if (Array.isArray(response)) {
      testHistory.value = response
    } else {
      testHistory.value = []
      console.warn('意外的API响应格式:', response)
    }
  } catch (error: any) {
    ElMessage.error('获取测试历史失败：' + (error.message || '未知错误'))
    testHistory.value = []
  } finally {
    isLoadingHistory.value = false
  }
}

// 获取模型标签类型
const getModelTagType = (model: string) => {
  switch(model) {
    case 'GPT-4':
      return 'success'
    case 'GPT-3.5':
      return 'primary'
    case 'CLAUDE':
      return 'warning'
    default:
      return 'info'
  }
}

// 运行测试
const runTest = async () => {
  if (!isFormValid.value) {
    ElMessage.warning('请填写所有必需的字段')
    return
  }

  isRunning.value = true
  try {
    const response = await runTemplateTest({
      template: testForm.value.template,
      model: testForm.value.model,
      input_data: variableInputs.value
    })
    testResult.value = response.data.output_content
    ElMessage.success('测试运行成功')
    await fetchTestHistory()
  } catch (error: any) {
    ElMessage.error('测试运行失败：' + (error.message || '未知错误'))
  } finally {
    isRunning.value = false
  }
}

// 查看测试详情
const viewTestDetail = (row: any) => {
  currentTestDetail.value = row
  showTestDetail.value = true
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化JSON
const formatJson = (json: any) => {
  try {
    return JSON.stringify(json, null, 2)
  } catch {
    return json
  }
}

// 格式化Markdown
const formatMarkdown = (markdown: string) => {
  if (!markdown) return ''
  // 添加自定义样式类到渲染后的HTML
  const rendered = md.render(markdown)
  return `<div class="markdown-content">${rendered}</div>`
}

// 页面加载时获取数据
fetchTemplates()
fetchTestHistory()
</script>

<style lang="scss" scoped>
@use '@/styles/_variables.scss' as *;
.template-test {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.test-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.form-header {
  display: flex;
  gap: 16px;
}

.form-header .el-form-item {
  flex: 1;
}

.template-test h2 {
  font-family: 'Orbitron', sans-serif;
  font-weight: 600;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 28px;
  margin-bottom: 24px;
}

:deep(.el-form-item__label) {
  color: var(--el-text-color-primary) !important;
  font-weight: 500;
  font-size: 14px;
}

:deep(.el-select-dropdown__item) {
  color: var(--el-text-color-primary);
}

:deep(.el-select-dropdown__item.selected) {
  color: var(--el-color-primary);
  font-weight: 600;
}

:deep(.el-select__input) {
  color: var(--el-text-color-primary) !important;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset !important;
}

.template-option {
  padding: 8px 0;
}

.template-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.template-description {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.variables-section {
  padding: 20px;
  border-radius: 12px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  color: var(--text-primary);
}

.variables-section h3 {
  color: var(--primary-color);
  font-size: 18px;
  margin-bottom: 16px;
  font-family: 'Orbitron', sans-serif;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 8px;
}

.variables-description {
  margin-bottom: 20px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  padding: 12px;
  background-color: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.variable-input {
  position: relative;
}

.variable-input :deep(.el-input__wrapper) {
  background-color: var(--el-bg-color);
}

.variable-input :deep(.el-input__inner) {
  color: var(--el-text-color-primary);
  font-size: 14px;
}

.variable-input :deep(.el-input__inner::placeholder) {
  color: var(--el-text-color-placeholder);
}

.variable-label {
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.4;
}

.variable-description-inline {
  color: var(--el-text-color-secondary);
  font-size: 13px;
  font-weight: normal;
}

.preview-section {
  padding: 20px;
  border-radius: 12px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  color: var(--text-primary);
  margin-top: 16px;
}

.preview-section h3 {
  color: var(--primary-color);
  font-size: 18px;
  margin-bottom: 16px;
  font-family: 'Orbitron', sans-serif;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 8px;
}

.framework-content {
  margin-top: 16px;
}

.preview-item {
  margin-bottom: 16px;
}

.preview-label {
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--neon-blue);
  font-size: 14px;
}

.preview-text {
  padding: 12px;
  background: var(--bg-card);
  border-radius: 8px;
  white-space: pre-wrap;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.6;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.test-result {
  padding: 24px;
  border-radius: 12px;
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
}

.test-result :deep(h1),
.test-result :deep(h2),
.test-result :deep(h3),
.test-result :deep(h4),
.test-result :deep(h5),
.test-result :deep(h6) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  color: var(--el-text-color-primary);
}

.test-result :deep(h1) {
  font-size: 2em;
  margin-top: 0;
}

.test-result :deep(h2) {
  font-size: 1.5em;
}

.test-result :deep(h3) {
  font-size: 1.25em;
}

.test-result :deep(p) {
  margin-top: 0;
  margin-bottom: 16px;
  line-height: 1.6;
  color: var(--el-text-color-primary);
}

.test-result :deep(ul),
.test-result :deep(ol) {
  margin-top: 0;
  margin-bottom: 16px;
  padding-left: 2em;
  line-height: 1.6;
}

.test-result :deep(li) {
  margin-bottom: 8px;
}

.test-result :deep(code) {
  font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 90%;
  background-color: var(--bg-card);
  color: var(--text-primary);
  border-radius: 4px;
}

.test-result :deep(pre) {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: var(--el-fill-color);
  border-radius: 6px;
  margin-bottom: 16px;
}

.test-result :deep(pre code) {
  display: block;
  padding: 1em;
  margin: 0;
  overflow: auto;
  line-height: 1.5;
  word-wrap: normal;
  background-color: var(--bg-dark);
  color: var(--text-primary);
  border-radius: 8px;
  font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
  font-size: 14px;
  border: 1px solid var(--border-color);
}

.test-result :deep(pre) {
  margin: 16px 0;
  padding: 0;
  background: transparent;
}

.test-result :deep(table) {
  border-spacing: 0;
  border-collapse: collapse;
  margin-top: 0;
  margin-bottom: 16px;
  width: 100%;
}

.test-result :deep(table th),
.test-result :deep(table td) {
  padding: 6px 13px;
  border: 1px solid var(--el-border-color);
}

.test-result :deep(table th) {
  font-weight: 600;
  background-color: var(--el-fill-color-lighter);
}

.test-result :deep(blockquote) {
  padding: 0 1em;
  color: var(--el-text-color-secondary);
  border-left: 0.25em solid var(--el-border-color-darker);
  margin-bottom: 16px;
}

.test-result :deep(hr) {
  height: 0.25em;
  padding: 0;
  margin: 24px 0;
  background-color: var(--el-border-color);
  border: 0;
}

.test-history {
  border-top: 1px solid var(--el-border-color);
  padding-top: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  margin: 0;
  font-family: 'Orbitron', sans-serif;
  font-weight: 600;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 20px;
}

.empty-history {
  margin: 40px 0;
}

@media (max-width: 768px) {
  .form-header {
    flex-direction: column;
  }
}

.test-detail {
  .detail-section {
    margin-bottom: 20px;

    h4 {
      margin-bottom: 12px;
      color: var(--el-text-color-primary);
    }

    .detail-content {
      padding: 16px;
      background-color: var(--el-fill-color-lighter);
      border-radius: 4px;
      white-space: pre-wrap;
    }
  }
}

.dialog-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  
  h3 {
    margin: 0;
    font-size: 20px;
    font-family: 'Orbitron', sans-serif;
    font-weight: 600;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .test-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    
    .test-time {
      color: var(--el-text-color-secondary);
      font-size: 13px;
    }
  }
}

.result-content {
  max-height: 60vh;
  overflow-y: auto;
  padding: 20px;
}

.input-data {
  padding: 16px;
}

:deep(.el-tabs__item) {
  color: var(--el-text-color-primary);
  font-weight: 500;
}

:deep(.el-tabs__item.is-active) {
  color: var(--el-color-primary);
  font-weight: 600;
}

:deep(.el-descriptions__label) {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

:deep(.el-descriptions__content) {
  color: var(--el-text-color-regular);
}

.detail-content :deep(h1),
.detail-content :deep(h2),
.detail-content :deep(h3),
.detail-content :deep(h4),
.detail-content :deep(h5),
.detail-content :deep(h6) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  color: var(--el-text-color-primary);
}

.detail-content :deep(p) {
  margin-top: 0;
  margin-bottom: 16px;
  line-height: 1.6;
}

.detail-content :deep(ul),
.detail-content :deep(ol) {
  margin-top: 0;
  margin-bottom: 16px;
  padding-left: 2em;
  line-height: 1.6;
}

.detail-content :deep(li) {
  margin-bottom: 8px;
}

.detail-content :deep(code) {
  font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(175, 184, 193, 0.2);
  border-radius: 6px;
}

.detail-content :deep(pre) {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: var(--el-fill-color);
  border-radius: 6px;
  margin-bottom: 16px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.markdown-body) {
  background-color: transparent;
}

:deep(.markdown-content) {
  font-size: 16px;
  line-height: 1.8;
  color: var(--el-text-color-primary);
}

.test-result-content {
  padding: 16px;
  background-color: var(--el-bg-color-page);
  border-radius: 6px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}
</style>