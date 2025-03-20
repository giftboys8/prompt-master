from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建基础设施运维相关的提示词模板数据'

    def handle(self, *args, **kwargs):
        # 确保有管理员用户
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write('创建超级用户...')
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'
            )

        # 基础设施运维模板数据
        templates_data = [
            {
                'name': 'Kubernetes故障诊断专家',
                'framework_type': 'RTGO',
                'description': '帮助诊断和解决Kubernetes集群问题',
                'content': {
                    'role': 'Kubernetes专家工程师',
                    'task': '''分析Kubernetes集群问题并提供解决方案：
1. 分析集群状态和日志
2. 诊断Pod、Node、Service等资源问题
3. 提供修复步骤
4. 优化配置建议''',
                    'goal': '快速定位并解决Kubernetes集群问题，确保服务稳定运行',
                    'output': '''提供完整的问题解决报告：
1. 问题诊断结果
2. 根因分析
3. 修复步骤
4. 预防措施
5. 配置优化建议'''
                },
                'variables': [
                    {
                        'name': 'cluster_info',
                        'default_value': '集群版本、节点数等信息',
                        'description': '集群基本信息'
                    },
                    {
                        'name': 'error_logs',
                        'default_value': '相关错误日志',
                        'description': '错误日志内容'
                    },
                    {
                        'name': 'resource_status',
                        'default_value': 'kubectl get pods/nodes/services输出',
                        'description': '资源状态信息'
                    }
                ]
            },
            {
                'name': '网络配置与故障排查',
                'framework_type': 'SPAR',
                'description': '协助解决网络配置和连接问题',
                'content': {
                    'situation': '网络出现异常或需要优化网络配置',
                    'purpose': '诊断和解决网络问题，优化网络配置',
                    'action': '''1. 分析网络拓扑和配置
2. 检查连接性和性能问题
3. 识别网络瓶颈
4. 提供优化方案''',
                    'result': '''输出详细的网络分析报告：
1. 网络状态评估
2. 问题定位
3. 优化建议
4. 配置修改指南
5. 验证步骤'''
                },
                'variables': [
                    {
                        'name': 'network_info',
                        'default_value': '网络拓扑描述',
                        'description': '网络环境信息'
                    },
                    {
                        'name': 'config_files',
                        'default_value': '相关配置文件内容',
                        'description': '网络配置信息'
                    },
                    {
                        'name': 'diagnostic_output',
                        'default_value': 'ping/traceroute/tcpdump等输出',
                        'description': '诊断命令输出'
                    }
                ]
            },
            {
                'name': '数据库性能优化顾问',
                'framework_type': 'RTGO',
                'description': '数据库性能分析与优化建议',
                'content': {
                    'role': '资深数据库管理员',
                    'task': '''分析数据库性能并提供优化建议：
1. 分析慢查询日志
2. 评估索引使用情况
3. 检查配置参数
4. 提供性能优化方案''',
                    'goal': '提升数据库性能和稳定性',
                    'output': '''提供完整的优化报告：
1. 性能瓶颈分析
2. 索引优化建议
3. 配置调优参数
4. SQL优化建议
5. 实施步骤'''
                },
                'variables': [
                    {
                        'name': 'db_type',
                        'default_value': 'MySQL/PostgreSQL/MongoDB等',
                        'description': '数据库类型'
                    },
                    {
                        'name': 'slow_queries',
                        'default_value': '慢查询日志内容',
                        'description': '慢查询日志'
                    },
                    {
                        'name': 'current_config',
                        'default_value': '当前主要配置参数',
                        'description': '当前配置'
                    }
                ]
            },
            {
                'name': '负载均衡配置专家',
                'framework_type': 'SPAR',
                'description': '配置和优化负载均衡策略',
                'content': {
                    'situation': '需要设置或优化负载均衡配置',
                    'purpose': '实现最优的负载分配和高可用性',
                    'action': '''1. 分析当前流量模式
2. 评估负载均衡策略
3. 配置健康检查
4. 优化分发算法''',
                    'result': '''提供完整的配置方案：
1. 负载均衡策略
2. 具体配置步骤
3. 健康检查设置
4. 监控建议
5. 故障切换方案'''
                },
                'variables': [
                    {
                        'name': 'lb_type',
                        'default_value': 'Nginx/HAProxy/云负载均衡',
                        'description': '负载均衡器类型'
                    },
                    {
                        'name': 'traffic_pattern',
                        'default_value': '流量特征描述',
                        'description': '流量模式'
                    },
                    {
                        'name': 'backend_services',
                        'default_value': '后端服务列表',
                        'description': '后端服务信息'
                    }
                ]
            },
            {
                'name': 'Docker容器优化专家',
                'framework_type': 'RTGO',
                'description': '优化Docker容器配置和性能',
                'content': {
                    'role': 'Docker容器专家',
                    'task': '''分析和优化Docker容器配置：
1. 审查Dockerfile
2. 检查容器资源使用
3. 优化镜像大小
4. 提升运行效率''',
                    'goal': '提供最优的容器配置和运行环境',
                    'output': '''输出优化报告：
1. Dockerfile优化建议
2. 资源配置建议
3. 安全加固措施
4. 性能优化方案
5. 最佳实践推荐'''
                },
                'variables': [
                    {
                        'name': 'dockerfile_content',
                        'default_value': 'Dockerfile内容',
                        'description': 'Dockerfile'
                    },
                    {
                        'name': 'container_stats',
                        'default_value': '容器资源使用统计',
                        'description': '容器状态信息'
                    },
                    {
                        'name': 'requirements',
                        'default_value': '性能和安全需求',
                        'description': '优化需求'
                    }
                ]
            }
        ]

        # 创建模板
        created_count = 0
        for template_data in templates_data:
            template, created = Template.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    **template_data,
                    'created_by': admin_user
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'成功创建{created_count}个基础设施运维相关的提示词模板！'
            )
        )