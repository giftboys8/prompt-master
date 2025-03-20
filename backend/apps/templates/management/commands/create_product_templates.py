from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.templates.models import Template

User = get_user_model()

class Command(BaseCommand):
    help = '创建产品经理相关的提示词模板数据'

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

        # 产品经理模板数据
        templates_data = [
            {
                'name': '用户需求分析专家',
                'framework_type': 'RTGO',
                'description': '帮助分析和提炼用户需求，转化为产品功能',
                'content': {
                    'role': '资深产品需求分析师',
                    'task': '''分析用户反馈并提炼为结构化的产品需求：
1. 识别用户痛点和核心需求
2. 区分必要需求和次要需求
3. 将需求转化为可执行的功能点
4. 评估实现优先级和复杂度''',
                    'goal': '将模糊的用户反馈转化为清晰、可执行的产品需求文档',
                    'output': '''输出完整的需求分析报告：
1. 用户需求摘要
2. 核心痛点分析
3. 功能需求列表（按优先级排序）
4. 实现复杂度评估
5. 验收标准建议'''
                },
                'variables': [
                    {
                        'name': 'user_feedback',
                        'default_value': '用户反馈和调研数据',
                        'description': '用户反馈内容'
                    },
                    {
                        'name': 'product_context',
                        'default_value': '产品背景和当前状态',
                        'description': '产品上下文'
                    },
                    {
                        'name': 'business_goals',
                        'default_value': '业务目标和KPI',
                        'description': '业务目标'
                    }
                ]
            },
            {
                'name': '产品规划路线图制定',
                'framework_type': 'SPAR',
                'description': '帮助制定产品发展路线图和迭代计划',
                'content': {
                    'situation': '需要规划产品未来的发展方向和功能迭代',
                    'purpose': '创建清晰的产品路线图，指导团队开发',
                    'action': '''1. 分析产品现状和市场定位
2. 评估用户需求和业务目标
3. 规划功能迭代优先级
4. 设定关键里程碑
5. 制定资源分配计划''',
                    'result': '''输出完整的产品路线图：
1. 产品愿景和战略目标
2. 季度/年度功能发布计划
3. 关键里程碑时间线
4. 资源需求评估
5. 成功指标和评估方法'''
                },
                'variables': [
                    {
                        'name': 'product_vision',
                        'default_value': '产品愿景和长期目标',
                        'description': '产品愿景'
                    },
                    {
                        'name': 'current_status',
                        'default_value': '产品当前状态和功能',
                        'description': '当前状态'
                    },
                    {
                        'name': 'planning_horizon',
                        'default_value': '6个月/1年/3年',
                        'description': '规划周期'
                    }
                ]
            },
            {
                'name': '竞品分析专家',
                'framework_type': 'RTGO',
                'description': '深入分析竞争产品，找出差异化优势',
                'content': {
                    'role': '市场竞争分析专家',
                    'task': '''全面分析竞争产品，找出差异化机会：
1. 评估竞品功能和用户体验
2. 分析竞品优势和劣势
3. 识别市场空白和机会
4. 提出差异化策略''',
                    'goal': '找出产品的差异化竞争优势，指导产品定位和功能开发',
                    'output': '''输出详细的竞品分析报告：
1. 竞品概览和市场定位
2. 功能对比矩阵
3. SWOT分析
4. 差异化机会点
5. 战略建议和行动计划'''
                },
                'variables': [
                    {
                        'name': 'competitors',
                        'default_value': '主要竞争对手列表',
                        'description': '竞争对手'
                    },
                    {
                        'name': 'product_features',
                        'default_value': '我们产品的核心功能',
                        'description': '产品功能'
                    },
                    {
                        'name': 'market_trends',
                        'default_value': '行业趋势和用户需求变化',
                        'description': '市场趋势'
                    }
                ]
            },
            {
                'name': '用户故事与场景设计',
                'framework_type': 'SPAR',
                'description': '创建用户故事和使用场景，指导产品设计',
                'content': {
                    'situation': '需要为产品功能创建具体的用户故事和使用场景',
                    'purpose': '通过生动的用户故事帮助团队理解产品价值和用户需求',
                    'action': '''1. 分析目标用户画像
2. 创建典型使用场景
3. 编写用户故事
4. 设计交互流程''',
                    'result': '''输出完整的用户故事文档：
1. 用户角色描述
2. 场景背景设定
3. 详细用户故事（As a... I want to... So that...）
4. 交互流程图
5. 验收标准'''
                },
                'variables': [
                    {
                        'name': 'user_personas',
                        'default_value': '目标用户画像描述',
                        'description': '用户画像'
                    },
                    {
                        'name': 'key_features',
                        'default_value': '需要覆盖的核心功能',
                        'description': '核心功能'
                    },
                    {
                        'name': 'business_value',
                        'default_value': '产品的业务价值和目标',
                        'description': '业务价值'
                    }
                ]
            },
            {
                'name': '产品PRD文档生成器',
                'framework_type': 'RTGO',
                'description': '生成专业的产品需求文档(PRD)',
                'content': {
                    'role': '产品经理',
                    'task': '''根据提供的信息创建结构完整的产品需求文档：
1. 整理产品目标和背景
2. 定义用户需求和使用场景
3. 详细描述功能规格
4. 设计交互流程
5. 定义验收标准''',
                    'goal': '创建一份清晰、完整、易于理解的产品需求文档',
                    'output': '''输出标准PRD文档，包含：
1. 文档信息（版本、作者、日期等）
2. 产品概述和目标
3. 用户需求和场景
4. 功能需求详述
5. 非功能需求（性能、安全等）
6. UI/UX设计要求
7. 验收标准
8. 附录（术语表、参考资料等）'''
                },
                'variables': [
                    {
                        'name': 'product_name',
                        'default_value': '产品名称',
                        'description': '产品名称'
                    },
                    {
                        'name': 'product_description',
                        'default_value': '产品简要描述和目标',
                        'description': '产品描述'
                    },
                    {
                        'name': 'feature_requirements',
                        'default_value': '主要功能需求列表',
                        'description': '功能需求'
                    },
                    {
                        'name': 'target_users',
                        'default_value': '目标用户群体',
                        'description': '目标用户'
                    }
                ]
            },
            {
                'name': 'A/B测试方案设计',
                'framework_type': 'SPAR',
                'description': '设计产品功能的A/B测试方案',
                'content': {
                    'situation': '需要通过A/B测试验证产品功能或设计方案',
                    'purpose': '设计科学的A/B测试方案，获取数据支持决策',
                    'action': '''1. 明确测试目标和假设
2. 设计测试变量和控制变量
3. 确定样本大小和分组方法
4. 设定成功指标
5. 规划数据收集和分析方法''',
                    'result': '''输出完整的A/B测试方案：
1. 测试目标和假设
2. 测试设计（变量、样本、分组）
3. 成功指标定义
4. 数据收集计划
5. 分析方法
6. 实施时间表
7. 风险评估和缓解措施'''
                },
                'variables': [
                    {
                        'name': 'test_feature',
                        'default_value': '需要测试的功能或设计',
                        'description': '测试功能'
                    },
                    {
                        'name': 'hypothesis',
                        'default_value': '测试假设',
                        'description': '测试假设'
                    },
                    {
                        'name': 'success_metrics',
                        'default_value': '关键成功指标',
                        'description': '成功指标'
                    },
                    {
                        'name': 'user_segments',
                        'default_value': '目标用户群体',
                        'description': '用户群体'
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
                f'成功创建{created_count}个产品经理相关的提示词模板！'
            )
        )