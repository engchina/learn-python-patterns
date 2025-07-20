# 迭代器模式 (Iterator Pattern)

迭代器模式是一种行为型设计模式，它提供一种方法来顺序访问聚合对象中的各个元素，而不需要暴露该对象的内部表示。Python内置了对迭代器模式的强大支持，使其成为最常用的设计模式之一。

## 🎯 模式概述

迭代器模式将遍历算法从聚合对象中分离出来，使得可以在不暴露聚合对象内部结构的情况下，统一地访问不同类型的集合。这种模式在Python中无处不在，从简单的列表遍历到复杂的数据流处理。

### 核心思想
- **统一访问**: 为不同的数据结构提供统一的遍历接口
- **惰性求值**: 按需计算，节省内存和提高性能
- **状态封装**: 将遍历状态封装在迭代器内部
- **可组合性**: 多个迭代器可以组合使用

## 📁 文件列表

### 01_basic_iterator.py
- **目的**: 迭代器模式的基础实现
- **内容**:
  - 自定义集合类和迭代器
  - Python迭代器协议的实现
  - 基本的遍历操作
- **学习要点**:
  - `__iter__`和`__next__`方法的实现
  - StopIteration异常的使用
  - 迭代器与可迭代对象的区别

### 02_data_iterators.py
- **目的**: 数据处理中的迭代器应用
- **内容**:
  - 文件行迭代器
  - CSV数据迭代器
  - 分页数据迭代器
- **学习要点**:
  - 大数据集的内存友好处理
  - 文件I/O与迭代器结合
  - 实际数据处理场景

### 03_filter_iterators.py
- **目的**: 过滤和转换迭代器
- **内容**:
  - 条件过滤迭代器
  - 数据转换迭代器
  - 链式操作迭代器
- **学习要点**:
  - 迭代器的组合和装饰
  - 函数式编程思想
  - 管道式数据处理

### 04_tree_iterators.py
- **目的**: 树形结构的迭代器
- **内容**:
  - 深度优先遍历迭代器
  - 广度优先遍历迭代器
  - 文件系统遍历示例
- **学习要点**:
  - 复杂数据结构的遍历
  - 不同遍历策略的实现
  - 栈和队列在迭代器中的应用

### 05_generators_vs_iterators.py
- **目的**: 生成器与迭代器的对比
- **内容**:
  - 生成器函数的使用
  - 生成器表达式
  - 性能和内存对比
- **学习要点**:
  - 生成器的简洁实现
  - yield关键字的工作原理
  - 何时选择生成器vs迭代器

### 06_real_world_examples.py
- **目的**: 实际应用场景示例
- **内容**:
  - 网络爬虫数据迭代
  - 日志文件分析
  - 数据库结果集迭代
- **学习要点**:
  - 迭代器在实际项目中的应用
  - 性能优化技巧
  - 错误处理和资源管理

## 🏗️ 模式结构

```
Iterable (可迭代对象)
    └── __iter__(): Iterator

Iterator (迭代器)
    ├── __iter__(): self
    └── __next__(): Object | raise StopIteration

ConcreteIterable (具体可迭代对象)
    ├── data: Collection
    └── __iter__(): ConcreteIterator

ConcreteIterator (具体迭代器)
    ├── position: int
    ├── collection: ConcreteIterable
    └── __next__(): Object
```

## 🐍 Python迭代器协议

```python
class Iterator:
    """迭代器协议的基本实现"""
    def __iter__(self):
        return self

    def __next__(self):
        # 返回下一个元素或抛出StopIteration
        if self.has_next():
            return self.get_next()
        else:
            raise StopIteration

class Iterable:
    """可迭代对象协议"""
    def __iter__(self):
        return Iterator(self)
```

## 🎭 主要角色

- **Iterable（可迭代对象）**: 实现`__iter__`方法，返回迭代器
- **Iterator（迭代器）**: 实现`__iter__`和`__next__`方法
- **Generator（生成器）**: Python特有的简化迭代器实现
- **Built-in Iterators（内置迭代器）**: Python提供的各种迭代器工具

## ✅ 模式优点

1. **内存效率**: 惰性求值，按需计算，适合处理大数据集
2. **统一接口**: 为不同数据结构提供一致的遍历方式
3. **可组合性**: 多个迭代器可以链式组合使用
4. **简化代码**: 隐藏复杂的遍历逻辑，提供简洁的使用方式
5. **支持无限序列**: 可以表示无限长的数据序列

## ⚠️ 注意事项

1. **一次性使用**: 大多数迭代器只能遍历一次
2. **状态管理**: 需要正确管理迭代器的内部状态
3. **异常处理**: 正确处理StopIteration异常
4. **资源管理**: 及时释放文件句柄等资源

## 🎯 使用场景

- **大数据处理**: 逐行处理大文件或数据库结果集
- **流式数据**: 处理网络数据流或实时数据
- **树形遍历**: 文件系统、DOM树等层次结构的遍历
- **数据管道**: 构建数据处理管道和ETL流程
- **惰性计算**: 需要按需计算的数学序列或算法

