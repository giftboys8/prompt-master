<template>
  <div class="template-test-container">
    <div class="template-test-header">
      <h1>模板测试</h1>
      <p v-if="template">当前测试: {{ template.name }}</p>
      <div v-else class="template-select">
        <FrameworkSelect v-model="selectedFramework" />
        <a-select
          v-model:value="selectedTemplateId"
          placeholder="选择模板"
          style="width: 250px"
          :loading="templatesLoading"
          @change="loadTemplate"
        >
          <a-select-option v-for="item in templates" :key="item.id" :value="item.id">
            {{ item.name }}
          </a-select-option>
        </a-select>
      </div>
    </div>

    <div class="template-test-content">
      <div class="template-form">
        <template v-if="template">
          <div class="template-preview">
            <div class="template-info">
              <h2>{{ template.name }}</h2>
              <p class="description">{{ template.description }}</p>
              <div class="tags">
                <a-tag v-if="template.framework_type">{{ template.framework_type }}</a-tag>
                <a-tag v-if="template.category">{{ template.category }}</a-tag>
              </div>
            </div>
            
            <a-form
              :model="formState"
              layout="vertical"
            >
              <div v-for="(field, index) in template.variables" :key="index" class="form-field">
                <a-form-item :label="field.name" :name="field.key">
                  <a-input
                    v-if="field.type === 'text'"
                    v-model:value="formState[field.key]"
                    :placeholder="field.description || `请输入${field.name}`"
                  />
                  <a-textarea
                    v-else-if="field.type === 'textarea'"
                    v-model:value="formState[field.key]"
                    :placeholder="field.description || `请输入${field.name}`"
                    :rows="4"
                  />
                  <a-select
                    v-else-if="field.type === 'select'"
                    v-model:value="formState[field.key]"
                    :placeholder="field.description || `请选择${field.name}`"
                  >
                    <a-select-option 
                      v-for="(option, optIndex) in field.options" 
                      :key="optIndex" 
                      :value="option.value"
                    >
                      {{ option.label }}
                    </a-select-option>
                  </a-select>
                  <a-radio-group 
                    v-else-if="field.type === 'radio'"
                    v-model:value="formState[field.key]"
                  >
                    <a-radio 
                      v-for="(option, optIndex) in field.options" 
                      :key="optIndex" 
                      :value="option.value"
                    >
                      {{ option.label }}
                    </a-radio>
                  </a-radio-group>
                </a-form-item>
              </div>
            </a-form>
          </div>

          <div class="action-buttons">
            <a-button type="primary" @click="generatePrompt" :loading="generating">
              生成提示词
            </a-button>
            <a-button @click="resetForm">
              重置
            </a-button>
          </div>
        </template>
        <div v-else-if="!selectedTemplateId" class="empty-state">
          <a-empty description="请选择一个模板进行测试" />
        </div>
        <div v-else-if="templateLoading" class="loading-state">
          <a-spin tip="加载模板中..." />
        </div>
      </div>

      <div class="result-panel">
        <div class="result-header">
          <h3>生成结果</h3>
          <div class="result-actions">
            <a-tooltip title="复制到剪贴板">
              <a-button 
                type="text" 
                :disabled="!generatedPrompt" 
                @click="copyToClipboard"
              >
                <template #icon><CopyOutlined /></template>
              </a-button>
            </a-tooltip>
          </div>
        </div>
        <a-spin :spinning="generating">
          <div 
            class="result-content" 
            :class="{ 'has-content': generatedPrompt }"
          >
            <pre v-if="generatedPrompt">{{ generatedPrompt }}</pre>
            <a-empty v-else description="填写表单并点击生成按钮" />
          </div>
        </a-spin>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { message } from 'ant-design-vue';
import { CopyOutlined } from '@ant-design/icons-vue';
import FrameworkSelect from '@/components/FrameworkSelect.vue';
import { useTemplateCache } from '@/hooks/useTemplateCache';
import { getTemplates, getTemplate } from '@/api/templates';
import type { Template } from '@/types';

const route = useRoute();
const { getFromCache, saveToCache } = useTemplateCache();

// 状态变量
const template = ref<Template | null>(null);
const templates = ref<Template[]>([]);
const selectedTemplateId = ref<string | null>(route.params.id as string || null);
const selectedFramework = ref<string | null>(null);
const templatesLoading = ref(false);
const templateLoading = ref(false);
const generating = ref(false);
const generatedPrompt = ref('');
const formState = reactive<Record<string, any>>({});

// 加载模板列表
const loadTemplates = async () => {
  try {
    templatesLoading.value = true;
    const response = await getTemplates({
      framework_id: selectedFramework.value || undefined,
      page: 1,
      page_size: 100
    });
    templates.value = response.data.results;
  } catch (error) {
    message.error('加载模板列表失败');
  } finally {
    templatesLoading.value = false;
  }
};

