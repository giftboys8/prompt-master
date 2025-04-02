from django.core.management.base import BaseCommand
from apps.scenes.models import Scene, SceneTask

class Command(BaseCommand):
    help = '创建产品经理竞品分析相关的场景数据'

    def handle(self, *args, **options):
        # 创建竞品分析主场景
        competitive_analysis_scene = Scene.objects.create(
            name="竞品分析",
            category="PM",
            description="帮助产品经理进行全面的竞品分析，包括功能对比、优劣势分析、市场定位等多个维度",
            target_roles=["产品经理", "产品负责人", "市场分析师"],
            status=True,
            version="1.0"
        )

        # 创建相关的场景任务
        tasks = [
            {
                "name": "竞品功能对比分析",
                "description": "对标竞品的核心功能进行全面对比分析，找出差异点和改进空间",
                "prompt": """请根据以下维度对[竞品名称]进行功能对比分析：
1. 核心功能清单对比
2. 功能实现方式对比
3. 用户体验对比
4. 技术实现难度评估
5. 功能创新点分析
6. 改进建议

请提供详细的分析报告。""",
                "target_roles": ["产品经理", "产品负责人"]
            },
            {
                "name": "竞品优劣势分析",
                "description": "深入分析竞品的优势与劣势，为产品策略制定提供参考",
                "prompt": """请对[竞品名称]进行优劣势分析，包含以下方面：
1. 产品定位优劣势
2. 目标用户覆盖优劣势
3. 商业模式优劣势
4. 技术实现优劣势
5. 运营策略优劣势
6. 市场表现优劣势

请给出详细的分析报告和建议。""",
                "target_roles": ["产品经理", "产品负责人", "市场分析师"]
            },
            {
                "name": "竞品市场定位分析",
                "description": "分析竞品的市场定位、目标用户和商业模式",
                "prompt": """请对[竞品名称]的市场定位进行分析：
1. 目标市场分析
2. 目标用户画像
3. 价值主张分析
4. 商业模式分析
5. 市场占有率分析
6. 发展趋势预测

请提供完整的市场定位分析报告。""",
                "target_roles": ["产品经理", "市场分析师", "商业分析师"]
            },
            {
                "name": "竞品用户体验分析",
                "description": "从用户视角分析竞品的使用体验和交互设计",
                "prompt": """请对[竞品名称]的用户体验进行分析：
1. 产品界面设计评估
2. 功能操作流程评估
3. 用户反馈分析
4. 易用性测试结果
5. 用户痛点分析
6. 改进建议

请提供详细的用户体验分析报告。""",
                "target_roles": ["产品经理", "UX设计师", "用户研究员"]
            },
            {
                "name": "竞品技术架构分析",
                "description": "分析竞品的技术实现方案和系统架构",
                "prompt": """请对[竞品名称]的技术实现进行分析：
1. 技术栈选择分析
2. 系统架构评估
3. 性能表现分析
4. 安全性评估
5. 扩展性分析
6. 技术创新点分析

请提供完整的技术分析报告。""",
                "target_roles": ["产品经理", "技术负责人", "架构师"]
            }
        ]

        # 批量创建场景任务
        for task_data in tasks:
            SceneTask.objects.create(
                scene=competitive_analysis_scene,
                name=task_data["name"],
                description=task_data["description"]
            )

        self.stdout.write(self.style.SUCCESS('成功创建竞品分析相关场景数据'))