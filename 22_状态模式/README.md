# 状态模式 (State Pattern)

状态模式是一种行为型设计模式，它允许对象在内部状态改变时改变它的行为。对象看起来好像修改了它的类。状态模式将与特定状态相关的行为局部化，并且将不同状态的行为分割开来。

## 核心概念

状态模式的核心思想是：
- **状态封装**：将每个状态的行为封装在独立的状态类中
- **状态转换**：通过状态对象的切换来改变对象的行为
- **消除条件语句**：避免大量的if-else或switch语句
- **行为变化**：同一个方法在不同状态下有不同的行为

## 文件列表

### 01_basic_state.py
- **目的**: 状态模式的基础实现
- **内容**:
  - 抽象状态和上下文接口
  - 简单的状态转换示例
  - 基本的状态管理机制
- **学习要点**:
  - 理解状态模式的核心结构
  - 掌握状态转换的基本原理
  - 学习上下文与状态的关系

### 02_traffic_light.py
- **目的**: 交通信号灯状态机
- **内容**:
  - 红绿灯的状态转换
  - 定时状态切换
  - 状态持续时间管理
- **学习要点**:
  - 实际场景中的状态应用
  - 定时状态转换的实现
  - 状态机的循环转换

### 03_order_system.py
- **目的**: 订单系统状态管理
- **内容**:
  - 订单生命周期状态
  - 复杂的状态转换规则
  - 状态验证和异常处理
- **学习要点**:
  - 业务流程中的状态设计
  - 状态转换的约束条件
  - 错误状态的处理机制

### 04_game_character.py
- **目的**: 游戏角色状态系统
- **内容**:
  - 角色的多种状态
  - 状态影响的行为变化
  - 状态间的复杂交互
- **学习要点**:
  - 游戏开发中的状态应用
  - 状态对行为的影响
  - 多维度状态的管理

### 05_real_world_examples.py
- **目的**: 实际项目中的状态模式应用
- **内容**:
  - 媒体播放器状态机
  - 网络连接状态管理
  - 工作流状态系统
- **学习要点**:
  - 复杂系统的状态设计
  - 状态模式的最佳实践
  - 性能优化和扩展性考虑

## 模式结构

```
Context (上下文)
    ├── state: State                    # 当前状态对象
    ├── set_state(state): void          # 设置状态
    └── request(): void                 # 处理请求
         └── state.handle(this)         # 委托给状态处理

State (抽象状态)
    └── handle(context): void           # 处理状态相关行为

ConcreteStateA (具体状态A)
    ├── handle(context): void           # 状态A的具体行为
    └── transition_to_B(): void         # 转换到状态B

ConcreteStateB (具体状态B)
    ├── handle(context): void           # 状态B的具体行为
    └── transition_to_A(): void         # 转换到状态A
```

## 主要角色

- **Context（上下文）**: 定义客户感兴趣的接口，维护当前状态对象的引用
- **State（抽象状态）**: 定义状态接口，封装与特定状态相关的行为
- **ConcreteState（具体状态）**: 实现抽象状态接口，定义具体状态的行为和转换逻辑

## 模式优点

1. **封装状态行为**: 将每个状态的行为封装在独立的类中
2. **消除条件语句**: 避免大量的if-else或switch语句
3. **状态转换清晰**: 状态转换逻辑明确，易于理解和维护
4. **易于扩展**: 增加新状态只需要增加新的状态类
5. **符合开闭原则**: 对扩展开放，对修改关闭

## 模式缺点

1. **增加类的数量**: 每个状态都需要一个类，可能导致类爆炸
2. **状态转换复杂**: 复杂的状态转换关系可能难以管理
3. **内存开销**: 如果状态对象较大，可能增加内存消耗

## 使用场景

- **对象行为依赖状态**: 对象的行为随状态变化而变化
- **复杂条件语句**: 代码中包含大量与状态相关的条件判断
- **状态机实现**: 需要实现有限状态机的场景
- **工作流系统**: 业务流程中的状态管理
- **游戏开发**: 角色状态、游戏状态管理
- **设备控制**: 设备的不同工作模式

## 快速开始

### 基本使用示例

