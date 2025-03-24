// 缓存键名枚举
export enum CacheKey {
  TEMPLATES = "templates",
  USER_PREFERENCES = "user_preferences",
  RECENT_TEMPLATES = "recent_templates",
  TEMPLATE_DRAFTS = "template_drafts",
}

// 缓存配置接口
interface CacheConfig {
  expire?: number; // 过期时间（毫秒）
}

// 缓存项接口
interface CacheItem<T> {
  data: T;
  timestamp: number;
  expire?: number;
}

/**
 * 缓存管理类
 */
export class CacheManager {
  private static instance: CacheManager;
  private storage: Storage;

  private constructor() {
    this.storage = window.localStorage;
  }

  /**
   * 获取缓存管理实例
   */
  public static getInstance(): CacheManager {
    if (!CacheManager.instance) {
      CacheManager.instance = new CacheManager();
    }
    return CacheManager.instance;
  }

  /**
   * 设置缓存
   * @param key 缓存键名
   * @param data 缓存数据
   * @param config 缓存配置
   */
  public set<T>(key: string, data: T, config: CacheConfig = {}): void {
    const cacheItem: CacheItem<T> = {
      data,
      timestamp: Date.now(),
      expire: config.expire,
    };

    try {
      this.storage.setItem(key, JSON.stringify(cacheItem));
    } catch (error) {
      console.error("Cache set error:", error);
      // 如果存储失败（可能是存储空间已满），尝试清理过期缓存
      this.clearExpired();
    }
  }

  /**
   * 获取缓存
   * @param key 缓存键名
   * @returns 缓存数据
   */
  public get<T>(key: string): T | null {
    const item = this.storage.getItem(key);
    if (!item) return null;

    try {
      const cacheItem: CacheItem<T> = JSON.parse(item);

      // 检查是否过期
      if (
        cacheItem.expire &&
        Date.now() - cacheItem.timestamp > cacheItem.expire
      ) {
        this.remove(key);
        return null;
      }

      return cacheItem.data;
    } catch (error) {
      console.error("Cache get error:", error);
      return null;
    }
  }

  /**
   * 移除缓存
   * @param key 缓存键名
   */
  public remove(key: string): void {
    this.storage.removeItem(key);
  }

  /**
   * 清理所有缓存
   */
  public clear(): void {
    this.storage.clear();
  }

  /**
   * 清理过期缓存
   */
  public clearExpired(): void {
    for (let i = 0; i < this.storage.length; i++) {
      const key = this.storage.key(i);
      if (key) {
        const item = this.storage.getItem(key);
        if (item) {
          try {
            const cacheItem: CacheItem<any> = JSON.parse(item);
            if (
              cacheItem.expire &&
              Date.now() - cacheItem.timestamp > cacheItem.expire
            ) {
              this.remove(key);
            }
          } catch (error) {
            // 如果解析失败，说明不是我们的缓存数据，跳过
            continue;
          }
        }
      }
    }
  }

  /**
   * 获取缓存大小（字节）
   */
  public size(): number {
    let size = 0;
    for (let i = 0; i < this.storage.length; i++) {
      const key = this.storage.key(i);
      if (key) {
        const item = this.storage.getItem(key);
        if (item) {
          size += key.length + item.length;
        }
      }
    }
    return size;
  }

  /**
   * 检查是否支持本地存储
   */
  public isSupported(): boolean {
    try {
      const testKey = "__test__";
      this.storage.setItem(testKey, testKey);
      this.storage.removeItem(testKey);
      return true;
    } catch (e) {
      return false;
    }
  }
}

// 导出缓存管理器实例
export const cacheManager = CacheManager.getInstance();
