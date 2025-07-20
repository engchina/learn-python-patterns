# 中介者模式 (Mediator Pattern)

中介者模式是一种行为型设计模式，它定义了一个中介对象来封装一系列对象之间的交互，使原有对象之间的耦合松散，且可以独立地改变它们之间的交互。这种模式在现代软件开发中广泛应用，特别是在GUI框架、聊天系统和工作流管理中。

## 🎯 模式概述

中介者模式的核心思想是"解耦复杂交互"。通过引入一个中介者对象来管理对象间的通信，各个对象不再直接相互引用，而是通过中介者进行交互。这样可以减少对象间的耦合度，使系统更容易维护和扩展。

### 核心思想
- **集中控制**: 将复杂的交互逻辑集中在中介者中管理
- **降低耦合**: 对象之间不直接通信，减少相互依赖
- **易于扩展**: 可以独立地改变和复用各个组件
- **符合迪米特法则**: 对象只与直接的朋友通信

## 📁 文件列表

### 01_basic_mediator.py
- **目的**: 中介者模式的基础实现
- **内容**:
  - 智能家居控制系统示例
  - 设备间的协调通信
  - 场景模式的实现
- **学习要点**:
  - 中介者接口的设计
  - 同事类的实现
  - 对象间通信的解耦

### 02_chat_system.py
- **目的**: 聊天系统中介者应用
- **内容**:
  - 多用户聊天室
  - 私聊和群聊功能
  - 用户状态管理
- **学习要点**:
  - 复杂通信场景的处理
  - 状态管理和事件分发
  - 实时消息传递

### 03_gui_mediator.py
- **目的**: GUI界面中介者模式
- **内容**:
  - 表单组件间的交互
  - 动态UI状态管理
  - 事件处理和响应
- **学习要点**:
  - UI组件解耦
  - 复杂表单逻辑管理
  - 用户交互优化

### 04_workflow_mediator.py
- **目的**: 工作流系统中介者
- **内容**:
  - 任务节点协调
  - 流程状态管理
  - 条件分支处理
- **学习要点**:
  - 业务流程建模
  - 状态机模式结合
  - 企业级应用设计

### 05_event_bus.py
- **目的**: 事件总线中介者实现
- **内容**:
  - 发布-订阅机制
  - 事件路由和过滤
  - 异步消息处理
- **学习要点**:
  - 现代事件驱动架构
  - 微服务通信模式
  - 系统解耦最佳实践

### 06_real_world_examples.py
- **目的**: 实际应用场景示例
- **内容**:
  - 游戏对象管理
  - 电商订单处理
  - 物联网设备协调
- **学习要点**:
  - 中介者在实际项目中的应用
  - 性能优化技巧
  - 架构设计考虑

## 🏗️ 模式结构

```
Mediator (中介者接口)
    └── notify(sender, event): void

ConcreteMediator (具体中介者)
    ├── components: Dict[str, Component]
    ├── register_component(component): void
    └── notify(sender, event): void

Component (组件基类)
    ├── mediator: Mediator
    └── notify_mediator(event): void

ConcreteComponent (具体组件)
    ├── perform_action(): void
    └── handle_event(event): void
```

## 🎭 主要角色

- **Mediator（中介者接口）**: 定义组件间通信的统一接口
- **ConcreteMediator（具体中介者）**: 实现中介者接口，协调各组件的交互
- **Component（组件基类）**: 定义组件的基本接口，持有中介者引用
- **ConcreteComponent（具体组件）**: 实现具体的业务逻辑，通过中介者通信

## ✅ 模式优点

1. **降低耦合度**: 组件间不直接引用，通过中介者通信
2. **集中管理**: 复杂的交互逻辑集中在中介者中，便于维护
3. **易于扩展**: 可以独立添加新组件或修改交互逻辑
4. **符合开闭原则**: 对扩展开放，对修改封闭
5. **提高可重用性**: 组件可以在不同的中介者中重用

## ⚠️ 注意事项

1. **中介者复杂性**: 避免中介者承担过多职责
2. **性能考虑**: 所有通信都经过中介者可能影响性能
3. **单点故障**: 中介者故障会影响整个系统
4. **过度设计**: 简单的交互不需要使用中介者模式

## 🎯 使用场景

