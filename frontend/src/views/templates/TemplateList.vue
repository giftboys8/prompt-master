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
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索模板名称"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
      </div>
      <div class="operation-buttons">
        <el-upload
          :auto-upload="false"
          :show-file-list="false"
          accept=".json"
          @change="handleImport"
        >
          <el-button type="primary">
            <el-icon><Upload /></el-icon>导入
          </el-button>
        </el-upload>
        <el-button type="primary" @click="handleExport">
          <el-icon><Download /></el-icon>导出
        </el-button>
        <el-button type="primary" @click="router.push('/templates/create')">
          <el-icon><Plus /></el-icon>新增模板
        </el-button>
      </div>
    </div>

    <el-row :gutter="20">
  <draggable
    v-model="sortedTemplates"
    v-loading="loading"
    item-key="id"
    :animation="150"
    ghost-class="ghost"
    @end="handleDragEnd"
    class="el-row"
    :class="{ 'is-flex': true, 'flex-wrap': true }"
  >
    <template #item="{ element: row }">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" class="mb-4">
        <div class="template-item h-full">
          <el-card 
            class="box-card h-full" 
            shadow="hover"
            @click.stop="handlePreview(row)"
          >
            <div class="template-content">
              <div class="template-info">
                <h3 class="mb-2">{{ row.name }}</h3>
                <el-tag class="mb-2">{{ row.framework_type }}</el-tag>
                <p class="description mb-2">{{ row.description }}</p>
                <p class="time mb-2">创建时间：{{ new Date(row.created_at).toLocaleString() }}</p>
              </div>
              <div class="template-actions" @click.stop>
                <el-button-group>
                  <el-button type="primary" text @click="handleEdit(row)">编辑</el-button>
                  <el-button type="primary" text @click="handleTest(row)">测试</el-button>
                  <el-button type="primary" text @click="handleVersionHistory(row)">
                    <el-icon><Timer /></el-icon>
                  </el-button>
                  <el-button type="primary" text @click="handleClone(row)">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                  <el-button type="danger" text @click="handleDelete(row)">删除</el-button>
                </el-button-group>
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
    </template>
  </draggable>
</el-row>
<!-- 删除了旧的表格结构 -->

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
    <TemplatePreview
      v-model="previewVisible"
      :template="selectedTemplate"
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
          <el-button type="danger" @click="confirmDelete" :loading="deleteLoading">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed, defineComponent } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Timer, CopyDocument, Upload, Download } from '@element-plus/icons-vue'
