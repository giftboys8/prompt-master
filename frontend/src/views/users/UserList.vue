<template>
  <div class="user-list-container">
    <div class="page-header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>新建用户
      </el-button>
    </div>

    <el-card class="user-list-card">
      <el-table :data="userList" v-loading="loading" style="width: 100%">
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="is_staff" label="角色">
          <template #default="{ row }">
            <el-tag :type="row.is_staff ? 'success' : 'info'">
              {{ row.is_staff ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date_joined" label="注册时间">
          <template #default="{ row }">
            {{ new Date(row.date_joined).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button
                size="small"
                :type="row.is_active ? 'danger' : 'success'"
                @click="handleToggleStatus(row)"
              >
                {{ row.is_active ? '禁用' : '启用' }}
              </el-button>
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
    </el-card>

    <!-- 用户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        style="max-width: 460px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="dialogMode === 'edit'" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogMode === 'create'">
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="角色" prop="is_staff">
          <el-select v-model="form.is_staff" style="width: 100%">
            <el-option label="普通用户" :value="false" />
            <el-option label="管理员" :value="true" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-select v-model="form.is_active" style="width: 100%">
            <el-option label="正常" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import { useUserStore } from '@/stores/user';
import { getUsers, updateUser, deleteUser } from '@/api/users';

const userStore = useUserStore();

// 表格数据
const loading = ref(false);
const userList = ref([]);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 对话框相关
const dialogVisible = ref(false);
const dialogMode = ref('create');
const dialogTitle = ref('新建用户');
const submitting = ref(false);
const formRef = ref<FormInstance>();

// 表单数据
const form = ref({
  username: '',
  email: '',
  password: '',
  is_staff: false,
  is_active: true
});

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ]
};

// 获取用户列表
const fetchUsers = async () => {
  try {
    loading.value = true;
    const data = await getUsers({
      page: currentPage.value,
      page_size: pageSize.value
    });
    userList.value = data.results;
    total.value = data.count;
  } catch (error) {
    ElMessage.error(error.message || '获取用户列表失败');
  } finally {
    loading.value = false;
  }
};

// 创建用户
const handleCreate = () => {
  dialogMode.value = 'create';
  dialogTitle.value = '新建用户';
  form.value = {
    username: '',
    email: '',
    password: '',
    is_staff: false,
    is_active: true
  };
  dialogVisible.value = true;
};

// 编辑用户
const handleEdit = (row) => {
  dialogMode.value = 'edit';
  dialogTitle.value = '编辑用户';
  form.value = {
    ...row,
    password: '' // 编辑时不显示密码
  };
  dialogVisible.value = true;
};

// 切换用户状态
const handleToggleStatus = async (row) => {
  try {
    const action = row.is_active ? '禁用' : '启用';
    await ElMessageBox.confirm(
      `确定要${action}用户 ${row.username} 吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    );

    await updateUser(row.id, {
      is_active: !row.is_active
    });

    ElMessage.success(`${action}成功`);
    fetchUsers();
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message);
    }
  }
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  try {
    await formRef.value.validate();
    submitting.value = true;

    if (dialogMode.value === 'create') {
      // 使用 auth.ts 中的 register 方法创建用户
      await userStore.register({
        username: form.value.username,
        email: form.value.email,
        password: form.value.password,
        password2: form.value.password
      });
    } else {
      // 更新用户
      await updateUser(form.value.id, {
        email: form.value.email,
        is_staff: form.value.is_staff,
        is_active: form.value.is_active
      });
    }

    ElMessage.success(`${dialogMode.value === 'create' ? '创建' : '更新'}成功`);
    dialogVisible.value = false;
    fetchUsers();
  } catch (error) {
    ElMessage.error(error.message);
  } finally {
    submitting.value = false;
  }
};

// 分页相关
const handleSizeChange = () => {
  currentPage.value = 1;
  fetchUsers();
};

const handleCurrentChange = () => {
  fetchUsers();
};

// 关闭对话框
const handleDialogClose = () => {
  formRef.value?.resetFields();
};

// 初始化
onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.user-list-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: var(--text-primary);
}

.user-list-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-card) {
  --el-card-padding: 20px;
}

:deep(.el-table) {
  --el-table-header-bg-color: var(--glass-bg);
  --el-table-tr-bg-color: transparent;
  --el-table-border-color: var(--glass-border);
}
</style>