### 适合使用的场景
- **GUI应用**: 窗口组件间的复杂交互
- **聊天系统**: 多用户间的消息传递
- **工作流系统**: 任务节点间的协调
- **游戏开发**: 游戏对象间的交互管理
- **微服务架构**: 服务间的通信协调

### 不适合使用的场景
- 简单的一对一通信
- 性能要求极高的实时系统
- 组件间交互逻辑非常简单

## 💡 快速开始

### 智能家居控制示例
```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: 'Device', event: str, data: Any = None) -> None:
        pass

class Device(ABC):
    def __init__(self, device_id: str, mediator: Mediator = None):
        self.device_id = device_id
        self.mediator = mediator
        self.is_on = False

    def notify_mediator(self, event: str, data: Any = None) -> None:
        if self.mediator:
            self.mediator.notify(self, event, data)

class SmartLight(Device):
    def __init__(self, device_id: str, mediator: Mediator = None):
        super().__init__(device_id, mediator)
        self.brightness = 0

    def turn_on(self) -> None:
        self.is_on = True
        self.brightness = 80
        print(f"💡 {self.device_id} 已开启")
        self.notify_mediator("light_on", {"brightness": self.brightness})

class SmartHomeMediator(Mediator):
    def __init__(self):
        self.devices: Dict[str, Device] = {}

    def register_device(self, device: Device) -> None:
        self.devices[device.device_id] = device
        device.mediator = self

    def notify(self, sender: Device, event: str, data: Any = None) -> None:
        print(f"🏠 中介者收到事件: {sender.device_id} -> {event}")

        if event == "light_on":
            # 自动调节其他设备
            self._adjust_environment_for_lighting()

    def _adjust_environment_for_lighting(self) -> None:
        print("🤖 自动调节环境设置...")

# 使用示例
home = SmartHomeMediator()
light = SmartLight("客厅主灯", home)
home.register_device(light)
light.turn_on()  # 触发自动化响应
```

