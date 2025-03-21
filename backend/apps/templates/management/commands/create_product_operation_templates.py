from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建商业经营相关的提示词模板数据'

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

        # 商业经营模板数据
        templates_data = [
            {
                'name': '市场竞争分析与战略规划',
                'framework_type': 'SPAR',
                'description': '分析市场竞争态势并制定战略规划',
                'content': {
                    'situation': '需要深入分析市场竞争环境并制定相应战略',
                    'purpose': '制定有效的市场竞争战略，提升市场地位',
                    'action': '''1. 分析市场规模和趋势
2. 评估竞争对手优劣势
3. 识别市场机会和威胁
4. 分析自身竞争优势
5. 制定市场定位策略
6. 设计竞争策略
7. 规划资源配置
8. 制定实施计划''',
                    'result': '''提供市场竞争分析与战略规划：
1. 市场分析报告
2. 竞争态势分析
3. SWOT分析结果
4. 战略规划方案
5. 行动计划建议
6. 预期效果评估'''
                },
                'variables': [
                    {
                        'name': 'market_data',
                        'default_value': '市场数据',
                        'description': '市场规模、增长率等相关数据'
                    },
                    {
                        'name': 'competitor_info',
                        'default_value': '竞争对手信息',
                        'description': '主要竞争对手的情况分析'
                    }
                ],
                'target_role': '市场战略经理,商业分析师,战略规划专家'
            },
            {
                'name': '营销策略制定与执行',
                'framework_type': 'RTGO',
                'description': '设计和实施有效的营销策略',
                'content': {
                    'role': '营销策略专家',
                    'task': '''制定和执行营销策略：
1. 分析目标市场
2. 定义目标客户群
3. 设计营销信息
4. 选择营销渠道
5. 制定推广计划
6. 设置营销预算
7. 规划执行时间
8. 设计效果评估''',
                    'goal': '通过有效的营销策略提升品牌知名度和市场份额',
                    'output': '''提供营销策略方案：
1. 市场细分分析
2. 营销策略设计
3. 渠道规划方案
4. 预算分配建议
5. 执行时间表
6. ROI预测分析'''
                },
                'variables': [
                    {
                        'name': 'target_audience',
                        'default_value': '目标受众',
                        'description': '目标客户群体特征描述'
                    },
                    {
                        'name': 'marketing_budget',
                        'default_value': '营销预算',
                        'description': '可用于营销活动的预算范围'
                    }
                ],
                'target_role': '营销经理,品牌经理,市场推广专员'
            },
            {
                'name': '客户关系管理与维护',
                'framework_type': 'SPAR',
                'description': '建立和维护良好的客户关系',
                'content': {
                    'situation': '需要改善客户关系管理体系',
                    'purpose': '提升客户满意度和忠诚度',
                    'action': '''1. 分析客户数据
2. 细分客户群体
3. 设计服务流程
4. 制定沟通策略
5. 建立反馈机制
6. 开发忠诚计划
7. 设置满意度指标
8. 规划危机处理''',
                    'result': '''提供客户关系管理方案：
1. 客户分析报告
2. 服务流程设计
3. 沟通策略建议
4. 忠诚计划方案
5. 满意度提升建议
6. 危机应对预案'''
                },
                'variables': [
                    {
                        'name': 'customer_data',
                        'default_value': '客户数据',
                        'description': '现有客户的相关数据分析'
                    },
                    {
                        'name': 'service_metrics',
                        'default_value': '服务指标',
                        'description': '当前客户服务相关指标'
                    }
                ],
                'target_role': '客户关系经理,服务总监,客户成功经理'
            },
            {
                'name': '财务预算规划与控制',
                'framework_type': 'RTGO',
                'description': '制定和管理财务预算，优化资源配置',
                'content': {
                    'role': '财务规划专家',
                    'task': '''规划和控制财务预算：
1. 分析历史数据
2. 预测收入支出
3. 制定预算方案
4. 分配资源额度
5. 设置控制指标
6. 建立监控机制
7. 规划应急方案
8. 评估执行效果''',
                    'goal': '实现合理的财务规划和有效的预算控制',
                    'output': '''提供财务预算方案：
1. 预算规划报告
2. 资源分配建议
3. 控制措施设计
4. 监控指标体系
5. 风险应对方案
6. 效果评估框架'''
                },
                'variables': [
                    {
                        'name': 'financial_data',
                        'default_value': '财务数据',
                        'description': '历史财务数据和预测'
                    },
                    {
                        'name': 'budget_objectives',
                        'default_value': '预算目标',
                        'description': '预算管理的具体目标'
                    }
                ],
                'target_role': '财务经理,预算主管,财务分析师'
            },
            {
                'name': '运营效率优化与流程改进',
                'framework_type': 'SPAR',
                'description': '优化运营流程，提升运营效率',
                'content': {
                    'situation': '需要提升运营效率和优化业务流程',
                    'purpose': '提高运营效率，降低运营成本',
                    'action': '''1. 评估当前流程
2. 识别效率瓶颈
3. 分析改进机会
4. 设计优化方案
5. 制定实施计划
6. 培训相关人员
7. 监控改进效果
8. 持续优化调整''',
                    'result': '''提供运营优化方案：
1. 流程分析报告
2. 瓶颈识别清单
3. 改进建议方案
4. 实施计划书
5. 培训计划设计
6. 效果评估框架'''
                },
                'variables': [
                    {
                        'name': 'process_data',
                        'default_value': '流程数据',
                        'description': '当前运营流程相关数据'
                    },
                    {
                        'name': 'efficiency_metrics',
                        'default_value': '效率指标',
                        'description': '运营效率相关指标'
                    }
                ],
                'target_role': '运营总监,流程优化专家,运营经理'
            },
            {
                'name': '产品定价策略制定',
                'framework_type': 'RTGO',
                'description': '制定科学合理的产品定价策略',
                'content': {
                    'role': '定价策略专家',
                    'task': '''制定产品定价策略：
1. 分析成本结构
2. 评估市场价格
3. 研究竞品定价
4. 分析客户支付意愿
5. 设计定价模型
6. 制定价格策略
7. 规划调价机制
8. 评估价格风险''',
                    'goal': '制定既能保证利润又具市场竞争力的定价策略',
                    'output': '''提供定价策略方案：
1. 成本分析报告
2. 市场价格研究
3. 定价策略建议
4. 价格体系设计
5. 调价机制方案
6. 风险评估报告'''
                },
                'variables': [
                    {
                        'name': 'cost_data',
                        'default_value': '成本数据',
                        'description': '产品成本结构分析'
                    },
                    {
                        'name': 'market_prices',
                        'default_value': '市场价格',
                        'description': '市场和竞品价格信息'
                    }
                ],
                'target_role': '产品经理,定价专家,市场策略师'
            },
            {
                'name': '供应链优化与管理',
                'framework_type': 'SPAR',
                'description': '优化供应链管理，提升运营效率',
                'content': {
                    'situation': '需要优化供应链管理体系',
                    'purpose': '提高供应链效率，降低运营成本',
                    'action': '''1. 评估供应链现状
2. 分析供应商体系
3. 优化库存管理
4. 改进物流配送
5. 加强质量控制
6. 优化采购流程
7. 建立绩效指标
8. 实施风险管理''',
                    'result': '''提供供应链优化方案：
1. 现状分析报告
2. 优化建议方案
3. 流程改进设计
4. 绩效指标体系
5. 风险管理预案
6. 实施计划书'''
                },
                'variables': [
                    {
                        'name': 'supply_chain_data',
                        'default_value': '供应链数据',
                        'description': '供应链运营相关数据'
                    },
                    {
                        'name': 'performance_metrics',
                        'default_value': '绩效指标',
                        'description': '供应链绩效相关指标'
                    }
                ],
                'target_role': '供应链经理,采购总监,物流主管'
            },
            {
                'name': '人才发展与团队建设',
                'framework_type': 'RTGO',
                'description': '规划人才发展战略，加强团队建设',
                'content': {
                    'role': '人才发展顾问',
                    'task': '''规划人才发展与团队建设：
1. 评估人才需求
2. 分析团队现状
3. 设计培养计划
4. 建立晋升体系
5. 优化激励机制
6. 加强文化建设
7. 提升团队协作
8. 建立评估体系''',
                    'goal': '建立高效能团队，促进人才发展',
                    'output': '''提供人才发展方案：
1. 需求分析报告
2. 培养计划设计
3. 晋升体系方案
4. 激励机制建议
5. 文化建设策略
6. 评估指标体系'''
                },
                'variables': [
                    {
                        'name': 'team_data',
                        'default_value': '团队数据',
                        'description': '团队构成和表现数据'
                    },
                    {
                        'name': 'development_needs',
                        'default_value': '发展需求',
                        'description': '人才发展相关需求'
                    }
                ],
                'target_role': '人力资源总监,组织发展经理,团队管理者'
            },
            {
                'name': '品牌建设与管理',
                'framework_type': 'SPAR',
                'description': '制定和实施品牌建设策略',
                'content': {
                    'situation': '需要加强品牌建设和管理',
                    'purpose': '提升品牌价值和市场影响力',
                    'action': '''1. 分析品牌现状
2. 定义品牌定位
3. 设计品牌策略
4. 规划传播方案
5. 制定视觉规范
6. 建设品牌文化
7. 管理品牌资产
8. 监测品牌声誉''',
                    'result': '''提供品牌建设方案：
1. 品牌分析报告
2. 定位策略建议
3. 传播方案设计
4. 视觉规范指南
5. 文化建设计划
6. 评估体系设计'''
                },
                'variables': [
                    {
                        'name': 'brand_data',
                        'default_value': '品牌数据',
                        'description': '品牌相关数据和分析'
                    },
                    {
                        'name': 'market_position',
                        'default_value': '市场定位',
                        'description': '目标市场定位信息'
                    }
                ],
                'target_role': '品牌总监,市场总监,品牌策略师'
            },
            {
                'name': '新业务拓展规划',
                'framework_type': 'RTGO',
                'description': '规划和实施新业务拓展战略',
                'content': {
                    'role': '业务发展顾问',
                    'task': '''规划新业务拓展：
1. 分析市场机会
2. 评估内部资源
3. 研究目标市场
4. 制定进入策略
5. 设计商业模式
6. 规划实施路径
7. 评估投资回报
8. 制定风险预案''',
                    'goal': '开拓新的业务增长点，实现可持续发展',
                    'output': '''提供业务拓展方案：
1. 市场机会分析
2. 可行性研究报告
3. 商业模式设计
4. 实施路径规划
5. 财务预测分析
6. 风险管理方案'''
                },
                'variables': [
                    {
                        'name': 'market_opportunity',
                        'default_value': '市场机会',
                        'description': '潜在市场机会分析'
                    },
                    {
                        'name': 'resource_assessment',
                        'default_value': '资源评估',
                        'description': '内部资源能力评估'
                    }
                ],
                'target_role': '业务发展总监,战略发展经理,商务拓展经理'
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
                f'成功创建{created_count}个商业经营相关的提示词模板！'
            )
        )