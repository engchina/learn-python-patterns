# 15 - 责任链模式 (Chain of Responsibility Pattern)

> **核心思想**: 使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合关系。将这些对象连成一条链，并沿着这条链传递该请求，直到有一个对象处理它为止。

## 📚 概念解析

责任链模式（Chain of Responsibility Pattern）是一种行为设计模式，它允许你将请求沿着处理者链进行发送。收到请求后，每个处理者都决定要么处理请求，要么将其传递给链中的下一个处理者。

这种模式在以下情况中非常有用：
- 当一个请求可以被多个处理器处理，但具体由哪个处理器处理是在运行时动态决定的。
- 当你希望在不明确指定接收者的情况下，向多个对象中的一个提交一个请求。
- 当处理器集合及其顺序应在运行时动态指定。

**主要角色**:
- **处理器 (Handler)**: 定义了处理请求的接口，并持有对下一个处理器的引用。
- **具体处理器 (Concrete Handler)**: 实现了处理器接口，处理它所负责的请求。如果它不能处理请求，就将请求转发给它的后继者。
- **客户端 (Client)**: 创建处理链，并向链上的第一个对象发送请求。

## 📂 代码示例

| 文件名                        | 描述                                                           |
| ----------------------------- | -------------------------------------------------------------- |
| `01_basic_chain.py`         | 一个基础的请求处理系统，根据请求类型（如“帮助”、“错误”）将其传递给不同的处理器。 |
| `02_request_processing.py`  | 一个模拟Web服务器中间件的示例，请求依次通过认证、授权、日志等处理器。 |
| `03_logging_chain.py`       | 一个日志系统，根据日志级别（如DEBUG, INFO, ERROR）将其发送到不同的目的地（控制台，文件）。 |
| `04_validation_chain.py`    | 一个数据验证链，对输入数据进行一系列的验证（如非空、格式、长度）。   |
| `05_real_world_examples.py`   | 真实世界的应用，如公司中的费用审批流程。                       |

## ✅ 优点

- **降低耦合度**: 请求的发送者和接收者解耦。
- **增强了灵活性**: 可以动态地改变链内的成员或调动它们的次序。
- **单一职责**: 每个处理器只需要处理自己的逻辑。

## ❌ 缺点

- **不保证被处理**: 请求可能一直传到链的末端都得不到处理。
- **可能不容易观察运行时的特征**: 调试时可能难以观察运行时的特征，以及链的配置是否正确。

## 🚀 如何运行

```bash
# 运行基础示例
python 15_责任链模式/01_basic_chain.py

# 运行请求处理示例
python 15_责任链模式/02_request_processing.py

# 运行日志链示例
python 15_责任链模式/03_logging_chain.py

# 运行验证链示例
python 15_责任链模式/04_validation_chain.py

# 运行实际应用示例
python 15_责任链模式/05_real_world_examples.py
```
