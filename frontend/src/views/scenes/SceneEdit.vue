<template>
  <div class="page-container">
    <div class="page-header">
      <h1>编辑场景</h1>
    </div>

    <el-form
      v-loading="loading"
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="scene-form"
    >
      <el-form-item label="场景名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入场景名称" />
      </el-form-item>

      <el-form-item label="场景分类" prop="category">
        <el-input v-model="form.category" placeholder="请输入场景分类" />
      </el-form-item>

      <el-form-item label="场景描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入场景描述"
        />
      </el-form-item>

      <el-form-item label="目标角色" prop="target_roles">
        <el-select
          v-model="form.target_roles"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="请选择或输入目标角色"
        >
          <el-option
            v-for="role in roleOptions"
            :key="role"
            :label="role"
            :value="role"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="版本号" prop="version">
        <el-input v-model="form.version" placeholder="请输入版本号，如：v1.0.0" />
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-switch v-model="form.status" />
      </el-form-item>

      <el-divider>任务列表</el-divider>

      <div v-for="(task, index) in form.tasks" :key="index" class="task-item">
        <div class="task-header">
          <h3>任务 {{ index + 1 }}</h3>
          <el-button type="danger" link @click="removeTask(index)">
            删除任务
          </el-button>
        </div>

        <el-form-item
          :label="'任务名称'"
          :prop="'tasks.' + index + '.name'"
          :rules="taskRules.name"
        >
          <el-input v-model="task.name" placeholder="请输入任务名称" />
        </el-form-item>

        <el-form-item
          :label="'任务描述'"
          :prop="'tasks.' + index + '.description'"
          :rules="taskRules.description"
        >
          <el-input
            v-model="task.description"
            type="textarea"
            :rows="2"
            placeholder="请输入任务描述"
          />
        </el-form-item>

        <el-form-item
          :label="'关联模板'"
          :prop="'tasks.' + index + '.template'"
          :rules="taskRules.template"
        >
          <el-select
            v-model="task.template"
            filterable
            placeholder="请选择关联模板"
          >
            <el-option
              v-for="template in templateOptions"
              :key="template.id"
              :label="template.name"
              :value="template.id"
            />
          </el-select>
        </el-form-item>
      </div>

      <el-button type="primary" link @click="addTask">
        <el-icon><Plus /></el-icon>添加任务
      </el-button>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存场景</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import { Plus } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import type { Template } from "@/types";
import request from "@/api/request";

const router = useRouter();
const route = useRoute();
const formRef = ref<FormInstance>();
const loading = ref(false);
const sceneId = route.params.id as string;

// 表单数据
const form = reactive({
  name: "",
  category: "",
  description: "",
  target_roles: [] as string[],
  status: true,
  version: "",
  tasks: [] as any[],
});

    // 确保target_roles中的值都是字符串，并处理嵌套数组
const ensureStringArray = (arr: any[]): string[] => {
  return arr.map(item => {
    if (typeof item === 'string') {
      // 如果是字符串形式的数组，尝试解析
      if (item.startsWith('[') && item.endsWith(']')) {
        try {
          const parsed = JSON.parse(item);
          return Array.isArray(parsed) ? parsed[0] : item.slice(1, -1);
        } catch (e) {
          return item;
        }
      }
      return item;
    }
    if (Array.isArray(item)) {
      return item[0] || '';
    }
    return String(item);
  });
};

// 角色选项
const roleOptions = [
  "产品经理",
  "开发工程师",
  "测试工程师",
  "运维工程师",
  "项目经理",
];

// 模板选项
const templateOptions = ref<Template[]>([]);

