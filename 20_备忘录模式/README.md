# 备忘录模式 (Memento Pattern)

备忘录模式是一种行为型设计模式，它在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态，以便以后当需要时能将该对象恢复到原先保存的状态。这种模式在现代软件开发中广泛应用，特别是在需要撤销/重做功能的应用中。

## 🎯 模式概述

备忘录模式的核心思想是"状态快照"。通过保存对象在某个时刻的状态快照，使得可以在需要时恢复到之前的状态。这种模式特别适用于需要撤销操作、状态回滚或历史记录功能的场景。

### 核心思想
- **状态保存**: 在不破坏封装的前提下保存对象状态
- **状态恢复**: 能够将对象恢复到之前保存的状态
- **历史管理**: 管理多个状态快照，支持多级撤销
- **封装保护**: 备忘录只能被创建它的对象访问

## 📁 文件列表

### 01_basic_memento.py
- **目的**: 备忘录模式的基础实现
- **内容**:
  - 文本编辑器的撤销/重做功能
  - 基本的状态保存和恢复机制
  - 历史记录管理
- **学习要点**:
  - 备忘录模式的核心概念
  - 发起人、备忘录、管理者三个角色
  - 状态的保存和恢复机制

### 02_document_editor.py
- **目的**: 文档编辑器中的备忘录应用
- **内容**:
  - 复杂文档状态的管理
  - 多种编辑操作的撤销
  - 文档版本历史
- **学习要点**:
  - 复杂对象状态的序列化
  - 增量备忘录的实现
  - 内存优化技巧

### 03_game_save_system.py
- **目的**: 游戏存档系统实现
- **内容**:
  - 游戏状态的完整保存
  - 多个存档槽管理
  - 自动保存机制
- **学习要点**:
  - 大型对象状态的管理
  - 存档的持久化存储
  - 版本兼容性处理

### 04_database_transaction.py
- **目的**: 数据库事务回滚模拟
- **内容**:
  - 事务状态的保存
  - 回滚机制的实现
  - 嵌套事务处理
- **学习要点**:
  - 事务性操作的备忘录应用
  - 原子性操作的保证
  - 错误恢复机制

### 05_configuration_manager.py
- **目的**: 配置管理系统
- **内容**:
  - 配置状态的版本管理
  - 配置回滚和恢复
  - 配置变更历史
- **学习要点**:
  - 配置管理中的备忘录应用
  - 配置验证和回滚
  - 系统配置的安全管理

### 06_real_world_examples.py
- **目的**: 实际应用场景示例
- **内容**:
  - 图形编辑器的操作历史
  - 工作流状态管理
  - 系统快照和恢复
- **学习要点**:
  - 备忘录在实际项目中的应用
  - 性能优化和内存管理
  - 复杂场景的设计考虑

## 🏗️ 模式结构

```
Originator (发起人)
    ├── state: Any
    ├── create_memento(): Memento
    ├── restore_from_memento(memento): void
    └── business_methods()

Memento (备忘录)
    ├── _state: Any (私有)
    ├── get_state(): Any (仅发起人可访问)
    └── timestamp: datetime

Caretaker (管理者)
    ├── history: List[Memento]
    ├── current_index: int
    ├── save_state(memento): void
    ├── undo(): Memento
    ├── redo(): Memento
    └── clear_history(): void
```

## 🎭 主要角色

- **Originator（发起人）**: 创建备忘录来记录当前状态，也可以使用备忘录恢复状态
- **Memento（备忘录）**: 存储发起人对象的内部状态，只有发起人可以访问其内容
- **Caretaker（管理者）**: 负责保存和管理备忘录，但不能访问备忘录的内容

## ✅ 模式优点

1. **状态恢复**: 提供了可靠的状态恢复机制
2. **封装保护**: 不破坏对象的封装性，外部无法直接访问状态
3. **历史管理**: 支持多级撤销/重做操作
4. **灵活性**: 可以选择性地保存状态快照
5. **简化设计**: 发起人不需要管理状态历史

## ⚠️ 注意事项

1. **内存消耗**: 大量备忘录会消耗大量内存
2. **性能开销**: 频繁创建备忘录可能影响性能
3. **深拷贝成本**: 复杂对象的状态保存成本较高
4. **生命周期管理**: 需要合理管理备忘录的数量和生命周期

## 🎯 使用场景

### 适合使用的场景
- **文本编辑器**: 撤销/重做功能
- **游戏开发**: 存档和读档系统
- **图形编辑**: 操作历史和撤销
- **数据库事务**: 事务回滚机制
- **配置管理**: 配置版本管理和回滚
- **工作流系统**: 流程状态的保存和恢复

