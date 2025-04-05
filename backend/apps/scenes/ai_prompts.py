# AI提示词配置

TASK_SPLITTING_PROMPT = """
基于以下场景信息，生成一个任务列表：

场景名称: {scene_name}
场景分类: {category}
场景描述: {description}
模板角色: {template_role}

请生成1到多个任务，每个任务包括：
1. 任务名称
2. 任务描述
3. 管理的提示词模板（从现有模板中选择最合适的）

输出格式应为JSON数组，例如：
[
    {
        "task_name": "任务1名称",
        "task_description": "任务1描述",
        "template_name": "选择的模板名称"
    },
    {
        "task_name": "任务2名称",
        "task_description": "任务2描述",
        "template_name": "选择的模板名称"
    }
]

请确保生成的任务合理、全面，并且与给定的场景信息相关。
"""