```python
from abc import ABC, abstractmethod

# 1. 定义状态接口
class State(ABC):
    @abstractmethod
    def handle(self, context) -> None:
        pass

    @abstractmethod
    def get_state_name(self) -> str:
        pass

# 2. 定义上下文类
class Context:
    def __init__(self, initial_state: State):
        self._state = initial_state

    def set_state(self, state: State) -> None:
        old_state = self._state.get_state_name()
        self._state = state
        print(f"状态转换: {old_state} → {state.get_state_name()}")

    def request(self) -> None:
        self._state.handle(self)

# 3. 实现具体状态
class OnState(State):
    def handle(self, context: Context) -> None:
        print("设备开启中...")
        # 可以根据条件转换到其他状态
        context.set_state(OffState())

    def get_state_name(self) -> str:
        return "开启"

class OffState(State):
    def handle(self, context: Context) -> None:
        print("设备关闭中...")
        context.set_state(OnState())

    def get_state_name(self) -> str:
        return "关闭"

# 4. 使用示例
def main():
    # 创建上下文，初始状态为关闭
    device = Context(OffState())

    # 执行操作，状态会自动转换
    for i in range(3):
        print(f"\n第{i+1}次操作:")
        device.request()

if __name__ == "__main__":
    main()
```

## 运行示例

每个示例文件都可以独立运行：

```bash
# 基础状态模式
python "01_basic_state.py"

# 交通信号灯状态机
python "02_traffic_light.py"

# 订单系统状态管理
python "03_order_system.py"

# 游戏角色状态系统
python "04_game_character.py"

# 实际项目应用
python "05_real_world_examples.py"
```

## 核心概念详解

### 状态转换方式

**1. 内部转换（状态自主转换）**
```python
class StateA(State):
    def handle(self, context):
        # 状态内部决定转换
        if some_condition:
            context.set_state(StateB())
```

**2. 外部转换（上下文控制转换）**
```python
class Context:
    def some_action(self):
        # 上下文根据业务逻辑决定转换
        if self.condition_met():
            self.set_state(NewState())
```

**3. 事件驱动转换**
```python
class StateMachine:
    def handle_event(self, event):
        # 根据事件类型转换状态
        new_state = self._state.handle_event(event)
        if new_state:
            self.set_state(new_state)
```

### 状态共享策略

**单例状态（无状态数据）**
```python
class IdleState(State):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**状态工厂（管理状态实例）**
```python
class StateFactory:
    _states = {}

    @classmethod
    def get_state(cls, state_type):
        if state_type not in cls._states:
            cls._states[state_type] = state_type()
        return cls._states[state_type]
```

## 设计原则

### 1. 单一职责原则
- 每个状态类只负责一个特定状态的行为
- 上下文类负责状态管理和委托
- 状态转换逻辑清晰分离

### 2. 开闭原则
- 对扩展开放：可以轻松添加新状态
- 对修改关闭：添加新状态不需要修改现有代码

### 3. 依赖倒置原则
- 上下文依赖抽象状态接口
- 具体状态实现抽象接口

## 实现技巧

### 1. 状态转换管理
```python
class StateManager:
    """状态转换管理器"""
    def __init__(self):
        self._transitions = {}

    def add_transition(self, from_state, to_state, condition=None):
        """添加状态转换规则"""
        if from_state not in self._transitions:
            self._transitions[from_state] = []
        self._transitions[from_state].append((to_state, condition))

    def can_transition(self, from_state, to_state, context=None):
        """检查是否可以转换"""
        if from_state not in self._transitions:
            return False

        for target, condition in self._transitions[from_state]:
            if target == to_state:
                return condition is None or condition(context)
        return False
```

### 2. 状态历史记录
```python
class StatefulContext:
    def __init__(self):
        self._state = None
        self._state_history = []

    def set_state(self, new_state):
        """设置状态并记录历史"""
        if self._state:
            self._state_history.append({
                'state': self._state,
                'timestamp': datetime.now(),
                'duration': time.time() - self._state_start_time
            })

        self._state = new_state
        self._state_start_time = time.time()

    def get_state_history(self):
        """获取状态历史"""
        return self._state_history.copy()
