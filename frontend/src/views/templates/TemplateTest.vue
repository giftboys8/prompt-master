<template>
  <div class="template-test">
    <h2>模板测试</h2>
    <el-form :model="testForm" @submit.prevent="runTest">
      <el-form-item label="选择模板">
        <el-select v-model="testForm.template" placeholder="请选择模板">
          <el-option
            v-for="template in templates"
            :key="template.id"
            :label="template.name"
            :value="template.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="选择模型">
        <el-select v-model="testForm.model" placeholder="请选择模型">
          <el-option label="GPT-3.5" value="GPT-3.5"></el-option>
          <el-option label="GPT-4" value="GPT-4"></el-option>
          <el-option label="Claude" value="CLAUDE"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="输入数据">
        <el-input
          v-model="testForm.input_data"
          type="textarea"
          :rows="4"
          placeholder="请输入 JSON 格式的数据"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">运行测试</el-button>
      </el-form-item>
    </el-form>

    <div v-if="testResult" class="test-result">
      <h3>测试结果</h3>
      <div v-html="formattedTestResult"></div>
    </div>

    <h3>测试历史</h3>
    <el-table :data="testHistory" style="width: 100%">
      <el-table-column prop="created_at" label="测试时间" width="180"></el-table-column>
      <el-table-column prop="model" label="模型" width="120"></el-table-column>
      <el-table-column prop="template_name" label="模板名称"></el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button @click="viewTestDetail(scope.row)" type="text" size="small">查看详情</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { runTemplateTest, getTemplateTests } from '@/api/templateTest';
import { getTemplateList } from '@/api/templates';
import MarkdownIt from 'markdown-it';
import router from '@/router';

export default defineComponent({
  name: 'TemplateTest',
  setup() {
    const templates = ref([]);
    const testForm = ref({
      template: '',
      model: '',
      input_data: '',
    });
    const testResult = ref('');
    const testHistory = ref([]);
    const md = new MarkdownIt();

    const formattedTestResult = computed(() => {
      return md.render(testResult.value);
    });

    const fetchTemplates = async () => {
      try {
        console.log('Fetching templates...');
        const token = localStorage.getItem('token');
        console.log('Current token:', token ? 'Token exists' : 'No token found');
        
        const response = await getTemplateList();
        console.log('Templates response:', response);
        
        if (response && response.results) {
          templates.value = response.results;
          console.log('Templates set:', templates.value);
        } else {
          console.warn('Unexpected response format:', response);
          ElMessage.warning('获取模板数据格式异常');
        }
      } catch (error) {
        console.error('Error fetching templates:', error);
        if (error.response) {
          console.error('Error response:', error.response.data);
          if (error.response.status === 401) {
            ElMessage.error('请先登录');
            router.push('/login');
          } else {
            ElMessage.error(`获取模板列表失败: ${error.response.data.detail || '未知错误'}`);
          }
        } else if (error.request) {
          ElMessage.error('网络请求失败，请检查网络连接');
        } else {
          ElMessage.error('获取模板列表失败');
        }
      }
    };

    const fetchTestHistory = async () => {
      try {
        const response = await getTemplateTests({});
        testHistory.value = response.data;
      } catch (error) {
        ElMessage.error('获取测试历史失败');
      }
    };

    const runTest = async () => {
      try {
        const inputData = JSON.parse(testForm.value.input_data);
        const response = await runTemplateTest({
          ...testForm.value,
          input_data: inputData,
        });
        testResult.value = response.data.output_content;
        ElMessage.success('测试运行成功');
        fetchTestHistory();
      } catch (error) {
        ElMessage.error('测试运行失败');
      }
    };

    const viewTestDetail = (row) => {
      testResult.value = row.output_content;
    };

    onMounted(() => {
      fetchTemplates();
      fetchTestHistory();
    });

    return {
      templates,
      testForm,
      testResult,
      formattedTestResult,
      testHistory,
      runTest,
      viewTestDetail,
    };
  },
});
</script>

<style scoped>
.template-test {
  max-width: 800px;
  margin: 0 auto;
}

.test-result {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}
</style>