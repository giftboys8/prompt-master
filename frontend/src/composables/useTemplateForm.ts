import { ref, reactive, computed } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { Framework } from '@/api/frameworks'

export interface TemplateVariable {
  name: string
  default_value: string
  description: string
}

export interface TemplateContent {
  [key: string]: string
  custom?: string
}

export interface TemplateForm {
  name: string
  framework: Framework | null
  description: string
  content: TemplateContent
  variables: TemplateVariable[]
}

export interface UseTemplateFormOptions {
  initialData?: Partial<TemplateForm>
}

export function useTemplateForm(options: UseTemplateFormOptions = {}) {
  const formRef = ref<FormInstance>()
  const loading = ref(false)
  const submitting = ref(false)

  // 表单数据
  const form = reactive<TemplateForm>({
    name: options.initialData?.name || '',
    framework: options.initialData?.framework || null,
    description: options.initialData?.description || '',
    content: options.initialData?.content || {},
    variables: options.initialData?.variables || []
  })

  // 基础验证规则
  const baseRules = reactive<FormRules>({
    name: [
      { required: true, message: "请输入模版名称", trigger: "blur" },
      { min: 2, max: 50, message: "长度在 2 到 50 个字符", trigger: "blur" }
    ],
    framework: [
      { required: true, message: "请选择框架", trigger: "change" }
    ],
    description: [
      { required: true, message: "请输入模版描述", trigger: "blur" }
    ]
  })

  // 变量验证规则
  const variableRules = {
    name: [
      { required: true, message: "请输入变量名称", trigger: "blur" },
      {
        pattern: /^[a-zA-Z_][a-zA-Z0-9_]*$/,
        message: "变量名称只能包含字母、数字和下划线，且不能以数字开头",
        trigger: "blur"
      }
    ],
    default_value: [
      { required: true, message: "请输入默认值", trigger: "blur" }
    ],
    description: [
      { required: true, message: "请输入描述", trigger: "blur" }
    ]
  }

  // 动态内容验证规则
  const contentRules = computed(() => {
    const rules: Record<string, any> = {}
    
    if (form.framework?.modules?.length) {
      form.framework.modules.forEach(module => {
        const fieldName = `content.${module.name.toLowerCase()}`
        rules[fieldName] = [
          { required: true, message: `请输入${module.name}`, trigger: "blur" }
        ]
      })
    } else {
      rules["content.custom"] = [
        { required: true, message: "请输入自定义内容", trigger: "blur" }
      ]
    }
    
    return rules
  })

  // 合并所有验证规则
  const rules = computed(() => ({
    ...baseRules,
    ...contentRules.value
  }))

  // 重置内容
  const resetContent = () => {
    const newContent: TemplateContent = {}
    
    if (form.framework?.modules?.length) {
      form.framework.modules.forEach(module => {
        const key = module.name.toLowerCase()
        newContent[key] = form.content[key] || ''
      })
    } else {
      newContent.custom = form.content.custom || ''
    }
    
    form.content = newContent
  }

  // 添加变量
  const addVariable = () => {
    form.variables.push({
      name: '',
      default_value: '',
      description: ''
    })
  }

  // 删除变量
  const removeVariable = (index: number) => {
    form.variables.splice(index, 1)
  }

  // 处理框架变更
  const handleFrameworkChange = async (framework: Framework | null) => {
    form.framework = framework
    resetContent()
  }

  // 获取提交数据
  const getSubmissionData = () => {
    return {
      name: form.name,
      description: form.description,
      framework: form.framework?.id || null,
      content: { ...form.content },
      variables: form.variables,
      framework_type: form.framework ? form.framework.name : 'CUSTOM'
    }
  }

  // 表单验证
  const validate = () => {
    if (!formRef.value) return Promise.reject('表单实例未初始化')
    return formRef.value.validate()
  }

  return {
    form,
    formRef,
    rules,
    variableRules,
    loading,
    submitting,
    resetContent,
    addVariable,
    removeVariable,
    handleFrameworkChange,
    getSubmissionData,
    validate
  }
}