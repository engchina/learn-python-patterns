"""
02_text_editor.py - 文本编辑器命令模式实现

这个示例展示了如何在文本编辑器中使用命令模式来实现撤销/重做功能。
通过将每个编辑操作封装成命令对象，我们可以轻松地实现复杂的撤销和重做机制。
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import time


# ==================== 命令接口 ====================
class EditorCommand(ABC):
    """文本编辑器命令接口"""
    
    @abstractmethod
    def execute(self) -> str:
        """执行命令"""
        pass
    
    @abstractmethod
    def undo(self) -> str:
        """撤销命令"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取命令描述"""
        pass


# ==================== 接收者：文本编辑器 ====================
class TextEditor:
    """文本编辑器 - 命令接收者"""
    
    def __init__(self):
        self.content = ""
        self.cursor_position = 0
        self.selection_start = 0
        self.selection_end = 0
    
    def insert_text(self, text: str, position: Optional[int] = None) -> str:
        """在指定位置插入文本"""
        if position is None:
            position = self.cursor_position
        
        if 0 <= position <= len(self.content):
            self.content = self.content[:position] + text + self.content[position:]
            self.cursor_position = position + len(text)
            return f"在位置{position}插入文本: '{text}'"
        return f"错误: 位置{position}超出范围"
    
    def delete_text(self, start: int, length: int) -> tuple[str, str]:
        """删除指定范围的文本，返回删除的文本和操作描述"""
        if 0 <= start < len(self.content) and length > 0:
            end = min(start + length, len(self.content))
            deleted_text = self.content[start:end]
            self.content = self.content[:start] + self.content[end:]
            self.cursor_position = start
            return deleted_text, f"删除位置{start}到{end-1}的文本: '{deleted_text}'"
        return "", f"错误: 无法删除位置{start}长度{length}的文本"
    
    def replace_text(self, start: int, length: int, new_text: str) -> tuple[str, str]:
        """替换指定范围的文本，返回原文本和操作描述"""
        if 0 <= start < len(self.content):
            end = min(start + length, len(self.content))
            old_text = self.content[start:end]
            self.content = self.content[:start] + new_text + self.content[end:]
            self.cursor_position = start + len(new_text)
            return old_text, f"替换位置{start}到{end-1}的文本: '{old_text}' -> '{new_text}'"
        return "", f"错误: 无法替换位置{start}长度{length}的文本"
    
    def get_content(self) -> str:
        """获取文本内容"""
        return self.content
    
    def get_cursor_position(self) -> int:
        """获取光标位置"""
        return self.cursor_position
    
    def set_cursor_position(self, position: int):
        """设置光标位置"""
        if 0 <= position <= len(self.content):
            self.cursor_position = position
    
    def get_status(self) -> str:
        """获取编辑器状态"""
        return f"内容长度: {len(self.content)}, 光标位置: {self.cursor_position}, 内容: '{self.content}'"


# ==================== 具体命令实现 ====================
class InsertCommand(EditorCommand):
    """插入文本命令"""
    
    def __init__(self, editor: TextEditor, text: str, position: Optional[int] = None):
        self.editor = editor
        self.text = text
        self.position = position if position is not None else editor.get_cursor_position()
        self.executed = False
    
    def execute(self) -> str:
        result = self.editor.insert_text(self.text, self.position)
        self.executed = True
        return result
    
    def undo(self) -> str:
        if self.executed:
            deleted_text, result = self.editor.delete_text(self.position, len(self.text))
            return f"撤销插入: {result}"
        return "命令未执行，无法撤销"
    
    def get_description(self) -> str:
        return f"插入文本'{self.text}'在位置{self.position}"


class DeleteCommand(EditorCommand):
    """删除文本命令"""
    
    def __init__(self, editor: TextEditor, start: int, length: int):
        self.editor = editor
        self.start = start
        self.length = length
        self.deleted_text = ""
        self.executed = False
    
    def execute(self) -> str:
        self.deleted_text, result = self.editor.delete_text(self.start, self.length)
        self.executed = True
        return result
    
    def undo(self) -> str:
        if self.executed and self.deleted_text:
            result = self.editor.insert_text(self.deleted_text, self.start)
            return f"撤销删除: {result}"
        return "命令未执行或无删除内容，无法撤销"
    
    def get_description(self) -> str:
        return f"删除位置{self.start}长度{self.length}的文本"


class ReplaceCommand(EditorCommand):
    """替换文本命令"""
    
    def __init__(self, editor: TextEditor, start: int, length: int, new_text: str):
        self.editor = editor
        self.start = start
        self.length = length
        self.new_text = new_text
        self.old_text = ""
        self.executed = False
    
    def execute(self) -> str:
        self.old_text, result = self.editor.replace_text(self.start, self.length, self.new_text)
        self.executed = True
        return result
    
    def undo(self) -> str:
        if self.executed:
            _, result = self.editor.replace_text(self.start, len(self.new_text), self.old_text)
            return f"撤销替换: {result}"
        return "命令未执行，无法撤销"
    
    def get_description(self) -> str:
        return f"替换位置{self.start}长度{self.length}的文本为'{self.new_text}'"


