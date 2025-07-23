# 01 - 面向对象基础 (Object-Oriented Programming Basics)

> **核心思想**：将现实世界的事物抽象为代码中的对象，通过封装、继承和多态来构建可维护、可扩展的软件。

## 📚 概念解析

面向对象编程（OOP）是一种编程范式，它使用“对象”来设计软件。这些对象包含了数据（属性）和操作数据的代码（方法）。Python 是一门完全支持面向对象的语言，其主要概念包括：

- **封装 (Encapsulation)**: 将数据和操作数据的代码捆绑到一个单元（类）中。这有助于隐藏内部实现细节，只暴露必要的接口。
- **继承 (Inheritance)**: 允许一个类（子类）获取另一个类（父类）的属性和方法。这促进了代码重用。
- **多态 (Polymorphism)**: 允许我们以统一的方式处理不同类型的对象。例如，一个函数可以接受任何形状的对象，只要它们都有一个 `draw()` 方法。
- **组合 (Composition)**: 通过将一个类的实例作为另一个类的属性，来构建复杂对象。它代表了“has-a”的关系。

## 📂 代码示例

| 文件名                        | 描述                                           |
| ----------------------------- | ---------------------------------------------- |
| `01_basic_classes.py`         | 演示了类、对象、属性和方法的基础。             |
| `02_employee_system.py`       | 一个更实际的员工管理系统示例。                 |
| `03_inheritance_demo.py`      | 展示如何使用继承来创建类的层次结构。           |
| `04_polymorphism_example.py`  | 解释了多态如何让代码更灵活。                   |
| `05_encapsulation_demo.py`    | 演示如何通过封装保护数据。                     |
| `06_composition_example.py`   | 展示了如何使用组合来构建复杂的对象。           |
| `07_real_world_application.py`| 一个综合性的图书管理系统，应用了所有OOP概念。  |

## 🚀 如何运行

```bash
# 运行基础类示例
python 01_面向对象基础/01_basic_classes.py

# 运行员工系统示例
python 01_面向对象基础/02_employee_system.py

# 运行继承演示示例
python 01_面向对象基础/03_inheritance_demo.py

# 运行多态示例
python 01_面向对象基础/04_polymorphism_example.py

# 运行封装演示示例
python 01_面向对象基础/05_encapsulation_demo.py

# 运行组合示例
python 01_面向对象基础/06_composition_example.py

# 运行实际应用示例
python 01_面向对象基础/07_real_world_application.py
```