### 不适合使用的场景
- 状态变化频繁且内存敏感的系统
- 状态数据量极大的应用
- 简单的状态管理需求

## 💡 快速开始

### 文本编辑器撤销功能
```python
from typing import List, Any
from datetime import datetime
import copy

class Memento:
    """备忘录类 - 存储状态快照"""
    def __init__(self, state: Any, description: str = ""):
        self._state = copy.deepcopy(state)
        self._timestamp = datetime.now()
        self._description = description

    def get_state(self) -> Any:
        return copy.deepcopy(self._state)

    def get_description(self) -> str:
        return self._description

class TextEditor:
    """文本编辑器 - 发起人"""
    def __init__(self):
        self._content = ""
        self._cursor_position = 0

    def write(self, text: str) -> None:
        """写入文本"""
        self._content += text
        self._cursor_position += len(text)
        print(f"📝 写入: '{text}' -> 内容: '{self._content}'")

    def delete(self, count: int = 1) -> None:
        """删除字符"""
        if len(self._content) >= count:
            deleted = self._content[-count:]
            self._content = self._content[:-count]
            self._cursor_position -= count
            print(f"🗑️ 删除: '{deleted}' -> 内容: '{self._content}'")

    def create_memento(self, description: str = "") -> Memento:
        """创建备忘录"""
        state = {
            'content': self._content,
            'cursor_position': self._cursor_position
        }
        return Memento(state, description)

    def restore_from_memento(self, memento: Memento) -> None:
        """从备忘录恢复"""
        state = memento.get_state()
        self._content = state['content']
        self._cursor_position = state['cursor_position']
        print(f"🔄 恢复: {memento.get_description()} -> '{self._content}'")

class EditorHistory:
    """编辑器历史管理器 - 管理者"""
    def __init__(self, max_history: int = 10):
        self._history: List[Memento] = []
        self._current_index = -1
        self._max_history = max_history

    def save_state(self, memento: Memento) -> None:
        """保存状态"""
        # 删除当前位置之后的历史
        if self._current_index < len(self._history) - 1:
            self._history = self._history[:self._current_index + 1]

        self._history.append(memento)
        self._current_index += 1

        # 限制历史数量
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._current_index -= 1

    def undo(self) -> Memento:
        """撤销"""
        if self._current_index > 0:
            self._current_index -= 1
            return self._history[self._current_index]
        return None

    def redo(self) -> Memento:
        """重做"""
        if self._current_index < len(self._history) - 1:
            self._current_index += 1
            return self._history[self._current_index]
        return None

# 使用示例
editor = TextEditor()
history = EditorHistory()

# 保存初始状态
history.save_state(editor.create_memento("初始状态"))

# 编辑操作
editor.write("Hello")
history.save_state(editor.create_memento("写入Hello"))

editor.write(" World")
history.save_state(editor.create_memento("写入World"))

# 撤销操作
memento = history.undo()
if memento:
    editor.restore_from_memento(memento)
```

