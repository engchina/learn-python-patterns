# 建造者模式 (Builder Pattern)

建造者模式是一种创建型设计模式，它允许分步骤创建复杂对象。该模式将复杂对象的构建过程分解为多个简单的步骤，通过不同的建造者可以创建不同表示的对象，使得同样的构建过程可以创建不同的表示。

## 📁 文件结构

```
9. Builder/
├── 01_basic_builder.py           # 基础建造者模式 - 计算机配置系统
├── 02_fluent_builder.py          # 流式建造者模式 - SQL查询构建器
├── 03_document_builder.py        # 文档建造者模式 - 文档生成系统
├── 04_configuration_builder.py   # 配置建造者模式 - 系统配置管理
├── 05_real_world_examples.py     # 实际应用示例 - 电商和游戏系统
├── BuildChoices.py               # 原始示例（保留）
├── TreeStates.py                 # 原始示例（保留）
└── README.md                     # 说明文档
```

## 🎯 模式概述

### 核心思想
建造者模式将复杂对象的构建过程分解为多个简单的步骤，通过不同的建造者可以创建不同表示的对象。它将对象的构建过程与表示分离，使得同样的构建过程可以创建不同的表示。

### 模式结构
```
Director (指挥者)
    └── construct(): void

Builder (抽象建造者)
    ├── buildPartA(): void
    ├── buildPartB(): void
    └── getResult(): Product

ConcreteBuilder (具体建造者)
    ├── buildPartA(): void
    ├── buildPartB(): void
    └── getResult(): ConcreteProduct

Product (产品)
    └── 复杂对象
```

## 📚 学习路径

### 1. 基础入门 - `01_basic_builder.py`
**计算机配置系统示例**
- 学习建造者模式的基本概念
- 理解指挥者的作用
- 掌握分步骤构建复杂对象
- 了解不同建造者创建不同产品

<augment_code_snippet path="9. Builder/01_basic_builder.py" mode="EXCERPT">
````python
class ComputerBuilder(ABC):
    """计算机建造者抽象基类"""

    def __init__(self):
        self.computer = Computer()

    @abstractmethod
    def build_cpu(self):
        """构建处理器"""
        pass

    @abstractmethod
    def build_motherboard(self):
        """构建主板"""
        pass
````
</augment_code_snippet>

### 2. 流式建造者 - `02_fluent_builder.py`
**SQL查询构建器示例**
- 学习流式接口设计
- 理解方法链的实现
- 掌握复杂查询的构建
- 了解流式建造者的优势

<augment_code_snippet path="9. Builder/02_fluent_builder.py" mode="EXCERPT">
````python
class SQLQueryBuilder:
    """流式SQL查询建造者"""

    def select(self, *fields: str) -> 'SQLQueryBuilder':
        """选择字段"""
        if fields:
            self.query.select_fields.extend(fields)
        return self

    def from_table(self, table: str, alias: str = None) -> 'SQLQueryBuilder':
        """指定表名"""
        if alias:
            self.query.from_table = f"{table} AS {alias}"
        else:
            self.query.from_table = table
        return self
````
</augment_code_snippet>

### 3. 文档建造者 - `03_document_builder.py`
**文档生成系统示例**
- 学习层次结构的构建
- 理解复杂文档的组织
- 掌握不同文档类型的构建
- 了解内容管理的实现

<augment_code_snippet path="9. Builder/03_document_builder.py" mode="EXCERPT">
````python
class DocumentBuilder(ABC):
    """文档建造者抽象基类"""

    @abstractmethod
    def set_document_info(self, title: str, author: str, doc_type: DocumentType):
        """设置文档基本信息"""
        pass

    @abstractmethod
    def add_title_page(self):
        """添加标题页"""
        pass
````
</augment_code_snippet>

### 4. 配置建造者 - `04_configuration_builder.py`
**系统配置管理示例**
- 学习配置对象的构建
- 理解环境配置的差异
- 掌握配置验证机制
- 了解配置导出功能

<augment_code_snippet path="9. Builder/04_configuration_builder.py" mode="EXCERPT">
````python
class ConfigurationBuilder(ABC):
    """配置建造者抽象基类"""

    @abstractmethod
    def configure_database(self):
        """配置数据库"""
        pass

    @abstractmethod
    def configure_cache(self):
        """配置缓存"""
        pass
````
</augment_code_snippet>

### 5. 实际应用 - `05_real_world_examples.py`
**电商和游戏系统示例**
- 学习复杂业务对象的构建
- 理解建造者模式的实际价值
- 掌握大型系统的设计
- 了解性能优化技巧