### 聊天室中介者示例
```python
from datetime import datetime
from typing import Dict, Set

# 用户类
class User(Colleague):
    """聊天室用户"""
    def __init__(self, mediator: Mediator, username: str):
        super().__init__(mediator, username)
        self.username = username
        self.online = True

    def send(self, message: str, target: str = None):
        """发送消息"""
        if not self.online:
            print(f"{self.username} 已离线，无法发送消息")
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        if target:
            print(f"[{timestamp}] {self.username} 私聊 {target}: {message}")
            self.mediator.send_private_message(message, self, target)
        else:
            print(f"[{timestamp}] {self.username} 群发: {message}")
            self.mediator.send_message(message, self)

    def receive(self, message: str):
        """接收消息"""
        if self.online:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {self.username} 收到: {message}")

    def join_room(self, room_name: str):
        """加入房间"""
        self.mediator.join_room(self, room_name)

    def leave_room(self, room_name: str):
        """离开房间"""
        self.mediator.leave_room(self, room_name)

    def go_offline(self):
        """下线"""
        self.online = False
        print(f"{self.username} 已下线")

    def go_online(self):
        """上线"""
        self.online = True
        print(f"{self.username} 已上线")

# 聊天室中介者
class ChatRoomMediator(Mediator):
    """聊天室中介者"""
    def __init__(self, name: str):
        self.name = name
        self.users: Dict[str, User] = {}
        self.rooms: Dict[str, Set[str]] = {}  # 房间名 -> 用户名集合
        self.message_history: List[str] = []

    def add_user(self, user: User):
        """添加用户"""
        self.users[user.username] = user
        print(f"用户 {user.username} 加入聊天室 {self.name}")

        # 通知其他在线用户
        welcome_msg = f"用户 {user.username} 加入了聊天室"
        for other_user in self.users.values():
            if other_user != user and other_user.online:
                other_user.receive(welcome_msg)

    def remove_user(self, username: str):
        """移除用户"""
        if username in self.users:
            user = self.users[username]
            # 从所有房间中移除
            for room_users in self.rooms.values():
                room_users.discard(username)

            del self.users[username]
            print(f"用户 {username} 离开聊天室 {self.name}")

            # 通知其他用户
            leave_msg = f"用户 {username} 离开了聊天室"
            for other_user in self.users.values():
                if other_user.online:
                    other_user.receive(leave_msg)

    def send_message(self, message: str, sender: User):
        """发送群组消息"""
        if not sender.online:
            return

        formatted_message = f"{sender.username}: {message}"
        self.message_history.append(formatted_message)

        # 发送给所有在线用户（除了发送者）
        for user in self.users.values():
            if user != sender and user.online:
                user.receive(formatted_message)

    def send_private_message(self, message: str, sender: User, target_username: str):
        """发送私人消息"""
        if not sender.online:
            return

        if target_username not in self.users:
            sender.receive(f"用户 {target_username} 不存在")
            return

        target_user = self.users[target_username]
        if not target_user.online:
            sender.receive(f"用户 {target_username} 不在线")
            return

        private_message = f"[私聊] {sender.username}: {message}"
        target_user.receive(private_message)

    def join_room(self, user: User, room_name: str):
        """用户加入房间"""
        if room_name not in self.rooms:
            self.rooms[room_name] = set()

        self.rooms[room_name].add(user.username)
        print(f"{user.username} 加入房间 {room_name}")

        # 通知房间内其他用户
        room_message = f"{user.username} 加入了房间 {room_name}"
        self.send_room_message(room_message, room_name, user)

    def leave_room(self, user: User, room_name: str):
        """用户离开房间"""
        if room_name in self.rooms and user.username in self.rooms[room_name]:
            self.rooms[room_name].remove(user.username)
            print(f"{user.username} 离开房间 {room_name}")

            # 通知房间内其他用户
            room_message = f"{user.username} 离开了房间 {room_name}"
            self.send_room_message(room_message, room_name, user)

    def send_room_message(self, message: str, room_name: str, sender: User = None):
        """发送房间消息"""
        if room_name not in self.rooms:
            return

        for username in self.rooms[room_name]:
            if username in self.users:
                user = self.users[username]
                if user != sender and user.online:
                    user.receive(f"[{room_name}] {message}")

    def get_online_users(self) -> List[str]:
        """获取在线用户列表"""
        return [user.username for user in self.users.values() if user.online]

    def get_room_users(self, room_name: str) -> List[str]:
        """获取房间用户列表"""
        if room_name in self.rooms:
            return list(self.rooms[room_name])
        return []

# 使用示例
def demo_chatroom_mediator():
    """聊天室中介者演示"""
    # 创建聊天室
    chatroom = ChatRoomMediator("技术讨论群")

    # 创建用户
    alice = User(chatroom, "Alice")
    bob = User(chatroom, "Bob")
    charlie = User(chatroom, "Charlie")
    diana = User(chatroom, "Diana")

    # 用户加入聊天室
    print("=== 用户加入聊天室 ===")
    chatroom.add_user(alice)
    chatroom.add_user(bob)
    chatroom.add_user(charlie)
    chatroom.add_user(diana)

    print(f"\n在线用户: {chatroom.get_online_users()}")

    # 群组消息
    print("\n=== 群组消息 ===")
    alice.send("大家好！我是Alice")
    bob.send("你好Alice，我是Bob")

    # 私人消息
    print("\n=== 私人消息 ===")
    charlie.send("你好Alice，很高兴认识你", "Alice")
    alice.send("你好Charlie！", "Charlie")

    # 房间功能
    print("\n=== 房间功能 ===")
    alice.join_room("Python讨论")
    bob.join_room("Python讨论")
    charlie.join_room("Java讨论")

    print(f"Python讨论房间用户: {chatroom.get_room_users('Python讨论')}")
    print(f"Java讨论房间用户: {chatroom.get_room_users('Java讨论')}")

    # 用户下线
    print("\n=== 用户状态变化 ===")
    diana.go_offline()
    alice.send("Diana还在吗？", "Diana")  # 应该收到离线提示

    # 用户离开
    print("\n=== 用户离开 ===")
    chatroom.remove_user("Charlie")

    print(f"最终在线用户: {chatroom.get_online_users()}")
```