### 文本编辑器备忘录示例
```python
from datetime import datetime

# 文本编辑器备忘录
class TextMemento:
    """文本编辑器备忘录"""
    def __init__(self, content: str, cursor_position: int, timestamp: datetime):
        self._content = content
        self._cursor_position = cursor_position
        self._timestamp = timestamp

    def get_content(self) -> str:
        return self._content

    def get_cursor_position(self) -> int:
        return self._cursor_position

    def get_timestamp(self) -> datetime:
        return self._timestamp

    def __str__(self):
        return f"备忘录[{self._timestamp.strftime('%H:%M:%S')}]: '{self._content[:20]}...'"

# 文本编辑器（发起人）
class TextEditor:
    """文本编辑器"""
    def __init__(self):
        self._content = ""
        self._cursor_position = 0

    def type_text(self, text: str):
        """输入文本"""
        # 在光标位置插入文本
        self._content = (self._content[:self._cursor_position] +
                        text +
                        self._content[self._cursor_position:])
        self._cursor_position += len(text)
        print(f"输入文本: '{text}' -> 当前内容: '{self._content}'")

    def delete_text(self, length: int):
        """删除文本"""
        if length > 0 and self._cursor_position >= length:
            self._content = (self._content[:self._cursor_position - length] +
                           self._content[self._cursor_position:])
            self._cursor_position -= length
            print(f"删除 {length} 个字符 -> 当前内容: '{self._content}'")

    def set_cursor_position(self, position: int):
        """设置光标位置"""
        if 0 <= position <= len(self._content):
            self._cursor_position = position
            print(f"光标移动到位置: {position}")

    def get_content(self) -> str:
        """获取内容"""
        return self._content

    def get_cursor_position(self) -> int:
        """获取光标位置"""
        return self._cursor_position

    def create_memento(self) -> TextMemento:
        """创建备忘录"""
        memento = TextMemento(self._content, self._cursor_position, datetime.now())
        print(f"创建备忘录: {memento}")
        return memento

    def restore_memento(self, memento: TextMemento):
        """恢复备忘录"""
        self._content = memento.get_content()
        self._cursor_position = memento.get_cursor_position()
        print(f"恢复到: {memento}")
        print(f"当前内容: '{self._content}', 光标位置: {self._cursor_position}")

# 历史记录管理器
class HistoryManager:
    """历史记录管理器"""
    def __init__(self, max_history: int = 10):
        self._history: List[TextMemento] = []
        self._current_index = -1
        self._max_history = max_history

    def save_state(self, memento: TextMemento):
        """保存状态"""
        # 如果当前不在历史记录的末尾，删除后面的记录
        if self._current_index < len(self._history) - 1:
            self._history = self._history[:self._current_index + 1]

        # 添加新的备忘录
        self._history.append(memento)
        self._current_index += 1

        # 限制历史记录数量
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._current_index -= 1

        print(f"保存状态，历史记录数: {len(self._history)}")

    def undo(self) -> Optional[TextMemento]:
        """撤销"""
        if self._current_index > 0:
            self._current_index -= 1
            memento = self._history[self._current_index]
            print(f"撤销到: {memento}")
            return memento
        else:
            print("没有可撤销的操作")
            return None

    def redo(self) -> Optional[TextMemento]:
        """重做"""
        if self._current_index < len(self._history) - 1:
            self._current_index += 1
            memento = self._history[self._current_index]
            print(f"重做到: {memento}")
            return memento
        else:
            print("没有可重做的操作")
            return None

    def can_undo(self) -> bool:
        """是否可以撤销"""
        return self._current_index > 0

    def can_redo(self) -> bool:
        """是否可以重做"""
        return self._current_index < len(self._history) - 1

    def get_history_info(self) -> str:
        """获取历史记录信息"""
        info = f"历史记录 ({len(self._history)} 项):\n"
        for i, memento in enumerate(self._history):
            marker = " -> " if i == self._current_index else "    "
            info += f"{marker}{i}: {memento}\n"
        return info

# 使用示例
def demo_text_editor():
    """文本编辑器备忘录演示"""
    editor = TextEditor()
    history = HistoryManager(max_history=5)

    print("=== 文本编辑器备忘录演示 ===")

    # 保存初始状态
    history.save_state(editor.create_memento())

    # 编辑操作
    print("\n--- 编辑操作 ---")
    editor.type_text("Hello")
    history.save_state(editor.create_memento())

    editor.type_text(" World")
    history.save_state(editor.create_memento())

    editor.type_text("!")
    history.save_state(editor.create_memento())

    editor.set_cursor_position(5)  # 移动到"Hello"后面
    editor.type_text(" Beautiful")
    history.save_state(editor.create_memento())

    print(f"\n当前内容: '{editor.get_content()}'")
    print(history.get_history_info())

    # 撤销操作
    print("\n--- 撤销操作 ---")
    for i in range(3):
        if history.can_undo():
            memento = history.undo()
            if memento:
                editor.restore_memento(memento)
        else:
            break

    # 重做操作
    print("\n--- 重做操作 ---")
    for i in range(2):
        if history.can_redo():
            memento = history.redo()
            if memento:
                editor.restore_memento(memento)
        else:
            break

    print(f"\n最终内容: '{editor.get_content()}'")
```

