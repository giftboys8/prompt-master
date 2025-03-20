// 防抖函数
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>

  return function (...args: Parameters<T>) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

// 节流函数
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let lastCall = 0

  return function (...args: Parameters<T>) {
    const now = Date.now()
    if (now - lastCall >= delay) {
      fn.apply(this, args)
      lastCall = now
    }
  }
}

// 安全的JSON解析
export function safeJSONParse<T>(str: string, fallback: T): T {
  try {
    return JSON.parse(str)
  } catch (e) {
    console.error('JSON parse error:', e)
    return fallback
  }
}

// 格式化日期
export function formatDate(date: Date | string | number): string {
  const d = new Date(date)
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 深度克隆对象
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }

  if (obj instanceof Date) {
    return new Date(obj.getTime()) as any
  }

  if (obj instanceof Array) {
    return obj.map(item => deepClone(item)) as any
  }

  if (obj instanceof Object) {
    const copy = {} as T
    Object.keys(obj).forEach(key => {
      copy[key as keyof T] = deepClone(obj[key as keyof T])
    })
    return copy
  }

  return obj
}

// 错误处理包装器
export function errorWrapper<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  errorHandler?: (error: Error) => void
): (...args: Parameters<T>) => Promise<ReturnType<T>> {
  return async function (...args: Parameters<T>): Promise<ReturnType<T>> {
    try {
      return await fn.apply(this, args)
    } catch (error) {
      if (errorHandler) {
        errorHandler(error as Error)
      }
      throw error
    }
  }
}