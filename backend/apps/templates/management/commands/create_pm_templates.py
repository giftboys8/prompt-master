from django.core.management.base import BaseCommand
from frameworks.models import Framework
from apps.templates.models import Template

class Command(BaseCommand):
    help = '创建产品经理工作场景的提示词模版'

    def handle(self, *args, **options):
        # 获取RTGO框架
        rtgo_framework = Framework.objects.get(name='RTGO框架')

        # 产品经理模版列表
        pm_templates = [
            {
                'name': '用户需求分析与梳理',
                'description': '帮助产品经理分析和整理用户需求，输出结构化的需求文档。',
                'content': {
                    'role': '作为一名专业的需求分析师，你擅长系统性思维，具备优秀的需求分析、归纳和结构化表达能力。',
                    'task': '分析和整理用户反馈的需求信息，提取核心痛点，梳理需求优先级，输出结构化的需求文档。',
                    'goal': [
                        '清晰识别用户痛点和核心需求',
                        '对需求进行分类和优先级排序',
                        '提供可执行的需求解决方案建议'
                    ],
                    'output': '''请按以下格式输出分析结果：
1. 需求概述
   - 背景说明
   - 核心问题

2. 需求分类
   - 功能需求
   - 非功能需求
   - 用户体验需求

3. 优先级排序
   - P0（必须解决）
   - P1（重要）
   - P2（待考虑）

4. 解决方案建议
   - 短期解决方案
   - 长期优化建议

5. 风险评估
   - 技术风险
   - 业务风险
   - 用户体验风险'''
                },
                'framework': rtgo_framework,
                'visibility': 'PUBLIC',
                'target_role': '产品经理',
                'variables': []
            },
            {
                'name': '竞品分析报告',
                'description': '系统性分析竞品的功能特性、优劣势，输出详细的竞品分析报告。',
                'content': {
                    'role': '作为一名专业的竞品分析专家，你擅长市场洞察，具备敏锐的产品分析能力和战略思维。',
                    'task': '对目标竞品进行全方位分析，包括产品定位、功能特性、用户体验、商业模式等维度，输出详细的竞品分析报告。',
                    'goal': [
                        '全面了解竞品的产品策略和市场表现',
                        '识别竞品的优势和不足',
                        '提供有价值的产品优化建议'
                    ],
                    'output': '''请按以下格式输出分析报告：
1. 竞品概况
   - 产品定位
   - 目标用户
   - 核心价值主张

2. 功能分析
   - 核心功能清单
   - 差异化特性
   - 功能完整度评估

3. 用户体验分析
   - 产品界面设计
   - 交互流程
   - 用户反馈分析

4. 商业模式分析
   - 盈利模式
   - 获客策略
   - 用户留存策略

5. 竞争优势分析
   - 优势清单
   - 劣势清单
   - 市场机会

6. 建议与启示
   - 可借鉴的经验
   - 需要规避的问题
   - 产品优化建议'''
                },
                'framework': rtgo_framework,
                'visibility': 'PUBLIC',
                'target_role': '产品经理',
                'variables': []
            },
            {
                'name': '产品功能规划',
                'description': '帮助产品经理规划产品功能路线图，制定清晰的功能开发计划。',
                'content': {
                    'role': '作为一名资深的产品规划专家，你擅长产品战略规划，具备优秀的系统设计能力和项目管理经验。',
                    'task': '基于产品愿景和市场需求，规划产品功能路线图，制定阶段性的功能开发计划。',
                    'goal': [
                        '明确产品发展方向和阶段性目标',
                        '制定可执行的功能开发计划',
                        '平衡业务价值和开发资源'
                    ],
                    'output': '''请按以下格式输出规划方案：
1. 产品愿景
   - 核心价值主张
   - 目标用户群
   - 市场定位

2. 功能地图
   - 核心功能模块
   - 功能依赖关系
   - 创新特性

3. 开发路线图
   - 第一阶段（1-3个月）
   - 第二阶段（4-6个月）
   - 第三阶段（7-12个月）

4. 优先级策略
   - 优先级评估标准
   - 资源分配建议
   - 风险控制措施

5. 衡量指标
   - 功能完成度指标
   - 用户体验指标
   - 业务价值指标

6. 执行建议
   - 团队协作建议
   - 里程碑设定
   - 调整机制'''
                },
                'framework': rtgo_framework,
                'visibility': 'PUBLIC',
                'target_role': '产品经理',
                'variables': []
            },
            {
                'name': '产品PRD文档',
                'description': '生成标准的产品需求文档(PRD)，详细描述产品功能和交互细节。',
                'content': {
                    'role': '作为一名专业的产品文档撰写专家，你擅长清晰准确地描述产品需求，具备优秀的文档撰写能力。',
                    'task': '编写详细的产品需求文档(PRD)，包含产品功能描述、交互设计、业务规则等内容。',
                    'goal': [
                        '清晰描述产品功能需求和实现细节',
                        '确保文档的完整性和准确性',
                        '提供可执行的开发指导'
                    ],
                    'output': '''请按以下格式输出PRD文档：
1. 文档信息
   - 文档版本
   - 作者信息
   - 修订历史

2. 产品概述
   - 产品背景
   - 目标用户
   - 产品目标

3. 功能需求
   - 功能描述
   - 业务规则
   - 处理流程
   - 异常处理

4. 交互设计
   - 页面布局
   - 交互流程
   - 状态定义

5. 非功能需求
   - 性能需求
   - 安全需求
   - 兼容性要求

6. 技术要求
   - 系统依赖
   - 接口定义
   - 数据结构

7. 附录
   - 术语表
   - 参考文档
   - 相关资源'''
                },
                'framework': rtgo_framework,
                'visibility': 'PUBLIC',
                'target_role': '产品经理',
                'variables': []
            },
            {
                'name': '产品数据分析',
                'description': '帮助产品经理分析产品数据，发现问题并提供优化建议。',
                'content': {
                    'role': '作为一名专业的产品数据分析师，你擅长数据分析和洞察，具备优秀的数据解读能力和问题诊断能力。',
                    'task': '分析产品关键指标数据，识别问题和机会，提供数据驱动的优化建议。',
                    'goal': [
                        '全面分析产品核心指标表现',
                        '发现数据异常和优化机会',
                        '提供可执行的优化建议'
                    ],
                    'output': '''请按以下格式输出分析报告：
1. 数据概览
   - 分析周期
   - 关键指标总览
   - 数据来源说明

2. 用户增长分析
   - 新增用户分析
   - 用户留存分析
   - 用户活跃度分析

3. 功能使用分析
   - 功能使用频率
   - 用户行为路径
   - 转化漏斗分析

4. 问题诊断
   - 数据异常点
   - 性能瓶颈
   - 用户流失原因

5. 竞品对标
   - 核心指标对比
   - 差距分析
   - 优势分析

6. 优化建议
   - 短期优化方案
   - 长期改进建议
   - 预期效果评估

7. 监测计划
   - 关键指标设定
   - 监测频率
   - 预警机制'''
                },
                'framework': rtgo_framework,
                'visibility': 'PUBLIC',
                'target_role': '产品经理',
                'variables': []
            }
        ]

        # 创建模版
        for template_data in pm_templates:
            # 获取系统用户作为创建者
            from django.contrib.auth import get_user_model
            User = get_user_model()
            admin_user = User.objects.filter(is_superuser=True).first()
            
            if not admin_user:
                self.stdout.write(self.style.ERROR('No admin user found. Please create an admin user first.'))
                return
            
            template, created = Template.objects.get_or_create(
                name=template_data['name'],
                defaults={
                    'description': template_data['description'],
                    'content': template_data['content'],
                    'framework': template_data['framework'],
                    'framework_type': template_data['framework'].name,
                    'visibility': template_data['visibility'],
                    'target_role': template_data['target_role'],
                    'variables': template_data['variables'],
                    'created_by': admin_user
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created template: {template.name}')
                )
            else:
                template.description = template_data['description']
                template.content = template_data['content']
                template.framework = template_data['framework']
                template.framework_type = template_data['framework'].name
                template.visibility = template_data['visibility']
                template.target_role = template_data['target_role']
                template.variables = template_data['variables']
                template.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated template: {template.name}')
                )