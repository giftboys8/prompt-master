// 框架选择组件属性
export interface FrameworkSelectProps {
  modelValue: number | null;
  placeholder?: string;
  disabled?: boolean;
  showDescription?: boolean;
}

// 用户类型
export interface User {
  id: number;
  username: string;
  email: string;
  is_staff: boolean;
  date_joined: string;
}

// 提示词模版类型
export interface Template {
  id: number;
  name: string;
  framework: {
    id: number;
    name: string;
    description?: string;
    modules?: Array<{
      id: number;
      name: string;
      description: string;
    }>;
  } | null;
  description: string;
  content: {
    role?: string;
    task?: string;
    goal?: string;
    output?: string;
    situation?: string;
    purpose?: string;
    action?: string;
    result?: string;
    custom?: string;
  };
  variables: Array<{
    name: string;
    default_value: string;
    description: string;
  }>;
  order: number;
  target_role: string;
  created_at: string;
  updated_at: string;
  created_by: number;
}

// 共享模板类型
export interface SharedTemplate {
  id: number;
  template: number;
  template_name: string;
  shared_with: User;
  created_by: User;
  can_edit: boolean;
  status: "pending" | "accepted" | "rejected";
  created_at: string;
}

export interface TemplateVersion {
  id: number;
  template: number;
  version_number: number;
  name: string;
  framework: any;
  description: string;
  content: {
    role?: string;
    task?: string;
    goal?: string;
    output?: string;
    situation?: string;
    purpose?: string;
    action?: string;
    result?: string;
    custom?: string;
  };
  variables: Array<{
    name: string;
    default_value: string;
    description: string;
  }>;
  is_current: boolean;
  created_at: string;
  created_by: number;
  created_by_username: string;
}

// 业务场景类型
export interface Scene {
  id: number;
  name: string;
  description: string;
  templates: number[];
  created_at: string;
  updated_at: string;
  created_by: number;
}

// 生成内容类型
export interface Content {
  id: number;
  title: string;
  content: string;
  template_id: number;
  scene_id: number;
  created_at: string;
  updated_at: string;
  created_by: number;
}

// 模板测试类型
export interface TemplateTest {
  id: number;
  template: number;
  model: string;
  input_data: Record<string, any>;
  output_content: string;
  prompt: string;
  dify_response: Record<string, any>;
  created_at: string;
  created_by: number;
}
