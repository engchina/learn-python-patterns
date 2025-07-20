# 原型模式 (Prototype Pattern)

原型模式是一种创建型设计模式，它允许通过复制现有对象来创建新对象，而无需知道对象的具体类型。这种模式在创建成本较高的对象时特别有用，可以避免重复的初始化工作。

## 📁 文件结构

```
10. Prototype/
├── 01_basic_prototype.py          # 基础原型模式 - 游戏角色系统
├── 02_document_prototype.py       # 文档原型模式 - 办公文档系统
├── 03_ui_component_prototype.py   # UI组件原型模式 - 界面组件系统
├── 04_configuration_prototype.py  # 配置原型模式 - 系统配置管理
├── 05_real_world_examples.py      # 实际应用示例 - 电商和游戏系统
├── Swimmers.txt                   # 示例数据文件
└── README.md                      # 说明文档
```

## 🎯 模式概述

### 核心思想
原型模式通过复制（克隆）现有实例来创建新实例，而不是通过实例化类。这种方式在以下情况下特别有用：
- 对象创建成本高昂
- 需要大量相似对象
- 对象初始化复杂
- 运行时动态创建对象

### 模式结构
```
Prototype (原型接口)
    └── clone(): Prototype

ConcretePrototype (具体原型)
    ├── clone(): ConcretePrototype
    └── 具体的业务属性和方法

Client (客户端)
    └── 使用原型创建对象

PrototypeManager (原型管理器，可选)
    ├── prototypes: Dict[str, Prototype]
    ├── register(name, prototype): void
    └── create(name): Prototype
```

## 📚 学习路径

### 1. 基础入门 - `01_basic_prototype.py`
**游戏角色系统示例**
- 学习原型模式的基本概念
- 理解克隆方法的实现
- 掌握原型管理器的使用
- 了解深拷贝与浅拷贝的区别

<augment_code_snippet path="10. Prototype/01_basic_prototype.py" mode="EXCERPT">
````python
class GameCharacterPrototype(ABC):
    """游戏角色原型抽象基类"""

    @abstractmethod
    def clone(self):
        """克隆方法 - 创建当前对象的副本"""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """获取角色信息"""
        pass
````
</augment_code_snippet>

### 2. 文档系统 - `02_document_prototype.py`
**办公文档系统示例**
- 学习复杂对象的克隆
- 理解模板模式的应用
- 掌握时间戳和ID的处理
- 了解文档属性的管理

<augment_code_snippet path="10. Prototype/02_document_prototype.py" mode="EXCERPT">
````python
class DocumentPrototype(ABC):
    """文档原型抽象基类"""

    @abstractmethod
    def clone(self):
        """克隆文档"""
        pass

    @abstractmethod
    def get_content(self) -> str:
        """获取文档内容"""
        pass
````
</augment_code_snippet>

### 3. UI组件系统 - `03_ui_component_prototype.py`
**用户界面组件系统示例**
- 学习UI组件的克隆
- 理解组件层次结构的复制
- 掌握组件工厂的实现
- 了解界面构建的优化

<augment_code_snippet path="10. Prototype/03_ui_component_prototype.py" mode="EXCERPT">
````python
class UIComponentPrototype(ABC):
    """UI组件原型抽象基类"""

    @abstractmethod
    def clone(self):
        """克隆组件"""
        pass

    @abstractmethod
    def render(self) -> str:
        """渲染组件"""
        pass
````
</augment_code_snippet>

### 4. 配置管理 - `04_configuration_prototype.py`
**系统配置管理示例**
- 学习配置对象的克隆
- 理解环境配置的管理
- 掌握配置验证机制
- 了解配置模板的应用

