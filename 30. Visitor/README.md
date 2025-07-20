# 访问者模式 (Visitor Pattern)

访问者模式是一种行为型设计模式，它允许你在不修改对象结构的情况下，为对象结构中的元素定义新的操作。这种模式通过将操作与对象结构分离，实现了算法与数据结构的解耦。

## 核心概念

访问者模式的核心思想是"双分派"：根据访问者的类型和被访问元素的类型，来决定执行哪个具体的操作。这样可以在不修改元素类的前提下，轻松添加新的操作。

## 文件列表

### 01_basic_visitor.py
- **目的**: 访问者模式的基础实现
- **内容**: 文档处理系统的访问者演示
- **学习要点**: 理解访问者模式的基本结构和双分派机制

### 02_file_system.py
- **目的**: 文件系统的访问者应用
- **内容**: 文件和目录的不同操作（统计、搜索、分析等）
- **学习要点**: 实际业务场景中的访问者模式应用

### 03_ast_processor.py
- **目的**: 抽象语法树处理的访问者实现
- **内容**: 代码分析、优化、生成等不同操作
- **学习要点**: 编译器设计中的访问者模式应用

### 04_report_generator.py
- **目的**: 报表生成系统的访问者设计
- **内容**: 不同格式报表的生成和导出
- **学习要点**: 复杂业务逻辑的访问者模式设计

### 05_real_world_examples.py
- **目的**: 实际项目中的访问者应用
- **内容**: 数据分析、图形渲染、业务规则处理等实际应用
- **学习要点**: 访问者模式在实际开发中的最佳实践

## 模式结构

```
抽象访问者 (Visitor)
    ├── visit_element_a(element)    # 访问元素A的方法
    ├── visit_element_b(element)    # 访问元素B的方法
    └── visit_element_c(element)    # 访问元素C的方法

具体访问者 (ConcreteVisitor)
    ├── visit_element_a(element)    # 实现对元素A的具体操作
    ├── visit_element_b(element)    # 实现对元素B的具体操作
    └── visit_element_c(element)    # 实现对元素C的具体操作

抽象元素 (Element)
    └── accept(visitor)             # 接受访问者的方法

具体元素 (ConcreteElement)
    ├── accept(visitor)             # 调用访问者的对应方法
    ├── get_data()                  # 元素特有的数据访问方法
    └── specific_operation()        # 元素特有的操作
```

## 主要角色

- **抽象访问者**: 定义访问各种元素的接口
- **具体访问者**: 实现对不同元素的具体操作
- **抽象元素**: 定义接受访问者的接口
- **具体元素**: 实现接受访问者的方法，调用访问者的对应操作
- **对象结构**: 包含元素的集合，提供遍历接口

## 模式优点

1. **易于添加新操作**: 新增访问者即可添加新的操作，无需修改元素类
2. **操作集中管理**: 相关操作集中在一个访问者类中，便于维护
3. **符合开闭原则**: 对扩展开放，对修改关闭
4. **分离算法与数据**: 将操作逻辑与数据结构分离

## 模式缺点

1. **难以添加新元素**: 新增元素类型需要修改所有访问者
2. **可能破坏封装**: 访问者需要访问元素的内部数据
3. **增加系统复杂性**: 引入了额外的抽象层

## 适用场景

- **对象结构稳定**: 元素类型相对固定，但需要频繁添加新操作
- **操作复杂多样**: 需要对同一组对象执行多种不相关的操作
- **避免污染元素类**: 不希望在元素类中添加过多操作方法
- **编译器设计**: 抽象语法树的遍历和处理
- **文档处理**: 对文档结构执行不同的操作（渲染、导出等）

## 快速开始

### 基本使用示例

