# 工厂方法模式 (Factory Method Pattern)

工厂方法模式是一种创建型设计模式，它提供了一种创建对象的接口，但由子类决定要实例化的类是哪一个。这种模式将对象的创建延迟到子类中，让子类决定实例化哪一个类，遵循"开闭原则"。

## 🎯 模式概述

工厂方法模式的核心思想是"延迟实例化"。它通过定义一个创建对象的接口，让子类决定实例化哪一个类。工厂方法让类的实例化推迟到子类中进行。

### 核心思想
- **延迟实例化**: 将对象创建推迟到子类中决定
- **开闭原则**: 对扩展开放，对修改关闭
- **单一职责**: 将产品创建代码集中在一个地方
- **松耦合**: 客户端代码与具体产品类解耦

## 📁 文件列表

### 01_basic_factory.py
- **目的**: 工厂方法模式的基础实现
- **内容**:
  - 文档处理器工厂示例
  - 展示工厂方法的基本结构和使用
- **学习要点**:
  - 工厂方法模式的核心概念
  - 抽象工厂和具体工厂的实现
  - 产品类的层次结构

### 02_notification_factory.py
- **目的**: 通知系统工厂示例
- **内容**:
  - 邮件、短信、推送通知的工厂实现
  - 不同通知方式的创建和发送
- **学习要点**:
  - 实际业务场景中的工厂方法应用
  - 策略模式与工厂方法的结合
  - 配置驱动的对象创建

### 03_database_factory.py
- **目的**: 数据库连接工厂示例
- **内容**:
  - MySQL、PostgreSQL、SQLite连接工厂
  - 数据库操作的统一接口
- **学习要点**:
  - 数据库抽象层的设计
  - 配置管理和工厂方法
  - 资源管理的最佳实践

### 04_ui_factory.py
- **目的**: UI组件工厂示例
- **内容**:
  - 不同主题的UI组件工厂
  - 按钮、输入框等组件的创建
- **学习要点**:
  - GUI开发中的工厂方法应用
  - 主题系统的实现
  - 组件的动态创建

### 05_real_world_examples.py
- **目的**: 工厂方法模式的实际应用示例
- **内容**:
  - 日志记录器工厂、解析器工厂等实际场景
  - 展示工厂方法在不同领域的应用
- **学习要点**:
  - 工厂方法的实际应用场景
  - 不同领域的设计技巧
  - 最佳实践和注意事项

## 🏗️ 模式结构

```
┌─────────────────────┐
│    抽象创建者       │
│   (Creator)         │
│                     │
│ + factoryMethod()   │ ←── 工厂方法（抽象）
│ + someOperation()   │ ←── 使用工厂方法的业务逻辑
└─────────────────────┘
           △
           │ 继承
           │
┌─────────────────────┐
│   具体创建者        │
│ (ConcreteCreator)   │
│                     │
│ + factoryMethod()   │ ←── 实现具体的创建逻辑
└─────────────────────┘
           │ 创建
           ▼
┌─────────────────────┐
│    抽象产品         │
│   (Product)         │
│                     │
│ + operation()       │
└─────────────────────┘
           △
           │ 实现
           │
┌─────────────────────┐
│   具体产品          │
│ (ConcreteProduct)   │
│                     │
│ + operation()       │
└─────────────────────┘
```

## 👥 主要角色

- **抽象创建者 (Creator)**: 声明工厂方法的抽象类，通常包含调用工厂方法的核心业务逻辑
- **具体创建者 (ConcreteCreator)**: 实现工厂方法的具体类，返回具体产品的实例
- **抽象产品 (Product)**: 工厂方法创建的对象的抽象接口
- **具体产品 (ConcreteProduct)**: 具体的产品实现，实现抽象产品接口

## ✅ 模式优点

1. **遵循开闭原则**: 添加新产品时不需要修改现有代码，只需添加新的具体创建者
2. **单一职责原则**: 将产品创建代码集中在一个地方，便于维护
3. **松耦合**: 客户端代码与具体产品类解耦，只依赖抽象接口
4. **多态性**: 通过继承实现不同的创建行为，提高代码的灵活性
5. **可扩展性**: 易于扩展新的产品类型

## ❌ 模式缺点

1. **代码复杂性**: 需要创建多个类，增加了代码的复杂性
2. **类的数量**: 每增加一个产品就需要增加一个具体创建者类
3. **理解成本**: 相比简单工厂，理解和维护成本较高

## 🎯 适用场景

- **框架设计**: 当框架需要向用户提供扩展点时
- **产品族扩展**: 当需要经常添加新的产品类型时
- **解耦需求**: 当客户端不应该依赖具体产品类时
- **配置驱动**: 当产品创建需要根据配置或运行时条件决定时
- **插件系统**: 当需要支持插件化架构时

## 🔄 与简单工厂的区别

