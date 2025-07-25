# 23 - 策略模式 (Strategy Pattern)

> **核心思想**: 定义一系列的算法,把它们一个个封装起来, 并且使它们可相互替换。本模式使得算法可独立于使用它的客户而变化。

## 📚 概念解析

策略模式（Strategy Pattern）是一种行为设计模式，它将一组算法封装到各自的类中，使得它们可以互相替换。这种模式让算法的变化独立于使用算法的客户端。

**主要角色**:
- **策略 (Strategy)**: 定义了所有支持的算法的公共接口。
- **具体策略 (Concrete Strategy)**: 实现了策略接口，提供了具体的算法实现。
- **上下文 (Context)**: 持有一个对策略对象的引用，并定义了一个接口，让策略对象可以访问其数据。

## 📂 代码示例

| 文件名                     | 描述                                                           |
| -------------------------- | -------------------------------------------------------------- |
| `01_basic_strategy.py`     | 一个基础的数据处理器，演示了如何使用不同的策略（如求和、平均值）来处理数据。 |
| `02_sorting_algorithms.py` | 封装了多种排序算法（如冒泡、快速排序），并可以在运行时切换。   |
| `03_payment_system.py`     | 一个支付系统，支持多种支付方式（如信用卡、支付宝）。           |
| `04_data_processing.py`    | 一个数据处理管道，组合了多种验证、转换和存储策略。             |
| `05_real_world_examples.py`| 真实世界的应用，如文件压缩、图像处理等。                       |

## ✅ 优点

- **算法可以自由切换**: 可以在运行时切换算法。
- **避免了多重条件判断**: 避免了使用 `if-else` 或 `switch` 来选择算法。
- **扩展性好**: 增加一个新的策略只需添加一个新的策略类。

## ❌ 缺点

- **客户端必须知道所有的策略**: 客户端需要知道所有的策略类，并自行决定使用哪一个。
- **增加了类的数量**: 每个策略都是一个类，会增加系统中的类的数量。

## 🚀 如何运行

```bash
# 运行基础示例
python 23_策略模式/01_basic_strategy.py

# 运行排序算法示例
python 23_策略模式/02_sorting_algorithms.py

# 运行支付系统示例
python 23_策略模式/03_payment_system.py

# 运行数据处理示例
python 23_策略模式/04_data_processing.py

# 运行实际应用示例
python 23_策略模式/05_real_world_examples.py
```
