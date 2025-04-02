<template>
  <div class="dify-platform-list">
    <el-card class="header-card">
      <div class="card-header">
        <h1>Dify平台管理</h1>
        <el-button type="primary" @click="openCreateDialog">
          <el-icon><Plus /></el-icon>添加平台
        </el-button>
      </div>
      <p class="description">
        管理您的Dify平台配置，每个平台可以包含多个应用。
      </p>
    </el-card>

    <el-card v-if="loading" class="loading-card">
      <el-skeleton :rows="5" animated />
    </el-card>

    <el-empty v-else-if="platforms.length === 0" description="暂无平台数据" />

    <div v-else class="platform-grid">
      <el-card
        v-for="platform in platforms"
        :key="platform.id"
        class="platform-card"
      >
        <div class="platform-header">
          <h2>{{ platform.name }}</h2>
          <div class="platform-actions">
            <el-tag
              :type="platform.is_active ? 'success' : 'info'"
              size="small"
            >
              {{ platform.is_active ? "启用" : "禁用" }}
            </el-tag>
            <el-dropdown trigger="click">
              <el-button type="text">
                <el-icon><MoreFilled /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="editPlatform(platform)">
                    <el-icon><Edit /></el-icon>编辑
                  </el-dropdown-item>
                  <el-dropdown-item @click="togglePlatformStatus(platform)">
                    <el-icon><SwitchButton /></el-icon>
                    {{ platform.is_active ? "禁用" : "启用" }}
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="viewApplications(platform)">
                    <el-icon><View /></el-icon>查看应用
                  </el-dropdown-item>
                  <el-dropdown-item @click="addApplication(platform)">
                    <el-icon><Plus /></el-icon>添加应用
                  </el-dropdown-item>
                  <el-dropdown-item
                    divided
                    type="danger"
                    @click="confirmDelete(platform)"
                  >
                    <el-icon><Delete /></el-icon>删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>

        <div class="platform-info">
          <p><strong>基础URL：</strong>{{ platform.base_url }}</p>
          <p v-if="platform.description">
            <strong>描述：</strong>{{ platform.description }}
          </p>
          <p><strong>应用数量：</strong>{{ platform.applications_count }}</p>
          <p>
            <strong>创建时间：</strong
            >{{ new Date(platform.created_at).toLocaleString() }}
          </p>
        </div>

        <div class="platform-footer">
          <el-button type="primary" plain @click="viewApplications(platform)">
            <el-icon><View /></el-icon>查看应用
          </el-button>
          <el-button type="success" plain @click="addApplication(platform)">
            <el-icon><Plus /></el-icon>添加应用
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 平台表单对话框 -->
    <el-dialog
      v-model="platformDialogVisible"
      :title="isEdit ? '编辑平台' : '添加平台'"
      width="500px"
    >
      <el-form
        ref="platformFormRef"
        :model="platformForm"
        :rules="platformRules"
        label-width="100px"
      >
        <el-form-item label="平台名称" prop="name">
          <el-input v-model="platformForm.name" placeholder="请输入平台名称" />
        </el-form-item>
        <el-form-item label="基础URL" prop="base_url">
          <el-input
            v-model="platformForm.base_url"
            placeholder="例如: https://api.dify.ai/v1"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="platformForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入平台描述（可选）"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="platformForm.is_active"
            :active-text="platformForm.is_active ? '启用' : '禁用'"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="platformDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitPlatformForm">确认</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 应用表单对话框 -->
    <el-dialog
      v-model="applicationDialogVisible"
      :title="isEditApp ? '编辑应用' : '添加应用'"
      width="500px"
    >
      <el-form
        ref="applicationFormRef"
        :model="applicationForm"
        :rules="applicationRules"
        label-width="100px"
      >
        <el-form-item label="平台" prop="platform">
          <el-select v-model="applicationForm.platform" disabled>
            <el-option
              v-for="platform in platforms"
              :key="platform.id"
              :label="platform.name"
              :value="platform.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="应用名称" prop="name">
          <el-input
            v-model="applicationForm.name"
            placeholder="请输入应用名称"
          />
        </el-form-item>
        <el-form-item label="应用ID" prop="app_id">
          <el-input
            v-model="applicationForm.app_id"
            placeholder="请输入应用ID"
          />
        </el-form-item>
        <el-form-item label="应用类型" prop="app_type">
          <el-select
            v-model="applicationForm.app_type"
            placeholder="请选择应用类型"
          >
            <el-option label="对话" value="chat" />
            <el-option label="文本补全" value="completion" />
          </el-select>
        </el-form-item>
        <el-form-item label="API密钥" prop="api_key">
          <el-input
            v-model="applicationForm.api_key"
            placeholder="请输入API密钥"
            show-password
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="applicationForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入应用描述（可选）"
          />
        </el-form-item>
        <el-form-item label="默认应用">
          <el-switch
            v-model="applicationForm.is_default"
            :active-text="applicationForm.is_default ? '是' : '否'"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="applicationForm.is_active"
            :active-text="applicationForm.is_active ? '启用' : '禁用'"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="applicationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitApplicationForm"
            >确认</el-button
          >
        </span>
      </template>
    </el-dialog>

    <!-- 应用列表对话框 -->
    <el-dialog
      v-model="applicationsListDialogVisible"
      :title="`${currentPlatform?.name || ''} - 应用列表`"
      width="800px"
    >
      <el-table
        v-if="applications.length > 0"
        :data="applications"
        border
        style="width: 100%"
      >
        <el-table-column prop="name" label="应用名称" />
        <el-table-column prop="app_id" label="应用ID" width="180" />
        <el-table-column prop="app_type" label="类型" width="100">
          <template #default="scope">
            {{ scope.row.app_type === "chat" ? "对话" : "文本补全" }}
          </template>
        </el-table-column>
        <el-table-column prop="is_default" label="默认" width="80">
          <template #default="scope">
            <el-tag
              :type="scope.row.is_default ? 'success' : 'info'"
              size="small"
            >
              {{ scope.row.is_default ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="scope">
            <el-tag
              :type="scope.row.is_active ? 'success' : 'info'"
              size="small"
            >
              {{ scope.row.is_active ? "启用" : "禁用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="editApplication(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="!scope.row.is_default"
              type="success"
              size="small"
              @click="setAsDefault(scope.row)"
            >
              设为默认
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="confirmDeleteApp(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无应用数据" />
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="addApplication(currentPlatform)">
            添加应用
          </el-button>
          <el-button @click="applicationsListDialogVisible = false"
            >关闭</el-button
          >
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  Plus,
  Edit,
  Delete,
  View,
  MoreFilled,
  SwitchButton,
} from "@element-plus/icons-vue";
import {
  getDifyPlatforms,
  createDifyPlatform,
  updateDifyPlatform,
  deleteDifyPlatform,
  getDifyApplications,
  createDifyApplication,
  updateDifyApplication,
  deleteDifyApplication,
  setDefaultApplication,
  DifyPlatform,
  DifyApplication,
} from "@/api/dify";

// 平台数据
const platforms = ref<DifyPlatform[]>([]);
const loading = ref(true);

// 应用数据
const applications = ref<DifyApplication[]>([]);
const currentPlatform = ref<DifyPlatform | null>(null);

// 对话框控制
const platformDialogVisible = ref(false);
const applicationDialogVisible = ref(false);
const applicationsListDialogVisible = ref(false);
const isEdit = ref(false);
const isEditApp = ref(false);

// 表单引用
const platformFormRef = ref();
const applicationFormRef = ref();

// 平台表单数据
const platformForm = reactive({
  id: 0,
  name: "",
  base_url: "",
  description: "",
  is_active: true,
});

// 应用表单数据
const applicationForm = reactive({
  id: 0,
  platform: 0,
  name: "",
  app_id: "",
  app_type: "chat" as "chat" | "completion",
  api_key: "",
  description: "",
  is_default: false,
  is_active: true,
});

// 表单验证规则
const platformRules = {
  name: [
    { required: true, message: "请输入平台名称", trigger: "blur" },
    { min: 2, max: 100, message: "长度在 2 到 100 个字符", trigger: "blur" },
  ],
  base_url: [
    { required: true, message: "请输入基础URL", trigger: "blur" },
    {
      pattern: /^https?:\/\//,
      message: "URL必须以http://或https://开头",
      trigger: "blur",
    },
  ],
};

const applicationRules = {
  name: [
    { required: true, message: "请输入应用名称", trigger: "blur" },
    { min: 2, max: 100, message: "长度在 2 到 100 个字符", trigger: "blur" },
  ],
  app_id: [{ required: true, message: "请输入应用ID", trigger: "blur" }],
  app_type: [{ required: true, message: "请选择应用类型", trigger: "change" }],
  api_key: [{ required: true, message: "请输入API密钥", trigger: "blur" }],
};

// 初始化
onMounted(() => {
  fetchPlatforms();
});

// 获取平台列表
const fetchPlatforms = async () => {
  loading.value = true;
  try {
    const res = await getDifyPlatforms();
    platforms.value = res.results || [];
  } catch (error) {
    ElMessage.error("获取平台列表失败");
  } finally {
    loading.value = false;
  }
};

// 获取应用列表
const fetchApplications = async (platformId: number) => {
  try {
    const res = await getDifyApplications({ platform: platformId });
    applications.value = res.results || [];
  } catch (error) {
    ElMessage.error("获取应用列表失败");
  }
};

// 打开创建平台对话框
const openCreateDialog = () => {
  isEdit.value = false;
  resetPlatformForm();
  platformDialogVisible.value = true;
};

// 编辑平台
const editPlatform = (platform: DifyPlatform) => {
  isEdit.value = true;
  platformForm.id = platform.id;
  platformForm.name = platform.name;
  platformForm.base_url = platform.base_url;
  platformForm.description = platform.description || "";
  platformForm.is_active = platform.is_active;
  platformDialogVisible.value = true;
};

// 切换平台状态
const togglePlatformStatus = async (platform: DifyPlatform) => {
  try {
    await updateDifyPlatform(platform.id, {
      is_active: !platform.is_active,
    });
    ElMessage.success(`${platform.is_active ? "禁用" : "启用"}平台成功`);
    fetchPlatforms();
  } catch (error) {
    ElMessage.error("更新平台状态失败");
  }
};

// 确认删除平台
const confirmDelete = (platform: DifyPlatform) => {
  ElMessageBox.confirm(
    `确定要删除平台 "${platform.name}" 吗？此操作将同时删除该平台下的所有应用。`,
    "警告",
    {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    },
  )
    .then(async () => {
      try {
        await deleteDifyPlatform(platform.id);
        ElMessage.success("删除平台成功");
        fetchPlatforms();
      } catch (error) {
        ElMessage.error("删除平台失败");
      }
    })
    .catch(() => {
      // 用户取消删除
    });
};

// 提交平台表单
const submitPlatformForm = async () => {
  if (!platformFormRef.value) return;

  await platformFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await updateDifyPlatform(platformForm.id, {
            name: platformForm.name,
            base_url: platformForm.base_url,
            description: platformForm.description,
            is_active: platformForm.is_active,
          });
          ElMessage.success("更新平台成功");
        } else {
          await createDifyPlatform({
            name: platformForm.name,
            base_url: platformForm.base_url,
            description: platformForm.description,
            is_active: platformForm.is_active,
          });
          ElMessage.success("创建平台成功");
        }
        platformDialogVisible.value = false;
        fetchPlatforms();
      } catch (error) {
        ElMessage.error("保存平台失败");
      }
    }
  });
};

