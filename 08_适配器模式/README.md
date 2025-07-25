# 08 - 适配器模式 (Adapter Pattern)

> **核心思想**: 将一个类的接口转换成客户希望的另外一个接口。适配器模式使得原本由于接口不兼容而不能一起工作的那些类可以一起工作。

## 📚 概念解析

适配器模式（Adapter Pattern）是一种结构型设计模式，它扮演着两个不兼容接口之间的桥梁。这种模式涉及到一个单一的类，该类负责加入独立的或不兼容的接口功能。

**主要角色**:
- **目标 (Target)**: 客户所期望的接口。
- **被适配者 (Adaptee)**: 需要被适配的类，它的接口与目标接口不兼容。
- **适配器 (Adapter)**: 将被适配者的接口转换成目标接口。它实现了目标接口，并持有被适配者的一个实例。

**两种实现方式**:
- **对象适配器**: 在适配器中组合一个被适配者对象。这是更常用、更灵活的方式。
- **类适配器**: 通过多重继承适配器类和被适配者类。在 Python 中可行，但在许多其他语言中不可行。

## 📂 代码示例

| 文件名                        | 描述                                                           |
| ----------------------------- | -------------------------------------------------------------- |
| `01_basic_adapter.py`         | 一个数据格式转换系统，演示了如何适配不同的数据源（XML, CSV）以供统一处理。 |
| `02_third_party_adapter.py`   | 一个支付网关适配器，统一了多种第三方支付（如AliPay, WeChat Pay）的接口。 |
| `03_legacy_system_adapter.py` | 适配一个遗留的数据库系统，使其能够与新的应用程序代码一起工作。   |
| `04_api_adapter.py`           | 适配一个返回XML的旧API，使其输出与新的JSON格式API一致。          |
| `05_real_world_examples.py`   | 真实世界的应用，如日志库适配器、缓存库适配器等。               |

## ✅ 优点

- **复用性**: 可以复用现有的类，而无需修改其源代码。
- **解耦**: 将客户端代码与被适配的具体类解耦。
- **单一职责**: 适配器只负责接口转换，职责清晰。

## ❌ 缺点

- **增加了复杂性**: 引入了额外的类，增加了系统的复杂性。
- **可能引入性能开销**: 额外的间接层可能会带来轻微的性能下降。

## 🚀 如何运行

```bash
# 运行基础示例
python 08_适配器模式/01_basic_adapter.py

# 运行第三方适配器示例
python 08_适配器模式/02_third_party_adapter.py

# 运行遗留系统适配器示例
python 08_适配器模式/03_legacy_system_adapter.py

# 运行API适配器示例
python 08_适配器模式/04_api_adapter.py

# 运行实际应用示例
python 08_适配器模式/05_real_world_examples.py
```
