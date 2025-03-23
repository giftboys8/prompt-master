import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { getUserList, getTemplateShares, addShare, deleteShare } from '@/api/share'
import type { User, Template, SharedTemplate } from '@/types'

export interface ShareFormState {
  userId: number | undefined
  canEdit: boolean
}

export function useTemplateShare() {
  // 当前模板
  const currentTemplate = ref<Template | null>(null)
  // 状态管理
  const loading = ref(false)
  const shareLoading = ref(false)
  const shares = ref<SharedTemplate[]>([])
  const userOptions = ref<User[]>([])

  // 初始化表单状态
  const shareForm = ref<ShareFormState>({
    userId: undefined,
    canEdit: false
  })

  // 更新当前模板
  const updateTemplate = (template: Template | null) => {
    currentTemplate.value = template
  }

  // 加载已分享用户列表
  const loadShares = async () => {
    if (!currentTemplate.value || !currentTemplate.value.id) {
    ElMessage.error('模板信息不存在')
    return false
  }
  
  try {
    const response = await getTemplateShares(currentTemplate.value.id)
    // 确保每个分享项都包含模板名称
    shares.value = response.map(share => ({
      ...share,
      template_name: currentTemplate.value.name // 从当前模板对象中获取名称
    }))
    return true
  } catch (error: any) {
    ElMessage.error(error.response?.data?.message || '获取分享列表失败')
    return false
  }
}

  // 搜索用户（带防抖）
  let searchTimeout: NodeJS.Timeout | null = null
  const handleSearch = async (query: string) => {
    if (searchTimeout) {
      clearTimeout(searchTimeout)
    }

    if (!query) {
      userOptions.value = []
      return
    }

    loading.value = true
    searchTimeout = setTimeout(async () => {
      try {
        const response = await getUserList(query)
        userOptions.value = response.results.filter(user => 
          currentTemplate.value ? user.id !== currentTemplate.value.created_by : true
        )
      } catch (error) {
        ElMessage.error('搜索用户失败')
        userOptions.value = []
      } finally {
        loading.value = false
      }
    }, 300) // 300ms 防抖
  }

  // 分享模板
const handleShare = async () => {
  if (!shareForm.value.userId) {
    ElMessage.warning('请选择要分享的用户')
    return false
  }
  
  if (!currentTemplate.value || !currentTemplate.value.id) {
    ElMessage.error('模板信息不存在')
    return false
  }

  shareLoading.value = true
  try {
    await addShare({
      template: currentTemplate.value.id,
      shared_with_id: shareForm.value.userId,
      can_edit: shareForm.value.canEdit
    })
    ElMessage.success('分享成功')
    await loadShares()
    shareForm.value.userId = undefined
    return true
  } catch (error: any) {
    if (error.message === '模板信息不存在') {
      ElMessage.error('模板信息不存在')
    } else {
      ElMessage.error(error.response?.data?.message || '分享失败')
    }
    return false
  } finally {
    shareLoading.value = false
  }
}

  // 撤销分享
  const handleRevoke = async (share: SharedTemplate) => {
    if (!currentTemplate.value) {
      ElMessage.error('模板信息不存在')
      return false
    }

    try {
      await deleteShare(currentTemplate.value.id, share.shared_with.id)
      ElMessage.success('已撤销分享')
      await loadShares()
      return true
    } catch (error: any) {
      ElMessage.error(error.response?.data?.message || '撤销分享失败')
      return false
    }
  }

  // 重置状态
  const reset = () => {
    shareForm.value = {
      userId: undefined,
      canEdit: false
    }
    userOptions.value = []
    if (searchTimeout) {
      clearTimeout(searchTimeout)
    }
  }

  return {
    // 状态
    loading,
    updateTemplate,
    shareLoading,
    shares,
    userOptions,
    shareForm,

    // 方法
    loadShares,
    handleSearch,
    handleShare,
    handleRevoke,
    reset
  }
}