# ==================== 调用者：编辑器控制器 ====================
class EditorController:
    """编辑器控制器 - 命令调用者"""
    
    def __init__(self, editor: TextEditor):
        self.editor = editor
        self.history: List[EditorCommand] = []
        self.current_position = -1
        self.max_history_size = 50
    
    def execute_command(self, command: EditorCommand) -> str:
        """执行命令并添加到历史记录"""
        result = command.execute()
        
        # 如果当前位置不在历史记录末尾，清除后面的记录
        if self.current_position < len(self.history) - 1:
            self.history = self.history[:self.current_position + 1]
        
        # 添加新命令到历史记录
        self.history.append(command)
        self.current_position += 1
        
        # 限制历史记录大小
        if len(self.history) > self.max_history_size:
            self.history.pop(0)
            self.current_position -= 1
        
        return result
    
    def undo(self) -> str:
        """撤销操作"""
        if self.current_position >= 0:
            command = self.history[self.current_position]
            result = command.undo()
            self.current_position -= 1
            return result
        return "没有可撤销的操作"
    
    def redo(self) -> str:
        """重做操作"""
        if self.current_position < len(self.history) - 1:
            self.current_position += 1
            command = self.history[self.current_position]
            result = command.execute()
            return f"重做: {result}"
        return "没有可重做的操作"
    
    def get_history(self) -> List[str]:
        """获取命令历史"""
        history_list = []
        for i, command in enumerate(self.history):
            marker = " -> " if i == self.current_position else "    "
            history_list.append(f"{marker}{i}: {command.get_description()}")
        return history_list
    
    def clear_history(self):
        """清空历史记录"""
        self.history.clear()
        self.current_position = -1
    
    def can_undo(self) -> bool:
        """是否可以撤销"""
        return self.current_position >= 0
    
    def can_redo(self) -> bool:
        """是否可以重做"""
        return self.current_position < len(self.history) - 1


# ==================== 演示函数 ====================
def demonstrate_text_editor():
    """演示文本编辑器命令模式"""
    print("=" * 60)
    print("文本编辑器命令模式演示")
    print("=" * 60)
    
    # 创建文本编辑器和控制器
    editor = TextEditor()
    controller = EditorController(editor)
    
    print("1. 初始状态:")
    print(f"   {editor.get_status()}")
    
    print("\n2. 执行一系列编辑操作:")
    
    # 插入文本
    insert1 = InsertCommand(editor, "Hello ")
    print(f"   {controller.execute_command(insert1)}")
    print(f"   {editor.get_status()}")
    
    insert2 = InsertCommand(editor, "World!")
    print(f"   {controller.execute_command(insert2)}")
    print(f"   {editor.get_status()}")
    
    # 插入换行和更多文本
    insert3 = InsertCommand(editor, "\n这是第二行。")
    print(f"   {controller.execute_command(insert3)}")
    print(f"   {editor.get_status()}")
    
    # 替换文本
    replace1 = ReplaceCommand(editor, 6, 6, "Python")  # 替换 "World!"
    print(f"   {controller.execute_command(replace1)}")
    print(f"   {editor.get_status()}")
    
    print("\n3. 命令历史:")
    for line in controller.get_history():
        print(f"   {line}")
    
    print("\n4. 执行撤销操作:")
    print(f"   {controller.undo()}")
    print(f"   {editor.get_status()}")
    
    print(f"   {controller.undo()}")
    print(f"   {editor.get_status()}")
    
    print("\n5. 执行重做操作:")
    print(f"   {controller.redo()}")
    print(f"   {editor.get_status()}")
    
    print("\n6. 删除操作:")
    delete1 = DeleteCommand(editor, 0, 6)  # 删除 "Hello "
    print(f"   {controller.execute_command(delete1)}")
    print(f"   {editor.get_status()}")
    
    print("\n7. 最终命令历史:")
    for line in controller.get_history():
        print(f"   {line}")
    
    print(f"\n8. 撤销能力: {controller.can_undo()}, 重做能力: {controller.can_redo()}")


def demonstrate_complex_editing():
    """演示复杂编辑场景"""
    print("\n" + "=" * 60)
    print("复杂编辑场景演示")
    print("=" * 60)
    
    editor = TextEditor()
    controller = EditorController(editor)
    
    # 模拟编写一段代码
    commands = [
        InsertCommand(editor, "def hello_world():\n"),
        InsertCommand(editor, "    print('Hello, World!')\n"),
        InsertCommand(editor, "\n"),
        InsertCommand(editor, "if __name__ == '__main__':\n"),
        InsertCommand(editor, "    hello_world()")
    ]
    
    print("编写Python代码:")
    for i, cmd in enumerate(commands):
        result = controller.execute_command(cmd)
        print(f"  步骤{i+1}: {result}")
    
    print(f"\n当前代码:\n{editor.get_content()}")
    
    # 修改函数名
    print("\n修改函数名:")
    replace_cmd = ReplaceCommand(editor, 4, 11, "greet_user")  # 替换 "hello_world"
    print(f"  {controller.execute_command(replace_cmd)}")
    
    # 修改调用
    replace_cmd2 = ReplaceCommand(editor, editor.get_content().rfind("hello_world"), 11, "greet_user")
    print(f"  {controller.execute_command(replace_cmd2)}")
    
    print(f"\n修改后的代码:\n{editor.get_content()}")
    
    # 撤销所有修改
    print("\n撤销最近的修改:")
    while controller.can_undo():
        result = controller.undo()
        print(f"  {result}")
        if "步骤1" in result or not controller.can_undo():
            break
    
    print(f"\n撤销后的代码:\n{editor.get_content()}")


if __name__ == "__main__":
    demonstrate_text_editor()
    demonstrate_complex_editing()