// 重置平台表单
const resetPlatformForm = () => {
  platformForm.id = 0;
  platformForm.name = "";
  platformForm.base_url = "";
  platformForm.description = "";
  platformForm.is_active = true;
};

// 查看应用
const viewApplications = async (platform: DifyPlatform) => {
  currentPlatform.value = platform;
  await fetchApplications(platform.id);
  applicationsListDialogVisible.value = true;
};

// 添加应用
const addApplication = (platform: DifyPlatform) => {
  isEditApp.value = false;
  resetApplicationForm();
  applicationForm.platform = platform.id;
  currentPlatform.value = platform;
  applicationDialogVisible.value = true;
};

// 编辑应用
const editApplication = (application: DifyApplication) => {
  isEditApp.value = true;
  applicationForm.id = application.id;
  applicationForm.platform = application.platform;
  applicationForm.name = application.name;
  applicationForm.app_id = application.app_id;
  applicationForm.app_type = application.app_type;
  applicationForm.api_key = application.api_key || "";
  applicationForm.description = application.description || "";
  applicationForm.is_default = application.is_default;
  applicationForm.is_active = application.is_active;
  applicationDialogVisible.value = true;
};

// 确认删除应用
const confirmDeleteApp = (application: DifyApplication) => {
  ElMessageBox.confirm(`确定要删除应用 "${application.name}" 吗？`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await deleteDifyApplication(application.id);
        ElMessage.success("删除应用成功");
        if (currentPlatform.value) {
          fetchApplications(currentPlatform.value.id);
          fetchPlatforms();
        }
      } catch (error) {
        ElMessage.error("删除应用失败");
      }
    })
    .catch(() => {
      // 用户取消删除
    });
};

