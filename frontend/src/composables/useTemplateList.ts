import { ref, computed } from "vue";
import { ElMessage } from "element-plus";
import {
  getTemplateList,
  deleteTemplate,
  cloneTemplate,
  exportTemplates,
  importTemplates,
  reorderTemplates,
} from "@/api/templates";
import { useTemplateCache } from "@/hooks/useTemplateCache";
import type { Template } from "@/types";

export function useTemplateList() {
  const loading = ref(false);
  const templates = ref<Template[]>([]);
  const total = ref(0);
  const currentPage = ref(1);
  const pageSize = ref(10);

  // 使用ref而不是computed，这样它是可变的
  const sortedTemplates = ref<Template[]>([]);

  const { loadTemplates, addRecentTemplate } = useTemplateCache();

  // 加载数据
  const loadData = async (
    params: {
      search?: string;
      target_role?: string;
      framework?: any;
    } = {},
  ) => {
    loading.value = true;
    try {
      const cachedTemplates = await loadTemplates();
      if (cachedTemplates) {
        templates.value = cachedTemplates;
        total.value = cachedTemplates.length;
        sortedTemplates.value = [...cachedTemplates].sort(
          (a, b) => (a.order || 0) - (b.order || 0),
        );
      } else {
        const res = await getTemplateList({
          page: currentPage.value,
          page_size: pageSize.value,
          ...params,
        });

        if (res && Array.isArray(res.results)) {
          templates.value = res.results;
          total.value = res.count;
          sortedTemplates.value = [...res.results].sort(
            (a, b) => (a.order || 0) - (b.order || 0),
          );
        } else {
          ElMessage.warning("返回的数据格式不符合预期");
        }
      }
    } catch (error: any) {
      if (error.response?.status === 401) {
        ElMessage.error("请先登录");
        throw new Error("未登录");
      } else {
        ElMessage.error(error.message || "加载失败");
      }
    } finally {
      loading.value = false;
    }
  };

  // 更新排序
  const updateOrder = async () => {
    try {
      const updatedOrder = sortedTemplates.value.map((template, index) => ({
        id: template.id,
        order: index,
      }));
      await reorderTemplates(updatedOrder);
      ElMessage.success("模板排序已更新");
      templates.value = [...sortedTemplates.value];
    } catch (error: any) {
      ElMessage.error(error.message || "更新排序失败");
      await loadData();
    }
  };

  // 导入模板
  const importTemplate = async (file: File) => {
    try {
      const result = await importTemplates(file);
      ElMessage.success(result.message);
      await loadData();
    } catch (error: any) {
      ElMessage.error(error.message || "导入失败");
    }
  };

  // 导出模板
  const exportTemplate = async () => {
    try {
      const response = await exportTemplates();
      const blob = new Blob([response], { type: "application/json" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "templates_export.json";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      ElMessage.success("导出成功");
    } catch (error: any) {
      ElMessage.error(error.message || "导出失败");
    }
  };

  // 克隆模板
  const cloneTemplateItem = async (id: number) => {
    try {
      const result = await cloneTemplate(id);
      if (result && result.id) {
        ElMessage.success("克隆成功");
        await loadData();
      }
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.error || error.message || "克隆失败";
      ElMessage.error(errorMessage);
    }
  };

  // 删除模板
  const removeTemplate = async (id: number) => {
    try {
      await deleteTemplate(id);
      ElMessage.success("删除成功");
      await loadData();
    } catch (error: any) {
      ElMessage.error(error.message || "删除失败");
    }
  };

  return {
    loading,
    templates,
    sortedTemplates,
    total,
    currentPage,
    pageSize,
    loadData,
    updateOrder,
    importTemplate,
    exportTemplate,
    cloneTemplateItem,
    removeTemplate,
  };
}
