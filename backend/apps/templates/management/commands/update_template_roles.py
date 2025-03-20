from django.core.management.base import BaseCommand
from apps.templates.models import Template

class Command(BaseCommand):
    help = '更新现有模板的使用角色字段'

    def handle(self, *args, **kwargs):
        # 定义模板角色映射
        role_mapping = {
            # 运维模板角色
            'Shell脚本分析优化助手': '运维工程师、系统管理员',
            '日志分析故障排查专家': '运维工程师、技术支持工程师',
            '系统性能分析与调优': '运维工程师、性能优化工程师',
            '系统配置审查与安全加固': '运维工程师、安全工程师',

            # 基础设施模板角色
            'Kubernetes故障诊断专家': '基础设施工程师、Kubernetes管理员',
            '网络配置与故障排查': '网络工程师、基础设施工程师',
            '数据库性能优化顾问': '数据库管理员、性能优化工程师',
            '负载均衡配置专家': '网络工程师、系统架构师',
            'Docker容器优化专家': '容器平台工程师、DevOps工程师',

            # SRE模板角色
            '分布式存储系统故障诊断': 'SRE、存储系统工程师',
            'SDN网络故障排查专家': 'SRE、网络工程师',
            'SLO/SLI设计与监控策略': 'SRE、监控平台工程师',
            '大规模基础设施自动化方案': 'SRE、自动化工程师',
            '高级容灾与业务连续性规划': 'SRE、灾备管理员',
            '可观测性系统设计专家': 'SRE、监控平台工程师',
            '高性能存储系统调优': 'SRE、存储系统工程师',
            '混合云网络架构设计': 'SRE、云平台架构师',
            '大规模系统容量规划': 'SRE、容量规划工程师',
            '自动化事件响应系统设计': 'SRE、运维开发工程师',

            # 故障排查模板角色
            '系统崩溃根因分析': '故障分析工程师、系统工程师',
            '网络连接问题排查': '网络工程师、故障分析工程师',
            '数据库性能问题诊断': '数据库管理员、性能工程师',
            '应用程序崩溃分析': '应用开发工程师、故障分析工程师',
            '安全漏洞事件分析': '安全工程师、事件响应工程师',
            '微服务故障链路追踪': '微服务开发工程师、SRE',

            # 产品运营模板角色
            '用户获取渠道策略分析师': '增长运营、渠道运营',
            '用户旅程优化专家': '产品运营、用户体验设计师',
            '用户留存策略设计师': '用户运营、产品运营',
            '用户行为数据分析师': '数据分析师、产品运营',
            '产品变现策略顾问': '商业化运营、产品经理',
            '用户激活策略设计师': '产品运营、用户增长专家',
            '用户增长实验设计师': '增长黑客、数据分析师',
            '产品运营数据仪表板设计师': '数据分析师、商业智能工程师',

            # 产品经理模板角色
            '文章写作助手': '内容运营、文案策划',
            '营销文案生成器': '市场营销、文案策划',
            '自定义提示词模板': '提示词工程师、AI应用开发者'
        }

        # 更新模板角色
        updated_count = 0
        for template in Template.objects.all():
            if template.name in role_mapping:
                template.target_role = role_mapping[template.name]
                template.save()
                updated_count += 1
                self.stdout.write(f'已更新模板 "{template.name}" 的角色为：{template.target_role}')
            else:
                self.stdout.write(self.style.WARNING(f'未找到模板 "{template.name}" 的角色映射'))

        self.stdout.write(
            self.style.SUCCESS(
                f'成功更新了 {updated_count} 个模板的使用角色！'
            )
        )