<template>
  <div class="test-history">
    <h3>历史记录</h3>
    <el-empty 
      v-if="!isLoading && (!history || history.length === 0)" 
      description="暂无测试记录" 
    />
    <el-table
      v-else
      v-loading="isLoading"
      :data="history"
      style="width: 100%"
      stripe
    >
      <el-table-column
        prop="created_at"
        label="测试时间"
        width="180"
        :formatter="formatDate"
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
            @click="$emit('view-detail', row)"
          >
            查看详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import type { TemplateTest } from '@/types'

defineProps<{
  history: TemplateTest[]
  isLoading: boolean
}>()

defineEmits<{
  (e: 'view-detail', record: TemplateTest): void
}>()

// 格式化日期
const formatDate = (row: TemplateTest) => {
  return new Date(row.created_at).toLocaleString()
}

// 解析测试结果
const parseTestResult = (content: string) => {
  try {
    return JSON.parse(content)
  } catch (e) {
    return null
  }
}

// 获取模型名称
const getModelName = (record: TemplateTest) => {
  if (record.model) {
    return record.model
  }
  return record.dify_response?.model || 'Dify API'
}
</script>

<style lang="scss" scoped>
.test-history {
  margin-top: 40px;

  h3 {
    color: var(--primary-color);
    font-size: 18px;
    margin-bottom: 16px;
    font-family: 'Orbitron', sans-serif;
  }
}

.input-data-preview,
.output-content-preview {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Fira Code', monospace;
  font-size: 12px;
}
</style>