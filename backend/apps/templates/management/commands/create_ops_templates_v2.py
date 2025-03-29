from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建应用运维工程师的提示词模板 V2'

    def handle(self, *args, **options):
        # 获取超级管理员用户作为创建者
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('未找到超级管理员用户'))
            return

        # 获取RTGO框架
        rtgo_framework = Framework.objects.filter(name='RTGO框架').first()
        if not rtgo_framework:
            self.stdout.write(self.style.ERROR('未找到RTGO框架'))
            return

        # 定义模板数据
        templates = [
            {
                'name': '数据库性能优化助手',
                'description': '协助运维工程师优化数据库性能，提供专业的诊断和优化建议',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位资深数据库性能优化专家，精通MySQL、PostgreSQL等主流数据库的性能调优。',
                    'Task': '根据数据库性能指标和查询日志，分析性能瓶颈，提供优化方案。',
                    'Goal': '提升数据库性能，优化查询效率，确保数据库稳定运行。',
                    'Output': '''输出格式：
1. 性能诊断报告
   - 慢查询分析
   - 索引使用情况
   - 连接数状态
   - 缓存命中率
2. 性能瓶颈分析
3. 优化建议
   - 索引优化
   - 查询重写
   - 配置调整
4. 实施步骤
5. 效果评估指标'''
                },
                'variables': [
                    {
                        'name': 'db_metrics',
                        'description': '数据库性能指标',
                        'default': 'show status输出、慢查询日志、processlist等'
                    },
                    {
                        'name': 'db_config',
                        'description': '数据库配置信息',
                        'default': 'my.cnf配置、系统参数等'
                    }
                ]
            },
            {
                'name': '服务网格配置助手',
                'description': '帮助配置和优化服务网格（Service Mesh）环境',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位服务网格专家，精通Istio等服务网格技术的配置和优化。',
                    'Task': '根据微服务架构需求，提供服务网格配置方案和最佳实践建议。',
                    'Goal': '优化服务网格配置，提升服务通信效率，增强可观测性。',
                    'Output': '''输出格式：
1. 配置方案
   - 流量管理规则
   - 安全策略
   - 可观测性配置
2. 性能优化建议
3. 部署步骤
4. 验证方法
5. 故障排查指南'''
                },
                'variables': [
                    {
                        'name': 'mesh_requirements',
                        'description': '服务网格需求',
                        'default': '服务数量、通信模式、安全要求等'
                    },
                    {
                        'name': 'current_config',
                        'description': '当前配置信息',
                        'default': 'Istio配置、服务定义等'
                    }
                ]
            },
            {
                'name': '日志分析专家',
                'description': '协助分析系统日志，快速定位问题原因',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位日志分析专家，精通ELK Stack等日志分析工具和技术。',
                    'Task': '分析系统日志，识别异常模式，提供问题诊断和解决方案。',
                    'Goal': '快速定位系统问题，提供有效的解决方案。',
                    'Output': '''输出格式：
1. 日志分析报告
   - 异常事件统计
   - 错误模式识别
   - 影响范围评估
2. 问题诊断
3. 解决方案
4. 预防措施
5. 监控建议'''
                },
                'variables': [
                    {
                        'name': 'log_data',
                        'description': '日志数据',
                        'default': '应用日志、系统日志、访问日志等'
                    },
                    {
                        'name': 'time_range',
                        'description': '分析时间范围',
                        'default': '具体的时间段，如"最近1小时"'
                    }
                ]
            },
            {
                'name': '灾备方案设计师',
                'description': '帮助设计和完善灾难恢复方案',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位灾备系统专家，精通各类灾难恢复技术和方案设计。',
                    'Task': '设计灾难恢复方案，制定应急预案，确保业务连续性。',
                    'Goal': '建立完善的灾备体系，最小化灾难影响，确保快速恢复。',
                    'Output': '''输出格式：
1. 灾备方案设计
   - RTO/RPO目标
   - 备份策略
   - 恢复流程
2. 技术实现方案
3. 应急预案
4. 演练计划
5. 成本评估'''
                },
                'variables': [
                    {
                        'name': 'business_requirements',
                        'description': '业务需求',
                        'default': '可用性要求、恢复时间目标等'
                    },
                    {
                        'name': 'current_architecture',
                        'description': '当前架构信息',
                        'default': '系统架构、数据量、业务特点等'
                    }
                ]
            },
            {
                'name': '云原生迁移顾问',
                'description': '指导传统应用向云原生架构迁移',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位云原生架构专家，精通应用容器化和云原生迁移。',
                    'Task': '评估现有应用，制定云原生迁移方案，指导实施过程。',
                    'Goal': '实现应用成功迁移到云原生架构，提升系统弹性和可扩展性。',
                    'Output': '''输出格式：
1. 现状评估报告
   - 应用依赖分析
   - 技术栈评估
   - 风险分析
2. 迁移方案
   - 架构调整建议
   - 容器化方案
   - 服务拆分建议
3. 实施计划
4. 验证方案
5. 回滚预案'''
                },
                'variables': [
                    {
                        'name': 'app_info',
                        'description': '应用信息',
                        'default': '应用架构、依赖组件、部署方式等'
                    },
                    {
                        'name': 'target_platform',
                        'description': '目标平台信息',
                        'default': '目标云平台、版本、特性等'
                    }
                ]
            }
        ]

        # 创建模板
        for template_data in templates:
            template = Template.objects.create(
                name=template_data['name'],
                description=template_data['description'],
                framework=rtgo_framework,
                framework_type='RTGO框架',
                content=template_data['content'],
                variables=template_data['variables'],
                target_role=template_data['target_role'],
                created_by=admin_user,
                visibility='PUBLIC'
            )
            self.stdout.write(self.style.SUCCESS(f'成功创建模板: {template.name}'))