### GUI对话框中介者示例
```python
# GUI组件基类
class Widget:
    """GUI组件基类"""
    def __init__(self, mediator, name: str):
        self.mediator = mediator
        self.name = name
        self.enabled = True

    def set_enabled(self, enabled: bool):
        """设置组件是否可用"""
        self.enabled = enabled
        status = "启用" if enabled else "禁用"
        print(f"{self.name} 已{status}")

    def notify_mediator(self, event: str):
        """通知中介者"""
        if self.enabled:
            self.mediator.notify(self, event)

# 具体GUI组件
class Button(Widget):
    """按钮组件"""
    def click(self):
        """点击按钮"""
        print(f"点击按钮: {self.name}")
        self.notify_mediator("click")

class CheckBox(Widget):
    """复选框组件"""
    def __init__(self, mediator, name: str):
        super().__init__(mediator, name)
        self.checked = False

    def toggle(self):
        """切换复选框状态"""
        self.checked = not self.checked
        status = "选中" if self.checked else "取消选中"
        print(f"{self.name} {status}")
        self.notify_mediator("toggle")

class TextBox(Widget):
    """文本框组件"""
    def __init__(self, mediator, name: str):
        super().__init__(mediator, name)
        self.text = ""

    def set_text(self, text: str):
        """设置文本"""
        self.text = text
        print(f"{self.name} 文本设置为: '{text}'")
        self.notify_mediator("text_changed")

class ListBox(Widget):
    """列表框组件"""
    def __init__(self, mediator, name: str):
        super().__init__(mediator, name)
        self.items = []
        self.selected_index = -1

    def add_item(self, item: str):
        """添加项目"""
        self.items.append(item)
        print(f"{self.name} 添加项目: {item}")

    def select_item(self, index: int):
        """选择项目"""
        if 0 <= index < len(self.items):
            self.selected_index = index
            print(f"{self.name} 选择项目: {self.items[index]}")
            self.notify_mediator("selection_changed")

# 对话框中介者
class DialogMediator:
    """对话框中介者"""
    def __init__(self):
        # 创建GUI组件
        self.ok_button = Button(self, "确定按钮")
        self.cancel_button = Button(self, "取消按钮")
        self.save_checkbox = CheckBox(self, "保存设置复选框")
        self.name_textbox = TextBox(self, "姓名文本框")
        self.file_listbox = ListBox(self, "文件列表")

        # 初始化文件列表
        self.file_listbox.add_item("文档1.txt")
        self.file_listbox.add_item("文档2.txt")
        self.file_listbox.add_item("文档3.txt")

        # 设置初始状态
        self.update_ui_state()

    def notify(self, sender: Widget, event: str):
        """处理组件事件"""
        print(f"中介者收到事件: {sender.name} -> {event}")

        if sender == self.ok_button and event == "click":
            self.handle_ok_click()
        elif sender == self.cancel_button and event == "click":
            self.handle_cancel_click()
        elif sender == self.save_checkbox and event == "toggle":
            self.handle_save_toggle()
        elif sender == self.name_textbox and event == "text_changed":
            self.handle_name_change()
        elif sender == self.file_listbox and event == "selection_changed":
            self.handle_file_selection()

        # 更新UI状态
        self.update_ui_state()

    def handle_ok_click(self):
        """处理确定按钮点击"""
        name = self.name_textbox.text
        save_settings = self.save_checkbox.checked
        selected_file = ""

        if self.file_listbox.selected_index >= 0:
            selected_file = self.file_listbox.items[self.file_listbox.selected_index]

        print(f"执行操作: 姓名='{name}', 保存设置={save_settings}, 选择文件='{selected_file}'")

    def handle_cancel_click(self):
        """处理取消按钮点击"""
        print("取消操作，重置所有设置")
        self.name_textbox.set_text("")
        self.save_checkbox.checked = False
        self.file_listbox.selected_index = -1

    def handle_save_toggle(self):
        """处理保存设置切换"""
        if self.save_checkbox.checked:
            print("启用设置保存功能")
        else:
            print("禁用设置保存功能")

    def handle_name_change(self):
        """处理姓名变化"""
        if self.name_textbox.text:
            print("姓名已输入，可以执行操作")
        else:
            print("姓名为空，请输入姓名")

    def handle_file_selection(self):
        """处理文件选择"""
        if self.file_listbox.selected_index >= 0:
            selected_file = self.file_listbox.items[self.file_listbox.selected_index]
            print(f"选择了文件: {selected_file}")

    def update_ui_state(self):
        """更新UI状态"""
        # 只有输入了姓名且选择了文件才能点击确定
        has_name = bool(self.name_textbox.text.strip())
        has_selection = self.file_listbox.selected_index >= 0

        self.ok_button.set_enabled(has_name and has_selection)

# 使用示例
def demo_dialog_mediator():
    """对话框中介者演示"""
    print("=== GUI对话框中介者演示 ===")

    # 创建对话框
    dialog = DialogMediator()

    print("\n--- 初始状态 ---")
    print("确定按钮应该是禁用的（没有姓名和文件选择）")

    print("\n--- 输入姓名 ---")
    dialog.name_textbox.set_text("张三")

    print("\n--- 选择文件 ---")
    dialog.file_listbox.select_item(0)

    print("\n--- 切换保存设置 ---")
    dialog.save_checkbox.toggle()

    print("\n--- 点击确定 ---")
    dialog.ok_button.click()

    print("\n--- 点击取消 ---")
    dialog.cancel_button.click()
```