<augment_code_snippet path="9. Builder/05_real_world_examples.py" mode="EXCERPT">
````python
class OrderBuilder:
    """订单建造者"""

    def set_customer(self, customer_id: str, name: str, email: str) -> 'OrderBuilder':
        """设置客户信息"""
        self.order.customer_id = customer_id
        self.order.customer_name = name
        self.order.customer_email = email
        return self
````
</augment_code_snippet>

## 🔍 建造者模式的变体

### 传统建造者模式
使用指挥者控制构建过程，适合复杂的构建逻辑。

```python
class Director:
    def __init__(self, builder):
        self.builder = builder

    def construct(self):
        self.builder.build_part_a()
        self.builder.build_part_b()
        return self.builder.get_result()
```

### 流式建造者模式
通过方法链实现，代码更简洁易读。

```python
result = (Builder()
          .set_property_a(value_a)
          .set_property_b(value_b)
          .build())
```

### 分步建造者模式
将构建过程分为多个阶段，每个阶段返回不同的建造者。

```python
builder = (StepBuilder()
           .step1()
           .required_field(value)
           .step2()
           .optional_field(value)
           .build())
```

## ✅ 模式优点

1. **分离构建和表示**: 构建过程和最终表示分离
2. **精细控制**: 可以精细控制对象的构建过程
3. **代码复用**: 相同的构建过程可以创建不同的产品
4. **易于扩展**: 可以独立地扩展建造者和产品
5. **可读性强**: 特别是流式建造者，代码非常易读

## ⚠️ 模式缺点

1. **增加复杂性**: 需要创建多个新类
2. **产品相似性**: 要求产品有足够的相似性
3. **内部结构暴露**: 建造者需要了解产品的内部结构
4. **过度设计**: 对于简单对象可能过度设计

## 🎯 使用场景

### 适合使用建造者模式的情况：
- **复杂对象创建**: 对象有很多组成部分，构建过程复杂
- **多种表示**: 同一构建过程需要创建不同表示的对象
- **分步构建**: 对象的创建需要多个步骤
- **可选参数多**: 对象有很多可选的配置参数
- **不可变对象**: 需要构建不可变的复杂对象

### 实际应用领域：
- **SQL查询构建**: 复杂查询语句的构建
- **配置管理**: 系统配置对象的构建
- **文档生成**: 复杂文档结构的构建
- **UI组件**: 复杂界面组件的构建
- **测试数据**: 测试用例数据的构建

## 🚀 运行示例

```bash
# 运行基础示例
python "01_basic_builder.py"

# 运行流式建造者示例
python "02_fluent_builder.py"

# 运行文档建造者示例
python "03_document_builder.py"

# 运行配置建造者示例
python "04_configuration_builder.py"

# 运行实际应用示例
python "05_real_world_examples.py"

# 运行原始示例
python "BuildChoices.py"
python "TreeStates.py"
```

## 💡 最佳实践

### 1. 选择合适的建造者类型
```python
# 简单对象 - 直接构造
obj = SimpleObject(param1, param2)

# 复杂对象 - 传统建造者
director = Director(ConcreteBuilder())
obj = director.construct()

# 多可选参数 - 流式建造者
obj = (FluentBuilder()
       .required_param(value)
       .optional_param(value)
       .build())
```

### 2. 实现方法链
```python
class FluentBuilder:
    def method(self, value):
        # 设置属性
        self.property = value
        # 返回self支持链式调用
        return self
```

### 3. 验证构建结果
```python
def build(self):
    # 验证必需参数
    if not self.required_field:
        raise ValueError("Required field is missing")

    # 构建对象
    return Product(self.required_field, self.optional_field)
```

### 4. 支持重置和复用
```python
class Builder:
    def reset(self):
        """重置建造者状态"""
        self.__init__()
        return self

    def clone(self):
        """克隆当前状态"""
        new_builder = Builder()
        new_builder.copy_state_from(self)
        return new_builder
```

## 🔗 相关模式

- **抽象工厂模式**: 都涉及对象创建，但建造者关注构建过程
- **组合模式**: 建造者常用于构建组合结构
- **策略模式**: 不同的建造者可以看作不同的策略
- **模板方法模式**: 指挥者定义了构建的算法骨架
- **原型模式**: 都是创建型模式，但关注点不同

## 📖 学习建议

1. **从简单开始**: 先理解传统建造者模式的结构
2. **掌握流式接口**: 学习如何设计优雅的方法链
3. **实践应用**: 在实际项目中尝试使用建造者模式
4. **性能考虑**: 注意构建过程的性能影响
5. **设计权衡**: 避免过度设计，选择合适的复杂度

## 🎓 进阶学习

- 结合泛型实现类型安全的建造者
- 使用注解和反射简化建造者实现
- 在大型系统中的架构设计
- 与依赖注入框架的结合使用
- 异步建造者模式的实现
