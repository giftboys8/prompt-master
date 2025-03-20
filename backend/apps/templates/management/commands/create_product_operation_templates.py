from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建产品运营工程师相关的高质量提示词模板'

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

        # 产品运营工程师模板数据
        templates_data = [
            {
                'name': '用户获取渠道策略分析师',
                'framework_type': 'RTGO',
                'description': '分析和优化多渠道用户获取策略，提升获客效率和质量',
                'content': {
                    'role': '用户增长与渠道策略专家',
                    'task': '''全面分析用户获取渠道效果并提出优化策略：
1. 评估各渠道的获客效果和成本
2. 分析渠道用户的质量和生命周期价值
3. 识别高潜力渠道和增长机会
4. 设计渠道组合和资源分配策略
5. 提出渠道优化和扩展建议''',
                    'goal': '优化用户获取策略，提高获客效率和用户质量，降低获客成本',
                    'output': '''提供详细的渠道策略分析报告：
1. 渠道效果数据分析
2. 渠道用户画像和行为特征
3. CAC(获客成本)和LTV(生命周期价值)分析
4. 渠道ROI评估
5. 渠道优化建议
6. 资源分配策略
7. 新渠道开发机会
8. 实施计划和KPI设定'''
                },
                'variables': [
                    {
                        'name': 'channel_data',
                        'default_value': '各渠道的获客数据(流量、转化率、成本等)',
                        'description': '渠道数据'
                    },
                    {
                        'name': 'user_behavior',
                        'default_value': '不同渠道用户的行为数据',
                        'description': '用户行为'
                    },
                    {
                        'name': 'business_goals',
                        'default_value': '业务目标和KPI',
                        'description': '业务目标'
                    },
                    {
                        'name': 'budget_constraints',
                        'default_value': '预算限制和资源约束',
                        'description': '预算约束'
                    }
                ]
            },
            {
                'name': '用户旅程优化专家',
                'framework_type': 'SPAR',
                'description': '分析和优化用户旅程，提升转化率和用户体验',
                'content': {
                    'situation': '用户旅程中存在流失点或体验问题，需要优化',
                    'purpose': '识别并消除用户旅程中的摩擦点，提升转化率和用户体验',
                    'action': '''1. 映射完整的用户旅程路径
2. 分析各环节的转化率和流失点
3. 识别用户体验痛点和摩擦因素
4. 进行竞品用户旅程对比
5. 设计优化方案和A/B测试
6. 制定实施计划和效果评估方法''',
                    'result': '''提供全面的用户旅程优化方案：
1. 用户旅程地图和流程分析
2. 关键流失点和原因诊断
3. 用户体验痛点清单
4. 竞品分析和最佳实践借鉴
5. 优化建议和实施优先级
6. A/B测试设计
7. 预期效果评估
8. 监控指标和成功标准'''
                },
                'variables': [
                    {
                        'name': 'journey_data',
                        'default_value': '用户旅程数据和转化漏斗',
                        'description': '旅程数据'
                    },
                    {
                        'name': 'user_feedback',
                        'default_value': '用户反馈和调研结果',
                        'description': '用户反馈'
                    },
                    {
                        'name': 'pain_points',
                        'default_value': '已知的用户痛点和问题',
                        'description': '用户痛点'
                    },
                    {
                        'name': 'business_constraints',
                        'default_value': '业务和技术限制',
                        'description': '业务限制'
                    }
                ]
            },
            {
                'name': '用户留存策略设计师',
                'framework_type': 'RTGO',
                'description': '设计有效的用户留存策略，提高产品的长期活跃度',
                'content': {
                    'role': '用户留存与活跃度专家',
                    'task': '''设计全面的用户留存策略：
1. 分析用户流失原因和时间点
2. 评估产品的核心价值和习惯养成机制
3. 设计分层的留存策略和激励机制
4. 规划用户生命周期沟通策略
5. 设计产品改进和功能优化方向''',
                    'goal': '提高用户留存率和活跃度，延长用户生命周期',
                    'output': '''提供完整的用户留存策略方案：
1. 用户留存现状分析
2. 流失原因和关键时间点识别
3. 用户分层策略
4. 核心留存机制设计
5. 触达策略和内容规划
6. 激励体系设计
7. 产品优化建议
8. 实施路线图和效果预测
9. 关键指标和监控方案'''
                },
                'variables': [
                    {
                        'name': 'retention_data',
                        'default_value': '用户留存曲线和流失数据',
                        'description': '留存数据'
                    },
                    {
                        'name': 'user_segments',
                        'default_value': '用户分群及其行为特征',
                        'description': '用户分群'
                    },
                    {
                        'name': 'product_features',
                        'default_value': '产品核心功能和价值主张',
                        'description': '产品功能'
                    },
                    {
                        'name': 'competitor_strategies',
                        'default_value': '竞品留存策略分析',
                        'description': '竞品策略'
                    }
                ]
            },
            {
                'name': '用户行为数据分析师',
                'framework_type': 'SPAR',
                'description': '深入分析用户行为数据，发掘洞察和优化机会',
                'content': {
                    'situation': '需要从海量用户行为数据中提取有价值的洞察',
                    'purpose': '通过数据分析发现用户行为模式和优化机会',
                    'action': '''1. 定义关键分析问题和假设
2. 收集和清洗相关数据
3. 进行探索性数据分析
4. 识别用户行为模式和分群
5. 构建预测模型和细分分析
6. 提取可操作的洞察和建议''',
                    'result': '''提供深度的用户行为分析报告：
1. 数据概览和质量评估
2. 关键行为指标分析
3. 用户行为模式发现
4. 用户分群和画像构建
5. 转化和流失因素分析
6. 产品使用热点和盲点
7. 可操作的优化建议
8. 进一步分析方向'''
                },
                'variables': [
                    {
                        'name': 'behavior_data',
                        'default_value': '用户行为数据描述',
                        'description': '行为数据'
                    },
                    {
                        'name': 'analysis_questions',
                        'default_value': '需要回答的关键问题',
                        'description': '分析问题'
                    },
                    {
                        'name': 'metrics_definition',
                        'default_value': '关键指标定义',
                        'description': '指标定义'
                    },
                    {
                        'name': 'business_context',
                        'default_value': '业务背景和决策需求',
                        'description': '业务背景'
                    }
                ]
            },
            {
                'name': '产品变现策略顾问',
                'framework_type': 'RTGO',
                'description': '设计有效的产品变现策略，优化收入结构和用户价值',
                'content': {
                    'role': '产品变现和商业模式专家',
                    'task': '''设计全面的产品变现策略：
1. 评估产品的价值主张和用户支付意愿
2. 分析当前变现模式的效果和瓶颈
3. 研究行业变现趋势和最佳实践
4. 设计多元化的变现模式和价格策略
5. 规划变现路径和用户转化流程''',
                    'goal': '优化产品变现效果，提高ARPU和总体收入',
                    'output': '''提供详细的产品变现策略方案：
1. 当前变现状况评估
2. 用户支付意愿和价值感知分析
3. 变现模式设计(订阅/一次性/广告/增值服务等)
4. 价格策略和套餐设计
5. 用户分层变现策略
6. 转化路径和触点优化
7. 促销和激励机制
8. 实施路线图和收入预测
9. 关键指标和监控方案'''
                },
                'variables': [
                    {
                        'name': 'revenue_data',
                        'default_value': '当前收入数据和变现指标',
                        'description': '收入数据'
                    },
                    {
                        'name': 'user_segments',
                        'default_value': '用户分群及其支付能力',
                        'description': '用户分群'
                    },
                    {
                        'name': 'product_value',
                        'default_value': '产品核心价值和差异化优势',
                        'description': '产品价值'
                    },
                    {
                        'name': 'market_benchmarks',
                        'default_value': '行业标杆和竞品定价策略',
                        'description': '市场标杆'
                    }
                ]
            },
            {
                'name': '用户激活策略设计师',
                'framework_type': 'SPAR',
                'description': '设计有效的用户激活策略，帮助新用户快速体验产品核心价值',
                'content': {
                    'situation': '新用户注册后未充分体验产品核心价值，激活率低',
                    'purpose': '设计有效的用户激活策略，提高新用户转为活跃用户的比例',
                    'action': '''1. 定义明确的用户激活标准
2. 分析当前用户激活路径和瓶颈
3. 识别核心功能和"啊哈时刻"
4. 设计简化的首次使用体验
5. 开发引导流程和教育内容
6. 构建激励机制和社交触发''',
                    'result': '''提供完整的用户激活策略方案：
1. 用户激活现状分析
2. 激活标准和指标定义
3. 首次使用体验优化
4. 引导流程设计
5. 核心价值展示策略
6. 激励机制设计
7. 个性化激活路径
8. 实施计划和A/B测试设计
9. 效果评估框架'''
                },
                'variables': [
                    {
                        'name': 'activation_data',
                        'default_value': '当前激活漏斗和转化数据',
                        'description': '激活数据'
                    },
                    {
                        'name': 'user_feedback',
                        'default_value': '新用户反馈和使用障碍',
                        'description': '用户反馈'
                    },
                    {
                        'name': 'core_actions',
                        'default_value': '产品核心行为和价值点',
                        'description': '核心行为'
                    },
                    {
                        'name': 'competitive_analysis',
                        'default_value': '竞品激活策略分析',
                        'description': '竞品分析'
                    }
                ]
            },
            {
                'name': '用户增长实验设计师',
                'framework_type': 'RTGO',
                'description': '设计科学的用户增长实验，验证假设并优化增长策略',
                'content': {
                    'role': '增长黑客和实验设计专家',
                    'task': '''设计严谨的用户增长实验：
1. 基于数据和洞察提出增长假设
2. 设计科学的实验方法和流程
3. 确定样本大小和分组策略
4. 定义明确的成功指标
5. 规划实验实施和数据收集
6. 设计结果分析和决策框架''',
                    'goal': '通过实验验证增长假设，找到有效的增长杠杆',
                    'output': '''提供详细的增长实验设计方案：
1. 增长机会分析和假设形成
2. 实验设计和方法论
3. 实验变量和控制因素
4. 样本规划和分组策略
5. 成功指标和评估框架
6. 实施计划和资源需求
7. 风险评估和缓解措施
8. 结果分析方法和决策标准
9. 学习循环和迭代策略'''
                },
                'variables': [
                    {
                        'name': 'growth_hypotheses',
                        'default_value': '增长假设和机会点',
                        'description': '增长假设'
                    },
                    {
                        'name': 'historical_data',
                        'default_value': '相关历史数据和基线',
                        'description': '历史数据'
                    },
                    {
                        'name': 'target_metrics',
                        'default_value': '目标改进的关键指标',
                        'description': '目标指标'
                    },
                    {
                        'name': 'constraints',
                        'default_value': '实验条件和资源限制',
                        'description': '实验限制'
                    }
                ]
            },
            {
                'name': '产品运营数据仪表板设计师',
                'framework_type': 'SPAR',
                'description': '设计全面的产品运营数据仪表板，支持数据驱动决策',
                'content': {
                    'situation': '需要构建清晰、实用的产品运营数据仪表板',
                    'purpose': '提供全面的数据视图，支持运营决策和绩效跟踪',
                    'action': '''1. 确定关键业务问题和决策需求
2. 定义核心指标体系和计算方法
3. 设计多层次的数据视图和钻取路径
4. 规划数据更新频率和展示方式
5. 设计异常检测和预警机制
6. 构建自助分析和报告功能''',
                    'result': '''提供完整的数据仪表板设计方案：
1. 仪表板架构和层次结构
2. 核心指标定义和计算逻辑
3. 数据可视化设计
4. 用户角色和权限设计
5. 交互功能和钻取路径
6. 异常检测和预警规则
7. 实施技术方案
8. 数据质量保障措施
9. 使用指南和培训计划'''
                },
                'variables': [
                    {
                        'name': 'business_questions',
                        'default_value': '需要回答的关键业务问题',
                        'description': '业务问题'
                    },
                    {
                        'name': 'key_metrics',
                        'default_value': '核心指标清单',
                        'description': '核心指标'
                    },
                    {
                        'name': 'data_sources',
                        'default_value': '可用数据源和数据结构',
                        'description': '数据源'
                    },
                    {
                        'name': 'user_roles',
                        'default_value': '仪表板使用者角色和需求',
                        'description': '用户角色'
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
                f'成功创建{created_count}个产品运营工程师相关的高质量提示词模板！'
            )
        )