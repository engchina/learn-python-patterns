"""
01_basic_factory.py - 工厂方法模式基础实现

文档处理器示例
这个示例展示了工厂方法模式的核心概念。
我们有不同类型的文档（PDF、Word、Excel），每种文档都有对应的处理器。
工厂方法模式让我们可以在不修改现有代码的情况下，轻松添加新的文档类型。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import time


# ==================== 抽象产品 ====================
class Document(ABC):
    """文档抽象基类"""
    
    def __init__(self, title: str):
        self.title = title
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    
    @abstractmethod
    def create_content(self) -> str:
        """创建文档内容"""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """获取文件扩展名"""
        pass
    
    @abstractmethod
    def get_mime_type(self) -> str:
        """获取MIME类型"""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """获取文档基本信息"""
        return {
            "title": self.title,
            "type": self.__class__.__name__,
            "extension": self.get_file_extension(),
            "mime_type": self.get_mime_type(),
            "created_at": self.created_at
        }


# ==================== 具体产品 ====================
class PDFDocument(Document):
    """PDF文档"""
    
    def create_content(self) -> str:
        return f"正在创建PDF文档: {self.title}\n- 设置页面布局\n- 添加文本内容\n- 生成PDF格式"
    
    def get_file_extension(self) -> str:
        return ".pdf"
    
    def get_mime_type(self) -> str:
        return "application/pdf"


class WordDocument(Document):
    """Word文档"""
    
    def create_content(self) -> str:
        return f"正在创建Word文档: {self.title}\n- 设置文档样式\n- 添加段落内容\n- 应用格式化"
    
    def get_file_extension(self) -> str:
        return ".docx"
    
    def get_mime_type(self) -> str:
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class ExcelDocument(Document):
    """Excel文档"""
    
    def create_content(self) -> str:
        return f"正在创建Excel文档: {self.title}\n- 创建工作表\n- 添加数据行\n- 设置单元格格式"
    
    def get_file_extension(self) -> str:
        return ".xlsx"
    
    def get_mime_type(self) -> str:
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


# ==================== 抽象创建者 ====================
class DocumentProcessor(ABC):
    """文档处理器抽象基类"""
    
    @abstractmethod
    def create_document(self, title: str) -> Document:
        """工厂方法：创建文档对象"""
        pass
    
    def process_document(self, title: str, content: str = "") -> str:
        """处理文档的业务逻辑（模板方法）"""
        print(f"📄 开始处理文档...")
        
        # 1. 创建文档对象（使用工厂方法）
        document = self.create_document(title)
        print(f"✓ 文档对象创建完成: {document.__class__.__name__}")
        
        # 2. 生成文档内容
        doc_content = document.create_content()
        print(f"✓ 文档内容生成完成")
        
        # 3. 添加用户内容
        if content:
            doc_content += f"\n\n用户内容:\n{content}"
        
        # 4. 获取文档信息
        doc_info = document.get_info()
        
        # 5. 返回处理结果
        result = f"""
{doc_content}

文档信息:
- 标题: {doc_info['title']}
- 类型: {doc_info['type']}
- 扩展名: {doc_info['extension']}
- MIME类型: {doc_info['mime_type']}
- 创建时间: {doc_info['created_at']}
"""
        print(f"✓ 文档处理完成")
        return result


# ==================== 具体创建者 ====================
class PDFProcessor(DocumentProcessor):
    """PDF处理器"""
    
    def create_document(self, title: str) -> Document:
        print("  → 使用PDF工厂创建PDF文档")
        return PDFDocument(title)


class WordProcessor(DocumentProcessor):
    """Word处理器"""
    
    def create_document(self, title: str) -> Document:
        print("  → 使用Word工厂创建Word文档")
        return WordDocument(title)


class ExcelProcessor(DocumentProcessor):
    """Excel处理器"""
    
    def create_document(self, title: str) -> Document:
        print("  → 使用Excel工厂创建Excel文档")
        return ExcelDocument(title)


# ==================== 客户端代码 ====================
def demo_basic_factory():
    """演示基础工厂方法模式"""
    print("=== 工厂方法模式演示 ===\n")
    
    # 创建不同类型的文档处理器
    processors = {
        "PDF": PDFProcessor(),
        "Word": WordProcessor(),
        "Excel": ExcelProcessor()
    }
    
    # 处理不同类型的文档
    documents = [
        ("PDF", "项目报告", "这是一个重要的项目总结报告。"),
        ("Word", "会议纪要", "今天的会议讨论了以下议题..."),
        ("Excel", "销售数据", "第一季度销售统计表格。")
    ]
    
    for doc_type, title, content in documents:
        print(f"\n{'='*50}")
        print(f"处理 {doc_type} 文档: {title}")
        print('='*50)
        
        processor = processors[doc_type]
        result = processor.process_document(title, content)
        print(result)


def demo_extensibility():
    """演示工厂方法模式的可扩展性"""
    print("\n" + "="*60)
    print("演示可扩展性：添加新的文档类型")
    print("="*60)
    
    # 新增PowerPoint文档类型
    class PowerPointDocument(Document):
        """PowerPoint文档"""
        
        def create_content(self) -> str:
            return f"正在创建PowerPoint文档: {self.title}\n- 创建幻灯片\n- 添加内容页\n- 设置动画效果"
        
        def get_file_extension(self) -> str:
            return ".pptx"
        
        def get_mime_type(self) -> str:
            return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    
    # 新增PowerPoint处理器
    class PowerPointProcessor(DocumentProcessor):
        """PowerPoint处理器"""
        
        def create_document(self, title: str) -> Document:
            print("  → 使用PowerPoint工厂创建PowerPoint文档")
            return PowerPointDocument(title)
    
    # 使用新的文档类型
    ppt_processor = PowerPointProcessor()
    result = ppt_processor.process_document("产品介绍", "我们的新产品具有以下特点...")
    print(result)


def main():
    """主函数"""
    demo_basic_factory()
    demo_extensibility()
    
    print("\n" + "="*60)
    print("工厂方法模式的优势:")
    print("1. 遵循开闭原则：添加新文档类型无需修改现有代码")
    print("2. 单一职责：每个处理器只负责一种文档类型")
    print("3. 松耦合：客户端代码不依赖具体的文档类")
    print("4. 易于扩展：可以轻松添加新的文档类型和处理器")
    print("="*60)


if __name__ == "__main__":
    main()
