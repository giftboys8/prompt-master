<template>
  <div class="template-test-container">
    <a-row :gutter="16">
      <!-- 左侧：提示词模板内容和测试按钮 -->
      <a-col :span="12">
        <a-card title="提示词模板内容" :bordered="false">
          <template v-if="template">
            <h2>{{ template.name }}</h2>
            <p>{{ template.description }}</p>
            <a-form :model="formState" @finish="handleTest">
              <div
                v-for="(field, index) in template.variables"
                :key="index"
                class="form-field"
              >
                <a-form-item
                  :label="field.name"
                  :name="field.name"
                  :rules="[{ required: true, message: '请输入' + field.name }]"
                >
                  <a-input
                    v-model:value="formState[field.name]"
                    :placeholder="'请输入' + field.name"
                  />
                </a-form-item>
              </div>
              <a-form-item>
                <a-select
                  v-model:value="selectedApiKey"
                  style="width: 100%"
                  placeholder="选择API密钥"
                >
                  <a-select-option
                    v-for="key in apiKeys"
                    :key="key.id"
                    :value="key.key"
                  >
                    {{ key.platform_name }} - {{ key.scene_name }}
                  </a-select-option>
                </a-select>
              </a-form-item>
              <a-form-item>
                <a-button type="primary" html-type="submit" :loading="testing"
                  >测试模板</a-button
                >
              </a-form-item>
            </a-form>
          </template>
          <div v-else-if="templateLoading" class="loading-state">
            <a-spin size="large" />
          </div>
          <div v-else>
            <a-empty description="请选择一个模板进行测试" />
          </div>
        </a-card>
      </a-col>

      <!-- 右侧：测试结果 -->
      <a-col :span="12">
        <a-card title="处理后的内容" :bordered="false">
          <template v-if="testResult">
            <div v-if="processedContent" class="test-result-content">
              <div class="processed-content" v-html="processedContent"></div>
            </div>
          </template>
          <div v-else class="no-result">
            <a-empty description="暂无测试结果" />
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- 底部：历史记录 -->
    <a-card title="历史记录" :bordered="false" style="margin-top: 16px">
      <a-table
        :data-source="testHistory"
        :columns="historyColumns"
        :pagination="{ pageSize: 5 }"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.dataIndex === 'action'">
            <a @click="viewHistoryDetail(record)">查看详情</a>
          </template>
        </template>
      </a-table>
    </a-card>

    <!-- 历史记录详情弹窗 -->
    <a-modal
      v-model:open="historyDetailVisible"
      title="测试历史详情"
      @ok="historyDetailVisible = false"
    >
      <pre v-if="selectedHistoryDetail">{{
        JSON.stringify(selectedHistoryDetail, null, 2)
      }}</pre>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, reactive, computed } from "vue";
import { useRoute } from "vue-router";
import { message } from "ant-design-vue";
import { getTemplate, runTemplateTest } from "@/api/templates";
import { getApiKeys } from "@/api/apikeys";
import { sendMessage } from "@/api/dify";
import request from "@/api/request";
import { getTemplateTests } from "@/api/templates";
import type { Template, TemplateTest } from "@/types";

const route = useRoute();
const template = ref<Template | null>(null);
const templateLoading = ref(false);
const formState = reactive<Record<string, any>>({});
const apiKeys = ref<any[]>([]);
const selectedApiKey = ref<string>("");
const testing = ref(false);
const testResult = ref<any | null>(null);
const testHistory = ref<TemplateTest[]>([]);
const processedContent = computed(() => {
  if (testResult.value && testResult.value.answer) {
    return testResult.value.answer.replace(/\n/g, "<br>");
  }
  return "";
});

const historyColumns = [
  { title: "测试时间", dataIndex: "created_at", key: "created_at" },
  { title: "模板名称", dataIndex: "template_name", key: "template_name" },
  { title: "操作", dataIndex: "action", key: "action" },
];

const historyDetailVisible = ref(false);
const selectedHistoryDetail = ref<TemplateTest | null>(null);

onMounted(async () => {
  const templateId = route.params.id ? Number(route.params.id) : null;
  if (templateId && !isNaN(templateId)) {
    await loadTemplate(templateId);
  }
  await loadApiKeys();
  await loadTestHistory();
});

const loadTemplate = async (id: number) => {
  templateLoading.value = true;
  try {
    template.value = await getTemplate(id);
    initFormState();
  } catch (error) {
    console.error("加载模板失败:", error);
    message.error("加载模板失败");
  } finally {
    templateLoading.value = false;
  }
};