```

### 3. 状态持久化
```python
class PersistentStateMachine:
    def save_state(self, filename):
        """保存状态到文件"""
        state_data = {
            'current_state': self._state.__class__.__name__,
            'context_data': self._get_context_data(),
            'timestamp': datetime.now().isoformat()
        }

        with open(filename, 'w') as f:
            json.dump(state_data, f)

    def load_state(self, filename):
        """从文件加载状态"""
        with open(filename, 'r') as f:
            state_data = json.load(f)

        state_class = self._get_state_class(state_data['current_state'])
        self._state = state_class()
        self._restore_context_data(state_data['context_data'])
```

## 常见问题和解决方案

### 1. 状态爆炸问题
```python
# 问题：状态过多导致类爆炸
# 解决方案：使用状态组合或层次状态
class CompositeState(State):
    """组合状态"""
    def __init__(self):
        self._sub_states = {}
        self._current_sub_state = None

    def add_sub_state(self, name, state):
        self._sub_states[name] = state

    def set_sub_state(self, name):
        if name in self._sub_states:
            self._current_sub_state = self._sub_states[name]
```

### 2. 状态转换死锁
```python
# 解决方案：添加转换验证
class SafeContext:
    def __init__(self):
        self._transition_in_progress = False

    def set_state(self, new_state):
        if self._transition_in_progress:
            raise RuntimeError("状态转换死锁检测")

        self._transition_in_progress = True
        try:
            # 执行状态转换
            self._state = new_state
        finally:
            self._transition_in_progress = False
```

### 3. 状态数据管理
```python
# 解决方案：分离状态行为和状态数据
class StatefulContext:
    def __init__(self):
        self._state = None
        self._state_data = {}  # 状态相关数据

    def get_state_data(self, key, default=None):
        return self._state_data.get(key, default)

    def set_state_data(self, key, value):
        self._state_data[key] = value
```

## 最佳实践

### 1. 状态接口设计
- 保持状态接口简洁明确
- 避免在状态接口中包含过多方法
- 使用组合而非继承来扩展状态功能

### 2. 状态转换管理
- 明确定义状态转换规则
- 使用状态图来设计和验证状态转换
- 实现状态转换的验证机制

### 3. 错误处理
- 为无效的状态转换提供明确的错误信息
- 实现状态恢复机制
- 记录状态转换的日志

### 4. 性能优化
- 对于无状态的状态对象使用单例模式
- 避免在状态转换中进行耗时操作
- 考虑使用状态缓存来提高性能

## 实际应用场景

### 1. 游戏开发
- **角色状态**: 正常、受伤、死亡、无敌等
- **游戏状态**: 菜单、游戏中、暂停、结束等
- **AI状态**: 巡逻、追击、攻击、逃跑等

### 2. 业务系统
- **订单状态**: 待支付、已支付、已发货、已完成等
- **工作流**: 草稿、审核中、已批准、已拒绝等
- **用户状态**: 活跃、休眠、冻结、注销等

### 3. 设备控制
- **设备状态**: 开机、运行、待机、关机等
- **连接状态**: 断开、连接中、已连接、错误等
- **传输状态**: 空闲、传输中、暂停、完成等

## 与其他模式的关系

- **策略模式**: 状态模式可以看作是策略模式的扩展，增加了状态转换
- **观察者模式**: 状态变化时可以通知观察者
- **命令模式**: 状态转换可以封装为命令
- **单例模式**: 无状态的状态对象通常使用单例模式

## 学习路径

1. **理解概念**: 掌握状态模式的基本概念和结构
2. **简单实现**: 从简单的开关状态开始实践
3. **复杂应用**: 学习游戏、业务系统中的状态管理
4. **高级特性**: 掌握状态组合、状态历史等高级特性
5. **实际项目**: 在实际项目中应用状态模式

## 总结

状态模式是一种强大的行为型设计模式，它将对象的状态相关行为封装在独立的状态类中，使得状态转换逻辑更加清晰和可维护。通过合理使用状态模式，可以有效地管理复杂的状态转换逻辑，提高代码的可读性和可扩展性。
