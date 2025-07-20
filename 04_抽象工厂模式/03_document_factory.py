"""
03_document_factory.py - 文档生成抽象工厂模式

文档导出系统示例
这个示例展示了如何使用抽象工厂模式来创建不同格式的文档组件。
在文档处理系统中，经常需要支持多种格式（如PDF、Word、HTML），
抽象工厂模式可以确保同一格式的所有组件协同工作。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


# ==================== 抽象产品类 ====================
class DocumentHeader(ABC):
    """文档头部抽象基类"""
    
    @abstractmethod
    def create_title(self, title: str) -> str:
        """创建标题"""
        pass
    
    @abstractmethod
    def create_metadata(self, author: str, date: str) -> str:
        """创建元数据"""
        pass


class DocumentBody(ABC):
    """文档正文抽象基类"""
    
    @abstractmethod
    def create_paragraph(self, text: str) -> str:
        """创建段落"""
        pass
    
    @abstractmethod
    def create_heading(self, text: str, level: int) -> str:
        """创建标题"""
        pass
    
    @abstractmethod
    def create_list(self, items: List[str], ordered: bool = False) -> str:
        """创建列表"""
        pass
    
    @abstractmethod
    def create_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """创建表格"""
        pass


class DocumentFooter(ABC):
    """文档尾部抽象基类"""
    
    @abstractmethod
    def create_page_number(self, page: int, total: int) -> str:
        """创建页码"""
        pass
    
    @abstractmethod
    def create_signature(self, signature: str) -> str:
        """创建签名"""
        pass


# ==================== PDF产品族 ====================
class PDFHeader(DocumentHeader):
    """PDF文档头部"""
    
    def create_title(self, title: str) -> str:
        """创建PDF标题"""
        return f"<pdf:title font-size='24' font-weight='bold'>{title}</pdf:title>"
    
    def create_metadata(self, author: str, date: str) -> str:
        """创建PDF元数据"""
        return f"<pdf:metadata author='{author}' created='{date}' format='PDF/A-1b'/>"


class PDFBody(DocumentBody):
    """PDF文档正文"""
    
    def create_paragraph(self, text: str) -> str:
        """创建PDF段落"""
        return f"<pdf:paragraph font-family='Arial' font-size='12'>{text}</pdf:paragraph>"
    
    def create_heading(self, text: str, level: int) -> str:
        """创建PDF标题"""
        font_size = 20 - (level - 1) * 2
        return f"<pdf:heading level='{level}' font-size='{font_size}' font-weight='bold'>{text}</pdf:heading>"
    
    def create_list(self, items: List[str], ordered: bool = False) -> str:
        """创建PDF列表"""
        list_type = "ordered" if ordered else "unordered"
        list_items = "".join([f"<pdf:list-item>{item}</pdf:list-item>" for item in items])
        return f"<pdf:list type='{list_type}'>{list_items}</pdf:list>"
    
    def create_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """创建PDF表格"""
        header_cells = "".join([f"<pdf:th>{header}</pdf:th>" for header in headers])
        header_row = f"<pdf:tr>{header_cells}</pdf:tr>"
        
        data_rows = []
        for row in rows:
            cells = "".join([f"<pdf:td>{cell}</pdf:td>" for cell in row])
            data_rows.append(f"<pdf:tr>{cells}</pdf:tr>")
        
        return f"<pdf:table border='1'>{header_row}{''.join(data_rows)}</pdf:table>"


class PDFFooter(DocumentFooter):
    """PDF文档尾部"""
    
    def create_page_number(self, page: int, total: int) -> str:
        """创建PDF页码"""
        return f"<pdf:page-number position='bottom-center'>第 {page} 页，共 {total} 页</pdf:page-number>"
    
    def create_signature(self, signature: str) -> str:
        """创建PDF签名"""
        return f"<pdf:signature position='bottom-right'>{signature}</pdf:signature>"


# ==================== Word产品族 ====================
class WordHeader(DocumentHeader):
    """Word文档头部"""
    
    def create_title(self, title: str) -> str:
        """创建Word标题"""
        return f"<w:p><w:pPr><w:jc w:val='center'/></w:pPr><w:r><w:rPr><w:sz w:val='48'/><w:b/></w:rPr><w:t>{title}</w:t></w:r></w:p>"
    
    def create_metadata(self, author: str, date: str) -> str:
        """创建Word元数据"""
        return f"<w:docProps><w:author>{author}</w:author><w:created>{date}</w:created></w:docProps>"


class WordBody(DocumentBody):
    """Word文档正文"""
    
    def create_paragraph(self, text: str) -> str:
        """创建Word段落"""
        return f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>"
    
    def create_heading(self, text: str, level: int) -> str:
        """创建Word标题"""
        style = f"Heading{level}"
        return f"<w:p><w:pPr><w:pStyle w:val='{style}'/></w:pPr><w:r><w:t>{text}</w:t></w:r></w:p>"
    
    def create_list(self, items: List[str], ordered: bool = False) -> str:
        """创建Word列表"""
        list_type = "decimal" if ordered else "bullet"
        list_items = []
        for item in items:
            list_items.append(f"<w:p><w:pPr><w:numPr><w:numId w:val='1'/></w:pPr></w:pPr><w:r><w:t>{item}</w:t></w:r></w:p>")
        return "".join(list_items)
    
    def create_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """创建Word表格"""
        header_cells = "".join([f"<w:tc><w:p><w:r><w:rPr><w:b/></w:rPr><w:t>{header}</w:t></w:r></w:p></w:tc>" for header in headers])
        header_row = f"<w:tr>{header_cells}</w:tr>"
        
        data_rows = []
        for row in rows:
            cells = "".join([f"<w:tc><w:p><w:r><w:t>{cell}</w:t></w:r></w:p></w:tc>" for cell in row])
            data_rows.append(f"<w:tr>{cells}</w:tr>")
        
        return f"<w:tbl><w:tblPr><w:tblBorders/></w:tblPr>{header_row}{''.join(data_rows)}</w:tbl>"


class WordFooter(DocumentFooter):
    """Word文档尾部"""
    
    def create_page_number(self, page: int, total: int) -> str:
        """创建Word页码"""
        return f"<w:ftr><w:p><w:pPr><w:jc w:val='center'/></w:pPr><w:r><w:t>第 {page} 页，共 {total} 页</w:t></w:r></w:p></w:ftr>"
    
    def create_signature(self, signature: str) -> str:
        """创建Word签名"""
        return f"<w:p><w:pPr><w:jc w:val='right'/></w:pPr><w:r><w:t>{signature}</w:t></w:r></w:p>"


# ==================== HTML产品族 ====================
class HTMLHeader(DocumentHeader):
    """HTML文档头部"""
    
    def create_title(self, title: str) -> str:
        """创建HTML标题"""
        return f"<h1 style='text-align: center; font-size: 24px; font-weight: bold;'>{title}</h1>"
    
    def create_metadata(self, author: str, date: str) -> str:
        """创建HTML元数据"""
        return f"<meta name='author' content='{author}'><meta name='date' content='{date}'>"


class HTMLBody(DocumentBody):
    """HTML文档正文"""
    
    def create_paragraph(self, text: str) -> str:
        """创建HTML段落"""
        return f"<p style='font-family: Arial; font-size: 12px;'>{text}</p>"
    
    def create_heading(self, text: str, level: int) -> str:
        """创建HTML标题"""
        return f"<h{level}>{text}</h{level}>"
    
    def create_list(self, items: List[str], ordered: bool = False) -> str:
        """创建HTML列表"""
        tag = "ol" if ordered else "ul"
        list_items = "".join([f"<li>{item}</li>" for item in items])
        return f"<{tag}>{list_items}</{tag}>"
    
    def create_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """创建HTML表格"""
        header_cells = "".join([f"<th style='border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;'>{header}</th>" for header in headers])
        header_row = f"<tr>{header_cells}</tr>"
        
        data_rows = []
        for row in rows:
            cells = "".join([f"<td style='border: 1px solid #ddd; padding: 8px;'>{cell}</td>" for cell in row])
            data_rows.append(f"<tr>{cells}</tr>")
        
        return f"<table style='border-collapse: collapse; width: 100%;'>{header_row}{''.join(data_rows)}</table>"


class HTMLFooter(DocumentFooter):
    """HTML文档尾部"""
    
    def create_page_number(self, page: int, total: int) -> str:
        """创建HTML页码"""
        return f"<div style='text-align: center; margin-top: 20px;'>第 {page} 页，共 {total} 页</div>"
    
    def create_signature(self, signature: str) -> str:
        """创建HTML签名"""
        return f"<div style='text-align: right; margin-top: 20px;'>{signature}</div>"


# ==================== 抽象工厂类 ====================
class DocumentFactory(ABC):
    """文档抽象工厂"""
    
    @abstractmethod
    def create_header(self) -> DocumentHeader:
        """创建文档头部"""
        pass
    
    @abstractmethod
    def create_body(self) -> DocumentBody:
        """创建文档正文"""
        pass
    
    @abstractmethod
    def create_footer(self) -> DocumentFooter:
        """创建文档尾部"""
        pass


# ==================== 具体工厂类 ====================
class PDFFactory(DocumentFactory):
    """PDF文档工厂"""
    
    def create_header(self) -> DocumentHeader:
        """创建PDF头部"""
        return PDFHeader()
    
    def create_body(self) -> DocumentBody:
        """创建PDF正文"""
        return PDFBody()
    
    def create_footer(self) -> DocumentFooter:
        """创建PDF尾部"""
        return PDFFooter()


class WordFactory(DocumentFactory):
    """Word文档工厂"""
    
    def create_header(self) -> DocumentHeader:
        """创建Word头部"""
        return WordHeader()
    
    def create_body(self) -> DocumentBody:
        """创建Word正文"""
        return WordBody()
    
    def create_footer(self) -> DocumentFooter:
        """创建Word尾部"""
        return WordFooter()


class HTMLFactory(DocumentFactory):
    """HTML文档工厂"""
    
    def create_header(self) -> DocumentHeader:
        """创建HTML头部"""
        return HTMLHeader()
    
    def create_body(self) -> DocumentBody:
        """创建HTML正文"""
        return HTMLBody()
    
    def create_footer(self) -> DocumentFooter:
        """创建HTML尾部"""
        return HTMLFooter()


# ==================== 文档生成器 ====================
class DocumentGenerator:
    """文档生成器"""
    
    def __init__(self, factory: DocumentFactory):
        self.factory = factory
        self.header = factory.create_header()
        self.body = factory.create_body()
        self.footer = factory.create_footer()
    
    def generate_report(self, title: str, author: str, data: Dict[str, Any]) -> str:
        """生成报告文档"""
        content = []
        
        # 创建头部
        content.append(self.header.create_title(title))
        content.append(self.header.create_metadata(author, datetime.now().strftime("%Y-%m-%d")))
        
        # 创建正文
        content.append(self.body.create_heading("概述", 2))
        content.append(self.body.create_paragraph(data.get("summary", "这是一份示例报告。")))
        
        content.append(self.body.create_heading("详细信息", 2))
        if "details" in data:
            for detail in data["details"]:
                content.append(self.body.create_paragraph(detail))
        
        # 创建数据表格
        if "table_data" in data:
            table_data = data["table_data"]
            content.append(self.body.create_heading("数据表格", 2))
            content.append(self.body.create_table(
                table_data["headers"],
                table_data["rows"]
            ))
        
        # 创建列表
        if "list_items" in data:
            content.append(self.body.create_heading("要点列表", 2))
            content.append(self.body.create_list(data["list_items"], ordered=True))
        
        # 创建尾部
        content.append(self.footer.create_page_number(1, 1))
        content.append(self.footer.create_signature(f"生成者: {author}"))
        
        return "\n".join(content)


# ==================== 演示函数 ====================
def demonstrate_pdf_generation():
    """演示PDF文档生成"""
    print("=" * 60)
    print("PDF文档生成演示")
    print("=" * 60)
    
    # 创建PDF工厂
    pdf_factory = PDFFactory()
    
    # 创建文档生成器
    generator = DocumentGenerator(pdf_factory)
    
    # 准备数据
    data = {
        "summary": "这是一份关于销售业绩的季度报告，展示了各个部门的表现情况。",
        "details": [
            "本季度总销售额达到了预期目标的120%。",
            "客户满意度调查显示，满意度达到了95%。",
            "新产品线的推出获得了市场的积极响应。"
        ],
        "table_data": {
            "headers": ["部门", "销售额", "增长率"],
            "rows": [
                ["销售部", "¥1,200,000", "15%"],
                ["市场部", "¥800,000", "8%"],
                ["技术部", "¥600,000", "25%"]
            ]
        },
        "list_items": [
            "继续加强客户关系管理",
            "扩大新产品的市场推广",
            "优化内部流程提高效率",
            "加强团队培训和发展"
        ]
    }
    
    # 生成PDF文档
    pdf_content = generator.generate_report("季度销售报告", "张经理", data)
    print("生成的PDF文档内容:")
    print(pdf_content)


def demonstrate_html_generation():
    """演示HTML文档生成"""
    print("\n" + "=" * 60)
    print("HTML文档生成演示")
    print("=" * 60)
    
    # 创建HTML工厂
    html_factory = HTMLFactory()
    
    # 创建文档生成器
    generator = DocumentGenerator(html_factory)
    
    # 准备数据
    data = {
        "summary": "这是一份技术文档，介绍了新系统的架构和功能特性。",
        "details": [
            "系统采用微服务架构，具有良好的可扩展性。",
            "前端使用React框架，提供了良好的用户体验。",
            "后端使用Spring Boot，确保了系统的稳定性。"
        ],
        "table_data": {
            "headers": ["组件", "技术栈", "状态"],
            "rows": [
                ["前端", "React + TypeScript", "已完成"],
                ["后端", "Spring Boot + MySQL", "开发中"],
                ["部署", "Docker + Kubernetes", "计划中"]
            ]
        },
        "list_items": [
            "完成用户认证模块",
            "实现数据同步功能",
            "优化系统性能",
            "编写用户手册"
        ]
    }
    
    # 生成HTML文档
    html_content = generator.generate_report("系统技术文档", "李工程师", data)
    print("生成的HTML文档内容:")
    print(html_content)


def main():
    """主函数"""
    print("抽象工厂模式演示 - 文档生成系统")
    
    demonstrate_pdf_generation()
    demonstrate_html_generation()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
