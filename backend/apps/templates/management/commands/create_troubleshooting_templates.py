from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建故障排除和根因分析相关的提示词模板数据'

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

        # 故障排除和根因分析模板数据
        templates_data = [
            {
                'name': '系统崩溃根因分析',
                'framework_type': 'RTGO',
                'description': '分析系统崩溃日志，找出根本原因',
                'content': {
                    'role': '系统故障分析专家',
                    'task': '''分析系统崩溃日志和错误信息，确定根本原因：
1. 检查关键错误信息和堆栈跟踪
2. 分析系统状态和资源使用情况
3. 识别触发事件和条件
4. 确定故障的根本原因
5. 提供修复和预防措施''',
                    'goal': '准确找出系统崩溃的根本原因，并提供解决方案',
                    'output': '''输出详细的根因分析报告：
1. 事件摘要和影响
2. 时间线分析
3. 技术分析和发现
4. 根本原因确定
5. 短期修复建议
6. 长期预防措施
7. 监控和警报建议'''
                },
                'variables': [
                    {
                        'name': 'crash_logs',
                        'default_value': '系统崩溃日志内容',
                        'description': '崩溃日志'
                    },
                    {
                        'name': 'system_info',
                        'default_value': '操作系统、软件版本等信息',
                        'description': '系统信息'
                    },
                    {
                        'name': 'recent_changes',
                        'default_value': '最近的系统变更',
                        'description': '近期变更'
                    }
                ]
            },
            {
                'name': '网络连接问题排查',
                'framework_type': 'SPAR',
                'description': '系统性排查网络连接问题',
                'content': {
                    'situation': '系统出现网络连接问题，需要诊断和解决',
                    'purpose': '确定网络连接问题的根本原因并恢复服务',
                    'action': '''1. 检查网络连接状态和配置
2. 分析网络流量和数据包
3. 测试网络组件和路径
4. 识别故障点和瓶颈
5. 实施修复措施''',
                    'result': '''提供完整的网络故障排除报告：
1. 问题描述和影响范围
2. 诊断步骤和发现
3. 根本原因分析
4. 解决方案和实施步骤
5. 验证方法
6. 预防措施建议'''
                },
                'variables': [
                    {
                        'name': 'connection_errors',
                        'default_value': '连接错误信息',
                        'description': '错误信息'
                    },
                    {
                        'name': 'network_topology',
                        'default_value': '网络拓扑描述',
                        'description': '网络拓扑'
                    },
                    {
                        'name': 'diagnostic_results',
                        'default_value': 'ping、traceroute等诊断结果',
                        'description': '诊断结果'
                    }
                ]
            },
            {
                'name': '数据库性能问题诊断',
                'framework_type': 'RTGO',
                'description': '诊断和解决数据库性能下降问题',
                'content': {
                    'role': '数据库性能专家',
                    'task': '''分析数据库性能问题并找出根本原因：
1. 分析数据库性能指标和日志
2. 检查慢查询和执行计划
3. 评估索引使用情况
4. 分析资源使用和瓶颈
5. 确定性能下降的根本原因''',
                    'goal': '找出数据库性能问题的根本原因，并提供优化方案',
                    'output': '''输出详细的数据库性能分析报告：
1. 性能问题描述
2. 关键指标分析
3. 问题SQL和执行计划
4. 根本原因确定
5. 短期优化建议
6. 长期改进计划
7. 监控和预警策略'''
                },
                'variables': [
                    {
                        'name': 'db_logs',
                        'default_value': '数据库日志内容',
                        'description': '数据库日志'
                    },
                    {
                        'name': 'slow_queries',
                        'default_value': '慢查询日志',
                        'description': '慢查询'
                    },
                    {
                        'name': 'performance_metrics',
                        'default_value': 'CPU、内存、IO等性能指标',
                        'description': '性能指标'
                    }
                ]
            },
            {
                'name': '应用程序崩溃分析',
                'framework_type': 'SPAR',
                'description': '分析应用程序崩溃原因并提供解决方案',
                'content': {
                    'situation': '应用程序频繁崩溃或出现异常',
                    'purpose': '找出崩溃原因并提供稳定性解决方案',
                    'action': '''1. 分析崩溃日志和异常堆栈
2. 检查内存使用和资源分配
3. 评估代码质量和错误处理
4. 识别触发条件和复现步骤
5. 确定根本原因''',
                    'result': '''提供详细的应用崩溃分析报告：
1. 崩溃模式和频率
2. 技术分析和发现
3. 根本原因确定
4. 代码修复建议
5. 测试和验证方法
6. 预防类似问题的最佳实践'''
                },
                'variables': [
                    {
                        'name': 'crash_reports',
                        'default_value': '应用崩溃报告内容',
                        'description': '崩溃报告'
                    },
                    {
                        'name': 'app_info',
                        'default_value': '应用版本和环境信息',
                        'description': '应用信息'
                    },
                    {
                        'name': 'user_steps',
                        'default_value': '用户操作步骤',
                        'description': '操作步骤'
                    }
                ]
            },
            {
                'name': '安全漏洞事件分析',
                'framework_type': 'RTGO',
                'description': '分析安全事件，确定漏洞和入侵路径',
                'content': {
                    'role': '安全事件响应专家',
                    'task': '''分析安全事件日志，确定漏洞和入侵路径：
1. 检查安全日志和告警
2. 分析可疑活动和访问模式
3. 识别漏洞和利用方法
4. 确定攻击路径和影响范围
5. 评估数据泄露和损害程度''',
                    'goal': '准确找出安全漏洞和入侵路径，提供修复和加固方案',
                    'output': '''输出完整的安全事件分析报告：
1. 事件摘要和时间线
2. 技术分析和发现
3. 漏洞和入侵路径确定
4. 影响评估
5. 修复和加固建议
6. 防止再次发生的措施
7. 监控和检测改进建议'''
                },
                'variables': [
                    {
                        'name': 'security_logs',
                        'default_value': '安全日志和告警信息',
                        'description': '安全日志'
                    },
                    {
                        'name': 'system_config',
                        'default_value': '系统配置和安全设置',
                        'description': '系统配置'
                    },
                    {
                        'name': 'suspicious_activities',
                        'default_value': '可疑活动描述',
                        'description': '可疑活动'
                    }
                ]
            },
            {
                'name': '微服务故障链路追踪',
                'framework_type': 'SPAR',
                'description': '在微服务架构中追踪故障传播路径',
                'content': {
                    'situation': '微服务系统出现故障，需要追踪故障传播路径',
                    'purpose': '找出故障的源头和传播路径，恢复服务稳定性',
                    'action': '''1. 分析分布式追踪日志
2. 检查服务依赖和调用关系
3. 识别故障点和异常服务
4. 评估故障影响范围
5. 确定根本原因和传播机制''',
                    'result': '''提供详细的故障链路分析报告：
1. 故障概述和影响
2. 服务调用图和故障路径
3. 关键时间点和事件
4. 根本原因分析
5. 修复建议和优先级
6. 服务韧性改进建议
7. 监控和告警优化'''
                },
                'variables': [
                    {
                        'name': 'trace_logs',
                        'default_value': '分布式追踪日志',
                        'description': '追踪日志'
                    },
                    {
                        'name': 'service_map',
                        'default_value': '服务依赖关系图',
                        'description': '服务依赖'
                    },
                    {
                        'name': 'error_messages',
                        'default_value': '错误信息和异常堆栈',
                        'description': '错误信息'
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
                f'成功创建{created_count}个故障排除和根因分析相关的提示词模板！'
            )
        )