<template>
  <div class="page-container">
    <div class="page-header">
      <h1>编辑提示词模版</h1>
    </div>

    <div v-loading="loading">
      <el-form
        v-if="form"
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="template-form"
      >
        <!-- 基本信息 -->
        <el-card class="form-card">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
            </div>
          </template>

          <el-form-item label="模版名称" prop="name">
            <el-input v-model="form.name" placeholder="请输入模版名称" />
          </el-form-item>

          <el-form-item label="框架类型" prop="framework_type">
            <el-select
              v-model="form.framework_type"
              placeholder="请选择框架类型"
              class="w-full"
            >
              <el-option label="RTGO" value="RTGO" />
              <el-option label="SPAR" value="SPAR" />
              <el-option label="自定义" value="CUSTOM" />
            </el-select>
          </el-form-item>

          <el-form-item label="描述" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              rows="3"
              placeholder="请输入模版描述"
            />
          </el-form-item>
        </el-card>

        <!-- 提示词内容 -->
        <el-card class="form-card">
          <template #header>
            <div class="card-header">
              <span>提示词内容</span>
            </div>
          </template>

          <template v-if="form.framework_type === 'RTGO'">
            <el-form-item label="角色(Role)" prop="content.role">
              <el-input
                v-model="form.content.role"
                type="textarea"
                rows="2"
                placeholder="描述AI应该扮演的角色"
              />
            </el-form-item>

            <el-form-item label="任务(Task)" prop="content.task">
              <el-input
                v-model="form.content.task"
                type="textarea"
                rows="2"
                placeholder="描述需要完成的具体任务"
              />
            </el-form-item>

            <el-form-item label="目标(Goal)" prop="content.goal">
              <el-input
                v-model="form.content.goal"
                type="textarea"
                rows="2"
                placeholder="描述期望达到的目标"
              />
            </el-form-item>

            <el-form-item label="输出(Output)" prop="content.output">
              <el-input
                v-model="form.content.output"
                type="textarea"
                rows="2"
                placeholder="描述期望的输出格式和要求"
              />
            </el-form-item>
          </template>

          <template v-else-if="form.framework_type === 'SPAR'">
            <el-form-item label="情境(Situation)" prop="content.situation">
              <el-input
                v-model="form.content.situation"
                type="textarea"
                rows="2"
                placeholder="描述当前的情境或背景"
              />
            </el-form-item>

            <el-form-item label="目的(Purpose)" prop="content.purpose">
              <el-input
                v-model="form.content.purpose"
                type="textarea"
                rows="2"
                placeholder="描述想要达到的目的"
              />
            </el-form-item>

            <el-form-item label="行动(Action)" prop="content.action">
              <el-input
                v-model="form.content.action"
                type="textarea"
                rows="2"
                placeholder="描述需要采取的行动"
              />
            </el-form-item>

            <el-form-item label="结果(Result)" prop="content.result">
              <el-input
                v-model="form.content.result"
                type="textarea"
                rows="2"
                placeholder="描述期望的结果"
              />
            </el-form-item>
          </template>

          <template v-else>
            <el-form-item label="自定义内容" prop="content.custom">
              <el-input
                v-model="form.content.custom"
                type="textarea"
                rows="6"
                placeholder="请输入自定义的提示词内容"
              />
            </el-form-item>
          </template>
        </el-card>

        <!-- 变量设置 -->
        <el-card class="form-card">
          <template #header>
            <div class="card-header">
              <span>变量设置</span>
              <el-button type="primary" @click="addVariable">
                <el-icon><Plus /></el-icon>添加变量
              </el-button>
            </div>
          </template>

          <div
            v-for="(variable, index) in form.variables"
            :key="index"
            class="variable-item"
          >
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item
                  :label="'变量名称'"
                  :prop="'variables.' + index + '.name'"
                  :rules="variableRules.name"
                >
                  <el-input
                    v-model="variable.name"
                    placeholder="请输入变量名称"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item
                  :label="'默认值'"
                  :prop="'variables.' + index + '.default_value'"
                  :rules="variableRules.default_value"
                >
                  <el-input
                    v-model="variable.default_value"
                    placeholder="请输入默认值"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item
                  :label="'描述'"
                  :prop="'variables.' + index + '.description'"
                  :rules="variableRules.description"
                >
                  <el-input
                    v-model="variable.description"
                    placeholder="请输入描述"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="2" class="flex items-center">
                <el-button type="danger" circle @click="removeVariable(index)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </el-col>
            </el-row>
          </div>
        </el-card>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button @click="$router.back()">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            保存
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Plus, Delete } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import { getTemplate, updateTemplate } from "@/api/templates";
import type { Template } from "@/types";

const route = useRoute();
const router = useRouter();
const formRef = ref<FormInstance>();
const loading = ref(false);
const submitting = ref(false);

