from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建运维相关的提示词模板数据'

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

        # 运维模板数据
        templates_data = [
            {
                'name': 'Shell脚本分析优化助手',
                'framework_type': 'RTGO',
                'description': '帮助分析和优化Shell脚本，提供最佳实践建议',
                'content': {
                    'role': '高级Linux系统工程师',
                    'task': '''分析提供的Shell脚本，从以下几个方面提供优化建议：
1. 代码规范性和可读性
2. 性能优化点
3. 安全性考虑
4. 错误处理完善
5. 可维护性提升''',
                    'goal': '提供一个更安全、高效、易维护的脚本版本',
                    'output': '''输出包含：
1. 脚本分析总结
2. 具体优化建议
3. 优化后的脚本代码
4. 改进说明和最佳实践建议'''
                },
                'variables': [
                    {
                        'name': 'script_content',
                        'default_value': '#!/bin/bash\n# 在此粘贴您的脚本内容',
                        'description': '需要分析的脚本内容'
                    },
                    {
                        'name': 'focus_areas',
                        'default_value': '性能,安全性,可维护性',
                        'description': '重点关注的优化方向'
                    }
                ]
            },
            {
                'name': '日志分析故障排查专家',
                'framework_type': 'SPAR',
                'description': '协助分析系统日志，快速定位和解决问题',
                'content': {
                    'situation': '系统出现异常，需要通过日志快速定位问题',
                    'purpose': '通过日志分析找出问题根因并提供解决方案',
                    'action': '''1. 分析日志内容和模式
2. 识别关键错误信息和异常模式
3. 确定问题的根本原因
4. 提供解决方案和预防措施''',
                    'result': '''提供完整的分析报告，包括：
1. 问题概述
2. 根因分析
3. 解决方案
4. 预防措施建议'''
                },
                'variables': [
                    {
                        'name': 'log_content',
                        'default_value': '在此粘贴日志内容',
                        'description': '需要分析的日志内容'
                    },
                    {
                        'name': 'system_info',
                        'default_value': '操作系统类型和版本',
                        'description': '系统环境信息'
                    },
                    {
                        'name': 'error_keywords',
                        'default_value': 'error,failed,exception',
                        'description': '需要特别关注的错误关键词'
                    }
                ]
            },
            {
                'name': '系统性能分析与调优',
                'framework_type': 'RTGO',
                'description': '帮助分析系统性能数据并提供调优建议',
                'content': {
                    'role': '系统性能优化专家',
                    'task': '''分析系统性能数据，识别瓶颈并提供优化建议：
1. 分析CPU、内存、磁盘IO和网络性能
2. 识别性能瓶颈
3. 提供具体的优化建议
4. 建议监控指标和阈值''',
                    'goal': '提供可执行的性能优化方案，提升系统整体性能',
                    'output': '''输出完整的性能分析报告：
1. 性能数据分析结果
2. 瓶颈点识别
3. 优化建议清单
4. 实施步骤
5. 效果评估方法'''
                },
                'variables': [
                    {
                        'name': 'performance_data',
                        'default_value': '在此粘贴性能监控数据',
                        'description': '系统性能数据'
                    },
                    {
                        'name': 'system_spec',
                        'default_value': 'CPU核数,内存大小,磁盘配置',
                        'description': '系统规格信息'
                    },
                    {
                        'name': 'optimization_focus',
                        'default_value': 'CPU使用率,内存使用,IO延迟',
                        'description': '重点优化方向'
                    }
                ]
            },
            {
                'name': '系统配置审查与安全加固',
                'framework_type': 'SPAR',
                'description': '审查系统配置并提供安全加固建议',
                'content': {
                    'situation': '需要对系统进行安全性审查和加固',
                    'purpose': '找出潜在的安全隐患并提供加固建议',
                    'action': '''1. 审查系统配置文件
2. 检查安全策略设置
3. 识别潜在风险
4. 提供加固建议''',
                    'result': '''提供详细的安全审查报告：
1. 配置审查结果
2. 安全风险列表
3. 加固建议
4. 实施步骤
5. 最佳实践建议'''
                },
                'variables': [
                    {
                        'name': 'config_content',
                        'default_value': '在此粘贴配置文件内容',
                        'description': '需要审查的配置内容'
                    },
                    {
                        'name': 'security_level',
                        'default_value': '高/中/低',
                        'description': '期望的安全等级'
                    },
                    {
                        'name': 'compliance_standards',
                        'default_value': 'CIS,NIST,等',
                        'description': '需要遵循的安全标准'
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
                f'成功创建{created_count}个运维相关的提示词模板！'
            )
        )