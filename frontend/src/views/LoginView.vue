<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>{{ isLogin ? '登录' : '注册' }}</span>
        </div>
      </template>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        
        <el-form-item v-if="!isLogin" label="邮箱" prop="email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>
        
        <el-form-item v-if="!isLogin" label="昵称" prop="nickname">
          <el-input v-model="form.nickname" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" />
        </el-form-item>
        
        <el-form-item v-if="!isLogin" label="确认密码" prop="password2">
          <el-input v-model="form.password2" type="password" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" style="width: 100%">
            {{ isLogin ? '登录' : '注册' }}
          </el-button>
        </el-form-item>
        
        <el-form-item>
          <el-button link @click="toggleMode" style="width: 100%">
            {{ isLogin ? '没有账号？立即注册' : '已有账号？立即登录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'

export default {
  name: 'LoginView',
  setup() {
    const store = useStore()
    const router = useRouter()
    const formRef = ref(null)
    const isLogin = ref(true)
    
    const form = reactive({
      username: '',
      email: '',
      nickname: '',
      password: '',
      password2: ''
    })
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, message: '用户名长度不能小于3个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      nickname: [
        { required: true, message: '请输入昵称', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
      ],
      password2: [
        { required: true, message: '请再次输入密码', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== form.password) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }
    
    const handleSubmit = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        if (isLogin.value) {
          // 登录
          const result = await store.dispatch('auth/login', {
            username: form.username,
            password: form.password
          })
          if (result) {
            ElMessage.success('登录成功')
            router.push('/')
          }
        } else {
          // 注册
          const result = await store.dispatch('auth/register', {
            username: form.username,
            email: form.email,
            nickname: form.nickname,
            password: form.password,
            password2: form.password2
          })
          if (result) {
            ElMessage.success('注册成功，请登录')
            isLogin.value = true
            formRef.value.resetFields()
          }
        }
      } catch (error) {
        console.error(error)
        ElMessage.error(error.message || '操作失败')
      }
    }
    
    const toggleMode = () => {
      isLogin.value = !isLogin.value
      formRef.value?.resetFields()
    }
    
    return {
      formRef,
      form,
      rules,
      isLogin,
      handleSubmit,
      toggleMode
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.card-header {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
}
</style>