"""
01_basic_visitor.py - 访问者模式基础实现

这个示例展示了访问者模式的核心概念：
- 双分派机制的实现
- 访问者与元素的分离
- 在不修改元素类的情况下添加新操作
"""

from abc import ABC, abstractmethod
from typing import List


# ==================== 抽象访问者 ====================
class DocumentVisitor(ABC):
    """文档访问者抽象类"""
    
    @abstractmethod
    def visit_paragraph(self, paragraph):
        """访问段落元素"""
        pass
    
    @abstractmethod
    def visit_image(self, image):
        """访问图片元素"""
        pass
    
    @abstractmethod
    def visit_table(self, table):
        """访问表格元素"""
        pass
    
    @abstractmethod
    def visit_list(self, list_element):
        """访问列表元素"""
        pass


# ==================== 抽象文档元素 ====================
class DocumentElement(ABC):
    """文档元素抽象类"""
    
    @abstractmethod
    def accept(self, visitor: DocumentVisitor):
        """接受访问者"""
        pass


# ==================== 具体文档元素 ====================
class Paragraph(DocumentElement):
    """段落元素"""
    
    def __init__(self, text: str, font_size: int = 12):
        self.text = text
        self.font_size = font_size
        self.word_count = len(text.split())
    
    def accept(self, visitor: DocumentVisitor):
        """接受访问者 - 这里体现了双分派"""
        visitor.visit_paragraph(self)
    
    def __str__(self):
        return f"段落(字数: {self.word_count})"


class Image(DocumentElement):
    """图片元素"""
    
    def __init__(self, src: str, width: int, height: int, alt_text: str = ""):
        self.src = src
        self.width = width
        self.height = height
        self.alt_text = alt_text
        self.file_size = width * height * 3  # 模拟文件大小
    
    def accept(self, visitor: DocumentVisitor):
        visitor.visit_image(self)
    
    def __str__(self):
        return f"图片({self.width}x{self.height})"


class Table(DocumentElement):
    """表格元素"""
    
    def __init__(self, rows: int, cols: int, has_header: bool = True):
        self.rows = rows
        self.cols = cols
        self.has_header = has_header
        self.cell_count = rows * cols
    
    def accept(self, visitor: DocumentVisitor):
        visitor.visit_table(self)
    
    def __str__(self):
        return f"表格({self.rows}x{self.cols})"


class ListElement(DocumentElement):
    """列表元素"""
    
    def __init__(self, items: List[str], is_ordered: bool = False):
        self.items = items
        self.is_ordered = is_ordered
        self.item_count = len(items)
    
    def accept(self, visitor: DocumentVisitor):
        visitor.visit_list(self)
    
    def __str__(self):
        list_type = "有序列表" if self.is_ordered else "无序列表"
        return f"{list_type}({self.item_count}项)"


# ==================== 具体访问者 ====================
class HTMLExporter(DocumentVisitor):
    """HTML导出访问者"""
    
    def __init__(self):
        self.html_content = []
        self.element_count = 0
    
    def visit_paragraph(self, paragraph: Paragraph):
        """导出段落为HTML"""
        style = f"font-size: {paragraph.font_size}px;"
        html = f'<p style="{style}">{paragraph.text}</p>'
        self.html_content.append(html)
        self.element_count += 1
        print(f"📝 导出段落: {paragraph.word_count} 个字")
    
    def visit_image(self, image: Image):
        """导出图片为HTML"""
        html = (f'<img src="{image.src}" '
                f'width="{image.width}" height="{image.height}" '
                f'alt="{image.alt_text}">')
        self.html_content.append(html)
        self.element_count += 1
        print(f"🖼️  导出图片: {image.src}")
    
    def visit_table(self, table: Table):
        """导出表格为HTML"""
        html = f'<table border="1">'
        if table.has_header:
            html += '<thead><tr>' + '<th>Header</th>' * table.cols + '</tr></thead>'
        html += '<tbody>'
        for i in range(table.rows - (1 if table.has_header else 0)):
            html += '<tr>' + '<td>Data</td>' * table.cols + '</tr>'
        html += '</tbody></table>'
        self.html_content.append(html)
        self.element_count += 1
        print(f"📊 导出表格: {table.rows}x{table.cols}")
    
    def visit_list(self, list_element: ListElement):
        """导出列表为HTML"""
        tag = 'ol' if list_element.is_ordered else 'ul'
        html = f'<{tag}>'
        for item in list_element.items:
            html += f'<li>{item}</li>'
        html += f'</{tag}>'
        self.html_content.append(html)
        self.element_count += 1
        print(f"📋 导出列表: {list_element.item_count} 项")
    
    def get_html(self) -> str:
        """获取完整的HTML内容"""
        return '\n'.join(self.html_content)
    
    def get_summary(self) -> str:
        """获取导出摘要"""
        return f"HTML导出完成: {self.element_count} 个元素"


