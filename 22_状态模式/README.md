# 22 - 状态模式 (State Pattern)

> **核心思想**: 允许一个对象在其内部状态改变时改变它的行为。对象看起来似乎修改了它的类。

## 📚 概念解析

状态模式（State Pattern）是一种行为设计模式，它将与特定状态相关的行为局部化，并且将不同状态的行为分割开来。当一个对象的行为取决于它的状态，并且它必须在运行时根据状态改变它的行为时，就可以考虑使用状态模式。

**主要角色**:
- **上下文 (Context)**: 定义了客户端感兴趣的接口，并维护一个具体状态类的实例，这个实例定义了对象的当前状态。
- **状态 (State)**: 定义了一个接口，用于封装与上下文的一个特定状态相关的行为。
- **具体状态 (Concrete State)**: 实现了状态接口，并实现了具体状态相关的行为。

## 📂 代码示例

| 文件名                  | 描述                                                           |
| ----------------------- | -------------------------------------------------------------- |
| `01_basic_state.py`     | 一个基础的开关状态机，演示了“开”、“关”、“高功率”等状态之间的转换。 |
| `02_traffic_light.py`   | 一个交通信号灯，模拟了红、黄、绿灯之间的定时切换。             |
| `03_order_system.py`    | 一个订单处理系统，管理订单在“待支付”、“已支付”、“已发货”等状态间的流转。 |
| `04_game_character.py`  | 一个游戏角色，根据其状态（如站立、行走、攻击）表现出不同的行为。   |
| `05_real_world_examples.py`| 真实世界的应用，如媒体播放器的状态（播放、暂停、停止）。       |

## ✅ 优点

- **封装性**: 将与特定状态相关的行为局部化，并且将不同状态的行为分割开来。
- **易于扩展**: 可以很容易地添加新的状态和转换。
- **消除了大量的条件分支语句**。

## ❌ 缺点

- **增加了类的数量**: 状态模式的使用会增加系统类和对象的个数。
- **结构复杂**: 状态模式的结构与实现都较为复杂，如果使用不当将导致程序结构和代码的混乱。

## 🚀 如何运行

```bash
# 运行基础示例
python 22_状态模式/01_basic_state.py

# 运行交通信号灯示例
python 22_状态模式/02_traffic_light.py

# 运行订单系统示例
python 22_状态模式/03_order_system.py

# 运行游戏角色示例
python 22_状态模式/04_game_character.py

# 运行实际应用示例
python 22_状态模式/05_real_world_examples.py
```