const initFormState = () => {
  if (!template.value) return;
  template.value.variables.forEach((variable) => {
    formState[variable.name] = "";
  });
};

const loadApiKeys = async () => {
  try {
    const response = await getApiKeys();
    console.log("API密钥响应:", response);
    apiKeys.value = response.results || [];
    if (!apiKeys.value.length) {
      console.warn("API密钥列表为空");
    }
  } catch (error) {
    console.error("加载API密钥失败:", error);
    message.error("加载API密钥失败");
  }
};

const loadTestHistory = async () => {
  try {
    const response = await getTemplateTests({
      template_id: template.value?.id,
    });
    console.log("测试历史响应:", response);
    testHistory.value = response.results || [];
    if (!testHistory.value.length) {
      console.warn("测试历史列表为空");
    }
  } catch (error) {
    console.error("加载测试历史失败:", error);
    message.error("加载测试历史失败");
  }
};

// 定义测试模板的函数
const testTemplate = async (templateId: number, data: any) => {
  testing.value = true;
  let difyResponse;

  try {
    const variableValues = { ...formState };

    // 处理模板内容
    const templateContent = template.value?.content || "";
    // 确保query是字符串而不是对象
    const query = typeof templateContent === 'string' ? templateContent : JSON.stringify(templateContent);

    difyResponse = await sendMessage({
      api_key: selectedApiKey.value,
      user_id: "template-tester",
      inputs: variableValues,
      query: query,
      response_mode: "blocking",
      conversation_id: "",
      user: "template-tester",
    });

    console.log("收到测试响应:", difyResponse);

    // 处理响应数据
    const finalResponse =
      typeof difyResponse === "string"
        ? JSON.parse(difyResponse)
        : difyResponse;

    console.log("收到最终响应:", finalResponse);

    // 设置测试结果
    testResult.value = {
      ...finalResponse,
      answer: finalResponse.answer || "",
      raw_final_response: finalResponse,
      metadata: finalResponse.metadata || {},
    };

    console.log("设置最终测试结果:", testResult.value);

    // 构造测试记录数据
    const testData = {
      template: template.value?.id,
      model: finalResponse.metadata?.usage?.model || "Dify API",
      input_data: formState,
      dify_response: finalResponse,
      output_content: finalResponse.answer || JSON.stringify(finalResponse),
    };

    // 如果有使用统计信息，添加到测试数据中
    if (finalResponse.metadata?.usage) {
      testData.dify_response.metadata = {
        usage: finalResponse.metadata.usage,
      };
    }

      // 保存测试记录到后端
      try {
        const saveResponse = await runTemplateTest(testData);
      console.log("保存测试记录响应:", saveResponse);
      message.success("测试记录已保存");
    } catch (saveError) {
      console.error("保存测试记录失败:", saveError);
      message.error("保存测试记录失败");
    }

    message.success("测试成功");
    await loadTestHistory(); // 刷新测试历史
  } catch (error) {
    console.error("测试失败:", error);
    let errorMessage = "未知错误";
    if (error instanceof Error) {
      errorMessage = error.message;
    } else if (typeof error === "object" && error !== null) {
      errorMessage = JSON.stringify(error);
    }
    message.error(`测试失败: ${errorMessage}`);
    testResult.value = {
      error: true,
      answer: `测试失败: ${errorMessage}`,
      metadata: {
        error_details: error,
      },
    };
  } finally {
    testing.value = false;
    return testResult.value;
  }
};

const handleTest = async () => {
  if (!template.value || !selectedApiKey.value) {
    message.error("请选择模板和API密钥");
    return;
  }

  testing.value = true;
  testResult.value = null; // 清空之前的测试结果

  try {
    const response = await testTemplate(template.value.id, {
      inputs: formState,
    });

    if (response) {
      testResult.value = response;
    }
  } catch (error) {
    console.error("测试模板时出错:", error);
    testResult.value = {
      error: true,
      answer:
        "测试模板时出错: " +
        (error instanceof Error ? error.message : String(error)),
      metadata: {
        error_details: error,
      },
    };
  }
};

const viewHistoryDetail = (record: TemplateTest) => {
  selectedHistoryDetail.value = record;
  historyDetailVisible.value = true;
};
</script>

<style scoped>
.template-test-container {
  padding: 24px;
}
.form-field {
  margin-bottom: 16px;
}
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}
.test-result-content {
  margin-bottom: 20px;
  padding: 16px;
  background: var(--bg-light);
  border-radius: 8px;
}
.processed-content {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
}
.no-result {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}
</style>