// 表单数据
const form = ref<{
  name: string;
  framework_type: string;
  description: string;
  content: {
    role?: string;
    task?: string;
    goal?: string;
    output?: string;
    situation?: string;
    purpose?: string;
    action?: string;
    result?: string;
    custom?: string;
  };
  variables: Array<{
    name: string;
    default_value: string;
    description: string;
  }>;
}>();

// 表单验证规则
const rules = reactive<FormRules>({
  name: [
    { required: true, message: "请输入模版名称", trigger: "blur" },
    { min: 2, max: 50, message: "长度在 2 到 50 个字符", trigger: "blur" },
  ],
  framework_type: [
    { required: true, message: "请选择框架类型", trigger: "change" },
  ],
  description: [{ required: true, message: "请输入模版描述", trigger: "blur" }],
});

// 动态设置必填字段
const getContentRules = (type: string) => {
  if (type === "RTGO") {
    return {
      "content.role": [
        { required: true, message: "请输入角色描述", trigger: "blur" },
      ],
      "content.task": [
        { required: true, message: "请输入任务描述", trigger: "blur" },
      ],
      "content.goal": [
        { required: true, message: "请输入目标描述", trigger: "blur" },
      ],
      "content.output": [
        { required: true, message: "请输入输出要求", trigger: "blur" },
      ],
    };
  } else if (type === "SPAR") {
    return {
      "content.situation": [
        { required: true, message: "请输入情境描述", trigger: "blur" },
      ],
      "content.purpose": [
        { required: true, message: "请输入目的描述", trigger: "blur" },
      ],
      "content.action": [
        { required: true, message: "请输入行动描述", trigger: "blur" },
      ],
      "content.result": [
        { required: true, message: "请输入结果描述", trigger: "blur" },
      ],
    };
  } else if (type === "CUSTOM") {
    return {
      "content.custom": [
        { required: true, message: "请输入自定义内容", trigger: "blur" },
      ],
    };
  }
  return {};
};

// 变量验证规则
const variableRules = {
  name: [
    { required: true, message: "请输入变量名称", trigger: "blur" },
    {
      pattern: /^[a-zA-Z_][a-zA-Z0-9_]*$/,
      message: "变量名称只能包含字母、数字和下划线，且不能以数字开头",
      trigger: "blur",
    },
  ],
  default_value: [{ required: true, message: "请输入默认值", trigger: "blur" }],
  description: [{ required: true, message: "请输入描述", trigger: "blur" }],
};

// 监听框架类型变化
const stopWatch = watch(
  () => form.value?.framework_type,
  (newType) => {
    if (newType) {
      Object.assign(rules, getContentRules(newType));
    }
  },
);

// 组件卸载前清理
onBeforeUnmount(() => {
  stopWatch();
});

// 添加变量
const addVariable = () => {
  if (form.value) {
    form.value.variables.push({
      name: "",
      default_value: "",
      description: "",
    });
  }
};

// 删除变量
const removeVariable = (index: number) => {
  if (form.value) {
    form.value.variables.splice(index, 1);
  }
};

// 加载模板数据
const loadTemplate = async (id: string) => {
  loading.value = true;
  try {
    const data = await getTemplate(Number(id));
    form.value = {
      name: data.name,
      framework_type: data.framework_type,
      description: data.description,
      content: data.content,
      variables: data.variables || [],
    };
  } catch (error: any) {
    ElMessage.error(error.message || "加载失败");
    router.back();
  } finally {
    loading.value = false;
  }
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value || !form.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true;
      try {
        // 清理空的内容字段
        const submissionData = {
          ...form.value,
          content: {},
        };

        if (form.value.framework_type === "RTGO") {
          submissionData.content = {
            role: form.value.content.role,
            task: form.value.content.task,
            goal: form.value.content.goal,
            output: form.value.content.output,
          };
        } else if (form.value.framework_type === "SPAR") {
          submissionData.content = {
            situation: form.value.content.situation,
            purpose: form.value.content.purpose,
            action: form.value.content.action,
            result: form.value.content.result,
          };
        } else {
          submissionData.content = {
            custom: form.value.content.custom,
          };
        }

        const result = await updateTemplate(
          Number(route.params.id),
          submissionData,
        );
        if (result && result.id) {
          ElMessage.success("保存成功");
          router.push("/templates");
        } else {
          throw new Error("更新模板失败");
        }
      } catch (error: any) {
        ElMessage.error(error.message || "保存失败");
      } finally {
        submitting.value = false;
      }
    }
  });
};

onMounted(() => {
  if (route.params.id) {
    loadTemplate(route.params.id as string);
  } else {
    router.back();
  }
});
</script>

<style scoped>
.template-form {
  max-width: 1200px;
  margin: 0 auto;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.variable-item {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.variable-item:last-child {
  margin-bottom: 0;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

.w-full {
  width: 100%;
}
</style>
