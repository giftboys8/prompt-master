<!-- FrameworkSelect.vue -->
<template>
  <div class="framework-select">
    <el-select
      v-model="selectedFramework"
      :placeholder="placeholder"
      :disabled="disabled"
      :loading="loading"
      clearable
      @change="handleChange"
    >
      <el-option
        v-for="framework in frameworks"
        :key="framework.id"
        :label="framework.name"
        :value="framework.id"
      >
        <div class="framework-option">
          <span>{{ framework.name }}</span>
          <small v-if="showDescription" class="description">{{
            framework.description
          }}</small>
          <div
            v-if="showModules && framework.modules?.length"
            class="modules-list"
          >
            <span
              v-for="module in framework.modules"
              :key="module.id"
              class="module-tag"
            >
              {{ module.name }}
            </span>
          </div>
        </div>
      </el-option>
    </el-select>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { getFrameworks } from "@/api/frameworks";
import type { Framework } from "@/api/frameworks";

const props = defineProps({
  modelValue: {
    type: [Number, Object, null],
    default: null,
  },
  placeholder: {
    type: String,
    default: "请选择框架",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  showDescription: {
    type: Boolean,
    default: false,
  },
  showModules: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(["update:modelValue", "change"]);

const frameworks = ref<Framework[]>([]);
// 如果modelValue是对象，则使用其id值；否则直接使用modelValue
const selectedFramework = ref(
  typeof props.modelValue === "object" && props.modelValue
    ? props.modelValue.id
    : props.modelValue,
);
const loading = ref(false);

const fetchFrameworks = async () => {
  loading.value = true;
  try {
    const response = await getFrameworks();
    console.log("Frameworks API Response:", response);
    frameworks.value = response.results || response.data || [];
    console.log("Frameworks after assignment:", frameworks.value);
  } catch (error) {
    console.error("获取框架列表失败:", error);
  } finally {
    loading.value = false;
  }
};

const handleChange = (value: number | null) => {
  emit("update:modelValue", value);
  console.log("FrameworkSelect - Selected value:", value);

  if (value === null) {
    console.log("FrameworkSelect - Emitting null");
    emit("change", null);
  } else {
    const selectedItem = frameworks.value.find((item) => item.id === value);
    console.log("FrameworkSelect - Selected framework:", selectedItem);

    // 检查模块信息
    if (selectedItem) {
      console.log("FrameworkSelect - Framework modules:", selectedItem.modules);
    }

    emit("change", value); // 只传递框架 ID
  }
};

// 监听外部传入的值变化
watch(
  () => props.modelValue,
  (newVal) => {
    // 如果是对象，则取其id值；否则直接使用newVal
    selectedFramework.value =
      typeof newVal === "object" && newVal ? newVal.id : newVal;
    console.log(
      "FrameworkSelect - modelValue changed:",
      newVal,
      "selectedFramework set to:",
      selectedFramework.value,
    );
  },
);

onMounted(() => {
  fetchFrameworks();
});
</script>

<style scoped lang="scss">
.framework-select {
  width: 100%;

  :deep(.el-select) {
    width: 100%;
  }
}

.framework-option {
  display: flex;
  flex-direction: column;
  gap: 4px;

  .description {
    color: #999;
    font-size: 12px;
  }

  .modules-list {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 4px;

    .module-tag {
      background-color: #f0f2f5;
      color: #666;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 12px;
    }
  }
}
</style>
