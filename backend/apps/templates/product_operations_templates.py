from django.contrib.auth import get_user_model
from frameworks.models import Framework
from .models import Template

User = get_user_model()

def create_product_operations_templates(user_id):
    """创建产品运营经理的提示词模板"""
    user = User.objects.get(id=user_id)
    rtgo_framework = Framework.objects.get(name='RTGO框架')
    smart_framework = Framework.objects.get(name='SMART框架')

    templates = [
        {
            "name": "产品活动策划与执行",
            "description": "帮助产品运营经理规划和执行产品推广活动，包括活动策划、执行计划和效果评估",
            "framework": rtgo_framework,
            "framework_type": "RTGO框架",
            "content": {
                "prompt": """作为产品运营经理，请为产品{product_name}设计一个完整的活动方案：

Role（角色定位）：
- 产品运营经理，负责产品推广和用户增长

Task（具体任务）：
1. 设计针对{target_audience}的产品推广活动
2. 制定详细的执行计划
3. 设置活动效果评估指标

Goal（目标）：
- 活动预期参与人数：{expected_participants}
- 活动预算：{budget}
- 活动周期：{duration}

请提供以下Output（输出）：
1. 活动概述
   - 活动名称和主题
   - 活动时间和周期
   - 活动形式和玩法

2. 详细执行计划
   - 前期准备工作清单
   - 活动物料清单
   - 推广渠道规划
   - 时间节点安排
   - 人力资源分配

3. 预算分配方案
   - 各环节预算明细
   - 预算使用计划

4. 活动效果评估方案
   - 核心KPI设置
   - 数据监控方案
   - ROI评估方法

5. 风险管控
   - 可能存在的风险点
   - 应对措施
   - 紧急预案

请确保方案具有可操作性，并包含具体的时间节点和负责人角色分配。"""
            },
            "variables": ["product_name", "target_audience", "expected_participants", "budget", "duration"],
            "target_role": "产品运营经理"
        },
        {
            "name": "用户运营数据分析与决策",
            "description": "基于用户行为数据进行深度分析，为产品运营决策提供数据支持",
            "framework": rtgo_framework,
            "framework_type": "RTGO框架",
            "content": {
                "prompt": """作为产品运营经理，请对{time_period}的用户运营数据进行分析并提供决策建议：

Role（角色定位）：
- 数据分析导向的产品运营经理

Task（具体任务）：
1. 分析用户行为数据
2. 识别关键问题和机会
3. 提供数据驱动的决策建议

Goal（目标）：
- 提升用户活跃度
- 改善用户留存率
- 优化用户转化漏斗

基于以下数据，请提供详细的Output（输出）：
- 新增用户数：{new_users}
- 日活用户数（DAU）：{daily_active_users}
- 月活用户数（MAU）：{monthly_active_users}
- 用户留存率：{retention_rate}
- 用户转化率：{conversion_rate}

1. 数据概览与趋势分析
   - 关键指标表现
   - 环比/同比变化
   - 异常数据识别

2. 用户行为洞察
   - 用户活跃度分析
   - 用户留存分析
   - 用户转化漏斗分析
   - 用户分层分析

3. 问题诊断
   - 关键问题识别
   - 原因分析
   - 影响评估

4. 优化建议
   - 短期优化方案
   - 中长期改进计划
   - 预期效果评估

5. 行动计划
   - 具体执行步骤
   - 优先级排序
   - 资源需求评估
   - 时间节点规划

请确保分析结论有数据支持，并提供可执行的优化建议。"""
            },
            "variables": ["time_period", "new_users", "daily_active_users", "monthly_active_users", "retention_rate", "conversion_rate"],
            "target_role": "产品运营经理"
        },
        {
            "name": "产品运营KPI制定与跟踪",
            "description": "使用SMART框架制定产品运营的关键绩效指标并建立跟踪机制",
            "framework": smart_framework,
            "framework_type": "SMART框架",
            "content": {
                "prompt": """作为产品运营经理，请为{product_name}制定{quarter}的KPI指标体系：

Specific（具体）：
- 产品类型：{product_type}
- 当前阶段：{product_stage}
- 主要目标用户群：{target_users}

Measurable（可衡量）：
请基于以下基础数据制定具体的量化指标：
- 上季度用户增长率：{last_quarter_growth}
- 当前月活用户数：{current_mau}
- 用户平均支付金额：{average_payment}

Achievable（可实现）：
考虑以下因素设定合理目标：
- 市场环境：{market_condition}
- 可用资源：{available_resources}
- 团队规模：{team_size}

Relevant（相关性）：
确保KPI与以下目标相关：
- 公司整体目标
- 产品发展战略
- 团队核心任务

Time-bound（时限性）：
- 考核周期：季度
- 重要时间节点设置
- 阶段性目标设定

请提供以下输出：

1. 核心KPI指标体系
   - 用户增长指标
   - 用户活跃指标
   - 商业化指标
   - 产品质量指标

2. 分解指标
   - 月度目标分解
   - 团队任务分配
   - 个人目标设定

3. 跟踪机制
   - 日常监控方案
   - 周期性复盘机制
   - 预警机制设置

4. 激励方案
   - 团队激励机制
   - 个人绩效考核
   - 奖惩制度设计

请确保所有指标都符合SMART原则，并提供具体的数值目标和评估标准。"""
            },
            "variables": ["product_name", "quarter", "product_type", "product_stage", "target_users", 
                         "last_quarter_growth", "current_mau", "average_payment", "market_condition", 
                         "available_resources", "team_size"],
            "target_role": "产品运营经理"
        },
        {
            "name": "用户反馈收集与分析",
            "description": "系统化收集和分析用户反馈，并转化为产品优化建议",
            "framework": rtgo_framework,
            "framework_type": "RTGO框架",
            "content": {
                "prompt": """作为产品运营经理，请对{feedback_period}期间收集的用户反馈进行系统化分析：

Role（角色定位）：
- 负责用户体验和产品优化的产品运营经理

Task（具体任务）：
1. 整理和分类用户反馈
2. 分析核心问题和需求
3. 提供优化建议

Goal（目标）：
- 识别关键用户痛点
- 提出可行的改进方案
- 提升用户满意度

基于以下反馈数据，请提供详细的Output（输出）：
- 用户评分：{user_rating}
- 反馈来源：{feedback_channels}
- 样本数量：{feedback_count}
- 主要问题类型：{issue_types}
- 用户期望：{user_expectations}

1. 反馈概览
   - 反馈数据统计
   - 评分分布分析
   - 问题类型占比

2. 详细分析
   - 核心问题识别
   - 用户痛点归类
   - 需求优先级排序
   - 用户情感分析

3. 改进建议
   - 短期快速优化项
   - 中长期改进计划
   - 资源投入评估
   - 预期效果预测

4. 行动计划
   - 具体优化措施
   - 责任分工建议
   - 时间节点规划
   - 效果评估方案

5. 持续跟踪机制
   - 反馈收集流程优化
   - 用户沟通机制
   - 效果跟踪方案

请确保分析全面且建议具有可操作性，并注意优先级的合理分配。"""
            },
            "variables": ["feedback_period", "user_rating", "feedback_channels", "feedback_count", 
                         "issue_types", "user_expectations"],
            "target_role": "产品运营经理"
        },
        {
            "name": "产品运营月度总结报告",
            "description": "全面总结产品运营工作，包括数据分析、工作成效和未来规划",
            "framework": rtgo_framework,
            "framework_type": "RTGO框架",
            "content": {
                "prompt": """作为产品运营经理，请生成{year_month}的月度运营总结报告：

Role（角色定位）：
- 产品运营负责人，对产品运营整体负责

Task（具体任务）：
1. 总结月度运营工作
2. 分析关键指标表现
3. 规划下月工作重点

Goal（目标）：
- 全面展示运营成效
- 复盘经验与不足
- 明确下月发展方向

基于以下数据，请提供详细的Output（输出）：
- 核心指标完成情况：{kpi_completion}
- 重点项目进展：{project_progress}
- 运营活动效果：{campaign_results}
- 用户反馈概况：{user_feedback_summary}
- 资源使用情况：{resource_utilization}

1. 月度概览
   - 关键指标达成情况
   - 重点工作完成情况
   - 预算执行情况

2. 详细工作内容
   A. 用户运营
      - 用户增长情况
      - 用户活跃度
      - 用户留存率
      - 用户反馈处理

   B. 活动运营
      - 活动列表及效果
      - ROI分析
      - 经验总结

   C. 产品优化
      - 已完成的优化项
      - 用户反馈改进
      - 效果评估

3. 问题与挑战
   - 存在的主要问题
   - 原因分析
   - 解决方案

4. 经验与启示
   - 成功经验总结
   - 失败教训分析
   - 可推广的方法

5. 下月工作规划
   - 重点工作方向
   - 具体工作计划
   - 资源需求
   - 预期目标

请确保报告数据准确，分析深入，并对未来工作有清晰的规划和建议。"""
            },
            "variables": ["year_month", "kpi_completion", "project_progress", "campaign_results", 
                         "user_feedback_summary", "resource_utilization"],
            "target_role": "产品运营经理"
        }
    ]

    for template_data in templates:
        Template.objects.create(
            name=template_data["name"],
            framework=template_data["framework"],
            framework_type=template_data["framework_type"],
            description=template_data["description"],
            content=template_data["content"],
            variables=template_data["variables"],
            target_role=template_data["target_role"],
            created_by=user,
            visibility='PUBLIC'  # 设置为公开可见
        )

    print(f"Successfully created {len(templates)} product operations templates.")