"""
02_document_prototype.py - 文档原型模式

办公文档系统示例
这个示例展示了如何使用原型模式来创建各种类型的办公文档。
在办公软件中，用户经常需要基于模板创建新文档，
原型模式可以提供预配置的文档模板，用户可以快速创建并自定义。
"""

import copy
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any


# ==================== 文档原型接口 ====================
class DocumentPrototype(ABC):
    """文档原型抽象基类"""
    
    @abstractmethod
    def clone(self):
        """克隆文档"""
        pass
    
    @abstractmethod
    def get_content(self) -> str:
        """获取文档内容"""
        pass
    
    @abstractmethod
    def set_title(self, title: str):
        """设置文档标题"""
        pass


# ==================== 具体文档类 ====================
class WordDocument(DocumentPrototype):
    """Word文档类"""
    
    def __init__(self, title: str = "新建文档"):
        self.title = title
        self.content = ""
        self.font_family = "宋体"
        self.font_size = 12
        self.margins = {"top": 2.5, "bottom": 2.5, "left": 3.0, "right": 3.0}
        self.headers = []
        self.footers = []
        self.styles = {
            "heading1": {"font_size": 18, "bold": True},
            "heading2": {"font_size": 16, "bold": True},
            "normal": {"font_size": 12, "bold": False}
        }
        self.created_time = datetime.now()
        self.last_modified = datetime.now()
    
    def clone(self):
        """克隆Word文档"""
        new_doc = copy.copy(self)
        # 深拷贝复杂的可变对象
        new_doc.margins = self.margins.copy()
        new_doc.headers = self.headers.copy()
        new_doc.footers = self.footers.copy()
        new_doc.styles = copy.deepcopy(self.styles)
        # 重置时间戳
        new_doc.created_time = datetime.now()
        new_doc.last_modified = datetime.now()
        return new_doc
    
    def set_title(self, title: str):
        """设置文档标题"""
        self.title = title
        self.last_modified = datetime.now()
    
    def add_content(self, content: str):
        """添加内容"""
        self.content += content
        self.last_modified = datetime.now()
    
    def set_font(self, family: str, size: int):
        """设置字体"""
        self.font_family = family
        self.font_size = size
        self.last_modified = datetime.now()
    
    def add_header(self, header_text: str):
        """添加页眉"""
        self.headers.append(header_text)
        self.last_modified = datetime.now()
    
    def add_footer(self, footer_text: str):
        """添加页脚"""
        self.footers.append(footer_text)
        self.last_modified = datetime.now()
    
    def get_content(self) -> str:
        """获取文档内容"""
        return (f"Word文档: {self.title}\n"
                f"创建时间: {self.created_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"修改时间: {self.last_modified.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"字体: {self.font_family} {self.font_size}pt\n"
                f"页边距: {self.margins}\n"
                f"页眉: {self.headers}\n"
                f"页脚: {self.footers}\n"
                f"内容: {self.content}")


class ExcelDocument(DocumentPrototype):
    """Excel文档类"""
    
    def __init__(self, title: str = "新建工作簿"):
        self.title = title
        self.worksheets = {"Sheet1": []}
        self.active_sheet = "Sheet1"
        self.formulas = {}
        self.charts = []
        self.cell_formats = {}
        self.created_time = datetime.now()
        self.last_modified = datetime.now()
    
    def clone(self):
        """克隆Excel文档"""
        new_doc = copy.copy(self)
        # 深拷贝复杂对象
        new_doc.worksheets = copy.deepcopy(self.worksheets)
        new_doc.formulas = self.formulas.copy()
        new_doc.charts = self.charts.copy()
        new_doc.cell_formats = copy.deepcopy(self.cell_formats)
        # 重置时间戳
        new_doc.created_time = datetime.now()
        new_doc.last_modified = datetime.now()
        return new_doc
    
    def set_title(self, title: str):
        """设置文档标题"""
        self.title = title
        self.last_modified = datetime.now()
    
    def add_worksheet(self, sheet_name: str):
        """添加工作表"""
        self.worksheets[sheet_name] = []
        self.last_modified = datetime.now()
    
    def set_cell_value(self, sheet: str, row: int, col: int, value: Any):
        """设置单元格值"""
        if sheet not in self.worksheets:
            self.add_worksheet(sheet)
        
        # 确保工作表有足够的行
        while len(self.worksheets[sheet]) <= row:
            self.worksheets[sheet].append([])
        
        # 确保行有足够的列
        while len(self.worksheets[sheet][row]) <= col:
            self.worksheets[sheet][row].append("")
        
        self.worksheets[sheet][row][col] = value
        self.last_modified = datetime.now()
    
    def add_formula(self, cell: str, formula: str):
        """添加公式"""
        self.formulas[cell] = formula
        self.last_modified = datetime.now()
    
    def get_content(self) -> str:
        """获取文档内容"""
        content = (f"Excel文档: {self.title}\n"
                  f"创建时间: {self.created_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"修改时间: {self.last_modified.strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"工作表数量: {len(self.worksheets)}\n"
                  f"公式数量: {len(self.formulas)}\n")
        
        for sheet_name, data in self.worksheets.items():
            content += f"工作表 '{sheet_name}': {len(data)} 行数据\n"
        
        return content


class PowerPointDocument(DocumentPrototype):
    """PowerPoint文档类"""
    
    def __init__(self, title: str = "新建演示文稿"):
        self.title = title
        self.slides = []
        self.theme = "默认主题"
        self.slide_size = "16:9"
        self.master_slides = []
        self.animations = []
        self.transitions = []
        self.created_time = datetime.now()
        self.last_modified = datetime.now()
    
    def clone(self):
        """克隆PowerPoint文档"""
        new_doc = copy.copy(self)
        # 深拷贝复杂对象
        new_doc.slides = copy.deepcopy(self.slides)
        new_doc.master_slides = copy.deepcopy(self.master_slides)
        new_doc.animations = self.animations.copy()
        new_doc.transitions = self.transitions.copy()
        # 重置时间戳
        new_doc.created_time = datetime.now()
        new_doc.last_modified = datetime.now()
        return new_doc
    
    def set_title(self, title: str):
        """设置文档标题"""
        self.title = title
        self.last_modified = datetime.now()
    
    def add_slide(self, slide_title: str, content: str = ""):
        """添加幻灯片"""
        slide = {
            "title": slide_title,
            "content": content,
            "layout": "标题和内容",
            "background": "白色"
        }
        self.slides.append(slide)
        self.last_modified = datetime.now()
    
    def set_theme(self, theme: str):
        """设置主题"""
        self.theme = theme
        self.last_modified = datetime.now()
    
    def add_animation(self, slide_index: int, animation_type: str):
        """添加动画"""
        animation = {
            "slide": slide_index,
            "type": animation_type,
            "duration": 1.0
        }
        self.animations.append(animation)
        self.last_modified = datetime.now()
    
    def get_content(self) -> str:
        """获取文档内容"""
        content = (f"PowerPoint文档: {self.title}\n"
                  f"创建时间: {self.created_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"修改时间: {self.last_modified.strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"主题: {self.theme}\n"
                  f"幻灯片尺寸: {self.slide_size}\n"
                  f"幻灯片数量: {len(self.slides)}\n"
                  f"动画数量: {len(self.animations)}\n")
        
        for i, slide in enumerate(self.slides):
            content += f"幻灯片 {i+1}: {slide['title']}\n"
        
        return content


# ==================== 文档模板管理器 ====================
class DocumentTemplateManager:
    """文档模板管理器"""
    
    def __init__(self):
        self._templates: Dict[str, DocumentPrototype] = {}
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """初始化默认模板"""
        # Word模板
        report_template = WordDocument("报告模板")
        report_template.add_content("这是一个报告模板...")
        report_template.add_header("公司报告")
        report_template.add_footer("第 1 页")
        report_template.set_font("微软雅黑", 14)
        
        letter_template = WordDocument("信函模板")
        letter_template.add_content("尊敬的先生/女士：\n\n")
        letter_template.set_font("宋体", 12)
        
        # Excel模板
        budget_template = ExcelDocument("预算表模板")
        budget_template.add_worksheet("收入")
        budget_template.add_worksheet("支出")
        budget_template.set_cell_value("收入", 0, 0, "项目")
        budget_template.set_cell_value("收入", 0, 1, "金额")
        
        # PowerPoint模板
        presentation_template = PowerPointDocument("演示模板")
        presentation_template.set_theme("商务主题")
        presentation_template.add_slide("欢迎", "欢迎参加本次演示")
        presentation_template.add_slide("议程", "今天的议程包括...")
        
        # 注册模板
        self.register_template("word_report", report_template)
        self.register_template("word_letter", letter_template)
        self.register_template("excel_budget", budget_template)
        self.register_template("ppt_presentation", presentation_template)
    
    def register_template(self, name: str, template: DocumentPrototype):
        """注册模板"""
        self._templates[name] = template
        print(f"模板管理器: 已注册模板 '{name}'")
    
    def create_document(self, template_name: str, title: str = None) -> DocumentPrototype:
        """基于模板创建文档"""
        if template_name not in self._templates:
            raise ValueError(f"未找到模板 '{template_name}'")
        
        # 克隆模板
        new_document = self._templates[template_name].clone()
        
        # 设置新标题
        if title:
            new_document.set_title(title)
        
        print(f"模板管理器: 基于 '{template_name}' 创建了文档")
        return new_document
    
    def list_templates(self) -> List[str]:
        """列出所有模板"""
        return list(self._templates.keys())


# ==================== 演示函数 ====================
def demonstrate_document_cloning():
    """演示文档克隆"""
    print("=" * 50)
    print("文档克隆演示")
    print("=" * 50)
    
    # 创建原始文档
    original_doc = WordDocument("原始报告")
    original_doc.add_content("这是原始报告的内容。")
    original_doc.add_header("重要报告")
    original_doc.set_font("微软雅黑", 14)
    
    print("原始文档:")
    print(original_doc.get_content())
    print()
    
    # 克隆文档
    cloned_doc = original_doc.clone()
    cloned_doc.set_title("克隆报告")
    cloned_doc.add_content("这是克隆文档的额外内容。")
    
    print("克隆文档:")
    print(cloned_doc.get_content())


def demonstrate_template_manager():
    """演示模板管理器"""
    print("\n" + "=" * 50)
    print("模板管理器演示")
    print("=" * 50)
    
    manager = DocumentTemplateManager()
    
    print("可用模板:")
    for template in manager.list_templates():
        print(f"- {template}")
    print()
    
    # 创建文档
    doc1 = manager.create_document("word_report", "月度销售报告")
    doc2 = manager.create_document("excel_budget", "2024年预算")
    doc3 = manager.create_document("ppt_presentation", "产品发布会")
    
    documents = [doc1, doc2, doc3]
    for i, doc in enumerate(documents, 1):
        print(f"文档 {i}:")
        print(doc.get_content())
        print("-" * 30)


def main():
    """主函数"""
    print("文档原型模式演示")
    
    demonstrate_document_cloning()
    demonstrate_template_manager()
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