class StatisticsCollector(DocumentVisitor):
    """统计信息收集访问者"""
    
    def __init__(self):
        self.paragraph_count = 0
        self.image_count = 0
        self.table_count = 0
        self.list_count = 0
        self.total_words = 0
        self.total_images_size = 0
        self.total_table_cells = 0
        self.total_list_items = 0
    
    def visit_paragraph(self, paragraph: Paragraph):
        """统计段落信息"""
        self.paragraph_count += 1
        self.total_words += paragraph.word_count
        print(f"📊 统计段落: +{paragraph.word_count} 字")
    
    def visit_image(self, image: Image):
        """统计图片信息"""
        self.image_count += 1
        self.total_images_size += image.file_size
        print(f"📊 统计图片: +{image.file_size} bytes")
    
    def visit_table(self, table: Table):
        """统计表格信息"""
        self.table_count += 1
        self.total_table_cells += table.cell_count
        print(f"📊 统计表格: +{table.cell_count} 个单元格")
    
    def visit_list(self, list_element: ListElement):
        """统计列表信息"""
        self.list_count += 1
        self.total_list_items += list_element.item_count
        print(f"📊 统计列表: +{list_element.item_count} 项")
    
    def get_statistics(self) -> str:
        """获取统计报告"""
        return f"""
文档统计报告:
- 段落: {self.paragraph_count} 个 (总字数: {self.total_words})
- 图片: {self.image_count} 个 (总大小: {self.total_images_size:,} bytes)
- 表格: {self.table_count} 个 (总单元格: {self.total_table_cells})
- 列表: {self.list_count} 个 (总列表项: {self.total_list_items})
- 总元素数: {self.paragraph_count + self.image_count + self.table_count + self.list_count}
        """.strip()


class MarkdownExporter(DocumentVisitor):
    """Markdown导出访问者"""
    
    def __init__(self):
        self.markdown_content = []
        self.element_count = 0
    
    def visit_paragraph(self, paragraph: Paragraph):
        """导出段落为Markdown"""
        self.markdown_content.append(paragraph.text)
        self.markdown_content.append("")  # 空行
        self.element_count += 1
        print(f"📝 Markdown段落: {paragraph.word_count} 字")
    
    def visit_image(self, image: Image):
        """导出图片为Markdown"""
        markdown = f"![{image.alt_text}]({image.src})"
        self.markdown_content.append(markdown)
        self.markdown_content.append("")
        self.element_count += 1
        print(f"🖼️  Markdown图片: {image.src}")
    
    def visit_table(self, table: Table):
        """导出表格为Markdown"""
        # 简化的Markdown表格
        header = "| " + " | ".join([f"列{i+1}" for i in range(table.cols)]) + " |"
        separator = "| " + " | ".join(["---" for _ in range(table.cols)]) + " |"
        self.markdown_content.append(header)
        self.markdown_content.append(separator)
        
        for i in range(table.rows - (1 if table.has_header else 0)):
            row = "| " + " | ".join([f"数据{i+1}-{j+1}" for j in range(table.cols)]) + " |"
            self.markdown_content.append(row)
        
        self.markdown_content.append("")
        self.element_count += 1
        print(f"📊 Markdown表格: {table.rows}x{table.cols}")
    
    def visit_list(self, list_element: ListElement):
        """导出列表为Markdown"""
        for i, item in enumerate(list_element.items, 1):
            if list_element.is_ordered:
                self.markdown_content.append(f"{i}. {item}")
            else:
                self.markdown_content.append(f"- {item}")
        self.markdown_content.append("")
        self.element_count += 1
        print(f"📋 Markdown列表: {list_element.item_count} 项")
    
    def get_markdown(self) -> str:
        """获取完整的Markdown内容"""
        return '\n'.join(self.markdown_content)
    
    def get_summary(self) -> str:
        """获取导出摘要"""
        return f"Markdown导出完成: {self.element_count} 个元素"


