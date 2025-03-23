<template>
  <div class="template-test">
    <div class="page-header">
      <h2>模板测试</h2>
      <el-button @click="router.push({ name: 'template-list' })" type="primary" plain>
        <el-icon><Back /></el-icon>
        返回列表
      </el-button>
    </div>

    <!-- 选择模板部分 -->
    <template-selector 
      v-model="selectedTemplateId" 
      :templates="templates" 
      @change="handleTemplateChange"
    />

    <!-- 主要内容区域：两栏布局 -->
    <div class="main-content">
      <!-- 左侧：模板预览 -->
      <template-preview 
        :template="selectedTemplate" 
        mode="inline"
        class="preview-panel"
      />

      <!-- 右侧：变量设置 -->
      <div class="settings-panel">
        <template-variable-form
          v-if="selectedTemplate"
          :template="selectedTemplate"
          v-model:variables="variableInputs"
          v-model:apiKey="selectedApiKey"
          :is-running="isRunning"
          @run-test="runTest"
        />
      </div>
    </div>

    <!-- 测试结果 -->
    <div class="result-container">
      <template-test-result
        v-if="testResult"
        :result="testResult"
      />
    </div>

    <!-- 历史记录 -->
    <div class="history-container">
      <template-test-history
        :history="testHistory"
        :is-loading="isLoadingHistory"
        @view-detail="showHistoryDetail"
      />
    </div>

    <!-- 历史记录详情对话框 -->
    <template-history-detail
      v-model:visible="historyDetailVisible"
      :record="selectedHistoryRecord"
    />
  </div>
</template>

<script setup lang="ts">
import { Back } from '@element-plus/icons-vue'
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getTemplateList, getTemplateTests, saveTemplateTest } from '@/api/templates'
import { sendMessage } from '@/api/dify'
import type { Template, TemplateTest as ITemplateTest } from '@/types'

// 导入拆分的组件
import TemplateSelector from '@/components/TemplateSelector.vue'
import TemplatePreview from '@/components/TemplatePreview.vue'
import TemplateVariableForm from '@/components/TemplateVariableForm.vue'
import TemplateTestResult from '@/components/TemplateTestResult.vue'
import TemplateTestHistory from '@/components/TemplateTestHistory.vue'
import TemplateHistoryDetail from '@/components/TemplateHistoryDetail.vue'

const router = useRouter()
const route = useRoute()

// 接收路由参数
defineProps<{
  id?: string | number
}>()

// 状态管理
const templates = ref<Template[]>([])
const selectedTemplate = ref<Template | null>(null)
const selectedTemplateId = ref<number | null>(null)
const variableInputs = ref<Record<string, string>>({})
const selectedApiKey = ref<any>(null)
const testResult = ref('')
const isRunning = ref(false)
const testHistory = ref<ITemplateTest[]>([])
const isLoadingHistory = ref(false)
const historyDetailVisible = ref(false)
const selectedHistoryRecord = ref<ITemplateTest | null>(null)