```python
from abc import ABC, abstractmethod

# 抽象访问者
class DocumentVisitor(ABC):
    """文档访问者接口"""

    @abstractmethod
    def visit_paragraph(self, paragraph):
        """访问段落"""
        pass

    @abstractmethod
    def visit_image(self, image):
        """访问图片"""
        pass

    @abstractmethod
    def visit_table(self, table):
        """访问表格"""
        pass

# 抽象文档元素
class DocumentElement(ABC):
    """文档元素接口"""

    @abstractmethod
    def accept(self, visitor: DocumentVisitor):
        """接受访问者"""
        pass

# 具体文档元素
class Paragraph(DocumentElement):
    """段落元素"""

    def __init__(self, text: str):
        self.text = text

    def accept(self, visitor: DocumentVisitor):
        visitor.visit_paragraph(self)

class Image(DocumentElement):
    """图片元素"""

    def __init__(self, src: str, width: int, height: int):
        self.src = src
        self.width = width
        self.height = height

    def accept(self, visitor: DocumentVisitor):
        visitor.visit_image(self)

class Table(DocumentElement):
    """表格元素"""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

    def accept(self, visitor: DocumentVisitor):
        visitor.visit_table(self)

# 具体访问者 - HTML导出
class HTMLExporter(DocumentVisitor):
    """HTML导出访问者"""

    def __init__(self):
        self.html_content = []

    def visit_paragraph(self, paragraph):
        self.html_content.append(f"<p>{paragraph.text}</p>")

    def visit_image(self, image):
        self.html_content.append(
            f'<img src="{image.src}" width="{image.width}" height="{image.height}">'
        )

    def visit_table(self, table):
        self.html_content.append(f"<table rows='{table.rows}' cols='{table.cols}'></table>")

    def get_html(self) -> str:
        return "\n".join(self.html_content)

# 具体访问者 - 统计信息
class StatisticsCollector(DocumentVisitor):
    """统计信息收集访问者"""

    def __init__(self):
        self.paragraph_count = 0
        self.image_count = 0
        self.table_count = 0
        self.total_text_length = 0

    def visit_paragraph(self, paragraph):
        self.paragraph_count += 1
        self.total_text_length += len(paragraph.text)

    def visit_image(self, image):
        self.image_count += 1

    def visit_table(self, table):
        self.table_count += 1

    def get_statistics(self) -> str:
        return (f"段落: {self.paragraph_count}, 图片: {self.image_count}, "
                f"表格: {self.table_count}, 总文本长度: {self.total_text_length}")

# 使用示例
def demo_document_visitor():
    """文档访问者演示"""
    # 创建文档元素
    elements = [
        Paragraph("这是第一段文字"),
        Image("image1.jpg", 800, 600),
        Paragraph("这是第二段文字"),
        Table(3, 4),
        Paragraph("这是第三段文字")
    ]

    # HTML导出
    html_exporter = HTMLExporter()
    for element in elements:
        element.accept(html_exporter)

    print("HTML导出结果:")
    print(html_exporter.get_html())

    # 统计信息收集
    stats_collector = StatisticsCollector()
    for element in elements:
        element.accept(stats_collector)

    print(f"\n文档统计: {stats_collector.get_statistics()}")

# 运行示例
demo_document_visitor()
```

## 运行方法

```bash
# 运行基础示例
python 01_basic_visitor.py

# 运行文件系统示例
python 02_file_system.py

# 运行AST处理示例
python 03_ast_processor.py

# 运行报表生成示例
python 04_report_generator.py

# 运行实际应用示例
python 05_real_world_examples.py
```

## 学习建议

1. **从简单开始**: 先理解基本的访问者结构，再学习复杂应用
2. **理解双分派**: 深入理解访问者模式的核心机制
3. **识别适用场景**: 学会判断何时使用访问者模式
4. **对比其他模式**: 理解访问者与策略模式的区别
5. **实践应用**: 在实际项目中寻找可以应用访问者的场景

## 实际应用场景

- **编译器设计**: 抽象语法树的遍历、优化、代码生成
- **文档处理**: 不同格式的导出（HTML、PDF、Word等）
- **数据分析**: 对复杂数据结构执行不同的分析算法
- **图形渲染**: 对图形对象执行不同的渲染操作
- **业务规则**: 对业务对象执行不同的验证和处理规则
- **报表系统**: 生成不同格式和样式的报表

## 与其他模式的关系

- **组合模式**: 访问者经常用于遍历组合结构
- **策略模式**: 访问者可以看作是针对对象结构的策略
- **命令模式**: 访问者的操作可以封装成命令
- **迭代器模式**: 可以结合使用来遍历复杂结构

## 最佳实践

1. **保持元素接口稳定**: 避免频繁修改元素类型
2. **合理组织访问者**: 将相关操作组织在同一个访问者中
3. **考虑性能影响**: 在性能敏感的场景中谨慎使用
4. **文档化访问者**: 清楚说明每个访问者的用途和行为
5. **异常处理**: 在访问者中妥善处理可能的异常情况

## 注意事项

⚠️ **元素类型稳定**: 访问者模式适用于元素类型相对稳定的场景
⚠️ **避免过度使用**: 不要为了使用模式而强行应用访问者
⚠️ **考虑封装性**: 访问者可能需要访问元素的内部状态
⚠️ **性能权衡**: 双分派机制可能带来额外的性能开销