<augment_code_snippet path="10. Prototype/04_configuration_prototype.py" mode="EXCERPT">
````python
class ConfigurationPrototype(ABC):
    """配置原型抽象基类"""

    @abstractmethod
    def clone(self):
        """克隆配置"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """验证配置有效性"""
        pass
````
</augment_code_snippet>

### 5. 实际应用 - `05_real_world_examples.py`
**电商和游戏系统示例**
- 学习复杂业务场景的应用
- 理解原型模式的实际价值
- 掌握大型系统的设计
- 了解性能优化技巧

<augment_code_snippet path="10. Prototype/05_real_world_examples.py" mode="EXCERPT">
````python
class Product(ABC):
    """商品原型抽象基类"""

    @abstractmethod
    def clone(self):
        """克隆商品"""
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """获取商品信息"""
        pass
````
</augment_code_snippet>

## 🔍 深拷贝 vs 浅拷贝

### 浅拷贝 (Shallow Copy)
创建新对象，但内部元素是原对象元素的引用。

**适用场景：**
- 性能要求高
- 有意共享状态
- 内部数据不可变
- 只操作顶层结构

```python
def clone(self):
    """浅拷贝实现"""
    new_obj = copy.copy(self)
    # 手动处理可变属性
    new_obj.list_attr = self.list_attr.copy()
    new_obj.dict_attr = self.dict_attr.copy()
    return new_obj
```

### 深拷贝 (Deep Copy)
创建新对象，并递归复制所有内部对象。

**适用场景：**
- 需要完全独立的副本
- 避免副作用
- 复杂嵌套结构
- 多线程环境

```python
def deep_clone(self):
    """深拷贝实现"""
    return copy.deepcopy(self)
```

## ✅ 模式优点

1. **性能优势**: 避免重复的初始化工作
2. **动态配置**: 运行时动态增加和删除产品
3. **减少子类**: 不需要创建平行的工厂层次
4. **简化创建**: 客户端无需知道具体产品类
5. **灵活性**: 可以在运行时添加和删除原型

## ⚠️ 模式缺点

1. **克隆复杂性**: 实现克隆方法可能很复杂
2. **循环引用**: 对象间循环引用可能导致问题
3. **深拷贝成本**: 深拷贝可能比直接创建更昂贵
4. **内存占用**: 大量原型可能占用较多内存

## 🎯 使用场景

### 适合使用原型模式的情况：
- **对象创建成本高**: 数据库查询、网络请求、复杂计算
- **大量相似对象**: 游戏中的敌人、UI组件、配置对象
- **复杂初始化**: 需要多步骤初始化的对象
- **动态对象创建**: 运行时根据用户输入创建对象
- **避免工厂层次**: 不想创建复杂的工厂类层次

### 实际应用领域：
- **游戏开发**: 角色、道具、技能系统
- **图形编辑**: 图形元素、画笔、滤镜
- **办公软件**: 文档模板、样式模板
- **配置管理**: 环境配置、部署配置
- **电商系统**: 商品模板、促销活动

## 🚀 运行示例

```bash
# 运行基础示例
python "01_basic_prototype.py"

# 运行文档系统示例
python "02_document_prototype.py"

# 运行UI组件示例
python "03_ui_component_prototype.py"

# 运行配置管理示例
python "04_configuration_prototype.py"

# 运行实际应用示例
python "05_real_world_examples.py"
```

## 💡 最佳实践

### 1. 正确处理可变属性
```python
def clone(self):
    new_obj = copy.copy(self)
    # 为可变属性创建新副本
    new_obj.list_attr = self.list_attr.copy()
    new_obj.dict_attr = self.dict_attr.copy()
    return new_obj
```

### 2. 重置唯一标识
```python
def clone(self):
    new_obj = copy.copy(self)
    new_obj.id = str(uuid.uuid4())  # 生成新ID
    new_obj.created_at = datetime.now()  # 重置时间戳
    return new_obj
```

### 3. 实现标准克隆接口
```python
def __copy__(self):
    """支持 copy.copy()"""
    return self.clone()

def __deepcopy__(self, memo):
    """支持 copy.deepcopy()"""
    return copy.deepcopy(self, memo)
```

### 4. 使用原型管理器
```python
class PrototypeManager:
    def __init__(self):
        self._prototypes = {}

    def register(self, name, prototype):
        self._prototypes[name] = prototype

    def create(self, name):
        return self._prototypes[name].clone()
```

## 🔗 相关模式

- **工厂方法模式**: 都涉及对象创建，但原型模式通过克隆创建
- **单例模式**: 原型注册表通常是单例
- **备忘录模式**: 都涉及对象状态的保存和恢复
- **享元模式**: 可以结合使用减少内存占用
- **建造者模式**: 都用于创建复杂对象，但方式不同

## 📖 学习建议

1. **从简单开始**: 先理解基本的克隆概念
2. **理解拷贝类型**: 深入掌握深拷贝和浅拷贝的区别
3. **实践应用**: 在实际项目中尝试使用原型模式
4. **性能测试**: 比较克隆和直接创建的性能差异
5. **注意陷阱**: 避免循环引用和内存泄漏

## 🎓 进阶学习

- 结合其他创建型模式使用
- 在大型系统中的架构设计
- 性能优化和内存管理
- 多线程环境下的原型模式
- 序列化和反序列化的应用
