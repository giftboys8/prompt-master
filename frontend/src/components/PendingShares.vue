<template>
  <div class="pending-shares">
    <el-dialog
      v-model="dialogVisible"
      title="待处理的共享请求"
      width="600px"
      destroy-on-close
      :before-close="handleClose"
    >
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
      </div>
      <div v-else-if="pendingShares.length === 0" class="empty-container">
        <el-empty description="暂无待处理的共享请求" />
      </div>
      <div v-else class="shares-list">
        <el-table :data="pendingShares" style="width: 100%">
          <el-table-column prop="template_name" label="模板名称" />
          <el-table-column prop="created_by.username" label="分享者" />
          <el-table-column prop="can_edit" label="权限">
            <template #default="{ row }">
              <el-tag :type="row.can_edit ? 'success' : 'info'">
                {{ row.can_edit ? '可编辑' : '只读' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button
                type="success"
                size="small"
                @click="handleAccept(row)"
              >
                接受
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleReject(row)"
              >
                拒绝
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getPendingShares, acceptShare, rejectShare } from '@/api/share'
import type { SharedTemplate } from '@/types'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'refresh'): void
}>()

const dialogVisible = ref(props.modelValue)
const loading = ref(false)
const pendingShares = ref<SharedTemplate[]>([])

// 监听对话框可见性
watch(() => props.modelValue, (val) => {
  dialogVisible.value = val
})

watch(dialogVisible, (val) => {
  emit('update:modelValue', val)
})

// 加载待处理的共享请求
const loadPendingShares = async () => {
  loading.value = true
  try {
    const response = await getPendingShares()
    pendingShares.value = response
  } catch (error) {
    ElMessage.error('获取待处理共享请求失败')
  } finally {
    loading.value = false
  }
}

// 处理关闭对话框
const handleClose = () => {
  emit('update:modelValue', false)
}

// 接受共享请求
const handleAccept = async (share: SharedTemplate) => {
  try {
    await acceptShare(share.id)
    ElMessage.success('已接受共享请求')
    await loadPendingShares()
    emit('refresh')
  } catch (error) {
    ElMessage.error('接受共享请求失败')
  }
}

// 拒绝共享请求
const handleReject = async (share: SharedTemplate) => {
  try {
    await rejectShare(share.id)
    ElMessage.success('已拒绝共享请求')
    await loadPendingShares()
    emit('refresh')
  } catch (error) {
    ElMessage.error('拒绝共享请求失败')
  }
}

// 组件挂载时加载数据
onMounted(() => {
  if (dialogVisible.value) {
    loadPendingShares()
  }
})

// 监听对话框打开，重新加载数据
watch(dialogVisible, (val) => {
  if (val) {
    loadPendingShares()
  }
})
</script>

<style scoped>
.pending-shares {
  .loading-container,
  .empty-container {
    padding: 20px;
    text-align: center;
  }

  .shares-list {
    margin-top: 10px;
  }
}
</style>