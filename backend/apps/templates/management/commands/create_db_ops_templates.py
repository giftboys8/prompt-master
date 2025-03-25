from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建数据库运维工程师的提示词模板'

    def add_arguments(self, parser):
        parser.add_argument('--user_id', type=int, help='创建模板的用户ID')

    def handle(self, *args, **options):
        user_id = options.get('user_id')
        if not user_id:
            self.stderr.write(self.style.ERROR('请提供用户ID'))
            return

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'用户ID {user_id} 不存在'))
            return

        # 使用COSTAR框架
        framework, created = Framework.objects.get_or_create(
            name='COSTAR',
            defaults={
                'description': 'Context（上下文）、Objective（目标）、Scope（范围）、Task（任务）、Action（行动）、Result（结果）框架，适用于项目规划场景。'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'创建了新的框架: {framework.name}'))

        templates = [
            {
                "name": "数据库性能诊断与优化",
                "description": "对数据库性能问题进行诊断和优化",
                "content": {
                    "prompt": """作为一名资深数据库运维工程师，请对以下数据库性能问题进行诊断和优化：

Context（上下文）:
- 数据库类型：{db_type}
- 性能问题描述：{performance_issue}
- 当前状态指标：{current_metrics}

Objective（目标）:
1. 准确诊断性能瓶颈
2. 提供优化建议
3. 制定实施方案
4. 评估优化效果

Scope（范围）:
- SQL查询性能
- 索引使用情况
- 资源利用率
- 配置参数
- 数据库架构

Task（任务）:
1. 性能数据收集和分析
2. 慢查询识别和优化
3. 索引评估和优化
4. 配置参数调优
5. 架构优化建议

Action（行动）:
请提供详细的：
1. 性能诊断步骤
2. 具体优化建议
3. 实施方案
4. 回滚预案

Result（结果）:
请输出：
1. 性能问题根因分析
2. 优化建议清单
3. 具体实施步骤
4. 预期改进效果
5. 长期优化建议"""
                },
                "variables": ["db_type", "performance_issue", "current_metrics"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库备份恢复方案",
                "description": "设计数据库备份策略和恢复方案",
                "content": {
                    "prompt": """作为数据库运维工程师，请设计以下数据库的备份恢复方案：

Context（上下文）:
- 数据库环境：{db_environment}
- 数据量规模：{data_volume}
- 业务要求：{business_requirements}

Objective（目标）:
1. 确保数据安全性
2. 满足恢复时间目标
3. 优化备份性能
4. 减少对业务影响

Scope（范围）:
- 备份策略
- 恢复流程
- 监控告警
- 定期验证
- 容灾考虑

Task（任务）:
1. 备份需求分析
2. 备份方案设计
3. 恢复流程设计
4. 监控方案设计
5. 验证计划制定

Action（行动）:
请提供：
1. 备份策略详情
2. 恢复流程步骤
3. 监控方案
4. 验证方法

Result（结果）:
请输出：
1. 完整备份方案
2. 恢复流程文档
3. 监控配置建议
4. 演练计划
5. 应急预案"""
                },
                "variables": ["db_environment", "data_volume", "business_requirements"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库容量规划",
                "description": "进行数据库容量评估和规划",
                "content": {
                    "prompt": """作为数据库运维工程师，请进行数据库容量规划分析：

Context（上下文）:
- 数据库类型：{db_type}
- 当前容量状况：{current_capacity}
- 增长预测：{growth_forecast}

Objective（目标）:
1. 评估当前容量使用
2. 预测未来需求
3. 制定扩容方案
4. 优化资源利用

Scope（范围）:
- 存储容量
- 性能容量
- 备份空间
- 网络带宽
- 硬件资源

Task（任务）:
1. 容量使用分析
2. 增长趋势预测
3. 瓶颈识别
4. 扩容方案设计
5. 优化建议

Action（行动）:
请提供：
1. 容量评估报告
2. 增长预测分析
3. 扩容建议
4. 优化措施

Result（结果）:
请输出：
1. 容量规划方案
2. 具体实施步骤
3. 成本估算
4. 风险评估
5. 长期规划建议"""
                },
                "variables": ["db_type", "current_capacity", "growth_forecast"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库高可用架构设计",
                "description": "设计数据库高可用解决方案",
                "content": {
                    "prompt": """作为数据库运维工程师，请设计数据库高可用方案：

Context（上下文）:
- 数据库类型：{db_type}
- 业务需求：{business_needs}
- 当前架构：{current_architecture}

Objective（目标）:
1. 提升系统可用性
2. 实现故障自动切换
3. 确保数据一致性
4. 优化运维效率

Scope（范围）:
- 架构设计
- 复制方案
- 监控告警
- 切换机制
- 数据同步

Task（任务）:
1. 需求分析
2. 方案设计
3. 实施规划
4. 运维流程设计
5. 应急预案制定

Action（行动）:
请提供：
1. 架构设计方案
2. 部署配置说明
3. 监控方案
4. 维护流程

Result（结果）:
请输出：
1. 完整技术方案
2. 实施步骤
3. 运维手册
4. 故障处理流程
5. 演练计划"""
                },
                "variables": ["db_type", "business_needs", "current_architecture"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库迁移方案",
                "description": "设计数据库迁移方案",
                "content": {
                    "prompt": """作为数据库运维工程师，请设计数据库迁移方案：

Context（上下文）:
- 源数据库：{source_db}
- 目标数据库：{target_db}
- 数据量：{data_volume}

Objective（目标）:
1. 确保数据完整性
2. 最小化停机时间
3. 保证迁移可靠性
4. 支持回滚操作

Scope（范围）:
- 数据迁移
- 架构迁移
- 应用切换
- 性能优化
- 监控验证

Task（任务）:
1. 迁移前评估
2. 方案设计
3. 测试验证
4. 执行计划
5. 切换规划

Action（行动）:
请提供：
1. 迁移步骤详情
2. 验证方法
3. 回滚方案
4. 监控方案

Result（结果）:
请输出：
1. 完整迁移方案
2. 风险评估
3. 时间计划
4. 验收标准
5. 应急预案"""
                },
                "variables": ["source_db", "target_db", "data_volume"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库安全审计",
                "description": "进行数据库安全审计和加固",
                "content": {
                    "prompt": """作为数据库运维工程师，请进行数据库安全审计：

Context（上下文）:
- 数据库环境：{db_environment}
- 安全要求：{security_requirements}
- 当前状况：{current_status}

Objective（目标）:
1. 识别安全风险
2. 评估合规性
3. 提供加固建议
4. 建立安全基线

Scope（范围）:
- 访问控制
- 权限管理
- 数据加密
- 审计日志
- 漏洞管理

Task（任务）:
1. 安全扫描
2. 配置审计
3. 权限审查
4. 日志分析
5. 漏洞评估

Action（行动）:
请提供：
1. 审计检查项
2. 风险评估
3. 加固建议
4. 整改方案

Result（结果）:
请输出：
1. 安全审计报告
2. 风险清单
3. 整改建议
4. 长期维护计划
5. 安全基线"""
                },
                "variables": ["db_environment", "security_requirements", "current_status"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库监控方案",
                "description": "设计数据库监控和告警方案",
                "content": {
                    "prompt": """作为数据库运维工程师，请设计数据库监控方案：

Context（上下文）:
- 数据库类型：{db_type}
- 监控需求：{monitoring_requirements}
- 现有工具：{existing_tools}

Objective（目标）:
1. 全面监控覆盖
2. 准确告警触发
3. 快速问题定位
4. 优化告警质量

Scope（范围）:
- 性能监控
- 容量监控
- 可用性监控
- 安全监控
- 业务监控

Task（任务）:
1. 监控指标设计
2. 告警规则制定
3. 监控部署规划
4. 告警流程设计
5. dashboard设计

Action（行动）:
请提供：
1. 监控指标清单
2. 告警规则配置
3. 部署架构
4. 响应流程

Result（结果）:
请输出：
1. 监控方案设计
2. 告警规则文档
3. 部署手册
4. 运维指南
5. 优化建议"""
                },
                "variables": ["db_type", "monitoring_requirements", "existing_tools"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库灾备方案",
                "description": "设计数据库灾难恢复方案",
                "content": {
                    "prompt": """作为数据库运维工程师，请设计数据库灾备方案：

Context（上下文）:
- 数据库环境：{db_environment}
- RPO要求：{rpo_requirement}
- RTO要求：{rto_requirement}

Objective（目标）:
1. 满足RPO/RTO要求
2. 确保数据安全
3. 快速恢复能力
4. 定期演练验证

Scope（范围）:
- 灾备架构
- 数据同步
- 切换机制
- 演练验证
- 应急响应

Task（任务）:
1. 需求分析
2. 方案设计
3. 实施规划
4. 演练计划
5. 文档编制

Action（行动）:
请提供：
1. 灾备架构设计
2. 同步方案
3. 切换流程
4. 演练方案

Result（结果）:
请输出：
1. 灾备技术方案
2. 实施计划
3. 演练文档
4. 应急手册
5. 维护指南"""
                },
                "variables": ["db_environment", "rpo_requirement", "rto_requirement"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库升级方案",
                "description": "设计数据库版本升级方案",
                "content": {
                    "prompt": """作为数据库运维工程师，请设计数据库升级方案：

Context（上下文）:
- 当前版本：{current_version}
- 目标版本：{target_version}
- 业务影响：{business_impact}

Objective（目标）:
1. 安全完成升级
2. 最小化停机时间
3. 确保业务连续性
4. 支持回滚操作

Scope（范围）:
- 兼容性评估
- 升级步骤
- 数据迁移
- 性能优化
- 应用适配

Task（任务）:
1. 升级评估
2. 方案设计
3. 测试验证
4. 实施规划
5. 回滚准备

Action（行动）:
请提供：
1. 升级步骤
2. 验证方案
3. 回滚方案
4. 应急预案

Result（结果）:
请输出：
1. 升级技术方案
2. 实施计划
3. 验收标准
4. 风险应对
5. 运维建议"""
                },
                "variables": ["current_version", "target_version", "business_impact"],
                "target_role": "数据库运维工程师"
            },
            {
                "name": "数据库运维自动化",
                "description": "设计数据库运维自动化方案",
                "content": {
                    "prompt": """作为数据库运维工程师，请设计数据库运维自动化方案：

Context（上下文）:
- 运维场景：{ops_scenario}
- 自动化需求：{automation_needs}
- 现有工具：{existing_tools}

Objective（目标）:
1. 提升运维效率
2. 降低人为错误
3. 标准化操作
4. 优化运维成本

Scope（范围）:
- 日常运维
- 变更管理
- 备份恢复
- 监控告警
- 报表生成

Task（任务）:
1. 需求分析
2. 工具评估
3. 方案设计
4. 流程优化
5. 实施规划

Action（行动）:
请提供：
1. 自动化方案
2. 工具选型
3. 实施步骤
4. 验证方法

Result（结果）:
请输出：
1. 技术方案设计
2. 实施路线图
3. 效果评估
4. 维护手册
5. 培训计划"""
                },
                "variables": ["ops_scenario", "automation_needs", "existing_tools"],
                "target_role": "数据库运维工程师"
            }
        ]

        created_count = 0
        for template_data in templates:
            # 检查模板是否已存在
            existing = Template.objects.filter(
                name=template_data["name"],
                target_role=template_data["target_role"]
            ).exists()
            
            if not existing:
                Template.objects.create(
                    name=template_data["name"],
                    framework=framework,
                    framework_type=framework.name,
                    description=template_data["description"],
                    content=template_data["content"],
                    variables=template_data["variables"],
                    target_role=template_data["target_role"],
                    created_by=user,
                    visibility='PUBLIC'  # 设置为公开可见
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'创建模板: {template_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'模板已存在，跳过: {template_data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'成功创建 {created_count} 个数据库运维工程师模板'))