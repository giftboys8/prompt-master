import { useUserStore } from '@/stores/user';

export interface Resource {
  creator_id?: number;
  created_by?: number;
  id: number;
}

/**
 * 检查用户是否有指定权限
 * @param permission 权限代码
 * @returns boolean
 */
export function hasPermission(permission: string): boolean {
  const userStore = useUserStore();
  return userStore.permissions.includes(permission);
}

/**
 * 检查用户是否对特定资源有操作权限
 * @param permission 基础权限代码
 * @param resource 资源对象
 * @returns boolean
 */
export function hasResourcePermission(permission: string, resource?: Resource): boolean {
  const userStore = useUserStore();
  const userId = userStore.user?.id;

  // 如果是管理员，拥有所有权限
  if (userStore.user?.is_staff) {
    return true;
  }

  // 允许所有已登录用户创建资源
  if (permission === 'create') {
    return true;
  }

  // 检查基础权限
  if (hasPermission(permission)) {
    return true;
  }

  // 检查针对自己创建的资源的权限
  if (resource && userId) {
    const creatorId = resource.creator_id || resource.created_by;
    // 允许用户编辑和删除自己创建的资源
    if (creatorId === userId && (permission === 'edit' || permission === 'delete')) {
      return true;
    }
    const ownPermission = `${permission}:own`;
    return creatorId === userId && hasPermission(ownPermission);
  }

  return false;
}

/**
 * 检查用户是否可以编辑资源
 */
export function canEdit(resource?: Resource): boolean {
  return hasResourcePermission('edit', resource);
}

/**
 * 检查用户是否可以删除资源
 */
export function canDelete(resource?: Resource): boolean {
  return hasResourcePermission('delete', resource);
}

/**
 * 检查用户是否可以克隆资源
 */
export function canClone(resource?: Resource): boolean {
  return hasResourcePermission('clone', resource);
}

/**
 * 检查用户是否可以测试资源
 */
export function canTest(resource?: Resource): boolean {
  return hasResourcePermission('test', resource);
}