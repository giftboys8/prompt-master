import request from './request'

export interface DifyMessageRequest {
  query: string
  inputs?: Record<string, any>
  response_mode?: 'streaming' | 'blocking'
  user: string
  conversation_id?: string
  files?: Array<{
    type: string
    transfer_method: 'remote_url' | 'local_file'
    url?: string
  }>
  auto_generate_name?: boolean
}

export interface DifyMessageResponse {
  message_id: string
  conversation_id: string
  mode: string
  answer: string
  metadata: {
    usage: {
      prompt_tokens: number
      completion_tokens: number
      total_tokens: number
      total_price: string
      currency: string
      latency: number
    }
    retriever_resources?: Array<{
      position: number
      dataset_id: string
      dataset_name: string
      document_id: string
      document_name: string
      segment_id: string
      score: number
      content: string
    }>
  }
  created_at: number
}

export function sendMessage(data: DifyMessageRequest) {
  // 打印环境变量，便于调试
  console.log('Dify API Base URL:', import.meta.env.VITE_DIFY_API_BASE_URL);
  console.log('Dify API Key is set:', !!import.meta.env.VITE_DIFY_API_KEY);
  
  const apiKey = import.meta.env.VITE_DIFY_API_KEY;
  if (!apiKey) {
    console.error('Dify API Key is not set in environment variables');
    return Promise.reject(new Error('API密钥未配置，请检查环境变量'));
  }
  
  const baseURL = import.meta.env.VITE_DIFY_API_BASE_URL;
  if (!baseURL) {
    console.error('Dify API Base URL is not set in environment variables');
    return Promise.reject(new Error('API基础URL未配置，请检查环境变量'));
  }
  
  console.log('Sending request to Dify API:', `${baseURL}/chat-messages`);
  console.log('Request data:', JSON.stringify(data, null, 2));
  
  // 创建一个独立的axios实例用于Dify API调用
  return request({
    url: '/chat-messages',
    method: 'post',
    data,
    baseURL,
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    // 不使用默认的request拦截器（它可能会添加JWT token）
    useDefaultInterceptors: false
  }).then(response => {
    console.log('Dify API Response:', response);
    return response;
  }).catch(error => {
    console.error('Dify API Error:', error);
    
    if (error.response) {
      console.error('Error Status:', error.response.status);
      console.error('Error Headers:', error.response.headers);
      console.error('Error Data:', error.response.data);
      
      if (error.response.status === 401) {
        console.error('Dify API认证失败，请检查API密钥是否正确');
      } else if (error.response.status === 404) {
        console.error('Dify API端点不存在，请检查API基础URL是否正确');
      } else if (error.response.status >= 500) {
        console.error('Dify API服务器错误');
      }
    } else if (error.request) {
      console.error('没有收到响应，请检查网络连接或API服务器是否可用');
    } else {
      console.error('请求配置错误:', error.message);
    }
    
    throw error;
  });
}