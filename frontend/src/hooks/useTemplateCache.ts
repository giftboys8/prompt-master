import { ref, onMounted } from "vue";
import { cacheManager, CacheKey } from "@/utils/cache";
import { getTemplateList } from "@/api/templates";
import type { Template } from "@/types";

interface UseTemplateCacheOptions {
  maxRecentTemplates?: number;
  cacheExpire?: number;
}

export function useTemplateCache(options: UseTemplateCacheOptions = {}) {
  const {
    maxRecentTemplates = 10,
    cacheExpire = 5 * 60 * 1000, // 5分钟
  } = options;

  const templates = ref<Template[]>([]);
  const recentTemplates = ref<Template[]>([]);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  // 从缓存或API加载模板列表
  const loadTemplates = async (forceRefresh = false) => {
    loading.value = true;
    error.value = null;

    try {
      // 如果不是强制刷新，先尝试从缓存获取
      if (!forceRefresh) {
        const cachedTemplates = cacheManager.get<Template[]>(
          CacheKey.TEMPLATES,
        );
        if (cachedTemplates) {
          templates.value = cachedTemplates;
          loading.value = false;
          return cachedTemplates;
        }
      }

      // 从API获取数据
      const response = await getTemplateList();
      templates.value = response.results;

      // 更新缓存
      cacheManager.set(CacheKey.TEMPLATES, templates.value, {
        expire: cacheExpire,
      });

      return templates.value;
    } catch (err) {
      error.value = err as Error;
      return null;
    } finally {
      loading.value = false;
    }
  };

  // 添加最近访问的模板
  const addRecentTemplate = (template: Template | null | undefined) => {
    // 安全检查：如果模板为空或没有ID，则不处理
    if (!template || template.id === undefined || template.id === null) {
      console.warn("尝试添加无效模板到缓存");
      return;
    }

    // 从缓存获取现有的最近模板
    const recent =
      cacheManager.get<Template[]>(CacheKey.RECENT_TEMPLATES) || [];

    // 移除重复项
    const filtered = recent.filter((t) => t && t.id !== template.id);

    // 添加到开头
    filtered.unshift(template);

    // 限制数量
    const updated = filtered.slice(0, maxRecentTemplates);

    // 更新状态和缓存
    recentTemplates.value = updated;
    cacheManager.set(CacheKey.RECENT_TEMPLATES, updated);
  };

  // 获取最近访问的模板
  const loadRecentTemplates = () => {
    const recent =
      cacheManager.get<Template[]>(CacheKey.RECENT_TEMPLATES) || [];
    recentTemplates.value = recent;
  };

  // 保存模板草稿
  const saveTemplateDraft = (template: Partial<Template>) => {
    const drafts =
      cacheManager.get<Partial<Template>[]>(CacheKey.TEMPLATE_DRAFTS) || [];
    const draftIndex = drafts.findIndex((d) => d.id === template.id);

    if (draftIndex !== -1) {
      drafts[draftIndex] = template;
    } else {
      drafts.push(template);
    }

    cacheManager.set(CacheKey.TEMPLATE_DRAFTS, drafts);
  };

  // 获取模板草稿
  const getTemplateDraft = (templateId: number) => {
    const drafts =
      cacheManager.get<Partial<Template>[]>(CacheKey.TEMPLATE_DRAFTS) || [];
    return drafts.find((d) => d.id === templateId);
  };

  // 删除模板草稿
  const deleteTemplateDraft = (templateId: number) => {
    const drafts =
      cacheManager.get<Partial<Template>[]>(CacheKey.TEMPLATE_DRAFTS) || [];
    const updatedDrafts = drafts.filter((d) => d.id !== templateId);
    cacheManager.set(CacheKey.TEMPLATE_DRAFTS, updatedDrafts);
  };

  // 组件挂载时加载数据
  onMounted(() => {
    loadTemplates();
    loadRecentTemplates();
  });

  return {
    templates,
    recentTemplates,
    loading,
    error,
    loadTemplates,
    addRecentTemplate,
    loadRecentTemplates,
    saveTemplateDraft,
    getTemplateDraft,
    deleteTemplateDraft,
  };
}
