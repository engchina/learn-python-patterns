# 抽象工厂模式 (Abstract Factory Pattern)

抽象工厂模式是一种创建型设计模式，它提供了一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类。这种模式特别适用于需要创建产品族的场景。

## 📁 文件结构

```
7. AbstractFactory/
├── 01_basic_abstract_factory.py  # 基础抽象工厂 - UI主题系统
├── 02_database_factory.py        # 数据库抽象工厂 - 数据访问层
├── 03_document_factory.py        # 文档生成抽象工厂 - 多格式导出
├── 04_game_factory.py            # 游戏开发抽象工厂 - 游戏主题系统
├── 05_gardening_factory.py       # 园艺规划抽象工厂 - 园艺风格系统
└── README.md                     # 说明文档
```

## 🎯 模式概述

### 核心思想
抽象工厂模式提供了一种方式，可以将一组具有同一主题的单独的工厂封装起来。它比工厂方法模式更加抽象，可以创建一系列相关的产品对象，确保产品族的一致性。

### 模式结构
```
AbstractFactory (抽象工厂)
    ├── createProductA(): AbstractProductA
    └── createProductB(): AbstractProductB

ConcreteFactory1 (具体工厂1)
    ├── createProductA(): ProductA1
    └── createProductB(): ProductB1

ConcreteFactory2 (具体工厂2)
    ├── createProductA(): ProductA2
    └── createProductB(): ProductB2

AbstractProductA (抽象产品A)
AbstractProductB (抽象产品B)

ProductA1, ProductA2 (具体产品A)
ProductB1, ProductB2 (具体产品B)
```

## 📚 学习路径

### 1. 基础入门 - `01_basic_abstract_factory.py`
**UI主题系统示例**
- 学习抽象工厂的基本概念
- 理解产品族的概念
- 掌握工厂的层次结构
- 了解主题一致性的重要性

<augment_code_snippet path="7. AbstractFactory/01_basic_abstract_factory.py" mode="EXCERPT">
````python
class UIFactory(ABC):
    """UI组件抽象工厂"""

    @abstractmethod
    def create_button(self, text: str = "按钮") -> Button:
        """创建按钮"""
        pass

    @abstractmethod
    def create_text_field(self, placeholder: str = "请输入...") -> TextField:
        """创建文本框"""
        pass
````
</augment_code_snippet>

### 2. 数据库访问 - `02_database_factory.py`
**数据库访问层示例**
- 学习企业级应用场景
- 理解数据库组件的协同
- 掌握连接、查询、事务的统一管理
- 了解多数据库支持的实现

<augment_code_snippet path="7. AbstractFactory/02_database_factory.py" mode="EXCERPT">
````python
class DatabaseFactory(ABC):
    """数据库抽象工厂"""

    @abstractmethod
    def create_connection(self, host: str, port: int, database: str,
                         username: str, password: str) -> Connection:
        """创建数据库连接"""
        pass

    @abstractmethod
    def create_query(self, connection: Connection) -> Query:
        """创建查询构建器"""
        pass
````
</augment_code_snippet>

### 3. 文档生成 - `03_document_factory.py`
**文档导出系统示例**
- 学习文档处理场景
- 理解格式一致性的重要性
- 掌握复杂对象的创建
- 了解多格式支持的实现

<augment_code_snippet path="7. AbstractFactory/03_document_factory.py" mode="EXCERPT">
````python
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
````
</augment_code_snippet>

### 4. 游戏开发 - `04_game_factory.py`
**游戏主题系统示例**
- 学习游戏开发场景
- 理解主题风格的统一
- 掌握复杂游戏元素的创建
- 了解可扩展性的设计

<augment_code_snippet path="7. AbstractFactory/04_game_factory.py" mode="EXCERPT">
````python
class GameFactory(ABC):
    """游戏元素抽象工厂"""

    @abstractmethod
    def create_weapon(self, weapon_type: WeaponType) -> Weapon:
        """创建武器"""
        pass

    @abstractmethod
    def create_enemy(self, enemy_type: EnemyType) -> Enemy:
        """创建敌人"""
        pass
````
````
</augment_code_snippet>

### 5. 园艺规划 - `05_gardening_factory.py`
**园艺风格系统示例**
- 学习传统应用场景的现代实现
- 理解风格一致性的重要性
- 掌握复杂产品族的设计
- 了解原始示例的改进方法

<augment_code_snippet path="7. AbstractFactory/05_gardening_factory.py" mode="EXCERPT">
````python
class GardenFactory(ABC):
    """园艺抽象工厂"""

    @abstractmethod
    def create_shade_plant(self) -> Plant:
        """创建阴生植物"""
        pass

    @abstractmethod
    def create_center_plant(self) -> Plant:
        """创建中心植物"""
        pass
````
</augment_code_snippet>

## 🔍 主要角色

- **AbstractFactory（抽象工厂）**: 声明创建抽象产品对象的操作接口
- **ConcreteFactory（具体工厂）**: 实现创建具体产品对象的操作
- **AbstractProduct（抽象产品）**: 为一类产品对象声明接口
- **ConcreteProduct（具体产品）**: 定义具体工厂创建的产品对象
- **Client（客户端）**: 仅使用抽象工厂和抽象产品类声明的接口

