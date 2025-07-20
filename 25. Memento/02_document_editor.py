#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文档编辑器中的备忘录应用

本模块演示了备忘录模式在复杂文档编辑器中的应用，包括：
1. 复杂文档状态的管理
2. 多种编辑操作的撤销
3. 文档版本历史
4. 增量备忘录的实现

作者: Assistant
日期: 2024-01-20
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import copy
import json


class OperationType(Enum):
    """操作类型枚举"""
    INSERT_TEXT = "插入文本"
    DELETE_TEXT = "删除文本"
    FORMAT_TEXT = "格式化文本"
    INSERT_IMAGE = "插入图片"
    DELETE_IMAGE = "删除图片"
    MOVE_IMAGE = "移动图片"
    CHANGE_STYLE = "修改样式"


@dataclass
class TextFormat:
    """文本格式"""
    bold: bool = False
    italic: bool = False
    underline: bool = False
    font_size: int = 12
    font_family: str = "Arial"
    color: str = "#000000"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline,
            'font_size': self.font_size,
            'font_family': self.font_family,
            'color': self.color
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextFormat':
        return cls(**data)


@dataclass
class TextSegment:
    """文本片段"""
    content: str
    format: TextFormat
    start_pos: int
    end_pos: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'content': self.content,
            'format': self.format.to_dict(),
            'start_pos': self.start_pos,
            'end_pos': self.end_pos
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextSegment':
        return cls(
            content=data['content'],
            format=TextFormat.from_dict(data['format']),
            start_pos=data['start_pos'],
            end_pos=data['end_pos']
        )


@dataclass
class Image:
    """图片对象"""
    id: str
    path: str
    x: int
    y: int
    width: int
    height: int
    alt_text: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'path': self.path,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'alt_text': self.alt_text
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Image':
        return cls(**data)


class DocumentMemento:
    """文档备忘录"""
    
    def __init__(self, document_state: Dict[str, Any], operation_type: OperationType, description: str):
        self._state = copy.deepcopy(document_state)
        self._operation_type = operation_type
        self._description = description
        self._timestamp = datetime.now()
        self._size = self._calculate_size()
    
    def get_state(self) -> Dict[str, Any]:
        """获取状态"""
        return copy.deepcopy(self._state)
    
    def get_operation_type(self) -> OperationType:
        """获取操作类型"""
        return self._operation_type
    
    def get_description(self) -> str:
        """获取描述"""
        return self._description
    
    def get_timestamp(self) -> datetime:
        """获取时间戳"""
        return self._timestamp
    
    def get_size(self) -> int:
        """获取备忘录大小（字节）"""
        return self._size
    
    def _calculate_size(self) -> int:
        """计算备忘录大小"""
        try:
            # 简单估算：将状态序列化为JSON并计算字节数
            json_str = json.dumps(self._state, default=str)
            return len(json_str.encode('utf-8'))
        except:
            return 0
    
    def __str__(self) -> str:
        return f"{self._operation_type.value}: {self._description} [{self._timestamp.strftime('%H:%M:%S')}]"


