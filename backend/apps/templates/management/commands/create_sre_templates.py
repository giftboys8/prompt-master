from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template
import json

User = get_user_model()

class Command(BaseCommand):
    help = '创建SRE(站点可靠性工程)相关的高质量提示词模板'

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

        # SRE模板数据
        templates_data = [
            {
                'name': '分布式存储系统故障诊断',
                'framework_type': 'RTGO',
                'description': '诊断和解决分布式存储系统(如Ceph、GlusterFS等)的复杂故障',
                'content': {
                    'role': '分布式存储系统专家',
                    'task': '''全面分析分布式存储系统故障：
1. 解析集群状态和健康报告
2. 分析节点间通信和数据同步问题
3. 诊断存储池和数据分片异常
4. 评估性能下降和延迟问题
5. 确定数据一致性和完整性问题''',
                    'goal': '精确定位分布式存储系统故障根因，并提供恢复方案',
                    'output': '''提供专业的存储系统诊断报告：
1. 集群状态评估
2. 故障节点和组件识别
3. 根因分析和技术发现
4. 数据安全性评估
5. 恢复步骤和优先级
6. 性能优化建议
7. 监控改进和预警机制'''
                },
                'variables': [
                    {
                        'name': 'cluster_status',
                        'default_value': '集群状态输出(如ceph status)',
                        'description': '集群状态'
                    },
                    {
                        'name': 'error_logs',
                        'default_value': '关键错误日志',
                        'description': '错误日志'
                    },
                    {
                        'name': 'system_config',
                        'default_value': '存储系统配置信息',
                        'description': '系统配置'
                    },
                    {
                        'name': 'performance_metrics',
                        'default_value': '性能指标数据',
                        'description': '性能指标'
                    }
                ]
            },
            {
                'name': 'SDN网络故障排查专家',
                'framework_type': 'SPAR',
                'description': '排查和解决软件定义网络(SDN)环境中的复杂网络问题',
                'content': {
                    'situation': 'SDN网络环境出现连接、性能或配置问题',
                    'purpose': '快速定位和解决SDN网络故障，恢复网络服务',
                    'action': '''1. 分析控制平面和数据平面状态
2. 检查网络拓扑和流表配置
3. 验证虚拟网络和物理网络映射
4. 诊断协议栈和隧道问题
5. 评估QoS和流量策略执行
6. 排查SDN控制器与交换机通信问题''',
                    'result': '''提供全面的SDN网络诊断报告：
1. 网络状态概述
2. 控制平面分析结果
3. 数据平面问题发现
4. 根本原因确定
5. 网络配置修复建议
6. 拓扑优化建议
7. 监控和可观测性改进
8. 预防类似问题的最佳实践'''
                },
                'variables': [
                    {
                        'name': 'network_topology',
                        'default_value': '网络拓扑描述或图表',
                        'description': '网络拓扑'
                    },
                    {
                        'name': 'controller_logs',
                        'default_value': 'SDN控制器日志',
                        'description': '控制器日志'
                    },
                    {
                        'name': 'flow_tables',
                        'default_value': '流表配置和状态',
                        'description': '流表配置'
                    },
                    {
                        'name': 'connectivity_issues',
                        'default_value': '连接问题描述',
                        'description': '连接问题'
                    }
                ]
            },
            {
                'name': 'SLO/SLI设计与监控策略',
                'framework_type': 'RTGO',
                'description': '设计有效的服务水平目标(SLO)和指标(SLI)，并制定相应监控策略',
                'content': {
                    'role': 'SRE可靠性专家',
                    'task': '''为关键服务设计科学的SLO/SLI和监控策略：
1. 分析服务特性和关键功能
2. 确定用户体验的关键指标
3. 设计合理的SLO目标和SLI指标
4. 制定全面的监控策略
5. 设计告警阈值和升级流程''',
                    'goal': '建立完善的服务可靠性指标体系和监控系统，提升服务质量',
                    'output': '''提供专业的SLO/SLI设计文档：
1. 服务概述和关键功能
2. SLI指标定义和计算方法
3. SLO目标值和合理性分析
4. 监控实现方案
5. 数据收集和存储策略
6. 告警配置和升级矩阵
7. SLO违规处理流程
8. 持续改进机制'''
                },
                'variables': [
                    {
                        'name': 'service_description',
                        'default_value': '服务功能和架构描述',
                        'description': '服务描述'
                    },
                    {
                        'name': 'critical_paths',
                        'default_value': '关键用户路径和功能',
                        'description': '关键路径'
                    },
                    {
                        'name': 'current_metrics',
                        'default_value': '当前可用的监控指标',
                        'description': '现有指标'
                    },
                    {
                        'name': 'business_requirements',
                        'default_value': '业务可靠性要求',
                        'description': '业务要求'
                    }
                ]
            },
            {
                'name': '大规模基础设施自动化方案',
                'framework_type': 'SPAR',
                'description': '设计和实现大规模基础设施自动化解决方案',
                'content': {
                    'situation': '需要对大规模基础设施实现自动化管理和运维',
                    'purpose': '提高运维效率，减少人为错误，实现基础设施即代码',
                    'action': '''1. 评估当前基础设施和自动化水平
2. 设计自动化架构和工具链
3. 制定配置管理和版本控制策略
4. 设计CI/CD流程和测试框架
5. 实现自动化部署和配置
6. 建立自动化监控和响应机制''',
                    'result': '''提供完整的基础设施自动化方案：
1. 自动化架构设计
2. 工具选型和集成方案
3. 配置管理策略
4. CI/CD流程设计
5. 自动化脚本和模板示例
6. 测试和验证框架
7. 实施路线图和优先级
8. 安全控制和合规考虑
9. ROI分析和效益评估'''
                },
                'variables': [
                    {
                        'name': 'infra_description',
                        'default_value': '基础设施规模和组成',
                        'description': '基础设施描述'
                    },
                    {
                        'name': 'current_processes',
                        'default_value': '当前运维流程和痛点',
                        'description': '当前流程'
                    },
                    {
                        'name': 'automation_goals',
                        'default_value': '自动化目标和KPI',
                        'description': '自动化目标'
                    },
                    {
                        'name': 'tech_constraints',
                        'default_value': '技术限制和兼容性要求',
                        'description': '技术限制'
                    }
                ]
            },
            {
                'name': '高级容灾与业务连续性规划',
                'framework_type': 'RTGO',
                'description': '制定全面的容灾和业务连续性计划，应对各种灾难场景',
                'content': {
                    'role': '容灾与业务连续性专家',
                    'task': '''设计全面的容灾和业务连续性方案：
1. 评估关键业务系统和依赖关系
2. 识别潜在风险和灾难场景
3. 设计多层次容灾架构
4. 制定恢复策略和流程
5. 设计容灾演练方案''',
                    'goal': '确保在各种灾难场景下业务系统能够快速恢复，最小化影响',
                    'output': '''提供专业的容灾与业务连续性规划：
1. 业务影响分析(BIA)
2. 风险评估和灾难场景
3. 恢复时间目标(RTO)和恢复点目标(RPO)
4. 容灾架构设计
5. 数据备份和恢复策略
6. 故障转移和恢复流程
7. 容灾演练计划
8. 应急响应团队和职责
9. 通信和升级矩阵'''
                },
                'variables': [
                    {
                        'name': 'critical_systems',
                        'default_value': '关键业务系统清单',
                        'description': '关键系统'
                    },
                    {
                        'name': 'business_requirements',
                        'default_value': '业务连续性要求和SLA',
                        'description': '业务要求'
                    },
                    {
                        'name': 'current_dr_measures',
                        'default_value': '当前容灾措施',
                        'description': '现有措施'
                    },
                    {
                        'name': 'risk_scenarios',
                        'default_value': '需考虑的风险场景',
                        'description': '风险场景'
                    }
                ]
            },
            {
                'name': '可观测性系统设计专家',
                'framework_type': 'SPAR',
                'description': '设计全面的可观测性系统，整合日志、指标和追踪',
                'content': {
                    'situation': '需要建立或优化系统的可观测性，提升问题排查效率',
                    'purpose': '构建统一的可观测性平台，实现日志、指标和追踪的整合',
                    'action': '''1. 评估当前监控和可观测性状况
2. 设计日志收集和处理架构
3. 规划指标采集和存储策略
4. 实现分布式追踪系统
5. 整合告警和通知机制
6. 设计可视化和分析平台''',
                    'result': '''提供完整的可观测性系统设计方案：
1. 可观测性架构设计
2. 日志管理解决方案
3. 指标体系和采集方案
4. 分布式追踪实现
5. 告警策略和通知渠道
6. 可视化仪表板设计
7. 存储和扩展性考虑
8. 实施路线图和优先级
9. 工具选型和集成方案'''
                },
                'variables': [
                    {
                        'name': 'system_architecture',
                        'default_value': '系统架构描述',
                        'description': '系统架构'
                    },
                    {
                        'name': 'current_monitoring',
                        'default_value': '当前监控和日志系统',
                        'description': '当前监控'
                    },
                    {
                        'name': 'scale_requirements',
                        'default_value': '规模和性能要求',
                        'description': '规模要求'
                    },
                    {
                        'name': 'key_metrics',
                        'default_value': '需要关注的关键指标',
                        'description': '关键指标'
                    }
                ]
            },
            {
                'name': '高性能存储系统调优',
                'framework_type': 'RTGO',
                'description': '优化高性能存储系统(如SAN、NAS、对象存储)的性能和可靠性',
                'content': {
                    'role': '存储性能优化专家',
                    'task': '''全面分析和优化存储系统性能：
1. 评估存储架构和配置
2. 分析IO模式和工作负载特征
3. 识别性能瓶颈和热点
4. 优化存储层级和缓存策略
5. 调整RAID配置和数据布局
6. 优化网络和协议设置''',
                    'goal': '显著提升存储系统性能和可靠性，满足业务需求',
                    'output': '''提供专业的存储系统优化报告：
1. 存储系统评估结果
2. 性能瓶颈分析
3. 工作负载特征分析
4. 短期优化建议
5. 长期架构改进方案
6. 参数调优指南
7. 基准测试结果对比
8. 监控和性能指标建议'''
                },
                'variables': [
                    {
                        'name': 'storage_architecture',
                        'default_value': '存储系统架构和配置',
                        'description': '存储架构'
                    },
                    {
                        'name': 'workload_characteristics',
                        'default_value': '工作负载特征(读写比例、IO大小等)',
                        'description': '工作负载'
                    },
                    {
                        'name': 'performance_data',
                        'default_value': '性能测试或监控数据',
                        'description': '性能数据'
                    },
                    {
                        'name': 'business_requirements',
                        'default_value': '业务性能需求和SLA',
                        'description': '业务需求'
                    }
                ]
            },
            {
                'name': '混合云网络架构设计',
                'framework_type': 'SPAR',
                'description': '设计安全、高效的混合云网络架构和连接方案',
                'content': {
                    'situation': '需要设计连接本地数据中心和多个云平台的网络架构',
                    'purpose': '建立安全、高性能、可扩展的混合云网络基础设施',
                    'action': '''1. 评估当前网络架构和需求
2. 设计云互联和VPN策略
3. 规划网络地址分配和路由
4. 设计安全域和访问控制
5. 优化流量路径和负载均衡
6. 实现网络自动化和编排''',
                    'result': '''提供完整的混合云网络架构设计：
1. 网络拓扑图和架构设计
2. 连接方案和技术选型
3. IP地址分配方案
4. 路由策略和流量工程
5. 安全控制和防护措施
6. 高可用性和冗余设计
7. 性能优化建议
8. 监控和管理方案
9. 实施路线图和迁移策略'''
                },
                'variables': [
                    {
                        'name': 'current_network',
                        'default_value': '当前网络架构描述',
                        'description': '当前网络'
                    },
                    {
                        'name': 'cloud_platforms',
                        'default_value': '涉及的云平台和区域',
                        'description': '云平台'
                    },
                    {
                        'name': 'traffic_patterns',
                        'default_value': '主要流量模式和带宽需求',
                        'description': '流量模式'
                    },
                    {
                        'name': 'security_requirements',
                        'default_value': '安全和合规要求',
                        'description': '安全要求'
                    }
                ]
            },
            {
                'name': '大规模系统容量规划',
                'framework_type': 'RTGO',
                'description': '为大规模分布式系统进行科学的容量规划和资源预测',
                'content': {
                    'role': '系统容量规划专家',
                    'task': '''为分布式系统进行全面的容量规划：
1. 分析历史使用趋势和增长模式
2. 评估当前资源利用率和瓶颈
3. 预测未来负载和资源需求
4. 制定扩展策略和触发条件
5. 设计资源分配和优化方案''',
                    'goal': '确保系统资源与业务需求匹配，既避免过度配置又能应对增长',
                    'output': '''提供专业的容量规划报告：
1. 当前资源使用分析
2. 历史趋势和模式识别
3. 增长预测和场景分析
4. 资源需求预估
5. 扩展策略和时间表
6. 成本优化建议
7. 风险评估和缓解措施
8. 监控和预警指标'''
                },
                'variables': [
                    {
                        'name': 'system_description',
                        'default_value': '系统架构和组件描述',
                        'description': '系统描述'
                    },
                    {
                        'name': 'historical_data',
                        'default_value': '历史使用数据和趋势',
                        'description': '历史数据'
                    },
                    {
                        'name': 'growth_projections',
                        'default_value': '业务增长预测',
                        'description': '增长预测'
                    },
                    {
                        'name': 'resource_constraints',
                        'default_value': '资源限制和预算约束',
                        'description': '资源约束'
                    }
                ]
            },
            {
                'name': '自动化事件响应系统设计',
                'framework_type': 'SPAR',
                'description': '设计自动化事件响应系统，实现故障自愈和智能处理',
                'content': {
                    'situation': '需要减少人工干预，提高故障响应速度和一致性',
                    'purpose': '构建自动化事件响应系统，实现常见故障的自动检测和修复',
                    'action': '''1. 分析常见故障模式和处理流程
2. 设计事件检测和分类机制
3. 开发自动化响应规则和脚本
4. 实现决策逻辑和升级流程
5. 设计反馈和学习机制
6. 建立审计和安全控制''',
                    'result': '''提供完整的自动化事件响应系统设计：
1. 系统架构和组件设计
2. 事件分类和优先级矩阵
3. 响应规则库和决策树
4. 自动化脚本和工具集成
5. 升级流程和人工干预点
6. 安全控制和审计机制
7. 性能指标和效果评估
8. 实施路线图和优先级
9. 持续改进机制'''
                },
                'variables': [
                    {
                        'name': 'common_incidents',
                        'default_value': '常见故障类型和模式',
                        'description': '常见故障'
                    },
                    {
                        'name': 'current_processes',
                        'default_value': '当前事件响应流程',
                        'description': '当前流程'
                    },
                    {
                        'name': 'automation_scope',
                        'default_value': '自动化范围和目标',
                        'description': '自动化范围'
                    },
                    {
                        'name': 'integration_points',
                        'default_value': '需要集成的系统和工具',
                        'description': '集成点'
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
                f'成功创建{created_count}个SRE相关的高质量提示词模板！'
            )
        )