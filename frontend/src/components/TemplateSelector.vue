<template>
  <div class="template-selector">
    <el-form-item label="选择模板" required>
      <el-select
        :model-value="modelValue"
        placeholder="请选择模板"
        @update:modelValue="$emit('update:modelValue', $event)"
        @change="$emit('change', $event)"
        filterable
        class="template-select"
      >
        <el-option
          v-for="template in templates"
          :key="template.id"
          :label="template.name"
          :value="template.id"
        >
          <div class="template-option">
            <div class="template-name">{{ template.name }}</div>
            <div class="template-description">{{ template.description }}</div>
          </div>
        </el-option>
      </el-select>
    </el-form-item>
  </div>
</template>

<script setup lang="ts">
import type { Template } from "@/types";

defineProps<{
  modelValue: number | null;
  templates: Template[];
}>();

defineEmits<{
  (e: "update:modelValue", value: number): void;
  (e: "change", value: number): void;
}>();
</script>

<style lang="scss" scoped>
.template-selector {
  margin-bottom: 24px;

  .template-select {
    width: 100%;
  }
}

.template-option {
  padding: 8px 0;
}

.template-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.template-description {
  font-size: 12px;
  color: var(--text-secondary);
}
</style>