## ✅ 模式优点

1. **产品族一致性**: 确保同一族的产品被一起使用
2. **易于交换产品系列**: 只需要改变具体工厂即可
3. **有利于产品的一致性**: 同一族的产品设计风格统一
4. **分离接口和实现**: 客户端与具体类分离
5. **符合开闭原则**: 增加新的产品族很容易

## ⚠️ 模式缺点

1. **难以支持新种类的产品**: 需要修改抽象工厂接口
2. **增加系统复杂性**: 引入了很多类和接口
3. **理解难度较高**: 抽象层次较多
4. **代码量增加**: 需要为每个产品族创建对应的工厂

## 🎯 使用场景

### 适合使用抽象工厂模式的情况：
- **系统需要独立于产品的创建、组合和表示**
- **系统需要由多个产品系列中的一个来配置**
- **需要强调一系列相关产品对象的设计以便进行联合使用**
- **提供一个产品类库，只想显示接口而不是实现**

### 实际应用领域：
- **GUI工具包**: 不同操作系统的UI组件（Windows、macOS、Linux）
- **数据库访问**: 不同数据库的连接和操作对象（MySQL、PostgreSQL、Oracle）
- **游戏开发**: 不同主题的游戏元素（科幻、魔幻、现代）
- **文档处理**: 不同格式的文档解析器（PDF、Word、HTML）
- **跨平台开发**: 不同平台的API实现

## 🚀 运行示例

```bash
# 运行基础UI主题示例
python "01_basic_abstract_factory.py"

# 运行数据库访问示例
python "02_database_factory.py"

# 运行文档生成示例
python "03_document_factory.py"

# 运行游戏开发示例
python "04_game_factory.py"

# 运行园艺规划示例
python "05_gardening_factory.py"
```

## 💡 实现要点

### 1. 确定产品族
```python
# 识别相关的产品组
# 例如：UI主题中的按钮、文本框、窗口
# 数据库中的连接、查询、事务
```

### 2. 抽象工厂接口
```python
class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self):
        pass

    @abstractmethod
    def create_product_b(self):
        pass
```

### 3. 具体工厂实现
```python
class ConcreteFactory1(AbstractFactory):
    def create_product_a(self):
        return ConcreteProductA1()

    def create_product_b(self):
        return ConcreteProductB1()
```

### 4. 客户端使用
```python
def client_code(factory: AbstractFactory):
    product_a = factory.create_product_a()
    product_b = factory.create_product_b()
    # 使用产品
```

## 📊 与其他工厂模式的比较

| 特性 | 简单工厂 | 工厂方法 | 抽象工厂 |
|------|----------|----------|----------|
| 产品数量 | 单一产品 | 单一产品 | 产品族 |
| 工厂数量 | 一个工厂 | 多个工厂 | 多个工厂 |
| 扩展性 | 较差 | 良好 | 中等 |
| 复杂度 | 简单 | 中等 | 复杂 |
| 适用场景 | 简单创建 | 单产品扩展 | 产品族创建 |
| 主要优势 | 简单易用 | 易于扩展 | 产品一致性 |

## 💡 最佳实践

### 1. 产品族设计
```python
# 确保产品族内的产品能够协同工作
class ThemeFactory(ABC):
    def create_button(self) -> Button:
        pass

    def create_text_field(self) -> TextField:
        pass

    # 确保同一主题的组件风格一致
```

### 2. 工厂选择策略
```python
class FactoryProvider:
    @staticmethod
    def get_factory(factory_type: str) -> AbstractFactory:
        factories = {
            "dark": DarkThemeFactory(),
            "light": LightThemeFactory()
        }
        return factories.get(factory_type)
```

### 3. 客户端解耦
```python
def create_ui(factory: UIFactory):
    # 客户端只依赖抽象工厂
    button = factory.create_button("确定")
    text_field = factory.create_text_field("请输入")
    # 不需要知道具体的实现类
```

## 🔗 相关模式

- **工厂方法模式**: 抽象工厂的基础，单一产品的创建
- **建造者模式**: 复杂对象的构建，关注构建过程
- **单例模式**: 工厂的实例管理，确保工厂唯一性
- **原型模式**: 产品的复制创建，通过克隆创建对象
- **策略模式**: 工厂选择策略，动态选择工厂

## 📖 学习建议

1. **理解产品族**: 深入理解相关产品的概念和协同关系
2. **抽象思维**: 学会抽象出产品族的共同特征
3. **设计权衡**: 理解模式的优缺点和适用场景
4. **实际应用**: 思考GUI主题、数据库驱动等应用场景
5. **模式对比**: 与其他工厂模式进行对比学习

## 🎓 进阶学习

- 在微服务架构中的抽象工厂模式
- 抽象工厂模式的性能优化
- 与依赖注入框架的结合使用
- 抽象工厂模式的测试策略
- 动态工厂的实现方式