### 游戏存档备忘录示例
```python
import json
from typing import Dict, Any

# 游戏状态备忘录
class GameMemento:
    """游戏状态备忘录"""
    def __init__(self, save_data: Dict[str, Any], save_name: str):
        self._save_data = copy.deepcopy(save_data)
        self._save_name = save_name
        self._timestamp = datetime.now()

    def get_save_data(self) -> Dict[str, Any]:
        return copy.deepcopy(self._save_data)

    def get_save_name(self) -> str:
        return self._save_name

    def get_timestamp(self) -> datetime:
        return self._timestamp

    def __str__(self):
        return f"存档[{self._save_name}] - {self._timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

# 游戏状态（发起人）
class GameState:
    """游戏状态"""
    def __init__(self):
        self.player_name = ""
        self.level = 1
        self.score = 0
        self.health = 100
        self.inventory = []
        self.position = {"x": 0, "y": 0}
        self.achievements = []

    def set_player_name(self, name: str):
        """设置玩家姓名"""
        self.player_name = name
        print(f"玩家姓名设置为: {name}")

    def level_up(self):
        """升级"""
        self.level += 1
        self.health = 100  # 升级时恢复满血
        print(f"升级到等级 {self.level}！")

    def add_score(self, points: int):
        """增加分数"""
        self.score += points
        print(f"获得 {points} 分，总分: {self.score}")

    def take_damage(self, damage: int):
        """受到伤害"""
        self.health = max(0, self.health - damage)
        print(f"受到 {damage} 点伤害，剩余生命值: {self.health}")

    def add_item(self, item: str):
        """添加物品"""
        self.inventory.append(item)
        print(f"获得物品: {item}")

    def move_to(self, x: int, y: int):
        """移动到指定位置"""
        self.position = {"x": x, "y": y}
        print(f"移动到位置: ({x}, {y})")

    def unlock_achievement(self, achievement: str):
        """解锁成就"""
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            print(f"解锁成就: {achievement}")

    def create_memento(self, save_name: str) -> GameMemento:
        """创建游戏存档"""
        save_data = {
            "player_name": self.player_name,
            "level": self.level,
            "score": self.score,
            "health": self.health,
            "inventory": self.inventory.copy(),
            "position": self.position.copy(),
            "achievements": self.achievements.copy()
        }
        memento = GameMemento(save_data, save_name)
        print(f"创建存档: {memento}")
        return memento

    def restore_memento(self, memento: GameMemento):
        """加载游戏存档"""
        save_data = memento.get_save_data()
        self.player_name = save_data["player_name"]
        self.level = save_data["level"]
        self.score = save_data["score"]
        self.health = save_data["health"]
        self.inventory = save_data["inventory"]
        self.position = save_data["position"]
        self.achievements = save_data["achievements"]
        print(f"加载存档: {memento}")
        self.display_status()

    def display_status(self):
        """显示游戏状态"""
        print(f"=== 游戏状态 ===")
        print(f"玩家: {self.player_name}")
        print(f"等级: {self.level}")
        print(f"分数: {self.score}")
        print(f"生命值: {self.health}")
        print(f"位置: ({self.position['x']}, {self.position['y']})")
        print(f"物品: {self.inventory}")
        print(f"成就: {self.achievements}")

# 存档管理器
class SaveManager:
    """存档管理器"""
    def __init__(self):
        self._saves: Dict[str, GameMemento] = {}
        self._auto_saves: List[GameMemento] = []
        self._max_auto_saves = 3

    def save_game(self, memento: GameMemento):
        """保存游戏"""
        self._saves[memento.get_save_name()] = memento
        print(f"游戏已保存: {memento.get_save_name()}")

    def load_game(self, save_name: str) -> Optional[GameMemento]:
        """加载游戏"""
        if save_name in self._saves:
            return self._saves[save_name]
        else:
            print(f"存档不存在: {save_name}")
            return None

    def auto_save(self, memento: GameMemento):
        """自动保存"""
        self._auto_saves.append(memento)
        if len(self._auto_saves) > self._max_auto_saves:
            self._auto_saves.pop(0)
        print(f"自动保存完成，自动存档数: {len(self._auto_saves)}")

    def get_latest_auto_save(self) -> Optional[GameMemento]:
        """获取最新的自动存档"""
        if self._auto_saves:
            return self._auto_saves[-1]
        return None

    def list_saves(self):
        """列出所有存档"""
        print("\n=== 存档列表 ===")
        if self._saves:
            for name, memento in self._saves.items():
                print(f"  {memento}")
        else:
            print("  没有存档")

        if self._auto_saves:
            print("\n自动存档:")
            for i, memento in enumerate(self._auto_saves):
                print(f"  自动存档{i+1}: {memento}")

    def delete_save(self, save_name: str):
        """删除存档"""
        if save_name in self._saves:
            del self._saves[save_name]
            print(f"删除存档: {save_name}")
        else:
            print(f"存档不存在: {save_name}")

# 使用示例
def demo_game_save():
    """游戏存档备忘录演示"""
    game = GameState()
    save_manager = SaveManager()

    print("=== 游戏存档备忘录演示 ===")

    # 初始化游戏
    game.set_player_name("勇士")
    game.display_status()

    # 游戏进程1
    print("\n--- 游戏进程1 ---")
    game.add_score(100)
    game.add_item("铁剑")
    game.move_to(10, 5)
    save_manager.save_game(game.create_memento("新手村"))

    # 游戏进程2
    print("\n--- 游戏进程2 ---")
    game.level_up()
    game.add_score(200)
    game.add_item("魔法药水")
    game.move_to(25, 15)
    game.unlock_achievement("初次升级")
    save_manager.save_game(game.create_memento("森林入口"))
    save_manager.auto_save(game.create_memento("自动存档"))

    # 游戏进程3（危险区域）
    print("\n--- 游戏进程3（危险区域）---")
    game.move_to(50, 30)
    game.take_damage(80)  # 受到重伤
    game.add_score(50)

    print("\n当前状态（受伤）:")
    game.display_status()

    # 列出存档
    save_manager.list_saves()

    # 加载之前的存档
    print("\n--- 加载存档 ---")
    memento = save_manager.load_game("森林入口")
    if memento:
        game.restore_memento(memento)

    # 继续游戏
    print("\n--- 继续游戏 ---")
    game.add_item("治疗药水")
    game.unlock_achievement("明智的选择")
    save_manager.auto_save(game.create_memento("自动存档"))

    # 最终状态
    print("\n--- 最终状态 ---")
    game.display_status()
    save_manager.list_saves()
```

