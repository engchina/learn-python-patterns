#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
备忘录模式基础实现

本模块演示了备忘录模式的基本概念和实现方式，包括：
1. 文本编辑器的撤销/重做功能
2. 基本的状态保存和恢复机制
3. 历史记录管理
4. 备忘录模式的核心概念

作者: Assistant
日期: 2024-01-20
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from datetime import datetime
import copy


class Memento:
    """备忘录类 - 存储发起人的状态快照"""
    
    def __init__(self, state: Any, description: str = ""):
        self._state = copy.deepcopy(state)  # 深拷贝确保状态独立
        self._timestamp = datetime.now()
        self._description = description
    
    def get_state(self) -> Any:
        """获取状态（仅发起人可调用）"""
        return copy.deepcopy(self._state)
    
    def get_timestamp(self) -> datetime:
        """获取创建时间"""
        return self._timestamp
    
    def get_description(self) -> str:
        """获取描述"""
        return self._description
    
    def __str__(self) -> str:
        return f"备忘录[{self._timestamp.strftime('%H:%M:%S')}]: {self._description}"


class TextEditor:
    """文本编辑器 - 发起人角色"""
    
    def __init__(self):
        self._content = ""
        self._cursor_position = 0
        self._font_size = 12
        self._font_family = "Arial"
        
    def write(self, text: str) -> None:
        """写入文本"""
        before_content = self._content
        self._content = (self._content[:self._cursor_position] + 
                        text + 
                        self._content[self._cursor_position:])
        self._cursor_position += len(text)
        
        print(f"✏️ 写入文本: '{text}'")
        print(f"📝 当前内容: '{self._content}'")
    
    def delete(self, count: int = 1) -> None:
        """删除字符"""
        if self._cursor_position >= count:
            deleted_text = self._content[self._cursor_position - count:self._cursor_position]
            self._content = (self._content[:self._cursor_position - count] + 
                           self._content[self._cursor_position:])
            self._cursor_position -= count
            
            print(f"🗑️ 删除文本: '{deleted_text}'")
            print(f"📝 当前内容: '{self._content}'")
    
    def set_cursor_position(self, position: int) -> None:
        """设置光标位置"""
        if 0 <= position <= len(self._content):
            self._cursor_position = position
            print(f"📍 光标位置: {position}")
    
    def set_font_size(self, size: int) -> None:
        """设置字体大小"""
        self._font_size = size
        print(f"🔤 字体大小: {size}")
    
    def set_font_family(self, family: str) -> None:
        """设置字体族"""
        self._font_family = family
        print(f"🔤 字体族: {family}")
    
    def create_memento(self, description: str = "") -> Memento:
        """创建备忘录"""
        state = {
            'content': self._content,
            'cursor_position': self._cursor_position,
            'font_size': self._font_size,
            'font_family': self._font_family
        }
        
        if not description:
            description = f"内容长度: {len(self._content)}"
        
        memento = Memento(state, description)
        print(f"💾 创建备忘录: {description}")
        return memento
    
    def restore_from_memento(self, memento: Memento) -> None:
        """从备忘录恢复状态"""
        state = memento.get_state()
        self._content = state['content']
        self._cursor_position = state['cursor_position']
        self._font_size = state['font_size']
        self._font_family = state['font_family']
        
        print(f"🔄 恢复状态: {memento.get_description()}")
        print(f"📝 恢复后内容: '{self._content}'")
    
    def get_status(self) -> dict:
        """获取当前状态信息"""
        return {
            'content': self._content,
            'cursor_position': self._cursor_position,
            'font_size': self._font_size,
            'font_family': self._font_family,
            'content_length': len(self._content)
        }


class EditorHistory:
    """编辑器历史管理器 - 管理者角色"""
    
    def __init__(self, max_history: int = 10):
        self._history: List[Memento] = []
        self._current_index = -1  # 当前位置索引
        self._max_history = max_history
    
    def save_state(self, memento: Memento) -> None:
        """保存状态"""
        # 如果当前不在历史末尾，删除后面的历史
        if self._current_index < len(self._history) - 1:
            self._history = self._history[:self._current_index + 1]
        
        # 添加新的备忘录
        self._history.append(memento)
        self._current_index += 1
        
        # 限制历史记录数量
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._current_index -= 1
        
        print(f"📚 保存历史记录 ({self._current_index + 1}/{len(self._history)})")
    
    def undo(self) -> Optional[Memento]:
        """撤销操作"""
        if self._current_index > 0:
            self._current_index -= 1
            memento = self._history[self._current_index]
            print(f"↶ 撤销到: {memento}")
            return memento
        else:
            print("⚠️ 无法撤销：已到达历史起点")
            return None
    
    def redo(self) -> Optional[Memento]:
        """重做操作"""
        if self._current_index < len(self._history) - 1:
            self._current_index += 1
            memento = self._history[self._current_index]
            print(f"↷ 重做到: {memento}")
            return memento
        else:
            print("⚠️ 无法重做：已到达历史终点")
            return None
    
    def can_undo(self) -> bool:
        """检查是否可以撤销"""
        return self._current_index > 0
    
    def can_redo(self) -> bool:
        """检查是否可以重做"""
        return self._current_index < len(self._history) - 1
    
    def get_history_info(self) -> dict:
        """获取历史信息"""
        return {
            'total_count': len(self._history),
            'current_index': self._current_index,
            'can_undo': self.can_undo(),
            'can_redo': self.can_redo(),
            'max_history': self._max_history
        }
    
    def get_history_list(self) -> List[str]:
        """获取历史记录列表"""
        history_list = []
        for i, memento in enumerate(self._history):
            marker = " -> " if i == self._current_index else "    "
            history_list.append(f"{marker}{i + 1}. {memento}")
        return history_list
    
    def clear_history(self) -> None:
        """清空历史记录"""
        self._history.clear()
        self._current_index = -1
        print("🗑️ 历史记录已清空")


