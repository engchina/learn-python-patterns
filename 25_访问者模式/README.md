# 访问者模式 (Visitor Pattern)

一种行为型设计模式，允许在不修改对象结构的情况下，为对象结构中的元素定义新的操作。通过将操作与对象结构分离，实现了算法与数据结构的解耦。

## 概念解析

访问者模式的核心是“双分派”机制。它包含两个主要部分：
1.  **访问者 (Visitor)**: 定义了对不同元素执行操作的接口。
2.  **元素 (Element)**: 定义了接受访问者的接口。

当一个访问者访问一个元素时，元素的 `accept` 方法会调用访问者中对应其具体类型的 `visit` 方法，从而执行特定操作。

## 代码示例

| 文件 | 描述 |
| :--- | :--- |
| [`01_basic_visitor.py`](25_访问者模式/01_basic_visitor.py:1) | 访问者模式的基础实现，演示了文档处理系统中如何使用访问者进行HTML导出和统计收集。 |
| [`02_file_system.py`](25_访问者模式/02_file_system.py:1) | 文件系统的访问者应用，展示了如何对文件和目录执行不同的操作。 |
| [`03_ast_processor.py`](25_访问者模式/03_ast_processor.py:1) | 抽象语法树处理的访问者实现，常用于编译器设计。 |
| [`04_report_generator.py`](25_访问者模式/04_report_generator.py:1) | 报表生成系统的访问者设计，用于生成不同格式的报表。 |
| [`05_real_world_examples.py`](25_访问者模式/05_real_world_examples.py:1) | 实际项目中的访问者应用，如数据分析和图形渲染。 |

## 优点

- **易于添加新操作**: 只需创建新的访问者类，无需修改现有的元素类。
- **操作集中管理**: 相关操作被组织在同一个访问者类中，便于维护。
- **符合开闭原则**: 对扩展开放（添加新访问者），对修改关闭（不修改元素类）。

## 缺点

- **难以添加新元素**: 如果需要添加新的元素类型，必须修改所有现有的访问者接口和实现。
- **可能破坏封装**: 访问者通常需要访问元素的内部数据，这可能破坏对象的封装性。
- **增加系统复杂性**: 引入了额外的抽象层，使系统结构更复杂。

## 如何运行

```bash
# 运行基础示例
python 25_访问者模式/01_basic_visitor.py

# 运行文件系统示例
python 25_访问者模式/02_file_system.py

# 运行AST处理示例
python 25_访问者模式/03_ast_processor.py

# 运行报表生成示例
python 25_访问者模式/04_report_generator.py

# 运行实际应用示例
python 25_访问者模式/05_real_world_examples.py
```