class Document:
    """文档类 - 发起人"""
    
    def __init__(self, title: str = "新文档"):
        self.title = title
        self.text_segments: List[TextSegment] = []
        self.images: List[Image] = []
        self.cursor_position = 0
        self.selection_start = 0
        self.selection_end = 0
        self.default_format = TextFormat()
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
    
    def insert_text(self, text: str, position: int = None, format: TextFormat = None) -> None:
        """插入文本"""
        if position is None:
            position = self.cursor_position
        
        if format is None:
            format = copy.deepcopy(self.default_format)
        
        # 创建新的文本片段
        segment = TextSegment(
            content=text,
            format=format,
            start_pos=position,
            end_pos=position + len(text)
        )
        
        # 更新其他片段的位置
        for seg in self.text_segments:
            if seg.start_pos >= position:
                seg.start_pos += len(text)
                seg.end_pos += len(text)
        
        self.text_segments.append(segment)
        self.cursor_position = position + len(text)
        self.modified_at = datetime.now()
        
        print(f"📝 插入文本: '{text}' 在位置 {position}")
    
    def delete_text(self, start: int, end: int) -> str:
        """删除文本"""
        deleted_content = ""
        segments_to_remove = []
        
        for segment in self.text_segments:
            # 检查片段是否在删除范围内
            if segment.end_pos <= start or segment.start_pos >= end:
                # 片段不在删除范围内，但可能需要调整位置
                if segment.start_pos >= end:
                    segment.start_pos -= (end - start)
                    segment.end_pos -= (end - start)
            elif segment.start_pos >= start and segment.end_pos <= end:
                # 片段完全在删除范围内
                deleted_content += segment.content
                segments_to_remove.append(segment)
            else:
                # 片段部分在删除范围内（复杂情况，简化处理）
                deleted_content += segment.content
                segments_to_remove.append(segment)
        
        # 移除被删除的片段
        for segment in segments_to_remove:
            self.text_segments.remove(segment)
        
        self.cursor_position = start
        self.modified_at = datetime.now()
        
        print(f"🗑️ 删除文本: '{deleted_content}' 从位置 {start} 到 {end}")
        return deleted_content
    
    def format_text(self, start: int, end: int, format: TextFormat) -> None:
        """格式化文本"""
        for segment in self.text_segments:
            # 检查片段是否在格式化范围内
            if (segment.start_pos < end and segment.end_pos > start):
                segment.format = copy.deepcopy(format)
        
        self.modified_at = datetime.now()
        print(f"🎨 格式化文本: 位置 {start}-{end}")
    
    def insert_image(self, image: Image) -> None:
        """插入图片"""
        self.images.append(image)
        self.modified_at = datetime.now()
        print(f"🖼️ 插入图片: {image.id} 在位置 ({image.x}, {image.y})")
    
    def delete_image(self, image_id: str) -> bool:
        """删除图片"""
        for i, image in enumerate(self.images):
            if image.id == image_id:
                deleted_image = self.images.pop(i)
                self.modified_at = datetime.now()
                print(f"🗑️ 删除图片: {image_id}")
                return True
        return False
    
    def move_image(self, image_id: str, new_x: int, new_y: int) -> bool:
        """移动图片"""
        for image in self.images:
            if image.id == image_id:
                old_x, old_y = image.x, image.y
                image.x = new_x
                image.y = new_y
                self.modified_at = datetime.now()
                print(f"📦 移动图片: {image_id} 从 ({old_x}, {old_y}) 到 ({new_x}, {new_y})")
                return True
        return False
    
    def create_memento(self, operation_type: OperationType, description: str) -> DocumentMemento:
        """创建备忘录"""
        state = {
            'title': self.title,
            'text_segments': [seg.to_dict() for seg in self.text_segments],
            'images': [img.to_dict() for img in self.images],
            'cursor_position': self.cursor_position,
            'selection_start': self.selection_start,
            'selection_end': self.selection_end,
            'default_format': self.default_format.to_dict(),
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat()
        }
        
        memento = DocumentMemento(state, operation_type, description)
        print(f"💾 创建备忘录: {description} (大小: {memento.get_size()} 字节)")
        return memento
    
    def restore_from_memento(self, memento: DocumentMemento) -> None:
        """从备忘录恢复"""
        state = memento.get_state()
        
        self.title = state['title']
        self.text_segments = [TextSegment.from_dict(seg) for seg in state['text_segments']]
        self.images = [Image.from_dict(img) for img in state['images']]
        self.cursor_position = state['cursor_position']
        self.selection_start = state['selection_start']
        self.selection_end = state['selection_end']
        self.default_format = TextFormat.from_dict(state['default_format'])
        self.created_at = datetime.fromisoformat(state['created_at'])
        self.modified_at = datetime.fromisoformat(state['modified_at'])
        
        print(f"🔄 恢复文档状态: {memento.get_description()}")
    
    def get_content_summary(self) -> str:
        """获取内容摘要"""
        text_length = sum(len(seg.content) for seg in self.text_segments)
        image_count = len(self.images)
        return f"文本: {text_length} 字符, 图片: {image_count} 个"
    
    def get_full_text(self) -> str:
        """获取完整文本"""
        # 按位置排序文本片段
        sorted_segments = sorted(self.text_segments, key=lambda x: x.start_pos)
        return ''.join(seg.content for seg in sorted_segments)


