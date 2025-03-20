<template>
  <div class="page-container">
    <div class="page-header">
      <h1>提示词模板</h1>
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
      <el-button type="primary" @click="router.push('/templates/create')">
        <el-icon><Plus /></el-icon>新增模板
      </el-button>
    </div>

    <el-table v-loading="loading" :data="templates" style="width: 100%">
      <el-table-column prop="name" label="模板名称" />
      <el-table-column prop="framework_type" label="框架类型">
        <template #default="{ row }">
          <el-tag>{{ row.framework_type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ new Date(row.created_at).toLocaleString() }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" text @click="handleEdit(row)">编辑</el-button>
            <el-button type="primary" text @click="handlePreview(row)">预览</el-button>
            <el-button type="primary" text @click="handleVersionHistory(row)">
              <el-icon><Timer /></el-icon>
            </el-button>
            <el-button type="primary" text @click="handleClone(row)">
              <el-icon><CopyDocument /></el-icon>
            </el-button>
            <el-button type="danger" text @click="handleDelete(row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

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
    <el-dialog
      v-model="previewDialogVisible"
      title="模板预览"
      width="50%"
      destroy-on-close
    >
      <template v-if="currentTemplate">
        <h3>基本信息</h3>
        <p><strong>模板名称：</strong>{{ currentTemplate.name }}</p>
        <p><strong>框架类型：</strong>{{ currentTemplate.framework_type }}</p>
        <p><strong>描述：</strong>{{ currentTemplate.description }}</p>

        <h3>提示词内容</h3>
        <template v-if="currentTemplate.framework_type === 'RTGO'">
          <p><strong>角色(Role)：</strong>{{ currentTemplate.content.role }}</p>
          <p><strong>任务(Task)：</strong>{{ currentTemplate.content.task }}</p>
          <p><strong>目标(Goal)：</strong>{{ currentTemplate.content.goal }}</p>
          <p><strong>输出(Output)：</strong>{{ currentTemplate.content.output }}</p>
        </template>

        <template v-else-if="currentTemplate.framework_type === 'SPAR'">
          <p><strong>情境(Situation)：</strong>{{ currentTemplate.content.situation }}</p>
          <p><strong>目的(Purpose)：</strong>{{ currentTemplate.content.purpose }}</p>
          <p><strong>行动(Action)：</strong>{{ currentTemplate.content.action }}</p>
          <p><strong>结果(Result)：</strong>{{ currentTemplate.content.result }}</p>
        </template>

        <template v-else>
          <p><strong>自定义内容：</strong>{{ currentTemplate.content.custom }}</p>
        </template>

        <h3>变量列表</h3>
        <el-table :data="currentTemplate.variables">
          <el-table-column prop="name" label="变量名称" />
          <el-table-column prop="default_value" label="默认值" />
          <el-table-column prop="description" label="描述" />
        </el-table>
      </template>
    </el-dialog>

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
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Timer, CopyDocument } from '@element-plus/icons-vue'
import TemplateVersionHistory from '@/components/TemplateVersionHistory.vue'
import { getTemplateList, deleteTemplate, cloneTemplate } from '@/api/templates'
import type { Template } from '@/types'

const router = useRouter()
const loading = ref(false)
const templates = ref<Template[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

// 预览相关
const previewDialogVisible = ref(false)
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
    const res = await getTemplateList({
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value
    })
    templates.value = res.results
    total.value = res.count
  } catch (error: any) {
    ElMessage.error(error.message || '加载失败')
  } finally {
    loading.value = false
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
const handlePreview = (row: Template) => {
  currentTemplate.value = row
  previewDialogVisible.value = true
}

// 监听预览对话框关闭
watch(previewDialogVisible, (val) => {
  if (!val) {
    currentTemplate.value = null
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

.operation-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  gap: 10px;
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
</style>