<template>
  <div class="template-test">
    <div class="page-header">
      <h2>模板测试</h2>
      <el-button @click="router.push({ name: 'template-list' })" type="primary" plain>
        <el-icon><Back /></el-icon>
        返回列表
      </el-button>
    </div>
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

      <!-- 测试结果 -->
      <div v-if="testResult" class="test-result">
        <h3>测试结果</h3>
        <div v-html="formattedTestResult" class="test-result-content"></div>
      </div>
    </el-form>

    <!-- 历史记录 -->
    <div class="test-history">
      <h3>历史记录</h3>
      <el-empty v-if="!isLoadingHistory && (!testHistory || testHistory.length === 0)" description="暂无测试记录" />
      <el-table
        v-else
        v-loading="isLoadingHistory"
        :data="testHistory"
        style="width: 100%"
        stripe
      >
        <el-table-column
          prop="created_at"
          label="测试时间"
          width="180"
          :formatter="(row) => new Date(row.created_at).toLocaleString()"
        />
        <el-table-column
          label="模型"
          width="120"
        >
          <template #default="{ row }">
            {{ getModelName(row) }}
          </template>
        </el-table-column>
        <el-table-column
          label="输入数据"
          min-width="200"
        >
          <template #default="{ row }">
            <el-tooltip
              effect="dark"
              :content="JSON.stringify(row.input_data, null, 2)"
              placement="top"
            >
              <div class="input-data-preview">
                {{ JSON.stringify(row.input_data) }}
              </div>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          label="输出内容"
          min-width="300"
        >
          <template #default="{ row }">
            <div class="output-content-preview">
              {{ parseTestResult(row.output_content)?.answer || row.output_content }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="100"
        >
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click="showHistoryDetail(row)"
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 历史记录详情对话框 -->
    <el-dialog
      v-model="historyDetailVisible"
      title="测试记录详情"
      width="800px"
      destroy-on-close
      class="history-detail-dialog"
    >
      <template v-if="selectedHistoryRecord">
        <div class="detail-section">
          <h4>测试时间</h4>
          <div class="detail-content">
            {{ new Date(selectedHistoryRecord.created_at).toLocaleString() }}
          </div>
        </div>

        <div class="detail-section">
          <h4>使用模型</h4>
          <div class="detail-content">
            {{ getModelName(selectedHistoryRecord) }}
          </div>
        </div>

        <div class="detail-section">
          <h4>输入变量</h4>
          <div class="detail-content code-block">
            <pre>{{ JSON.stringify(selectedHistoryRecord.input_data, null, 2) }}</pre>
          </div>
        </div>

        <div class="detail-section">
          <h4>生成的提示词</h4>
          <div class="detail-content code-block">
            <pre>{{ parseTestResult(selectedHistoryRecord.output_content)?.prompt || '未找到提示词' }}</pre>
          </div>
        </div>

        <div class="detail-section">
          <h4>输出内容</h4>
          <div class="detail-content markdown-content" v-html="formatMarkdown(parseTestResult(selectedHistoryRecord.output_content)?.answer || selectedHistoryRecord.output_content)" />
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { Back } from '@element-plus/icons-vue'
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getTemplateList } from '@/api/templates'
import { sendMessage } from '@/api/dify'
import type { Template, TemplateTest as ITemplateTest } from '@/types'
import MarkdownIt from 'markdown-it'
import { getTemplateTests, saveTemplateTest } from '@/api/templates'

const router = useRouter()
const route = useRoute()

// 接收路由参数
defineProps<{
  id?: string | number
}>()
const md = new MarkdownIt({
  linkify: true,
  typographer: true,
  breaks: true
})
const templates = ref<Template[]>([])
const selectedTemplate = ref<Template | null>(null)
const variableInputs = ref<Record<string, string>>({})
const testResult = ref('')
const isRunning = ref(false)
const testHistory = ref<ITemplateTest[]>([])
const isLoadingHistory = ref(false)
const historyDetailVisible = ref(false)
const selectedHistoryRecord = ref<ITemplateTest | null>(null)

const parseTestResult = (content: string) => {
  try {
    return JSON.parse(content)
  } catch (e) {
    return null
  }
}

const testForm = ref({
  template: ''
})

