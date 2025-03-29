import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";
import axios from "axios";
import { ElMessage } from "element-plus";
import router from "@/router";

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  timeout: 50000,
  headers: { "Content-Type": "application/json" },
});

// 创建不带默认拦截器的axios实例，用于第三方API调用（如Dify）
const serviceWithoutInterceptors: AxiosInstance = axios.create({
  timeout: 50000,
  headers: { "Content-Type": "application/json" },
});

// 为第三方API调用添加基本的响应拦截器
serviceWithoutInterceptors.interceptors.response.use(
  (response: AxiosResponse) => {
    // 直接返回响应数据
    return response.data;
  },
  (error) => {
    console.error("Third-party API Error:", error);
    return Promise.reject(error);
  },
);

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 处理 2xx 的响应
    if (response.status >= 200 && response.status < 300) {
      console.log("API Response:", response.data);
      return response.data;
    }
    return Promise.reject(new Error(response.data?.detail || "请求失败"));
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 400:
          ElMessage.error(data.detail || data.error || "请求参数错误");
          break;
        case 401:
          ElMessage.error("登录已过期，请重新登录");
          localStorage.removeItem("token");
          router.push("/login");
          break;
        case 403:
          ElMessage.error("没有权限访问");
          break;
        case 404:
          ElMessage.error("请求的资源不存在");
          break;
        case 500:
          ElMessage.error(data.error || data.detail || "服务器内部错误");
          break;
        default:
          ElMessage.error(
            data.error || data.detail || error.message || "未知错误",
          );
      }
    } else if (error.request) {
      ElMessage.error("网络错误，请检查网络连接");
    } else {
      ElMessage.error("请求配置错误");
    }

    return Promise.reject(error);
  },
);

// 扩展AxiosRequestConfig类型，添加自定义选项
interface ExtendedAxiosRequestConfig extends AxiosRequestConfig {
  useDefaultInterceptors?: boolean;
}

const request = <T = any>(config: ExtendedAxiosRequestConfig): Promise<T> => {
  // 提取自定义选项
  const { useDefaultInterceptors = true, ...axiosConfig } = config;

  // 选择合适的axios实例
  const axiosInstance = useDefaultInterceptors
    ? service
    : serviceWithoutInterceptors;

  // 处理blob响应类型
  if (axiosConfig.responseType === "blob") {
    return axiosInstance(axiosConfig).then(
      (response) => response as unknown as T,
    );
  }
  return axiosInstance(axiosConfig);
};

export default request;