| 特性 | 简单工厂 | 工厂方法 |
|------|----------|----------|
| **扩展性** | 需要修改工厂类 | 通过继承扩展，无需修改现有代码 |
| **复杂度** | 简单，只有一个工厂类 | 相对复杂，需要多个类 |
| **灵活性** | 较低，硬编码产品创建逻辑 | 较高，支持运行时决定产品类型 |
| **遵循原则** | 违反开闭原则 | 遵循开闭原则 |
| **使用场景** | 产品类型固定且较少 | 产品类型经常变化或扩展 |

## 💡 实现示例

### 基本工厂方法实现

<augment_code_snippet path="6. FactoryMethod/01_basic_factory.py" mode="EXCERPT">
````python
from abc import ABC, abstractmethod

# 抽象产品
class Document(ABC):
    """文档抽象基类"""

    @abstractmethod
    def create_content(self) -> str:
        """创建文档内容"""
        pass

# 具体产品
class PDFDocument(Document):
    """PDF文档"""

    def create_content(self) -> str:
        return "创建PDF文档内容"

class WordDocument(Document):
    """Word文档"""

    def create_content(self) -> str:
        return "创建Word文档内容"

# 抽象创建者
class DocumentProcessor(ABC):
    """文档处理器抽象基类"""

    @abstractmethod
    def create_document(self) -> Document:
        """工厂方法：创建文档"""
        pass

    def process_document(self, content: str) -> str:
        """处理文档的业务逻辑"""
        document = self.create_document()
        doc_content = document.create_content()
        return f"{doc_content}: {content}"

# 具体创建者
class PDFProcessor(DocumentProcessor):
    """PDF处理器"""

    def create_document(self) -> Document:
        return PDFDocument()

class WordProcessor(DocumentProcessor):
    """Word处理器"""

    def create_document(self) -> Document:
        return WordDocument()
````
</augment_code_snippet>

### 通知系统工厂示例

<augment_code_snippet path="6. FactoryMethod/02_notification_factory.py" mode="EXCERPT">
````python
class NotificationFactory(ABC):
    """通知工厂抽象基类"""

    @abstractmethod
    def create_notification(self) -> Notification:
        """工厂方法：创建通知对象"""
        pass

    def send_notification(self, message: str, recipient: str) -> bool:
        """发送通知的业务逻辑"""
        notification = self.create_notification()
        return notification.send(message, recipient)

class EmailNotificationFactory(NotificationFactory):
    """邮件通知工厂"""

    def create_notification(self) -> Notification:
        return EmailNotification()

class SMSNotificationFactory(NotificationFactory):
    """短信通知工厂"""

    def create_notification(self) -> Notification:
        return SMSNotification()
````
</augment_code_snippet>

## 🚀 运行方法

```bash
# 运行基础工厂方法示例
python 01_basic_factory.py

# 运行通知系统工厂示例
python 02_notification_factory.py

# 运行数据库连接工厂示例
python 03_database_factory.py

# 运行UI组件工厂示例
python 04_ui_factory.py

# 运行实际应用示例
python 05_real_world_examples.py
```

## 📚 学习建议

1. **理解抽象**: 深入理解抽象类和接口的作用
2. **掌握继承**: 理解继承在工厂方法中的重要性
3. **多态应用**: 掌握多态在对象创建中的应用
4. **设计原则**: 理解开闭原则和单一职责原则
5. **实际应用**: 思考在框架设计和插件系统中的应用
6. **对比学习**: 与简单工厂和抽象工厂进行对比

## 🌍 实际应用场景

- **Web框架**: Django、Flask等框架中的视图工厂
- **ORM系统**: 数据库连接和查询构建器的创建
- **日志系统**: 不同类型日志记录器的创建
- **解析器**: XML、JSON、YAML等不同格式解析器
- **UI框架**: 不同主题或平台的UI组件创建

## 🔗 与其他模式的关系

- **简单工厂模式**: 工厂方法是简单工厂的进化版本
- **抽象工厂模式**: 工厂方法通常作为抽象工厂的实现方式
- **模板方法模式**: 工厂方法可以看作是模板方法的特殊应用
- **策略模式**: 都使用多态，但工厂方法关注对象创建
- **建造者模式**: 都是创建型模式，但建造者关注复杂对象的构建过程

## ⚠️ 注意事项

1. **避免过度设计**: 如果产品类型固定且很少变化，简单工厂可能更合适
2. **类的数量**: 每个产品都需要对应的工厂类，会增加类的数量
3. **理解成本**: 相比简单工厂，理解和维护成本较高
4. **性能考虑**: 多层继承可能影响性能，需要权衡

## 📋 前置知识

- 面向对象编程基础
- 继承和多态的理解
- 抽象类和接口的概念
- 5. SimpleFactory（简单工厂模式）

## 📖 后续学习

- 7. AbstractFactory（抽象工厂模式）
- 9. Builder（建造者模式）
- 10. Prototype（原型模式）

---

*工厂方法模式通过将对象创建延迟到子类，提供了一种灵活的对象创建方式。它是许多框架和库的核心设计模式，掌握它对于理解现代软件架构非常重要。*
