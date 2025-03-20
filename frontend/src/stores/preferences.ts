import { defineStore } from 'pinia'
import { ref } from 'vue'
import { cacheManager, CacheKey } from '@/utils/cache'

// 用户偏好设置接口
export interface UserPreferences {
  templateListView: 'grid' | 'list';
  templateSortOrder: 'manual' | 'name' | 'updateTime';
  theme: 'system' | 'light' | 'dark';
  language: string;
  previewMode: 'basic' | 'chat' | 'format' | 'interactive';
}

// 默认偏好设置
const defaultPreferences: UserPreferences = {
  templateListView: 'grid',
  templateSortOrder: 'manual',
  theme: 'system',
  language: 'zh-CN',
  previewMode: 'basic'
}

export const usePreferencesStore = defineStore('preferences', () => {
  // 状态
  const preferences = ref<UserPreferences>(
    cacheManager.get<UserPreferences>(CacheKey.USER_PREFERENCES) || defaultPreferences
  )

  // 更新偏好设置
  const updatePreferences = (newPreferences: Partial<UserPreferences>) => {
    preferences.value = {
      ...preferences.value,
      ...newPreferences
    }
    // 保存到本地存储
    cacheManager.set(CacheKey.USER_PREFERENCES, preferences.value)
  }

  // 重置偏好设置
  const resetPreferences = () => {
    preferences.value = { ...defaultPreferences }
    cacheManager.set(CacheKey.USER_PREFERENCES, preferences.value)
  }

  return {
    preferences,
    updatePreferences,
    resetPreferences
  }
})