# ==================== 文档类 ====================
class Document:
    """文档类 - 包含多个文档元素"""
    
    def __init__(self, title: str):
        self.title = title
        self.elements: List[DocumentElement] = []
    
    def add_element(self, element: DocumentElement):
        """添加文档元素"""
        self.elements.append(element)
        print(f"➕ 添加元素: {element}")
    
    def accept(self, visitor: DocumentVisitor):
        """让访问者访问所有元素"""
        print(f"\n🔍 {type(visitor).__name__} 开始处理文档: {self.title}")
        print("-" * 50)
        
        for element in self.elements:
            element.accept(visitor)
        
        print("-" * 50)


# ==================== 演示函数 ====================
def demo_basic_visitor():
    """基础访问者模式演示"""
    print("=" * 60)
    print("📚 访问者模式基础演示")
    print("=" * 60)
    
    # 创建文档
    doc = Document("产品介绍文档")
    
    # 添加各种文档元素
    doc.add_element(Paragraph("欢迎使用我们的产品！这是一个功能强大的解决方案。", 16))
    doc.add_element(Image("product.jpg", 800, 600, "产品图片"))
    doc.add_element(Paragraph("产品特性包括高性能、易用性和可扩展性。"))
    doc.add_element(Table(4, 3, True))
    doc.add_element(ListElement(["特性一：高性能", "特性二：易用性", "特性三：可扩展性"], False))
    doc.add_element(Paragraph("感谢您选择我们的产品！"))
    
    # 创建不同的访问者
    html_exporter = HTMLExporter()
    stats_collector = StatisticsCollector()
    markdown_exporter = MarkdownExporter()
    
    # 使用不同访问者处理文档
    visitors = [
        ("HTML导出器", html_exporter),
        ("统计收集器", stats_collector),
        ("Markdown导出器", markdown_exporter)
    ]
    
    for name, visitor in visitors:
        print(f"\n{'='*20} {name} {'='*20}")
        doc.accept(visitor)
        
        # 显示处理结果
        if isinstance(visitor, HTMLExporter):
            print(f"\n✅ {visitor.get_summary()}")
            print("HTML预览:")
            print(visitor.get_html()[:200] + "..." if len(visitor.get_html()) > 200 else visitor.get_html())
        
        elif isinstance(visitor, StatisticsCollector):
            print(f"\n✅ 统计完成")
            print(visitor.get_statistics())
        
        elif isinstance(visitor, MarkdownExporter):
            print(f"\n✅ {visitor.get_summary()}")
            print("Markdown预览:")
            print(visitor.get_markdown()[:200] + "..." if len(visitor.get_markdown()) > 200 else visitor.get_markdown())
    
    print("\n" + "=" * 60)
    print("🎉 访问者模式演示完成!")
    print("💡 关键点:")
    print("   - 每个元素都有accept方法，实现双分派")
    print("   - 访问者封装了对元素的操作")
    print("   - 可以轻松添加新的访问者而不修改元素类")
    print("=" * 60)


if __name__ == "__main__":
    demo_basic_visitor()