## 🚀 运行方法

```bash
# 基础备忘录概念
python "01_basic_memento.py"

# 文档编辑器应用
python "02_document_editor.py"

# 游戏存档系统
python "03_game_save_system.py"

# 数据库事务回滚
python "04_database_transaction.py"

# 配置管理系统
python "05_configuration_manager.py"

# 实际应用案例
python "06_real_world_examples.py"
```

## 🎓 学习路径

### 初学者
1. 从 `01_basic_memento.py` 开始，理解备忘录的基本概念
2. 学习 `02_document_editor.py`，掌握复杂状态的管理
3. 练习 `03_game_save_system.py` 中的持久化存储

### 进阶开发者
1. 深入研究 `04_database_transaction.py` 的事务处理机制
2. 分析 `05_configuration_manager.py` 的版本管理策略
3. 结合 `06_real_world_examples.py` 优化现有项目

### 架构师
1. 理解备忘录在系统设计中的作用
2. 掌握大型系统的状态管理策略
3. 设计高效的快照和恢复机制

## 🌟 实际应用场景

### 软件开发
- **IDE编辑器**: 代码编辑的撤销/重做功能
- **版本控制**: Git等版本控制系统的快照机制
- **调试工具**: 程序状态的保存和回放

### 游戏开发
- **存档系统**: 游戏进度的保存和加载
- **关卡编辑器**: 编辑操作的撤销功能
- **回放系统**: 游戏过程的录制和回放

### 企业应用
- **工作流系统**: 流程状态的检查点机制
- **配置管理**: 系统配置的版本控制
- **数据备份**: 数据库的快照和恢复

## 🔗 与其他模式的关系

- **📋 命令模式**: 常与备忘录结合实现撤销功能
- **🎭 原型模式**: 可以用原型模式来创建备忘录
- **🔄 迭代器模式**: 用来遍历备忘录历史
- **🎯 状态模式**: 备忘录可以保存状态对象
- **🏭 工厂方法**: 创建不同类型的备忘录

## ⚠️ 最佳实践

### 内存管理
1. **限制数量**: 设置备忘录的最大数量
2. **压缩存储**: 对大型状态进行压缩
3. **增量备份**: 只保存变化的部分
4. **定期清理**: 自动清理过期的备忘录

### 性能优化
1. **延迟创建**: 按需创建备忘录
2. **浅拷贝优化**: 对不变数据使用浅拷贝
3. **异步处理**: 异步创建和保存备忘录
4. **缓存机制**: 缓存频繁访问的状态

### 设计考虑
1. **封装保护**: 确保备忘录不破坏封装性
2. **版本兼容**: 处理不同版本间的兼容性
3. **错误恢复**: 处理备忘录损坏的情况
4. **并发安全**: 多线程环境下的安全性

## 📚 扩展阅读

- **《设计模式》**: GoF经典书籍中的备忘录模式章节
- **《重构》**: Martin Fowler关于代码重构的论述
- **《数据库系统概念》**: 事务处理和恢复机制
- **《游戏编程模式》**: 游戏开发中的状态管理

## 🎯 练习建议

1. **实现文本编辑器**: 支持多级撤销/重做功能
2. **设计游戏存档**: 实现完整的游戏状态保存
3. **构建配置系统**: 实现配置的版本管理
4. **优化内存使用**: 实现高效的备忘录管理策略