// 加载单个模板
const loadTemplate = async (id: string) => {
  try {
    templateLoading.value = true;
    
    // 尝试从缓存获取
    const cachedTemplate = getFromCache(id);
    if (cachedTemplate) {
      template.value = cachedTemplate;
      initFormState();
      templateLoading.value = false;
      return;
    }
    
    const response = await getTemplate(id);
    template.value = response.data;
    saveToCache(response.data);
    initFormState();
  } catch (error) {
    message.error('加载模板失败');
    template.value = null;
  } finally {
    templateLoading.value = false;
  }
};

// 初始化表单状态
const initFormState = () => {
  if (!template.value) return;
  
  const newState: Record<string, any> = {};
  template.value.variables.forEach(variable => {
    newState[variable.key] = variable.default_value || '';
  });
  
  Object.assign(formState, newState);
};

// 生成提示词
const generatePrompt = () => {
  if (!template.value) return;
  
  generating.value = true;
  
  try {
    let content = template.value.content;
    
    // 替换变量
    for (const variable of template.value.variables) {
      const value = formState[variable.key] || '';
      const regex = new RegExp(`\\{\\{\\s*${variable.key}\\s*\\}\\}`, 'g');
      content = content.replace(regex, value);
    }
    
    generatedPrompt.value = content;
    
    // 模拟API调用延迟
    setTimeout(() => {
      generating.value = false;
    }, 500);
  } catch (error) {
    message.error('生成提示词失败');
    generating.value = false;
  }
};

// 重置表单
const resetForm = () => {
  initFormState();
  generatedPrompt.value = '';
};

// 复制到剪贴板
const copyToClipboard = () => {
  if (!generatedPrompt.value) return;
  
  navigator.clipboard.writeText(generatedPrompt.value)
    .then(() => {
      message.success('已复制到剪贴板');
    })
    .catch(err => {
      message.error('复制失败');
    });
};

// 监听框架变化
watch(selectedFramework, () => {
  loadTemplates();
});

// 组件挂载时执行
onMounted(() => {
  loadTemplates();
  
  if (selectedTemplateId.value) {
    loadTemplate(selectedTemplateId.value);
  }
});
</script>

<style scoped lang="scss">
.template-test-container {
  padding: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.template-test-header {
  margin-bottom: 24px;
  
  h1 {
    margin-bottom: 8px;
    color: var(--text-primary);
  }
  
  .template-select {
    display: flex;
    gap: 16px;
    margin-top: 16px;
  }
}

.template-test-content {
  display: flex;
  gap: 24px;
  height: calc(100% - 100px);
  
  @media (max-width: 1024px) {
    flex-direction: column;
    height: auto;
  }
}

.template-form {
  flex: 1;
  background: var(--bg-component);
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  
  .template-preview {
    .template-info {
      margin-bottom: 24px;
      
      h2 {
        margin-bottom: 8px;
        color: var(--text-primary);
      }
      
      .description {
        color: var(--text-secondary);
        margin-bottom: 12px;
      }
      
      .tags {
        margin-top: 8px;
      }
    }
  }
  
  .form-field {
    margin-bottom: 16px;
  }
  
  .action-buttons {
    margin-top: 24px;
    display: flex;
    gap: 12px;
  }
  
  .empty-state, .loading-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px;
  }
}

.result-panel {
  flex: 1;
  background: var(--bg-component);
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  
  .result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    h3 {
      margin: 0;
      color: var(--text-primary);
    }
  }
  
  .result-content {
    flex: 1;
    background: var(--bg-code);
    border-radius: 6px;
    padding: 16px;
    overflow-y: auto;
    min-height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    &.has-content {
      justify-content: flex-start;
      align-items: flex-start;
    }
    
    pre {
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      color: var(--text-code);
      font-family: 'Fira Code', monospace, 'Courier New', Courier;
      width: 100%;
    }
  }
}

// 动画效果
.template-test-container {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.template-form, .result-panel {
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}

.action-buttons button {
  position: relative;
  overflow: hidden;
  
  &::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 5px;
    height: 5px;
    background: rgba(255, 255, 255, 0.5);
    opacity: 0;
    border-radius: 100%;
    transform: scale(1, 1) translate(-50%, -50%);
    transform-origin: 50% 50%;
  }
  
  &:focus:not(:active)::after {
    animation: ripple 0.6s ease-out;
  }
}

@keyframes ripple {
  0% {
    transform: scale(0, 0);
    opacity: 0.5;
  }
  20% {
    transform: scale(25, 25);
    opacity: 0.5;
  }
  100% {
    opacity: 0;
    transform: scale(40, 40);
  }
}
</style>