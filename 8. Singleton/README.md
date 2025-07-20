# 单例模式 (Singleton Pattern)

单例模式是一种创建型设计模式，它确保一个类只有一个实例，并提供全局访问点。这种模式在需要控制资源访问、协调系统行为或管理共享状态时特别有用。

## 📁 文件结构

```
8. Singleton/
├── 01_basic_singleton.py         # 基础单例模式 - 日志管理系统
├── 02_decorator_singleton.py     # 装饰器单例模式 - 配置管理系统
├── 03_metaclass_singleton.py     # 元类单例模式 - 数据库连接池系统
├── 04_module_singleton.py        # 模块级单例模式 - 系统监控器
├── 05_real_world_examples.py     # 实际应用示例 - 游戏和企业系统
├── Spooler.py                    # 原始示例（已重写）
├── testlock.py                   # 原始示例（保留）
└── README.md                     # 说明文档
```

## 🎯 模式概述

### 核心思想
单例模式确保某个类只能创建一个实例，并提供一个全局访问点来获取该实例。这种模式在需要控制资源访问、协调系统行为或管理共享状态时特别有用。

### 模式结构
```
Singleton
    ├── _instance: Singleton (类变量)
    ├── _lock: Lock (线程锁)
    ├── __new__(cls): Singleton
    └── getInstance(): Singleton (可选的静态方法)
```

## 文件列表

### Spooler.py
- **目的**: 打印假脱机程序的单例实现
- **内容**:
  - 打印队列管理的单例类
  - 线程安全的单例实现
  - 打印任务的管理和调度
- **学习要点**:
  - 单例模式的经典应用场景
  - 线程安全的考虑
  - 资源管理的单例应用

### testlock.py
- **目的**: 线程锁定机制测试
- **内容**:
  - 多线程环境下的单例测试
  - 线程安全机制的验证
  - 并发访问的控制
- **学习要点**:
  - 多线程编程基础
  - 线程安全的重要性
  - 锁机制的使用

## 模式结构

```
Singleton
    ├── _instance: Singleton (类变量)
    ├── __new__(cls): Singleton
    └── getInstance(): Singleton (可选的静态方法)
```

## 实现方式

### 1. 基本单例实现
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 2. 线程安全的单例
```python
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

### 3. 装饰器实现
```python
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class MyClass:
    pass
```

### 4. 元类实现
```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    pass
```

## 模式优点

1. **控制实例数量**: 确保只有一个实例存在
2. **全局访问点**: 提供全局访问的入口
3. **延迟初始化**: 可以在需要时才创建实例
4. **节约资源**: 避免重复创建相同的对象

## 模式缺点

1. **违反单一职责**: 类既要管理自身逻辑又要管理实例
2. **隐藏依赖关系**: 使用全局状态可能隐藏组件间的依赖
3. **测试困难**: 单例状态可能影响单元测试
4. **多线程复杂性**: 需要考虑线程安全问题

## 使用场景

- **日志记录器**: 整个应用使用同一个日志实例
- **配置管理**: 全局配置信息的管理
- **数据库连接池**: 管理数据库连接的复用
- **缓存管理**: 全局缓存的统一管理
- **打印假脱机**: 管理打印队列和任务

## 线程安全考虑

### 问题场景
```python
# 非线程安全的实现可能导致多个实例
class UnsafeSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:  # 竞态条件
            time.sleep(0.1)  # 模拟初始化时间
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 解决方案
```python
import threading

class SafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # 双重检查锁定
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

## 打印假脱机示例

```python
import threading
from queue import Queue

class PrintSpooler:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.print_queue = Queue()
                    cls._instance.is_printing = False
        return cls._instance

    def add_job(self, document):
        """添加打印任务"""
        self.print_queue.put(document)
        if not self.is_printing:
            self._start_printing()

    def _start_printing(self):
        """开始打印处理"""
        self.is_printing = True
        # 启动打印线程
        threading.Thread(target=self._print_worker).start()

    def _print_worker(self):
        """打印工作线程"""
        while not self.print_queue.empty():
            document = self.print_queue.get()
            self._print_document(document)
        self.is_printing = False

    def _print_document(self, document):
        """实际打印文档"""
        print(f"正在打印: {document}")
        time.sleep(1)  # 模拟打印时间
```

## 替代方案

### 依赖注入
```python
class Logger:
    def log(self, message):
        print(f"Log: {message}")

class Application:
    def __init__(self, logger):
        self.logger = logger  # 注入依赖

    def do_something(self):
        self.logger.log("执行某些操作")

# 使用
logger = Logger()
app = Application(logger)
```

### 模块级单例
```python
# config.py
class Config:
    def __init__(self):
        self.settings = {}

# 模块级实例
config_instance = Config()

# 其他模块中使用
from config import config_instance
```

## 运行方法

```bash
python "Spooler.py"
python "testlock.py"
```

## 学习建议

1. **理解需求**: 确认是否真的需要单例模式
2. **线程安全**: 在多线程环境中特别注意线程安全
3. **测试策略**: 学会在单例环境下进行单元测试
4. **替代方案**: 了解依赖注入等替代方案
5. **实际应用**: 思考实际项目中的应用场景

## 反模式警告

单例模式有时被认为是反模式，因为：
- 引入全局状态
- 使测试变得困难
- 违反依赖倒置原则
- 隐藏类之间的依赖关系

## 最佳实践

1. **谨慎使用**: 确保真的需要全局唯一实例
2. **线程安全**: 在多线程环境中使用适当的同步机制
3. **延迟初始化**: 在需要时才创建实例
4. **接口设计**: 提供清晰的接口而不是直接访问实例
5. **测试友好**: 考虑测试时的实例重置机制

## 相关模式

- **工厂模式**: 可以与单例结合使用
- **外观模式**: 单例常用于外观类
- **状态模式**: 状态对象可能是单例
- **享元模式**: 享元工厂通常是单例

## 前置知识

- 面向对象编程基础
- Python的特殊方法（__new__, __init__）
- 多线程编程基础
- 装饰器和元类（高级实现）

## 后续学习

- 9. Builder（建造者模式）
- 10. Prototype（原型模式）
- 结构型模式的学习
