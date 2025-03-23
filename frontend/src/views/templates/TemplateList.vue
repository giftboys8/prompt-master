<template>
  <div class="page-container">
    <div class="page-header">
      <h1>提示词模板</h1>
      <div class="drag-tip">
        <el-alert
          title="提示：您可以通过拖拽卡片来调整模板的显示顺序"
          type="info"
          :closable="false"
          show-icon
        />
      </div>
    </div>

    <div class="operation-bar">
      <!-- 搜索栏组件 -->
      <template-search-bar @search="handleSearchParams" />
      
      <!-- 操作栏组件 -->
      <template-operation-bar
        @import="handleImport"
        @export="handleExport"
        @create="handleCreate"
      />
    </div>

    <!-- 模板列表 -->
    <el-row :gutter="20">
      <draggable
        v-model="sortedTemplates"
        v-loading="loading"
        item-key="id"
        :animation="150"
        ghost-class="ghost"
        @end="handleDragEnd"
        class="el-row template-grid"
        :class="{ 'is-flex': true, 'flex-wrap': true }"
      >
        <template #item="{ element: template }">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="4" class="mb-4">
            <template-card 
              :template="template"
              @edit="handleEdit"
              @test="handleTest"
              @history="handleVersionHistory"
              @clone="handleClone"
              @delete="handleDelete"
              @preview="handlePreview"
            />
          </el-col>
        </template>
      </draggable>
    </el-row>

    <!-- 分页器 -->
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 预览对话框 -->
    <template-preview
      v-model="previewVisible"
      :template="selectedTemplate"
      mode="dialog"
      @update:model-value="handlePreviewVisibleChange"
    />

    <!-- 版本历史对话框 -->
    <template-version-history
      v-model="versionHistoryVisible"
      :template-id="currentTemplate?.id || 0"
      @restored="loadData"
    />

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
      destroy-on-close
    >
      <p>确定要删除这个模板吗？此操作无法撤销。</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button 
            type="danger" 
            @click="confirmDelete" 
            :loading="deleteLoading"
          >
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import draggable from 'vuedraggable'

import TemplateCard from '@/components/templates/TemplateCard.vue'
import TemplateSearchBar from '@/components/templates/TemplateSearchBar.vue'
import TemplateOperationBar from '@/components/templates/TemplateOperationBar.vue'
import TemplateVersionHistory from '@/components/TemplateVersionHistory.vue'
import TemplatePreview from '@/components/TemplatePreview.vue'

import { useTemplateList } from '@/composables/useTemplateList'
import type { Template } from '@/types'

const router = useRouter()

// 使用组合式函数管理模板列表
const {
  loading,
  templates,
  sortedTemplates,
  total,
  currentPage,
  pageSize,
  loadData,
  updateOrder,
  importTemplate,
  exportTemplate,
  cloneTemplateItem,
  removeTemplate
} = useTemplateList()

// 搜索参数
const searchParams = ref({
  search: '',
  target_role: '',
  framework_type: ''
})

// 预览相关
const previewVisible = ref(false)
const selectedTemplate = ref<Template | null>(null)
const currentTemplate = ref<Template | null>(null)

// 版本历史相关
const versionHistoryVisible = ref(false)

// 删除相关
const deleteDialogVisible = ref(false)
const deleteLoading = ref(false)
const templateToDelete = ref<Template | null>(null)

// 处理搜索参数
const handleSearchParams = (params: { query: string, role: string, framework: string }) => {
  searchParams.value = {
    search: params.query,
    target_role: params.role,
    framework_type: params.framework
  }
  currentPage.value = 1
  loadData(searchParams.value)
}

// 处理拖拽结束
const handleDragEnd = async () => {
  await updateOrder()
}

// 导入模板
const handleImport = async (file: any) => {
  await importTemplate(file.raw)
}

// 导出模板
const handleExport = async () => {
  await exportTemplate()
}

// 创建模板
const handleCreate = () => {
  router.push('/templates/create')
}

// 编辑模板
const handleEdit = (template: Template) => {
  router.push({
    path: `/templates/${template.id}/edit`,
    query: { name: template.name }
  })
}

// 测试模板
const handleTest = (template: Template) => {
  router.push({
    name: 'template-test',
    params: { id: template.id }
  })
}

// 克隆模板
const handleClone = async (template: Template) => {
  await cloneTemplateItem(template.id)
}

// 打开版本历史
const handleVersionHistory = (template: Template) => {
  currentTemplate.value = template
  versionHistoryVisible.value = true
}

// 预览模板
const handlePreview = (template: Template) => {
  selectedTemplate.value = template
  previewVisible.value = true
}

// 处理预览弹窗的显示状态
const handlePreviewVisibleChange = (val: boolean) => {
  previewVisible.value = val
  if (!val) {
    selectedTemplate.value = null
  }
}

// 删除模板
const handleDelete = (template: Template) => {
  templateToDelete.value = template
  deleteDialogVisible.value = true
}

// 确认删除
const confirmDelete = async () => {
  if (!templateToDelete.value) return

  deleteLoading.value = true
  try {
    await removeTemplate(templateToDelete.value.id)
    deleteDialogVisible.value = false
  } finally {
    deleteLoading.value = false
  }
}

// 分页相关
const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadData(searchParams.value)
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadData(searchParams.value)
}

// 监听预览对话框关闭
watch(previewVisible, (val) => {
  if (!val) {
    selectedTemplate.value = null
  }
})

// 监听删除对话框关闭
watch(deleteDialogVisible, (val) => {
  if (!val) {
    templateToDelete.value = null
  }
})

// 初始化
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.drag-tip {
  margin-top: 10px;
}

.operation-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

@media (max-width: 768px) {
  .operation-bar {
    flex-direction: column;
  }
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

/* 拖拽时的样式 */
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
  border: 1px dashed #409EFF;
}

/* 模板网格布局 */
.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  width: 100%;
}

@media (max-width: 576px) {
  .template-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}

/* 工具类 */
.mb-4 {
  margin-bottom: 16px;
}

/* Flex 布局 */
.is-flex {
  display: flex;
}

.flex-wrap {
  flex-wrap: wrap;
}

/* 响应式布局辅助类 */
:deep(.el-row) {
  margin: 0 !important;
  width: 100%;
  justify-content: flex-start;
}

:deep(.draggable) {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
}

/* 卡片容器响应式间距 */
@media (max-width: 576px) {
  .el-col {
    padding: 0 8px !important;
  }
}

@media (min-width: 577px) and (max-width: 992px) {
  .el-col {
    padding: 0 12px !important;
  }
}

@media (min-width: 993px) {
  .el-col {
    padding: 0 15px !important;
  }
}
</style>