## 💡 快速开始

### 基本迭代器实现
```python
class BookCollection:
    """图书集合 - 可迭代对象"""
    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def __iter__(self):
        return BookIterator(self._books)

class BookIterator:
    """图书迭代器"""
    def __init__(self, books):
        self._books = books
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._books):
            book = self._books[self._index]
            self._index += 1
            return book
        raise StopIteration

# 使用示例
library = BookCollection()
library.add_book("Python编程")
library.add_book("设计模式")

for book in library:
    print(f"📚 {book}")
```

### 生成器实现（推荐）
```python
def fibonacci_generator(max_count=None):
    """斐波那契生成器 - 更简洁的实现"""
    count, current, next_val = 0, 0, 1

    while max_count is None or count < max_count:
        yield current
        current, next_val = next_val, current + next_val
        count += 1

# 使用示例
for num in fibonacci_generator(10):
    print(num, end=' ')  # 0 1 1 2 3 5 8 13 21 34
```

### 数据处理管道
```python
def data_pipeline(data):
    """数据处理管道示例"""
    # 过滤偶数
    evens = (x for x in data if x % 2 == 0)
    # 平方
    squares = (x**2 for x in evens)
    # 转换为字符串
    strings = (f"结果: {x}" for x in squares)

    return strings

# 使用示例
numbers = range(1, 11)
for result in data_pipeline(numbers):
    print(result)  # 结果: 4, 结果: 16, 结果: 36, 结果: 64, 结果: 100
```

## 🚀 运行方法

```bash
# 基础迭代器概念
python "01_basic_iterator.py"

# 数据处理应用
python "02_data_iterators.py"

# 过滤和转换
python "03_filter_iterators.py"

# 树形结构遍历
python "04_tree_iterators.py"

# 生成器对比
python "05_generators_vs_iterators.py"

# 实际应用案例
python "06_real_world_examples.py"
```

## 🎓 学习路径

### 初学者
1. 从 `01_basic_iterator.py` 开始，理解迭代器协议
2. 学习 `05_generators_vs_iterators.py`，掌握生成器的优势
3. 练习 `03_filter_iterators.py` 中的数据处理技巧

### 进阶开发者
1. 深入研究 `04_tree_iterators.py` 的复杂数据结构遍历
2. 分析 `06_real_world_examples.py` 的实际应用场景
3. 结合 `02_data_iterators.py` 优化现有项目的数据处理

### 架构师
1. 理解迭代器在系统设计中的作用
2. 掌握大数据处理的内存优化策略
3. 设计可扩展的数据处理管道

## 🌟 实际应用场景

### 数据科学
- **大数据集处理**: 逐行读取TB级数据文件
- **特征工程**: 流式数据转换和清洗
- **模型训练**: 批量数据加载和预处理

### Web开发
- **API分页**: 自动处理分页数据获取
- **日志分析**: 实时日志文件监控和分析
- **数据库查询**: 大结果集的内存友好处理

### 系统运维
- **文件系统遍历**: 递归目录扫描和文件处理
- **配置管理**: 动态配置文件解析和监控
- **性能监控**: 实时指标数据收集和处理

## 🔗 与其他模式的关系

- **🏗️ 组合模式**: 遍历树形组合结构
- **👁️ 观察者模式**: 迭代通知观察者列表
- **🏭 工厂方法**: 创建不同类型的迭代器
- **🎭 装饰器模式**: 装饰和增强迭代器功能
- **🚰 管道模式**: 构建数据处理管道

## ⚠️ 最佳实践

### 性能优化
1. **优先使用生成器**: 内存效率更高
2. **避免不必要的列表转换**: 保持惰性求值
3. **合理设置批处理大小**: 平衡内存和性能
4. **及时释放资源**: 使用上下文管理器

### 错误处理
1. **正确处理StopIteration**: 避免无限循环
2. **资源清理**: 确保文件和连接正确关闭
3. **异常传播**: 合理处理迭代过程中的异常
4. **状态一致性**: 保证迭代器状态的正确性

### 代码设计
1. **单一职责**: 每个迭代器只负责一种遍历方式
2. **可重用性**: 设计可重置的迭代器
3. **组合性**: 支持迭代器的链式组合
4. **文档化**: 清晰说明迭代器的行为和限制

## 📚 扩展阅读

- **Python官方文档**: Iterator Protocol
- **PEP 234**: Iterators
- **PEP 289**: Generator Expressions
- **《Effective Python》**: Item 30-32 关于迭代器的章节

## 🎯 练习建议

1. **实现自定义迭代器**: 为自己的数据结构添加迭代支持
2. **性能对比测试**: 比较不同实现方式的性能差异
3. **实际项目应用**: 在现有项目中应用迭代器模式
4. **开源项目研究**: 分析知名开源项目中的迭代器使用
