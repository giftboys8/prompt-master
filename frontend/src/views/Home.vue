<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>业务场景</span>
              <el-button text @click="router.push('/scenes')">查看更多</el-button>
            </div>
          </template>
          <el-empty v-if="!sceneCount" description="暂无业务场景">
            <el-button type="primary" @click="router.push('/scenes')">
              创建场景
            </el-button>
          </el-empty>
          <div v-else class="stat-number">
            <span class="number">{{ sceneCount }}</span>
            <span class="label">个场景</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>提示词模板</span>
              <el-button text @click="router.push('/templates')">查看更多</el-button>
            </div>
          </template>
          <el-empty v-if="!templateCount" description="暂无提示词模板">
            <el-button type="primary" @click="router.push('/templates')">
              创建模板
            </el-button>
          </el-empty>
          <div v-else class="stat-number">
            <span class="number">{{ templateCount }}</span>
            <span class="label">个模板</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>生成内容</span>
              <el-button text @click="router.push('/contents')">查看更多</el-button>
            </div>
          </template>
          <el-empty v-if="!contentCount" description="暂无生成内容">
            <el-button type="primary" @click="router.push('/contents')">
              生成内容
            </el-button>
          </el-empty>
          <div v-else class="stat-number">
            <span class="number">{{ contentCount }}</span>
            <span class="label">个内容</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// TODO: 从API获取实际数据
const sceneCount = ref(0)
const templateCount = ref(0)
const contentCount = ref(0)
</script>

<style scoped>
.home {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-number {
  text-align: center;
  padding: 20px 0;
}

.stat-number .number {
  font-size: 36px;
  font-weight: bold;
  color: var(--primary-color);
}

.stat-number .label {
  font-size: 14px;
  color: var(--text-color-secondary);
  margin-left: 8px;
}
</style>