import TemplateVersionHistory from '@/components/TemplateVersionHistory.vue'
import TemplatePreview from '@/components/TemplatePreview.vue'
import { getTemplateList, deleteTemplate, cloneTemplate, exportTemplates, importTemplates, reorderTemplates } from '@/api/templates'
import type { Template } from '@/types'
// 正确导入 vuedraggable
import draggable from 'vuedraggable'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const templates = ref<Template[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

// 预览相关
const previewVisible = ref(false)
const selectedTemplate = ref<Template | null>(null)

// 使用ref而不是computed，这样它是可变的
const sortedTemplates = ref<Template[]>([]);

// 监听templates变化，更新sortedTemplates
watch(() => templates.value, (newTemplates) => {
  if (!newTemplates || !Array.isArray(newTemplates)) {
    console.warn('templates.value is not an array:', newTemplates);
    sortedTemplates.value = [];
    return;
  }
  sortedTemplates.value = [...newTemplates].sort((a, b) => (a.order || 0) - (b.order || 0));
}, { immediate: true });

const handleDragEnd = async () => {
  console.log('拖拽结束，新顺序:', sortedTemplates.value);
  
  const updatedOrder = sortedTemplates.value.map((template, index) => ({
    id: template.id,
    order: index
  }))

  try {
    console.log('发送更新排序请求:', updatedOrder);
    await reorderTemplates(updatedOrder)
    ElMessage.success('模板排序已更新')
    
    // 更新本地数据
    templates.value = [...sortedTemplates.value];
  } catch (error: any) {
    console.error('更新排序失败:', error);
    ElMessage.error(error.message || '更新排序失败')
    // 如果更新失败，重新加载数据以恢复原始顺序
    await loadData()
  }
}

// 预览相关
const currentTemplate = ref<Template | null>(null)

// 版本历史相关
const versionHistoryVisible = ref(false)

// 删除相关
const deleteDialogVisible = ref(false)
const deleteLoading = ref(false)
const templateToDelete = ref<Template | null>(null)

// 打开版本历史
const handleVersionHistory = (row: Template) => {
  currentTemplate.value = row
  versionHistoryVisible.value = true
}

// 导入模板
const handleImport = async (file: any) => {
  try {
    const result = await importTemplates(file.raw)
    ElMessage.success(result.message)
    loadData()
  } catch (error: any) {
    ElMessage.error(error.message || '导入失败')
  }
}

// 导出模板
const handleExport = async () => {
  try {
    const response = await exportTemplates()
    const blob = new Blob([response], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'templates_export.json'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error: any) {
    ElMessage.error(error.message || '导出失败')
  }
}

// 克隆模板
const handleClone = async (row: Template) => {
  try {
    const result = await cloneTemplate(row.id)
    if (result && result.id) {
      ElMessage.success('克隆成功')
      loadData()
    } else {
      throw new Error('克隆模板失败')
    }
  } catch (error: any) {
    ElMessage.error(error.message || '克隆失败')
  }
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    console.log('开始加载模板数据...');
    const res = await getTemplateList({
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value
    });
    console.log('获取到的模板数据:', res);
    
    if (res && Array.isArray(res.results)) {
      templates.value = res.results;
      total.value = res.count;
      console.log('模板数据已更新:', templates.value);
    } else {
      console.warn('返回的数据格式不正确:', res);
      ElMessage.warning('返回的数据格式不符合预期');
    }
  } catch (error: any) {
    console.error('加载模板数据失败:', error);
    if (error.response) {
      console.error('错误响应:', error.response);
      if (error.response.status === 401) {
        ElMessage.error('请先登录');
        router.push('/login');
      } else {
        ElMessage.error(`加载失败: ${error.response.data?.detail || error.message || '未知错误'}`);
      }
    } else if (error.request) {
      ElMessage.error('网络请求失败，请检查网络连接');
    } else {
      ElMessage.error(error.message || '加载失败');
    }
  } finally {
    loading.value = false;
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

// 编辑
const handleEdit = (row: Template) => {
  router.push({
    path: `/templates/${row.id}/edit`,
    query: { name: row.name } // 添加名称作为查询参数，方便面包屑导航显示
  })
}

// 预览
const handlePreview = (row: Template, e?: Event) => {
  selectedTemplate.value = row
  previewVisible.value = true
  // 阻止事件冒泡
  e?.stopPropagation()
}

// 测试
const handleTest = (row: Template) => {
  router.push({
    path: '/templates/test',
    query: { template: row.id.toString() }
  })
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

// 删除
const handleDelete = (row: Template) => {
  templateToDelete.value = row
  deleteDialogVisible.value = true
}

// 确认删除
const confirmDelete = async () => {
  if (!templateToDelete.value) return

  deleteLoading.value = true
  try {
    await deleteTemplate(templateToDelete.value.id)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    loadData()
  } catch (error: any) {
    ElMessage.error(error.message || '删除失败')
  } finally {
    deleteLoading.value = false
  }
}

// 分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadData()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadData()
}

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
}

.search-bar {
  display: flex;
  gap: 10px;
}

.operation-buttons {
  display: flex;
  gap: 10px;
}

:deep(.el-upload) {
  width: auto;
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

/* 拖拽相关样式 */
.template-item {
  height: 100%;
  cursor: pointer;
}

.template-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.template-info {
  flex: 1;
}

.template-info h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.template-info .description {
  color: #606266;
  font-size: 14px;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 40px;
}

.template-info .time {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

.template-actions {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #EBEEF5;
}

.template-actions :deep(.el-button-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 拖拽时的样式 */
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
  border: 1px dashed #409EFF;
}

.template-item:hover {
  transform: translateY(-2px);
  transition: all 0.3s;
}

.box-card {
  height: 100%;
  transition: all 0.3s;
  cursor: pointer;
}

.box-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.template-actions {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

/* 工具类 */
.mb-4 {
  margin-bottom: 16px;
}

.mb-2 {
  margin-bottom: 8px;
}

.h-full {
  height: 100%;
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
}

:deep(.draggable) {
  width: 100%;
}

/* 确保按钮在小屏幕上也能很好地显示 */
@media (max-width: 768px) {
  .template-actions :deep(.el-button) {
    padding: 8px;
  }
  
  .template-actions :deep(.el-button-group) {
    justify-content: center;
  }
}
</style>