// 处理模板选择变化
const handleTemplateChange = async (templateId: number) => {
  selectedTemplateId.value = templateId
  const template = templates.value.find(t => t.id === templateId) || null
  selectedTemplate.value = template
  
  // 重置变量输入和测试结果
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
  if (!selectedTemplate.value) {
    ElMessage.warning('请先选择一个模板')
    return
  }

  // 验证是否选择了API密钥
  if (!selectedApiKey.value) {
    ElMessage.warning('请选择一个API密钥')
    return
  }

  // 验证所有变量都已填写
  const allVariablesFilled = selectedTemplate.value.variables.every(
    variable => !!variableInputs.value[variable.name]
  )

  if (!allVariablesFilled) {
    ElMessage.warning('请填写所有必需的变量')
    return
  }

  isRunning.value = true
  testResult.value = ''
  isLoadingHistory.value = true
  
  try {
    const prompt = generatePrompt(selectedTemplate.value, variableInputs.value)
    
    if (!import.meta.env.VITE_DIFY_API_BASE_URL) {
      throw new Error('Dify API基础URL未配置，请检查环境变量')
    }

    const response = await sendMessage({
      query: prompt,
      inputs: variableInputs.value,
      response_mode: 'blocking',
      user: 'template_test_user'
    }, selectedApiKey.value.key)

    if (!response || typeof response !== 'object') {
      throw new Error('API响应格式不正确：未收到响应数据')
    }

    if (response.error) {
      throw new Error(`API返回错误：${response.error}`)
    }

    const answer = response.answer
    if (typeof answer !== 'string') {
      throw new Error('API响应格式不正确：answer字段格式错误')
    }

    testResult.value = answer
    
    try {
      await saveTemplateTest({
        template: selectedTemplate.value.id,
        model: response.metadata?.model || 'Dify API',
        input_data: variableInputs.value,
        dify_response: response
      })
      ElMessage.success('测试运行成功，记录已保存')
    } catch (saveError) {
      ElMessage.warning('测试结果已显示，但保存记录失败')
    }
    
    await fetchTestHistory()
  } catch (error: any) {
    let errorMessage = error.message || '未知错误'
    
    if (error.response) {
      const responseData = error.response.data
      errorMessage = responseData?.error 
        ? `API错误：${responseData.error}`
        : `API错误：${error.response.status} - ${error.response.statusText || '未知错误'}`
    }
    
    ElMessage.error('测试运行失败：' + errorMessage)
    testResult.value = `## 错误信息\n\n测试运行失败: ${errorMessage}\n\n请检查以下可能的问题:\n\n- Dify API密钥是否正确\n- API服务器是否可访问\n- 网络连接是否正常`
  } finally {
    isRunning.value = false
    isLoadingHistory.value = false
  }
}

// 获取测试历史
const fetchTestHistory = async () => {
  if (!selectedTemplate.value) return
  
  isLoadingHistory.value = true
  try {
    const response = await getTemplateTests({ template: selectedTemplate.value.id })
    testHistory.value = response.results || []
  } catch (error: any) {
    console.error('获取测试历史失败:', error)
    ElMessage.error('获取测试历史失败：' + (error.message || '未知错误'))
  } finally {
    isLoadingHistory.value = false
  }
}

// 显示历史记录详情
const showHistoryDetail = (record: ITemplateTest) => {
  selectedHistoryRecord.value = record
  historyDetailVisible.value = true
}

// 监听模板列表变化
watch(templates, (newTemplates) => {
  const templateId = route.params.id
  if (templateId && newTemplates.length > 0) {
    const template = newTemplates.find(t => t.id === Number(templateId))
    if (template) {
      selectedTemplateId.value = template.id
      handleTemplateChange(template.id)
    }
  }
}, { immediate: true })

// 页面加载时获取数据
onMounted(() => {
  fetchTemplates()
})

// 在组件卸载前清理状态
const cleanup = () => {
  selectedTemplate.value = null
  selectedTemplateId.value = null
  testResult.value = ''
  variableInputs.value = {}
  testHistory.value = []
  templates.value = []
  selectedHistoryRecord.value = null
  historyDetailVisible.value = false
  selectedApiKey.value = null
}

// 在组件卸载时进行清理
onUnmounted(cleanup)
</script>

<style lang="scss" scoped>
.template-test {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;

    h2 {
      color: var(--primary-color);
      font-size: 24px;
      font-family: 'Orbitron', sans-serif;
      margin: 0;
    }
  }

  .main-content {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 24px;
    margin-top: 24px;
    margin-bottom: 24px;

    .preview-panel {
      height: 100%;
      min-width: 0;
    }

    .settings-panel {
      height: 100%;
      min-width: 0;
    }
  }
  
  .result-container {
    margin-bottom: 24px;
    width: 100%;
  }
  
  .history-container {
    margin-top: 24px;
    width: 100%;
  }
}
</style>