// 计算表单是否有效
const isFormValid = computed(() => {
  if (!testForm.value.template) {
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
const handleTemplateChange = async (templateId: number) => {
  const template = templates.value.find(t => t.id === templateId) || null
  selectedTemplate.value = template
  
  // 重置变量输入
  variableInputs.value = {}
  testResult.value = ''
  
  // 如果模板有变量，初始化变量输入对象
  if (selectedTemplate.value) {
    selectedTemplate.value.variables.forEach(variable => {
      variableInputs.value[variable.name] = ''
    })
  }
  
  // 获取测试历史
  await fetchTestHistory()
  
  // 调试输出
  console.log('选中模板:', selectedTemplate.value)
  if (selectedTemplate.value) {
    console.log('模板内容类型:', typeof selectedTemplate.value.content)
    console.log('模板内容:', selectedTemplate.value.content)
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
      console.log('获取到的模板列表:', templates.value)
    }
  } catch (error: any) {
    ElMessage.error('获取模板列表失败：' + (error.message || '未知错误'))
  }
}

// 生成提示词
const generatePrompt = (template: Template, variables: Record<string, string>) => {
  let prompt = ''
  
  if (template.framework_type === 'RTGO') {
    prompt = `角色：${template.content.role}\n`
    prompt += `任务：${template.content.task}\n`
    prompt += `目标：${template.content.goal}\n`
    prompt += `输出：${template.content.output}`
  } else if (template.framework_type === 'SPAR') {
    prompt = `情境：${template.content.situation}\n`
    prompt += `目的：${template.content.purpose}\n`
    prompt += `行动：${template.content.action}\n`
    prompt += `结果：${template.content.result}`
  } else {
    prompt = template.content.custom || ''
  }

  // 替换变量
  Object.entries(variables).forEach(([key, value]) => {
    prompt = prompt.replace(new RegExp(`{{${key}}}`, 'g'), value)
  })

  return prompt
}

// 运行测试
const runTest = async () => {
  if (!isFormValid.value || !selectedTemplate.value) {
    ElMessage.warning('请填写所有必需的字段')
    return
  }

  isRunning.value = true
  testResult.value = ''
  isLoadingHistory.value = true // 添加历史记录的加载状态
  try {
    // 生成提示词
    const prompt = generatePrompt(selectedTemplate.value, variableInputs.value)
    
    // 检查环境变量
    if (!import.meta.env.VITE_DIFY_API_BASE_URL) {
      throw new Error('Dify API基础URL未配置，请检查环境变量')
    }
    
    if (!import.meta.env.VITE_DIFY_API_KEY) {
      throw new Error('Dify API密钥未配置，请检查环境变量')
    }
    
    console.log('发送请求到Dify API:', import.meta.env.VITE_DIFY_API_BASE_URL + '/chat-messages')

    // 调用Dify API
    const response = await sendMessage({
      query: prompt,
      inputs: variableInputs.value,
      response_mode: 'blocking',
      user: 'template_test_user'
    })

    // 打印完整的响应数据，便于调试
    console.log('Dify API 完整响应:', response)

    // 检查响应数据的完整性
    if (!response || typeof response !== 'object') {
      throw new Error('API响应格式不正确：未收到响应数据')
    }

    // 检查是否有错误信息
    if (response.error) {
      throw new Error(`API返回错误：${response.error}`)
    }

    // 检查必要字段
    const answer = response.answer
    if (typeof answer !== 'string') {
      console.error('API响应数据:', response)
      throw new Error('API响应格式不正确：answer字段格式错误')
    }

    testResult.value = answer
    
    // 保存测试记录到后端数据库
    try {
      console.log('正在保存测试记录到数据库...');
      await saveTemplateTest({
        template: selectedTemplate.value.id,
        model: response.metadata?.model || 'Dify API',
        input_data: variableInputs.value,
        dify_response: response
      });
      console.log('测试记录保存成功');
      ElMessage.success('测试运行成功，记录已保存');
    } catch (saveError) {
      console.error('保存测试记录失败:', saveError);
      ElMessage.warning('测试结果已显示，但保存记录失败');
    }
    
    // 刷新测试历史记录
    try {
      await fetchTestHistory()
    } catch (error) {
      console.error('刷新历史记录失败:', error)
      ElMessage.warning('历史记录更新可能不完整')
    }
  } catch (error: any) {
    let errorMessage = error.message || '未知错误'
    
    // 处理API错误响应
    if (error.response) {
      const responseData = error.response.data
      if (responseData && responseData.error) {
        errorMessage = `API错误：${responseData.error}`
      } else {
        errorMessage = `API错误：${error.response.status} - ${error.response.statusText || '未知错误'}`
      }
    }
    ElMessage.error('测试运行失败：' + errorMessage)
    console.error('测试运行错误:', error)
    
    // 显示更详细的错误信息
    if (error.response) {
      console.error('API响应状态:', error.response.status)
      console.error('API响应数据:', error.response.data)
    }
    
    // 在测试结果区域显示错误信息
    testResult.value = `## 错误信息\n\n测试运行失败: ${errorMessage}\n\n请检查以下可能的问题:\n\n- Dify API密钥是否正确\n- API服务器是否可访问\n- 网络连接是否正常`
  } finally {
    isRunning.value = false
    isLoadingHistory.value = false // 无论成功与否都要关闭加载状态
  }
}

// 获取测试历史
const fetchTestHistory = async () => {
  if (!selectedTemplate.value) return
  
  isLoadingHistory.value = true
  try {
    console.log('开始获取测试历史，模板ID:', selectedTemplate.value.id)
    const response = await getTemplateTests({ template: selectedTemplate.value.id })
    console.log('获取到的测试历史:', response)
    testHistory.value = response.results || []
  } catch (error: any) {
    console.error('获取测试历史失败:', error)
    ElMessage.error('获取测试历史失败：' + (error.message || '未知错误'))
  } finally {
    isLoadingHistory.value = false
  }
}

// 该函数已合并到上方的handleTemplateChange中

// 监听模板列表变化，当有初始模板ID时自动选中
watch(templates, (newTemplates) => {
  const templateId = route.params.id
  if (templateId && newTemplates.length > 0) {
    const template = newTemplates.find(t => t.id === Number(templateId))
    if (template) {
      testForm.value.template = template.id
      handleTemplateChange(template.id)
    }
  }
}, { immediate: true })

// 监听selectedTemplate变化
watch(selectedTemplate, (newTemplate) => {
  if (newTemplate) {
    console.log('模板内容类型:', typeof newTemplate.content)
    console.log('模板内容:', newTemplate.content)
  }
})

// 页面加载时获取数据
onMounted(() => {
  fetchTemplates()
})

// 在组件卸载前清理状态
const cleanup = () => {
  selectedTemplate.value = null
  testResult.value = ''
  variableInputs.value = {}
  testHistory.value = []
  testForm.value.template = ''
  templates.value = []
  selectedHistoryRecord.value = null
  historyDetailVisible.value = false
}

// 定义formatMarkdown函数
const formatMarkdown = (content: string) => {
  return content ? md.render(content) : ''
}

// 获取模型名称
const getModelName = (record: ITemplateTest) => {
  if (record.model) {
    return record.model
  }
  // 如果没有model字段，尝试从dify_response中获取
  if (record.dify_response && typeof record.dify_response === 'object') {
    return record.dify_response.model || 'Dify API'
  }
  return 'Dify API'
}

// 定义开发环境变量
const isDevelopment = import.meta.env.DEV

// 使用onMounted和onUnmounted来处理组件生命周期
import { onUnmounted } from 'vue'

// 显示历史记录详情
const showHistoryDetail = (record: ITemplateTest) => {
  selectedHistoryRecord.value = record
  historyDetailVisible.value = true
}

// 在组件卸载时进行清理
onUnmounted(() => {
  cleanup()
})
</script>

<style lang="scss" scoped>
@use '@/styles/_variables.scss' as *;
.template-test {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  min-height: 100vh;
  background: var(--bg-main);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
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
  margin-top: 32px;
}

.input-data-preview {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

.output-content-preview {
  max-height: 100px;
  overflow: hidden;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40px;
    background: linear-gradient(transparent, var(--el-bg-color));
  }
}

/* 历史记录详情对话框样式 */
:deep(.history-detail-dialog .el-dialog__header) {
  border-bottom: 1px solid var(--el-border-color-lighter);
  padding-bottom: 16px;
  margin-bottom: 0;
}

:deep(.history-detail-dialog .el-dialog__body) {
  padding: 20px;
  max-height: 70vh;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.detail-content {
  padding: 12px;
  background-color: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.code-block {
  background-color: var(--bg-dark);
  font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
}

.code-block pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: var(--text-primary);
}

.markdown-content {
  padding: 16px;
  background-color: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.8;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3),
.markdown-content :deep(h4),
.markdown-content :deep(h5),
.markdown-content :deep(h6) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  color: var(--el-text-color-primary);
}

.markdown-content :deep(p) {
  margin-top: 0;
  margin-bottom: 16px;
  line-height: 1.6;
}

.markdown-content :deep(pre) {
  padding: 16px;
  overflow: auto;
  font-size: 85%;
  line-height: 1.45;
  background-color: var(--bg-dark);
  border-radius: 6px;
  margin-bottom: 16px;
}

.markdown-content :deep(code) {
  font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 90%;
  background-color: var(--bg-dark);
  color: var(--text-primary);
  border-radius: 4px;
}
</style>