class DocumentHistory:
    """文档历史管理器"""
    
    def __init__(self, max_history: int = 20, max_memory_mb: int = 50):
        self.history: List[DocumentMemento] = []
        self.current_index = -1
        self.max_history = max_history
        self.max_memory_bytes = max_memory_mb * 1024 * 1024  # 转换为字节
    
    def save_state(self, memento: DocumentMemento) -> None:
        """保存状态"""
        # 如果不在历史末尾，删除后面的历史
        if self.current_index < len(self.history) - 1:
            removed_count = len(self.history) - self.current_index - 1
            self.history = self.history[:self.current_index + 1]
            print(f"🗑️ 删除 {removed_count} 个后续历史记录")
        
        # 添加新备忘录
        self.history.append(memento)
        self.current_index += 1
        
        # 检查内存限制
        self._manage_memory()
        
        print(f"📚 保存历史: {memento} ({self.current_index + 1}/{len(self.history)})")
    
    def _manage_memory(self) -> None:
        """管理内存使用"""
        # 计算总内存使用
        total_size = sum(m.get_size() for m in self.history)
        
        # 如果超过内存限制或数量限制，删除最旧的记录
        while (len(self.history) > self.max_history or 
               total_size > self.max_memory_bytes) and len(self.history) > 1:
            
            removed = self.history.pop(0)
            self.current_index -= 1
            total_size -= removed.get_size()
            print(f"🗑️ 删除旧历史记录: {removed} (内存管理)")
    
    def undo(self) -> Optional[DocumentMemento]:
        """撤销"""
        if self.current_index > 0:
            self.current_index -= 1
            memento = self.history[self.current_index]
            print(f"↶ 撤销到: {memento}")
            return memento
        else:
            print("⚠️ 无法撤销：已到达历史起点")
            return None
    
    def redo(self) -> Optional[DocumentMemento]:
        """重做"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            memento = self.history[self.current_index]
            print(f"↷ 重做到: {memento}")
            return memento
        else:
            print("⚠️ 无法重做：已到达历史终点")
            return None
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """获取内存使用情况"""
        total_size = sum(m.get_size() for m in self.history)
        return {
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'count': len(self.history),
            'max_count': self.max_history,
            'max_size_mb': self.max_memory_bytes / (1024 * 1024),
            'usage_percent': (total_size / self.max_memory_bytes) * 100
        }
    
    def get_history_summary(self) -> List[str]:
        """获取历史摘要"""
        summary = []
        for i, memento in enumerate(self.history):
            marker = " -> " if i == self.current_index else "    "
            size_kb = memento.get_size() / 1024
            summary.append(f"{marker}{i + 1}. {memento} ({size_kb:.1f}KB)")
        return summary


def demo_document_editor():
    """演示文档编辑器"""
    print("=" * 50)
    print("📄 文档编辑器备忘录演示")
    print("=" * 50)
    
    # 创建文档和历史管理器
    doc = Document("我的文档")
    history = DocumentHistory(max_history=10, max_memory_mb=5)
    
    # 保存初始状态
    initial_memento = doc.create_memento(OperationType.CHANGE_STYLE, "初始状态")
    history.save_state(initial_memento)
    
    print("\n📝 开始编辑文档:")
    
    # 插入文本
    doc.insert_text("Hello World!", 0)
    memento = doc.create_memento(OperationType.INSERT_TEXT, "插入标题")
    history.save_state(memento)
    
    # 插入更多文本
    doc.insert_text("\n这是一个测试文档。", doc.cursor_position)
    memento = doc.create_memento(OperationType.INSERT_TEXT, "插入内容")
    history.save_state(memento)
    
    # 格式化文本
    bold_format = TextFormat(bold=True, font_size=16)
    doc.format_text(0, 12, bold_format)
    memento = doc.create_memento(OperationType.FORMAT_TEXT, "标题加粗")
    history.save_state(memento)
    
    # 插入图片
    image = Image("img1", "/path/to/image.jpg", 100, 200, 300, 200, "测试图片")
    doc.insert_image(image)
    memento = doc.create_memento(OperationType.INSERT_IMAGE, "插入图片")
    history.save_state(memento)
    
    print(f"\n📊 文档内容: {doc.get_content_summary()}")
    print(f"📊 内存使用: {history.get_memory_usage()}")
    
    # 显示历史
    print("\n📚 编辑历史:")
    for item in history.get_history_summary():
        print(item)
    
    print("\n↶ 执行撤销操作:")
    for _ in range(2):
        memento = history.undo()
        if memento:
            doc.restore_from_memento(memento)
            print(f"📊 当前内容: {doc.get_content_summary()}")
    
    print("\n↷ 执行重做操作:")
    memento = history.redo()
    if memento:
        doc.restore_from_memento(memento)
        print(f"📊 当前内容: {doc.get_content_summary()}")


if __name__ == "__main__":
    print("🎯 文档编辑器备忘录模式演示")
    
    demo_document_editor()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 复杂文档的备忘录需要考虑内存管理和性能优化")
    print("=" * 50)