## 🚀 运行方法

```bash
# 基础中介者概念
python "01_basic_mediator.py"

# 聊天系统应用
python "02_chat_system.py"

# GUI界面中介者
python "03_gui_mediator.py"

# 工作流系统
python "04_workflow_mediator.py"

# 事件总线实现
python "05_event_bus.py"

# 实际应用案例
python "06_real_world_examples.py"
```

## 🎓 学习路径

### 初学者
1. 从 `01_basic_mediator.py` 开始，理解中介者的基本概念
2. 学习 `02_chat_system.py`，掌握复杂通信场景的处理
3. 练习 `03_gui_mediator.py` 中的界面交互管理

### 进阶开发者
1. 深入研究 `04_workflow_mediator.py` 的业务流程协调
2. 分析 `05_event_bus.py` 的现代事件驱动架构
3. 结合 `06_real_world_examples.py` 优化现有项目架构

### 架构师
1. 理解中介者在系统设计中的作用
2. 掌握大型系统的解耦策略
3. 设计可扩展的通信架构

## 🌟 实际应用场景

### 前端开发
- **React/Vue组件通信**: 父子组件间的复杂交互
- **状态管理**: Redux/Vuex等状态管理库的设计思想
- **表单验证**: 复杂表单字段间的联动验证

### 后端开发
- **微服务通信**: 服务间的消息路由和协调
- **工作流引擎**: 业务流程的节点协调
- **事件驱动架构**: 系统间的异步通信

### 游戏开发
- **游戏对象管理**: 角色、道具、环境间的交互
- **AI系统**: 多个AI代理间的协调
- **网络同步**: 多人游戏的状态同步

## 🔗 与其他模式的关系

- **🔍 观察者模式**: 都处理对象间通信，但中介者是集中式管理
- **🎭 外观模式**: 都提供统一接口，但中介者关注双向交互
- **📋 命令模式**: 中介者可以使用命令模式来处理请求
- **🎯 策略模式**: 中介者可以使用不同策略处理不同交互
- **🏭 工厂方法**: 创建不同类型的中介者

## ⚠️ 最佳实践

### 设计原则
1. **单一职责**: 中介者只负责协调，不处理业务逻辑
2. **开闭原则**: 易于添加新的组件类型
3. **迪米特法则**: 组件只与中介者通信
4. **接口隔离**: 为不同类型的交互定义不同接口

### 性能优化
1. **异步处理**: 使用异步机制避免阻塞
2. **事件过滤**: 只处理必要的事件
3. **批量处理**: 合并相似的操作
4. **缓存机制**: 缓存频繁访问的数据

### 错误处理
1. **异常隔离**: 一个组件的错误不影响其他组件
2. **重试机制**: 对失败的操作进行重试
3. **降级策略**: 在中介者故障时的备用方案
4. **监控告警**: 及时发现和处理问题

## 📚 扩展阅读

- **《设计模式》**: GoF经典书籍中的中介者模式章节
- **《企业应用架构模式》**: Martin Fowler关于架构模式的论述
- **《微服务架构设计模式》**: 现代分布式系统中的中介者应用
- **《游戏编程模式》**: 游戏开发中的设计模式应用

## 🎯 练习建议

1. **实现聊天室**: 支持私聊、群聊、房间等功能
2. **设计工作流引擎**: 实现简单的审批流程
3. **构建事件系统**: 实现发布-订阅机制
4. **重构现有代码**: 识别并重构紧耦合的代码
