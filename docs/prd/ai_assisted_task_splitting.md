# AI辅助任务拆分功能PRD文档

## 1. 业务目标
在新增场景页面提供“AI辅助任务拆分”功能，根据场景名称、分类、描述和模板角色，使用AI生成任务列表，并自动完成任务名称、任务描述和任务模板的选择。用户可以通过修改和确认，最终完成整个业务场景的创建。

## 2. 功能需求
### 2.1 功能概述
- **输入**：场景名称、分类、描述、模板角色
- **输出**：生成1到多个的任务，分别包括任务名称、任务描述、管理的提示词模板
- **用户操作**：用户可以对生成的任务进行修改和确认

### 2.2 功能流程
1. 用户在新增场景页面填写场景名称、分类、描述和选择模板角色。
2. 用户点击“AI辅助任务拆分”按钮。
3. 系统调用AI模型，根据输入信息生成任务集。
4. 系统展示生成的任务集，用户可以对任务进行修改。
5. 用户确认任务集后，系统保存任务列表并完成场景创建。

## 3. 用户流程
1. 用户进入新增场景页面。
2. 用户填写场景信息并选择目标角色。
3. 用户点击“AI辅助任务拆分”按钮。
4. 系统生成任务集（1到多个任务）并展示给用户。
5. 用户修改任务集，并确认信息。
6. 系统保存任务列表并完成场景创建。
