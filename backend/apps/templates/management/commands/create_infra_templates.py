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
                'name': '存储系统容量规划与扩展',
                'framework_type': 'RTGO',
                'description': '规划和扩展存储系统容量，确保数据存储需求',
                'content': {
                    'role': '存储架构专家',
                    'task': '''规划存储系统容量：
1. 分析当前存储使用情况
2. 预测未来存储需求
3. 评估存储性能指标
4. 设计扩容方案
5. 规划数据迁移策略
6. 制定备份与恢复计划
7. 优化存储资源分配''',
                    'goal': '确保存储系统容量满足业务需求，同时优化性能和成本',
                    'output': '''提供存储规划方案：
1. 存储使用分析报告
2. 容量预测模型
3. 扩容方案设计
4. 迁移实施计划
5. 性能优化建议
6. 成本效益分析'''
                },
                'variables': [
                    {
                        'name': 'storage_metrics',
                        'default_value': '存储指标数据',
                        'description': '当前存储系统的使用指标'
                    },
                    {
                        'name': 'business_growth',
                        'default_value': '业务增长预测',
                        'description': '业务增长和数据增长的预测'
                    }
                ],
                'target_role': '存储管理员,基础架构工程师,容量规划专家'
            },
            {
                'name': '数据库高可用架构设计',
                'framework_type': 'SPAR',
                'description': '设计数据库高可用解决方案，确保业务连续性',
                'content': {
                    'situation': '需要提高数据库系统可用性',
                    'purpose': '确保数据库服务的高可用性和业务连续性',
                    'action': '''1. 分析当前数据库架构
2. 评估业务需求和SLA
3. 设计复制与同步方案
4. 规划故障转移机制
5. 配置负载均衡策略
6. 实现自动化恢复
7. 设计监控与告警
8. 制定运维流程''',
                    'result': '''提供数据库高可用方案：
1. 架构设计文档
2. 复制配置指南
3. 故障转移流程
4. 监控与告警设置
5. 性能影响评估
6. 运维手册'''
                },
                'variables': [
                    {
                        'name': 'db_info',
                        'default_value': '数据库信息',
                        'description': '数据库类型、版本和当前架构'
                    },
                    {
                        'name': 'availability_requirements',
                        'default_value': '可用性要求',
                        'description': '业务对数据库可用性的要求和SLA'
                    }
                ],
                'target_role': '数据库管理员,高可用架构师,数据库可靠性工程师'
            },
            {
                'name': '中间件性能调优与故障排查',
                'framework_type': 'RTGO',
                'description': '优化中间件性能并排查解决故障问题',
                'content': {
                    'role': '中间件专家',
                    'task': '''调优中间件性能并排查故障：
1. 收集性能指标和日志
2. 分析性能瓶颈
3. 调整配置参数
4. 优化资源分配
5. 排查故障原因
6. 制定解决方案
7. 验证优化效果''',
                    'goal': '提高中间件性能和稳定性，快速解决故障问题',
                    'output': '''提供中间件优化与故障解决方案：
1. 性能分析报告
2. 配置优化建议
3. 故障根因分析
4. 解决步骤详解
5. 最佳实践推荐
6. 监控指标设置'''
                },
                'variables': [
                    {
                        'name': 'middleware_type',
                        'default_value': '中间件类型',
                        'description': '中间件的类型和版本信息'
                    },
                    {
                        'name': 'performance_issues',
                        'default_value': '性能问题描述',
                        'description': '当前遇到的性能问题或故障现象'
                    }
                ],
                'target_role': '中间件工程师,应用支持工程师,性能优化专家'
            },
            {
                'name': '计算资源弹性伸缩策略',
                'framework_type': 'SPAR',
                'description': '设计计算资源的弹性伸缩策略，优化资源利用',
                'content': {
                    'situation': '需要优化计算资源的使用效率',
                    'purpose': '实现计算资源的弹性伸缩，提高资源利用率',
                    'action': '''1. 分析工作负载模式
2. 识别峰谷规律
3. 设计伸缩触发条件
4. 制定伸缩策略
5. 配置自动化机制
6. 优化资源分配
7. 设置监控与告警
8. 评估成本效益''',
                    'result': '''提供弹性伸缩方案：
1. 负载分析报告
2. 伸缩策略设计
3. 自动化配置指南
4. 资源优化建议
5. 成本效益分析
6. 实施与监控计划'''
                },
                'variables': [
                    {
                        'name': 'workload_data',
                        'default_value': '工作负载数据',
                        'description': '计算资源的使用模式和负载数据'
                    },
                    {
                        'name': 'scaling_objectives',
                        'default_value': '伸缩目标',
                        'description': '弹性伸缩的业务目标和技术目标'
                    }
                ],
                'target_role': '云平台工程师,资源优化专家,自动化运维工程师'
            },
            {
                'name': '网络架构安全评估与优化',
                'framework_type': 'RTGO',
                'description': '评估网络架构安全性并提供优化方案',
                'content': {
                    'role': '网络安全架构师',
                    'task': '''评估网络安全并优化架构：
1. 分析当前网络拓扑
2. 识别安全风险点
3. 评估安全控制措施
4. 检查网络分段策略
5. 审核访问控制机制
6. 评估流量监控能力
7. 制定安全加固方案''',
                    'goal': '提高网络架构的安全性和可靠性，防范安全威胁',
                    'output': '''提供网络安全评估与优化方案：
1. 安全评估报告
2. 风险识别清单
3. 架构优化建议
4. 安全控制措施
5. 实施优先级
6. 监控与审计策略'''
                },
                'variables': [
                    {
                        'name': 'network_topology',
                        'default_value': '网络拓扑信息',
                        'description': '当前网络架构和拓扑结构'
                    },
                    {
                        'name': 'security_requirements',
                        'default_value': '安全要求',
                        'description': '业务对网络安全的要求和合规标准'
                    }
                ],
                'target_role': '网络安全工程师,网络架构师,安全合规专家'
            },
            {
                'name': '分布式存储系统故障排查',
                'framework_type': 'SPAR',
                'description': '诊断和解决分布式存储系统的故障问题',
                'content': {
                    'situation': '分布式存储系统出现故障或性能问题',
                    'purpose': '快速定位并解决存储系统故障，恢复正常服务',
                    'action': '''1. 收集系统日志和告警
2. 分析故障症状
3. 检查节点状态
4. 验证网络连接
5. 评估数据一致性
6. 定位故障根因
7. 制定修复方案
8. 执行恢复操作
9. 验证系统状态''',
                    'result': '''提供故障排查与解决方案：
1. 故障分析报告
2. 根因确定
3. 修复步骤详解
4. 数据恢复方案
5. 验证测试结果
6. 预防措施建议'''
                },
                'variables': [
                    {
                        'name': 'storage_system',
                        'default_value': '存储系统信息',
                        'description': '分布式存储系统的类型和版本'
                    },
                    {
                        'name': 'error_symptoms',
                        'default_value': '故障症状',
                        'description': '观察到的故障现象和错误信息'
                    }
                ],
                'target_role': '存储运维工程师,分布式系统专家,故障排查工程师'
            },
            {
                'name': '数据库备份与恢复策略',
                'framework_type': 'RTGO',
                'description': '设计数据库的备份与恢复策略，确保数据安全',
                'content': {
                    'role': '数据库备份专家',
                    'task': '''设计数据库备份与恢复策略：
1. 评估业务需求和RTO/RPO
2. 设计备份方案
3. 规划备份频率和保留期
4. 制定恢复流程
5. 设计验证机制
6. 规划存储资源
7. 自动化备份操作
8. 制定测试计划''',
                    'goal': '确保数据安全性和可恢复性，最小化数据丢失风险',
                    'output': '''提供数据库备份与恢复方案：
1. 备份策略设计
2. 恢复流程文档
3. 存储需求评估
4. 自动化脚本
5. 测试与验证计划
6. 运维操作手册'''
                },
                'variables': [
                    {
                        'name': 'database_environment',
                        'default_value': '数据库环境',
                        'description': '数据库类型、规模和业务重要性'
                    },
                    {
                        'name': 'recovery_requirements',
                        'default_value': '恢复要求',
                        'description': 'RTO、RPO和业务连续性要求'
                    }
                ],
                'target_role': '数据库管理员,备份恢复专家,数据保护工程师'
            },
            {
                'name': '消息队列中间件性能优化',
                'framework_type': 'SPAR',
                'description': '优化消息队列中间件性能，提高吞吐量和可靠性',
                'content': {
                    'situation': '消息队列中间件需要性能优化',
                    'purpose': '提高消息处理的吞吐量、可靠性和效率',
                    'action': '''1. 分析当前性能指标
2. 识别瓶颈点
3. 优化队列配置
4. 调整消费者模式
5. 优化消息持久化
6. 调整集群参数
7. 优化网络配置
8. 实施监控机制''',
                    'result': '''提供消息队列优化方案：
1. 性能分析报告
2. 瓶颈识别结果
3. 配置优化建议
4. 架构调整方案
5. 客户端优化指南
6. 监控指标设置'''
                },
                'variables': [
                    {
                        'name': 'queue_system',
                        'default_value': '消息队列系统',
                        'description': '消息队列中间件的类型和版本'
                    },
                    {
                        'name': 'performance_data',
                        'default_value': '性能数据',
                        'description': '当前性能指标和问题描述'
                    }
                ],
                'target_role': '中间件工程师,消息系统专家,性能优化工程师'
            },
            {
                'name': '虚拟化平台迁移与升级',
                'framework_type': 'RTGO',
                'description': '规划和执行虚拟化平台的迁移或升级',
                'content': {
                    'role': '虚拟化平台专家',
                    'task': '''规划虚拟化平台迁移与升级：
1. 评估当前环境
2. 制定迁移策略
3. 设计目标架构
4. 规划迁移步骤
5. 评估风险和影响
6. 制定回退计划
7. 设计测试验证
8. 规划切换流程''',
                    'goal': '实现虚拟化平台的平滑迁移或升级，最小化业务影响',
                    'output': '''提供虚拟化平台迁移方案：
1. 环境评估报告
2. 迁移策略设计
3. 详细实施计划
4. 风险管理措施
5. 测试与验证方案
6. 切换与回退流程'''
                },
                'variables': [
                    {
                        'name': 'current_platform',
                        'default_value': '当前平台信息',
                        'description': '当前虚拟化平台的详细信息'
                    },
                    {
                        'name': 'target_platform',
                        'default_value': '目标平台信息',
                        'description': '目标虚拟化平台的详细信息'
                    }
                ],
                'target_role': '虚拟化工程师,平台迁移专家,基础设施架构师'
            },
            {
                'name': '网络流量分析与优化',
                'framework_type': 'SPAR',
                'description': '分析网络流量模式并优化网络性能',
                'content': {
                    'situation': '网络性能需要优化或出现异常流量',
                    'purpose': '分析流量模式，优化网络性能和安全性',
                    'action': '''1. 收集网络流量数据
2. 分析流量模式和趋势
3. 识别异常流量
4. 检测瓶颈点
5. 优化路由策略
6. 调整QoS策略
7. 实施流量控制
8. 配置缓存和加速
9. 评估优化效果''',
                    'result': '''提供网络流量分析与优化方案：
1. 流量分析报告
2. 异常流量识别
3. 瓶颈点定位
4. 优化建议清单
5. 配置调整指南
6. 监控指标设定'''
                },
                'variables': [
                    {
                        'name': 'network_data',
                        'default_value': '网络数据',
                        'description': '网络流量和性能数据'
                    },
                    {
                        'name': 'performance_issues',
                        'default_value': '性能问题',
                        'description': '当前遇到的网络性能问题'
                    }
                ],
                'target_role': '网络工程师,流量分析专家,网络优化工程师'
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