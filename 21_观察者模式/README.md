# 21 - 观察者模式 (Observer Pattern)

> **核心思想**: 定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被自动更新。

## 📚 概念解析

观察者模式（Observer Pattern）是一种行为设计模式，它允许一个对象（称为“主题”或“可观察者”）维护一个依赖它的对象（称为“观察者”）列表，并在其状态发生变化时自动通知它们。这种模式也被称为**发布-订阅 (Publish-Subscribe)**模式。

**主要角色**:
- **主题 (Subject)**: 维护一个观察者列表，并提供了添加、删除和通知观察者的方法。
- **具体主题 (Concrete Subject)**: 存储了状态，并在状态改变时通知其观察者。
- **观察者 (Observer)**: 定义了一个更新接口，用于在接收到主题通知时更新自己。
- **具体观察者 (Concrete Observer)**: 实现了观察者接口，并维护着一个对具体主题对象的引用。

## 📂 代码示例

| 文件名                     | 描述                                                           |
| -------------------------- | -------------------------------------------------------------- |
| `01_basic_observer.py`     | 一个基础的新闻发布系统，当新闻机构（主题）发布新消息时，所有订阅的新闻频道（观察者）都会收到通知。 |
| `02_weather_station.py`    | 一个气象站示例，不同的显示面板（观察者）订阅气象站（主题）的数据更新。 |
| `03_event_system.py`       | 一个通用的事件总线系统，演示了观察者模式在事件驱动架构中的应用。 |
| `04_mvc_observer.py`       | 在模型-视图-控制器（MVC）架构中，模型作为主题，视图作为观察者。   |
| `05_real_world_examples.py`| 真实世界的应用，如股票价格监控、GUI事件监听等。                |

## ✅ 优点

- **松耦合**: 主题和观察者之间是松散耦合的，它们可以独立地变化和复用。
- **广播通信**: 支持一对多的广播通信。
- **动态关系**: 可以在运行时动态地添加和删除观察者。

## ❌ 缺点

- **更新顺序**: 如果观察者的更新顺序很重要，那么实现起来会比较困难。
- **可能导致意外的更新**: 在某些情况下，一个看似无害的更改可能会触发一系列复杂的更新。
- **内存泄漏**: 如果观察者没有被正确地移除，可能会导致内存泄漏。

## 🚀 如何运行

```bash
# 运行基础示例
python 21_观察者模式/01_basic_observer.py

# 运行气象站示例
python 21_观察者模式/02_weather_station.py

# 运行事件系统示例
python 21_观察者模式/03_event_system.py

# 运行MVC示例
python 21_观察者模式/04_mvc_observer.py

# 运行实际应用示例
python 21_观察者模式/05_real_world_examples.py
```