class TextEditorWithHistory:
    """带历史记录的文本编辑器"""
    
    def __init__(self, max_history: int = 10):
        self._editor = TextEditor()
        self._history = EditorHistory(max_history)
        
        # 保存初始状态
        initial_memento = self._editor.create_memento("初始状态")
        self._history.save_state(initial_memento)
    
    def write(self, text: str) -> None:
        """写入文本并保存状态"""
        self._editor.write(text)
        memento = self._editor.create_memento(f"写入: '{text}'")
        self._history.save_state(memento)
    
    def delete(self, count: int = 1) -> None:
        """删除字符并保存状态"""
        self._editor.delete(count)
        memento = self._editor.create_memento(f"删除 {count} 个字符")
        self._history.save_state(memento)
    
    def set_cursor_position(self, position: int) -> None:
        """设置光标位置并保存状态"""
        self._editor.set_cursor_position(position)
        memento = self._editor.create_memento(f"光标移动到 {position}")
        self._history.save_state(memento)
    
    def set_font_size(self, size: int) -> None:
        """设置字体大小并保存状态"""
        self._editor.set_font_size(size)
        memento = self._editor.create_memento(f"字体大小: {size}")
        self._history.save_state(memento)
    
    def undo(self) -> bool:
        """撤销操作"""
        memento = self._history.undo()
        if memento:
            self._editor.restore_from_memento(memento)
            return True
        return False
    
    def redo(self) -> bool:
        """重做操作"""
        memento = self._history.redo()
        if memento:
            self._editor.restore_from_memento(memento)
            return True
        return False
    
    def get_status(self) -> dict:
        """获取编辑器状态"""
        editor_status = self._editor.get_status()
        history_info = self._history.get_history_info()
        
        return {
            'editor': editor_status,
            'history': history_info
        }
    
    def show_history(self) -> None:
        """显示历史记录"""
        print("\n📚 历史记录:")
        history_list = self._history.get_history_list()
        for item in history_list:
            print(item)


def demo_basic_memento():
    """演示基本备忘录功能"""
    print("=" * 50)
    print("📝 基本备忘录模式演示")
    print("=" * 50)
    
    # 创建带历史记录的文本编辑器
    editor = TextEditorWithHistory(max_history=5)
    
    print("\n📝 开始编辑文档:")
    
    # 编辑操作
    editor.write("Hello")
    editor.write(" World")
    editor.write("!")
    
    # 显示当前状态
    print(f"\n📊 当前状态: {editor.get_status()}")
    
    # 显示历史记录
    editor.show_history()
    
    print("\n↶ 执行撤销操作:")
    editor.undo()
    editor.undo()
    
    print("\n↷ 执行重做操作:")
    editor.redo()
    
    print("\n🔤 修改格式:")
    editor.set_font_size(16)
    editor.set_cursor_position(5)
    
    print("\n📝 继续编辑:")
    editor.write(" Python")
    
    # 最终状态
    print(f"\n📊 最终状态: {editor.get_status()}")
    editor.show_history()


def demo_memento_components():
    """演示备忘录模式的各个组件"""
    print("\n" + "=" * 50)
    print("🔧 备忘录模式组件演示")
    print("=" * 50)
    
    # 1. 发起人（Originator）
    print("\n1️⃣ 发起人 - TextEditor:")
    editor = TextEditor()
    editor.write("测试文本")
    editor.set_font_size(14)
    
    # 2. 备忘录（Memento）
    print("\n2️⃣ 备忘录 - Memento:")
    memento1 = editor.create_memento("第一个快照")
    
    # 修改状态
    editor.write(" - 修改后")
    editor.set_font_size(18)
    
    memento2 = editor.create_memento("第二个快照")
    
    # 3. 管理者（Caretaker）
    print("\n3️⃣ 管理者 - EditorHistory:")
    history = EditorHistory(max_history=3)
    history.save_state(memento1)
    history.save_state(memento2)
    
    # 继续修改并保存
    editor.delete(5)
    memento3 = editor.create_memento("第三个快照")
    history.save_state(memento3)
    
    print(f"\n📊 历史信息: {history.get_history_info()}")
    
    # 演示撤销和重做
    print("\n🔄 状态恢复演示:")
    
    # 撤销到第二个状态
    memento = history.undo()
    if memento:
        editor.restore_from_memento(memento)
    
    # 撤销到第一个状态
    memento = history.undo()
    if memento:
        editor.restore_from_memento(memento)
    
    # 重做
    memento = history.redo()
    if memento:
        editor.restore_from_memento(memento)


if __name__ == "__main__":
    print("🎯 备忘录模式基础实现演示")
    
    # 运行演示
    demo_basic_memento()
    demo_memento_components()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 备忘录模式提供了强大的状态管理和恢复机制")
    print("=" * 50)
