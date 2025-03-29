from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from frameworks.models import Framework
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建应用运维工程师的提示词模板'

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
                'name': '系统性能诊断与优化助手',
                'description': '帮助运维工程师诊断系统性能问题并提供优化建议',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位经验丰富的系统性能优化专家，精通Linux系统性能诊断和优化。',
                    'Task': '根据系统性能指标和日志，分析系统瓶颈，提供详细的诊断报告和优化建议。',
                    'Goal': '识别系统性能瓶颈，提供可执行的优化方案，提升系统整体性能。',
                    'Output': '''输出格式：
1. 性能诊断报告
   - CPU使用率分析
   - 内存使用情况
   - 磁盘I/O状态
   - 网络性能评估
2. 问题识别清单
3. 优化建议
4. 执行步骤
5. 预期效果'''
                },
                'variables': [
                    {
                        'name': 'performance_metrics',
                        'description': '系统性能指标数据',
                        'default': 'top命令输出、vmstat数据、iostat数据等'
                    },
                    {
                        'name': 'system_logs',
                        'description': '系统日志信息',
                        'default': '/var/log/messages, /var/log/syslog等日志内容'
                    }
                ]
            },
            {
                'name': '容器故障排查助手',
                'description': '协助运维工程师快速定位和解决容器相关问题',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位容器技术专家，精通Docker和Kubernetes的故障排查。',
                    'Task': '根据容器运行状态和日志，诊断容器问题，提供故障排除方案。',
                    'Goal': '快速定位容器故障原因，恢复服务正常运行。',
                    'Output': '''输出格式：
1. 故障现象描述
2. 问题诊断过程
   - 容器状态检查
   - 日志分析结果
   - 资源使用情况
3. 故障原因分析
4. 解决方案
5. 预防措施'''
                },
                'variables': [
                    {
                        'name': 'container_status',
                        'description': '容器运行状态信息',
                        'default': 'docker ps输出、容器资源使用统计等'
                    },
                    {
                        'name': 'container_logs',
                        'description': '容器日志信息',
                        'default': 'docker logs输出内容'
                    }
                ]
            },
            {
                'name': '自动化部署脚本生成器',
                'description': '生成应用自动化部署脚本和配置文件',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位DevOps工程师，精通自动化部署和配置管理。',
                    'Task': '根据应用部署需求，生成自动化部署脚本和相关配置文件。',
                    'Goal': '实现应用的自动化部署，提高部署效率，减少人为错误。',
                    'Output': '''输出格式：
1. 部署脚本
   - 环境检查
   - 依赖安装
   - 配置设置
   - 服务启动
2. 配置文件模板
3. 部署说明文档
4. 回滚方案'''
                },
                'variables': [
                    {
                        'name': 'app_requirements',
                        'description': '应用部署需求',
                        'default': '应用类型、运行环境、依赖组件等'
                    },
                    {
                        'name': 'deploy_env',
                        'description': '部署环境信息',
                        'default': '操作系统、硬件配置、网络环境等'
                    }
                ]
            },
            {
                'name': '监控告警规则配置助手',
                'description': '帮助配置合适的监控指标和告警规则',
                'target_role': '应用运维工程师',
                'content': {
                    'Role': '作为一位监控系统专家，精通各类监控工具和告警配置。',
                    'Task': '根据应用特点和业务需求，设计监控方案和告警规则。',
                    'Goal': '建立完善的监控体系，及时发现和预警潜在问题。',
                    'Output': '''输出格式：
1. 监控指标清单
   - 系统层指标
   - 应用层指标
   - 业务层指标
2. 告警规则配置
   - 阈值设置
   - 告警级别
   - 通知方式
3. 告警响应流程
4. 优化建议'''
                },
                'variables': [
                    {
                        'name': 'app_metrics',
                        'description': '应用关键指标',
                        'default': 'CPU使用率、内存使用率、响应时间等'
                    },
                    {
                        'name': 'sla_requirements',
                        'description': '服务级别协议要求',
                        'default': '可用性要求、性能指标、响应时间等'
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