// 获取场景详情
const fetchSceneDetail = async () => {
  loading.value = true;
  try {
    const response = await request({
      url: `/scenes/${sceneId}/`,
      method: "get",
    });
    
    // 填充基本信息
    form.name = response.name;
    form.category = response.category;
    form.description = response.description;
    
    // 确保target_roles是字符串数组
    if (typeof response.target_roles === 'string') {
      try {
        form.target_roles = ensureStringArray(JSON.parse(response.target_roles));
      } catch (e) {
        form.target_roles = [String(response.target_roles)];
      }
    } else if (Array.isArray(response.target_roles)) {
      form.target_roles = ensureStringArray(response.target_roles);
    } else {
      form.target_roles = [];
    }
    
    form.status = response.status;
    form.version = response.version;
    
    // 填充任务
    form.tasks = response.tasks || [];
    
  } catch (error) {
    console.error("获取场景详情失败:", error);
    ElMessage.error("获取场景详情失败");
  } finally {
    loading.value = false;
  }
};

// 获取模板列表
const fetchTemplates = async () => {
  try {
    const response = await request({
      url: "/templates/templates/",
      method: "get",
      params: {
        page_size: 1000 // 设置一个较大的值以获取所有模板
      }
    });
    templateOptions.value = response.results || [];
  } catch (error) {
    console.error("获取模板列表失败:", error);
  }
};

// 初始化
onMounted(async () => {
  await fetchTemplates();
  await fetchSceneDetail();
});

// 表单验证规则
const rules = reactive<FormRules>({
  name: [{ required: true, message: "请输入场景名称", trigger: "blur" }],
  category: [{ required: true, message: "请输入场景分类", trigger: "blur" }],
  description: [{ required: true, message: "请输入场景描述", trigger: "blur" }],
  target_roles: [
    { required: true, message: "请选择目标角色", trigger: "change" },
    {
      type: "array",
      min: 1,
      message: "至少选择一个目标角色",
      trigger: "change",
    },
  ],
  version: [{ required: true, message: "请输入版本号", trigger: "blur" }],
});

// 任务表单验证规则
const taskRules = {
  name: [{ required: true, message: "请输入任务名称", trigger: "blur" }],
  description: [{ required: true, message: "请输入任务描述", trigger: "blur" }],
  template: [{ required: true, message: "请选择关联模板", trigger: "change" }],
};

// 添加任务
const addTask = () => {
  form.tasks.push({
    name: "",
    description: "",
    template: null,
  });
};

// 删除任务
const removeTask = (index: number) => {
  form.tasks.splice(index, 1);
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        // 创建表单数据的副本，避免修改原始表单
        const formData = JSON.parse(JSON.stringify(form));
        
        // 确保target_roles是一个简单的字符串数组
        if (Array.isArray(formData.target_roles)) {
          formData.target_roles = formData.target_roles
            .filter(role => role !== null && role !== undefined && role !== '')
            .map(role => {
              // 如果是字符串，直接使用
              if (typeof role === 'string') {
                return role.trim();
              }
              // 如果是数组，取第一个元素并转换为字符串
              if (Array.isArray(role)) {
                return String(role[0] || '').trim();
              }
              // 其他类型转换为字符串
              return String(role).trim();
            })
            .filter(role => role !== ''); // 过滤掉空字符串
        }
        
        // 确保任务数据中只包含必要的字段
        if (Array.isArray(formData.tasks)) {
          formData.tasks = formData.tasks.map(task => ({
            id: task.id,
            name: task.name,
            description: task.description,
            template: task.template
            // 移除只读字段如template_name和template_description
          }));
        }
        
        await request({
          url: `/scenes/${sceneId}/`,
          method: "put",
          data: formData,
        });
        ElMessage.success("更新场景成功");
        router.push("/scenes");
      } catch (error) {
        console.error("更新场景失败:", error);
      }
    } else {
      console.error("表单验证失败:", fields);
    }
  });
};

// 取消编辑
const handleCancel = () => {
  router.back();
};
</script>

<style scoped>
.scene-form {
  max-width: 800px;
  margin: 20px auto;
}

.task-item {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.task-header h3 {
  margin: 0;
}
</style>