"""
03_document_builder.py - 文档建造者模式

文档生成系统示例
这个示例展示了如何使用建造者模式来构建复杂的文档结构。
在文档生成中，需要按照特定的层次结构来组织内容，
建造者模式可以帮助我们分步骤构建不同类型的文档。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


# ==================== 枚举类型 ====================
class DocumentType(Enum):
    """文档类型"""
    REPORT = "报告"
    MANUAL = "手册"
    PROPOSAL = "提案"
    SPECIFICATION = "规格说明"


class ContentType(Enum):
    """内容类型"""
    TEXT = "文本"
    IMAGE = "图片"
    TABLE = "表格"
    CODE = "代码"
    LIST = "列表"


# ==================== 文档元素类 ====================
class DocumentElement:
    """文档元素基类"""
    
    def __init__(self, content_type: ContentType, content: str):
        self.content_type = content_type
        self.content = content
        self.style = {}
        self.metadata = {}
    
    def set_style(self, key: str, value: str):
        """设置样式"""
        self.style[key] = value
    
    def set_metadata(self, key: str, value: Any):
        """设置元数据"""
        self.metadata[key] = value
    
    def render(self) -> str:
        """渲染元素"""
        return f"[{self.content_type.value}] {self.content}"


class Section:
    """文档章节"""
    
    def __init__(self, title: str, level: int = 1):
        self.title = title
        self.level = level
        self.elements = []
        self.subsections = []
        self.metadata = {}
    
    def add_element(self, element: DocumentElement):
        """添加元素"""
        self.elements.append(element)
    
    def add_subsection(self, subsection: 'Section'):
        """添加子章节"""
        self.subsections.append(subsection)
    
    def render(self, indent: int = 0) -> str:
        """渲染章节"""
        prefix = "  " * indent
        result = f"{prefix}{'#' * self.level} {self.title}\n"
        
        # 渲染元素
        for element in self.elements:
            result += f"{prefix}  {element.render()}\n"
        
        # 渲染子章节
        for subsection in self.subsections:
            result += subsection.render(indent + 1)
        
        return result


# ==================== 文档产品类 ====================
class Document:
    """文档产品类"""
    
    def __init__(self):
        self.title = ""
        self.author = ""
        self.version = "1.0"
        self.created_date = datetime.now()
        self.document_type = DocumentType.REPORT
        self.metadata = {}
        self.sections = []
        self.table_of_contents = []
        self.bibliography = []
        self.appendices = []
        self.header = ""
        self.footer = ""
        self.page_settings = {
            "page_size": "A4",
            "margins": {"top": 2.5, "bottom": 2.5, "left": 3.0, "right": 3.0},
            "font_family": "宋体",
            "font_size": 12
        }
    
    def add_section(self, section: Section):
        """添加章节"""
        self.sections.append(section)
    
    def add_bibliography_entry(self, entry: str):
        """添加参考文献"""
        self.bibliography.append(entry)
    
    def add_appendix(self, title: str, content: str):
        """添加附录"""
        self.appendices.append({"title": title, "content": content})
    
    def generate_table_of_contents(self):
        """生成目录"""
        self.table_of_contents = []
        for i, section in enumerate(self.sections, 1):
            self.table_of_contents.append(f"{i}. {section.title}")
            for j, subsection in enumerate(section.subsections, 1):
                self.table_of_contents.append(f"  {i}.{j} {subsection.title}")
    
    def get_word_count(self) -> int:
        """获取字数统计"""
        total_words = 0
        for section in self.sections:
            for element in section.elements:
                if element.content_type == ContentType.TEXT:
                    total_words += len(element.content.split())
        return total_words
    
    def render(self) -> str:
        """渲染完整文档"""
        result = []
        
        # 文档头部信息
        result.append("=" * 60)
        result.append(f"文档标题: {self.title}")
        result.append(f"作者: {self.author}")
        result.append(f"版本: {self.version}")
        result.append(f"创建日期: {self.created_date.strftime('%Y-%m-%d')}")
        result.append(f"文档类型: {self.document_type.value}")
        result.append(f"字数统计: {self.get_word_count()} 字")
        result.append("=" * 60)
        
        # 目录
        if self.table_of_contents:
            result.append("\n目录:")
            result.extend(self.table_of_contents)
            result.append("")
        
        # 正文章节
        for section in self.sections:
            result.append(section.render())
        
        # 参考文献
        if self.bibliography:
            result.append("\n参考文献:")
            for i, entry in enumerate(self.bibliography, 1):
                result.append(f"[{i}] {entry}")
            result.append("")
        
        # 附录
        if self.appendices:
            result.append("\n附录:")
            for i, appendix in enumerate(self.appendices, 1):
                result.append(f"附录 {i}: {appendix['title']}")
                result.append(appendix['content'])
                result.append("")
        
        return "\n".join(result)


# ==================== 抽象建造者 ====================
class DocumentBuilder(ABC):
    """文档建造者抽象基类"""
    
    def __init__(self):
        self.document = Document()
    
    @abstractmethod
    def set_document_info(self, title: str, author: str, doc_type: DocumentType):
        """设置文档基本信息"""
        pass
    
    @abstractmethod
    def add_title_page(self):
        """添加标题页"""
        pass
    
    @abstractmethod
    def add_abstract(self, content: str):
        """添加摘要"""
        pass
    
    @abstractmethod
    def add_introduction(self):
        """添加引言"""
        pass
    
    @abstractmethod
    def add_main_content(self):
        """添加主要内容"""
        pass
    
    @abstractmethod
    def add_conclusion(self):
        """添加结论"""
        pass
    
    def add_bibliography(self):
        """添加参考文献（可选）"""
        pass
    
    def add_appendices(self):
        """添加附录（可选）"""
        pass
    
    def get_document(self) -> Document:
        """获取构建的文档"""
        return self.document


# ==================== 具体建造者类 ====================
class TechnicalReportBuilder(DocumentBuilder):
    """技术报告建造者"""
    
    def set_document_info(self, title: str, author: str, doc_type: DocumentType = DocumentType.REPORT):
        """设置文档基本信息"""
        self.document.title = title
        self.document.author = author
        self.document.document_type = doc_type
        self.document.metadata["report_type"] = "技术报告"
    
    def add_title_page(self):
        """添加标题页"""
        title_section = Section("标题页", 0)
        title_element = DocumentElement(ContentType.TEXT, 
                                      f"{self.document.title}\n\n"
                                      f"作者: {self.document.author}\n"
                                      f"日期: {self.document.created_date.strftime('%Y年%m月%d日')}")
        title_section.add_element(title_element)
        self.document.add_section(title_section)
    
    def add_abstract(self, content: str):
        """添加摘要"""
        abstract_section = Section("摘要", 1)
        abstract_element = DocumentElement(ContentType.TEXT, content)
        abstract_section.add_element(abstract_element)
        self.document.add_section(abstract_section)
    
    def add_introduction(self):
        """添加引言"""
        intro_section = Section("1. 引言", 1)
        
        # 背景介绍
        background_subsection = Section("1.1 背景", 2)
        background_element = DocumentElement(ContentType.TEXT, 
                                           "本报告旨在分析当前技术发展趋势，为决策提供技术支持。")
        background_subsection.add_element(background_element)
        intro_section.add_subsection(background_subsection)
        
        # 目标说明
        objective_subsection = Section("1.2 目标", 2)
        objective_element = DocumentElement(ContentType.TEXT, 
                                          "通过深入分析，提出可行的技术解决方案。")
        objective_subsection.add_element(objective_element)
        intro_section.add_subsection(objective_subsection)
        
        self.document.add_section(intro_section)
    
    def add_main_content(self):
        """添加主要内容"""
        # 技术分析章节
        analysis_section = Section("2. 技术分析", 1)
        
        # 现状分析
        current_subsection = Section("2.1 现状分析", 2)
        current_element = DocumentElement(ContentType.TEXT, 
                                        "当前技术栈包括前端、后端和数据库等多个层面。")
        current_subsection.add_element(current_element)
        
        # 添加技术架构图
        diagram_element = DocumentElement(ContentType.IMAGE, 
                                        "技术架构图: [系统架构示意图]")
        current_subsection.add_element(diagram_element)
        
        analysis_section.add_subsection(current_subsection)
        
        # 性能评估
        performance_subsection = Section("2.2 性能评估", 2)
        
        # 添加性能数据表格
        table_element = DocumentElement(ContentType.TABLE, 
                                      "性能指标表:\n"
                                      "| 指标 | 当前值 | 目标值 |\n"
                                      "|------|--------|--------|\n"
                                      "| 响应时间 | 200ms | 100ms |\n"
                                      "| 吞吐量 | 1000/s | 2000/s |")
        performance_subsection.add_element(table_element)
        
        analysis_section.add_subsection(performance_subsection)
        self.document.add_section(analysis_section)
        
        # 解决方案章节
        solution_section = Section("3. 解决方案", 1)
        
        # 技术选型
        tech_subsection = Section("3.1 技术选型", 2)
        tech_element = DocumentElement(ContentType.TEXT, 
                                     "基于分析结果，推荐使用微服务架构和容器化部署。")
        tech_subsection.add_element(tech_element)
        
        # 实施计划
        plan_subsection = Section("3.2 实施计划", 2)
        plan_element = DocumentElement(ContentType.LIST, 
                                     "实施步骤:\n"
                                     "1. 环境准备\n"
                                     "2. 系统迁移\n"
                                     "3. 性能优化\n"
                                     "4. 测试验证")
        plan_subsection.add_element(plan_element)
        
        solution_section.add_subsection(tech_subsection)
        solution_section.add_subsection(plan_subsection)
        self.document.add_section(solution_section)
    
    def add_conclusion(self):
        """添加结论"""
        conclusion_section = Section("4. 结论", 1)
        conclusion_element = DocumentElement(ContentType.TEXT, 
                                           "通过本次技术分析，我们确定了优化方向和实施路径。"
                                           "预期能够显著提升系统性能和用户体验。")
        conclusion_section.add_element(conclusion_element)
        self.document.add_section(conclusion_section)
    
    def add_bibliography(self):
        """添加参考文献"""
        self.document.add_bibliography_entry("《软件架构设计》, 张三, 2023")
        self.document.add_bibliography_entry("《微服务实战》, 李四, 2022")
        self.document.add_bibliography_entry("《性能优化指南》, 王五, 2023")
    
    def add_appendices(self):
        """添加附录"""
        self.document.add_appendix("A", "详细配置文件示例")
        self.document.add_appendix("B", "性能测试数据")


class UserManualBuilder(DocumentBuilder):
    """用户手册建造者"""
    
    def set_document_info(self, title: str, author: str, doc_type: DocumentType = DocumentType.MANUAL):
        """设置文档基本信息"""
        self.document.title = title
        self.document.author = author
        self.document.document_type = doc_type
        self.document.metadata["manual_type"] = "用户手册"
    
    def add_title_page(self):
        """添加标题页"""
        title_section = Section("用户手册封面", 0)
        title_element = DocumentElement(ContentType.TEXT, 
                                      f"{self.document.title}\n\n"
                                      f"版本: {self.document.version}\n"
                                      f"发布日期: {self.document.created_date.strftime('%Y年%m月%d日')}")
        title_section.add_element(title_element)
        self.document.add_section(title_section)
    
    def add_abstract(self, content: str):
        """添加概述"""
        overview_section = Section("产品概述", 1)
        overview_element = DocumentElement(ContentType.TEXT, content)
        overview_section.add_element(overview_element)
        self.document.add_section(overview_section)
    
    def add_introduction(self):
        """添加快速入门"""
        intro_section = Section("1. 快速入门", 1)
        
        # 系统要求
        requirements_subsection = Section("1.1 系统要求", 2)
        requirements_element = DocumentElement(ContentType.LIST, 
                                             "系统要求:\n"
                                             "• 操作系统: Windows 10 或更高版本\n"
                                             "• 内存: 4GB RAM 或更多\n"
                                             "• 硬盘空间: 2GB 可用空间")
        requirements_subsection.add_element(requirements_element)
        intro_section.add_subsection(requirements_subsection)
        
        # 安装指南
        install_subsection = Section("1.2 安装指南", 2)
        install_element = DocumentElement(ContentType.TEXT, 
                                        "请按照以下步骤进行安装...")
        install_subsection.add_element(install_element)
        intro_section.add_subsection(install_subsection)
        
        self.document.add_section(intro_section)
    
    def add_main_content(self):
        """添加功能说明"""
        # 基本功能
        basic_section = Section("2. 基本功能", 1)
        
        login_subsection = Section("2.1 登录系统", 2)
        login_element = DocumentElement(ContentType.TEXT, 
                                      "在登录页面输入用户名和密码，点击登录按钮。")
        login_subsection.add_element(login_element)
        
        # 添加截图说明
        screenshot_element = DocumentElement(ContentType.IMAGE, 
                                           "登录界面截图: [登录页面示例]")
        login_subsection.add_element(screenshot_element)
        
        basic_section.add_subsection(login_subsection)
        self.document.add_section(basic_section)
        
        # 高级功能
        advanced_section = Section("3. 高级功能", 1)
        
        config_subsection = Section("3.1 系统配置", 2)
        config_element = DocumentElement(ContentType.TEXT, 
                                       "在设置页面可以配置系统参数...")
        config_subsection.add_element(config_element)
        
        advanced_section.add_subsection(config_subsection)
        self.document.add_section(advanced_section)
    
    def add_conclusion(self):
        """添加常见问题"""
        faq_section = Section("4. 常见问题", 1)
        
        faq_element = DocumentElement(ContentType.TEXT, 
                                    "Q: 忘记密码怎么办？\n"
                                    "A: 请联系系统管理员重置密码。\n\n"
                                    "Q: 系统运行缓慢怎么办？\n"
                                    "A: 请检查网络连接和系统资源使用情况。")
        faq_section.add_element(faq_element)
        self.document.add_section(faq_section)


# ==================== 指挥者类 ====================
class DocumentDirector:
    """文档构建指挥者"""
    
    def __init__(self, builder: DocumentBuilder):
        self.builder = builder
    
    def build_complete_document(self, title: str, author: str, abstract: str) -> Document:
        """构建完整文档"""
        print(f"开始构建文档: {title}")
        
        # 设置基本信息
        self.builder.set_document_info(title, author, DocumentType.REPORT)
        
        # 构建文档结构
        self.builder.add_title_page()
        self.builder.add_abstract(abstract)
        self.builder.add_introduction()
        self.builder.add_main_content()
        self.builder.add_conclusion()
        self.builder.add_bibliography()
        self.builder.add_appendices()
        
        # 生成目录
        document = self.builder.get_document()
        document.generate_table_of_contents()
        
        print("文档构建完成！")
        return document
    
    def build_simple_document(self, title: str, author: str) -> Document:
        """构建简单文档"""
        print(f"开始构建简单文档: {title}")
        
        self.builder.set_document_info(title, author, DocumentType.REPORT)
        self.builder.add_title_page()
        self.builder.add_introduction()
        self.builder.add_main_content()
        self.builder.add_conclusion()
        
        document = self.builder.get_document()
        document.generate_table_of_contents()
        
        print("简单文档构建完成！")
        return document


# ==================== 演示函数 ====================
def demonstrate_technical_report():
    """演示技术报告构建"""
    print("=" * 60)
    print("技术报告构建演示")
    print("=" * 60)
    
    # 构建技术报告
    report_builder = TechnicalReportBuilder()
    director = DocumentDirector(report_builder)
    
    abstract = ("本报告分析了当前系统的技术架构，识别了性能瓶颈，"
               "并提出了基于微服务架构的优化方案。")
    
    report = director.build_complete_document(
        "系统性能优化技术报告",
        "技术团队",
        abstract
    )
    
    print("\n生成的技术报告:")
    print(report.render())


def demonstrate_user_manual():
    """演示用户手册构建"""
    print("\n" + "=" * 60)
    print("用户手册构建演示")
    print("=" * 60)
    
    # 构建用户手册
    manual_builder = UserManualBuilder()
    director = DocumentDirector(manual_builder)
    
    overview = ("本产品是一个企业级管理系统，"
               "提供用户管理、数据分析和报表生成等功能。")
    
    manual = director.build_complete_document(
        "企业管理系统用户手册",
        "产品团队",
        overview
    )
    
    print("\n生成的用户手册:")
    print(manual.render())


def main():
    """主函数"""
    print("文档建造者模式演示")
    
    demonstrate_technical_report()
    demonstrate_user_manual()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
