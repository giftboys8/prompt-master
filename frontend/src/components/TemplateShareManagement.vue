<template>
  <div class="template-share-management">
    <el-dialog
      v-model="dialogVisible"
      title="共享管理"
      width="600px"
      destroy-on-close
      :before-close="() => emit('update:modelValue', false)"
    >
      <div class="share-form">
        <div class="share-header">
          <!-- 移除顶部搜索框，因为已经在select中有搜索功能 -->
        </div>

        <div class="share-list">
          <el-table
            :data="shareList"
            style="width: 100%"
          >
            <el-table-column
              prop="shared_with.username"
              label="用户名"
              width="120"
            />
            <el-table-column
              prop="shared_with.email"
              label="邮箱"
              width="180"
            />
            <el-table-column
              prop="can_edit"
              label="权限"
              width="100"
            >
              <template #default="{ row }">
                <el-tag :type="row.can_edit ? 'success' : 'info'">
                  {{ row.can_edit ? '可编辑' : '只读' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              width="100"
            >
              <template #default="{ row }">
                <el-button
                  type="danger"
                  link
                  @click="handleRemoveShare(row)"
                >
                  移除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div class="share-form-add">
          <el-form
            :model="shareForm"
            label-width="80px"
            @submit.prevent="handleAddShare"
          >
            <el-form-item label="选择用户">
              <el-select
                v-model="shareForm.userId"
                filterable
                remote
                :remote-method="handleSearch"
                :loading="loading"
                placeholder="请输入用户名或邮箱搜索"
                clearable
                :reserve-keyword="true"
                :remote-show-suffix="false"
                :min-length="1"
              >
                <el-option
                  v-for="user in userList"
                  :key="user.id"
                  :label="`${user.username} (${user.email})`"
                  :value="user.id"
                >
                  <div style="display: flex; justify-content: space-between; align-items: center">
                    <span>{{ user.username }}</span>
                    <span class="user-email">{{ user.email }}</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="权限">
              <el-switch
                v-model="shareForm.canEdit"
                active-text="可编辑"
                inactive-text="只读"
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                @click="handleAddShare"
                :disabled="!shareForm.userId"
              >
                添加共享
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import type { User, SharedTemplate } from '@/types'
import {
  getUserList,
  getTemplateShares,
  addShare,
  deleteShare
} from '@/api/share'

const props = defineProps<{
  modelValue: boolean
  templateId: number
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'share-updated'): void
}>()

const dialogVisible = ref(false)
const searchQuery = ref('')
const userList = ref<User[]>([])
const shareList = ref<SharedTemplate[]>([])
const shareListLoading = ref(false)
const loading = ref(false)

const shareForm = ref({
  userId: null as number | null,
  canEdit: false
})

// 监听对话框显示状态
watch(
  () => props.modelValue,
  (val) => {
    dialogVisible.value = val
    if (val) {
      if (props.templateId && props.templateId > 0) {
        loadShareList()
      } else {
        console.warn('无效的模板ID，不加载共享列表')
        dialogVisible.value = false
      }
    } else {
      // 重置状态
      shareForm.value = { userId: null, canEdit: false }
      userList.value = []
      searchQuery.value = ''
    }
  }
)
const loadShareList = async () => {
  if (!props.templateId || props.templateId <= 0) {
    console.warn('无效的模板ID，无法加载共享列表')
    return
  }

  try {
    shareListLoading.value = true
    console.log('正在加载模板ID为', props.templateId, '的共享列表')
    const res = await getTemplateShares(props.templateId)
    console.log('获取到的共享列表:', res)
    shareList.value = res
  } catch (error: any) {
    console.error('加载共享列表失败:', error)
    ElMessage.error(error.message || '加载共享列表失败')
  } finally {
    shareListLoading.value = false
  }
}

// 搜索用户
const handleSearch = async (query: string) => {
  console.log('搜索查询:', query)
  if (!query || query.length < 1) {
    userList.value = []
    return
  }

  loading.value = true
  try {
    const response = await getUserList(query)
    console.log('搜索结果:', response)
    
    if (!response || !response.results) {
      throw new Error('搜索结果格式不正确')
    }
    
    // 使用返回的results数组，并过滤掉已经共享的用户
    userList.value = response.results.filter(
      user => !shareList.value.some(share => share.shared_with.id === user.id)
    )
    
    console.log('过滤后的用户列表:', userList.value)
  } catch (error: any) {
    console.error('搜索用户失败:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '搜索用户失败')
    userList.value = []
  } finally {
    loading.value = false
  }
}

// 添加共享
const handleAddShare = async () => {
  if (!shareForm.value.userId) return

  try {
    await addShare({
      template: props.templateId,
      shared_with_id: shareForm.value.userId,
      can_edit: shareForm.value.canEdit
    })
    ElMessage.success('添加共享成功')
    await loadShareList()
    shareForm.value.userId = null
    shareForm.value.canEdit = false
    emit('share-updated')
  } catch (error) {
    ElMessage.error('添加共享失败')
  }
}

// 移除共享
const handleRemoveShare = async (share: SharedTemplate) => {
  try {
    await deleteShare(props.templateId, share.shared_with.id)
    ElMessage.success('移除共享成功')
    await loadShareList()
    emit('share-updated')
  } catch (error) {
    ElMessage.error('移除共享失败')
  }
}

// 监听props
// 监听对话框可见性变化
watch(dialogVisible, (val) => {
  emit('update:modelValue', val)
})

// 初始化
onMounted(() => {
  if (props.modelValue) {
    loadShareList()
  }
})
</script>

<style scoped>
.template-share-management :deep(.share-header) {
  margin-bottom: 20px;
}

.template-share-management :deep(.share-list) {
  margin-bottom: 20px;
  max-height: 300px;
  overflow-y: auto;
}

.template-share-management :deep(.share-form-add) {
  border-top: 1px solid var(--el-border-color);
  padding-top: 20px;
}

.template-share-management :deep(.user-email) {
  margin-left: 10px;
  color: var(--el-text-color-secondary);
  font-size: 12px;
}
</style>