// 设置为默认应用
const setAsDefault = async (application: DifyApplication) => {
  try {
    await setDefaultApplication(application.id);
    ElMessage.success("设置默认应用成功");
    if (currentPlatform.value) {
      fetchApplications(currentPlatform.value.id);
    }
  } catch (error) {
    ElMessage.error("设置默认应用失败");
  }
};

// 提交应用表单
const submitApplicationForm = async () => {
  if (!applicationFormRef.value) return;

  await applicationFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (isEditApp.value) {
          await updateDifyApplication(applicationForm.id, {
            name: applicationForm.name,
            app_id: applicationForm.app_id,
            app_type: applicationForm.app_type,
            api_key: applicationForm.api_key,
            description: applicationForm.description,
            is_default: applicationForm.is_default,
            is_active: applicationForm.is_active,
          });
          ElMessage.success("更新应用成功");
        } else {
          await createDifyApplication({
            platform: applicationForm.platform,
            name: applicationForm.name,
            app_id: applicationForm.app_id,
            app_type: applicationForm.app_type,
            api_key: applicationForm.api_key,
            description: applicationForm.description,
            is_default: applicationForm.is_default,
            is_active: applicationForm.is_active,
          });
          ElMessage.success("创建应用成功");
        }
        applicationDialogVisible.value = false;
        if (currentPlatform.value) {
          fetchApplications(currentPlatform.value.id);
          fetchPlatforms();
        }
      } catch (error) {
        ElMessage.error("保存应用失败");
      }
    }
  });
};

// 重置应用表单
const resetApplicationForm = () => {
  applicationForm.id = 0;
  applicationForm.platform = currentPlatform.value?.id || 0;
  applicationForm.name = "";
  applicationForm.app_id = "";
  applicationForm.app_type = "chat";
  applicationForm.api_key = "";
  applicationForm.description = "";
  applicationForm.is_default = false;
  applicationForm.is_active = true;
};
</script>

<style scoped>
.dify-platform-list {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.description {
  color: #666;
  margin-bottom: 0;
}

.loading-card {
  padding: 20px;
}

.platform-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.platform-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.platform-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.platform-header h2 {
  margin: 0;
  font-size: 18px;
}

.platform-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.platform-info {
  flex: 1;
  margin-bottom: 15px;
}

.platform-info p {
  margin: 8px 0;
}

.platform-footer {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
}
</style>
