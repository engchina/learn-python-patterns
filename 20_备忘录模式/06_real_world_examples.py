#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
备忘录模式实际应用场景示例

本模块演示了备忘录模式在实际项目中的应用，包括：
1. 图形编辑器的操作历史
2. 工作流状态管理
3. 系统快照和恢复
4. 性能优化和内存管理

作者: Assistant
日期: 2024-01-20
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
import copy
import json
import threading
import time


# ==================== 图形编辑器示例 ====================

class ShapeType(Enum):
    """图形类型"""
    RECTANGLE = "矩形"
    CIRCLE = "圆形"
    LINE = "直线"
    TEXT = "文本"


@dataclass
class Shape:
    """图形对象"""
    id: str
    shape_type: ShapeType
    x: float
    y: float
    width: float = 0
    height: float = 0
    color: str = "#000000"
    text: str = ""
    
    def copy(self) -> 'Shape':
        return copy.deepcopy(self)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'shape_type': self.shape_type.value,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'color': self.color,
            'text': self.text
        }


class CanvasMemento:
    """画布备忘录"""
    
    def __init__(self, shapes: List[Shape], operation: str):
        self._shapes = [shape.copy() for shape in shapes]
        self._operation = operation
        self._timestamp = datetime.now()
        self._memory_size = self._calculate_memory_size()
    
    def get_shapes(self) -> List[Shape]:
        return [shape.copy() for shape in self._shapes]
    
    def get_operation(self) -> str:
        return self._operation
    
    def get_timestamp(self) -> datetime:
        return self._timestamp
    
    def get_memory_size(self) -> int:
        return self._memory_size
    
    def _calculate_memory_size(self) -> int:
        """估算内存大小"""
        return len(json.dumps([shape.to_dict() for shape in self._shapes]))
    
    def __str__(self) -> str:
        return f"{self._operation} [{self._timestamp.strftime('%H:%M:%S')}] ({len(self._shapes)} 个图形)"


class GraphicsEditor:
    """图形编辑器"""
    
    def __init__(self):
        self.shapes: List[Shape] = []
        self.selected_shapes: List[str] = []
        self.canvas_width = 800
        self.canvas_height = 600
        self.zoom_level = 1.0
        self.next_shape_id = 1
    
    def add_shape(self, shape: Shape) -> None:
        """添加图形"""
        shape.id = f"shape_{self.next_shape_id}"
        self.next_shape_id += 1
        self.shapes.append(shape)
        print(f"➕ 添加图形: {shape.shape_type.value} ({shape.id})")
    
    def remove_shape(self, shape_id: str) -> bool:
        """删除图形"""
        for i, shape in enumerate(self.shapes):
            if shape.id == shape_id:
                removed_shape = self.shapes.pop(i)
                if shape_id in self.selected_shapes:
                    self.selected_shapes.remove(shape_id)
                print(f"🗑️ 删除图形: {removed_shape.shape_type.value} ({shape_id})")
                return True
        return False
    
    def move_shape(self, shape_id: str, dx: float, dy: float) -> bool:
        """移动图形"""
        for shape in self.shapes:
            if shape.id == shape_id:
                shape.x += dx
                shape.y += dy
                print(f"📦 移动图形: {shape_id} 偏移 ({dx}, {dy})")
                return True
        return False
    
    def resize_shape(self, shape_id: str, new_width: float, new_height: float) -> bool:
        """调整图形大小"""
        for shape in self.shapes:
            if shape.id == shape_id:
                shape.width = new_width
                shape.height = new_height
                print(f"📏 调整大小: {shape_id} 到 {new_width}x{new_height}")
                return True
        return False
    
    def change_color(self, shape_id: str, new_color: str) -> bool:
        """改变颜色"""
        for shape in self.shapes:
            if shape.id == shape_id:
                shape.color = new_color
                print(f"🎨 改变颜色: {shape_id} 到 {new_color}")
                return True
        return False
    
    def select_shapes(self, shape_ids: List[str]) -> None:
        """选择图形"""
        self.selected_shapes = [sid for sid in shape_ids if any(s.id == sid for s in self.shapes)]
        print(f"🎯 选择图形: {self.selected_shapes}")
    
    def create_memento(self, operation: str) -> CanvasMemento:
        """创建备忘录"""
        memento = CanvasMemento(self.shapes, operation)
        print(f"💾 创建画布快照: {operation}")
        return memento
    
    def restore_from_memento(self, memento: CanvasMemento) -> None:
        """从备忘录恢复"""
        self.shapes = memento.get_shapes()
        self.selected_shapes = []  # 清除选择
        print(f"🔄 恢复画布: {memento.get_operation()}")
    
    def get_canvas_info(self) -> Dict[str, Any]:
        """获取画布信息"""
        shape_counts = {}
        for shape in self.shapes:
            shape_type = shape.shape_type.value
            shape_counts[shape_type] = shape_counts.get(shape_type, 0) + 1
        
        return {
            'total_shapes': len(self.shapes),
            'shape_types': shape_counts,
            'selected_count': len(self.selected_shapes),
            'canvas_size': f"{self.canvas_width}x{self.canvas_height}",
            'zoom_level': self.zoom_level
        }


class EditorHistoryManager:
    """编辑器历史管理器"""
    
    def __init__(self, max_history: int = 20, max_memory_mb: int = 100):
        self.history: List[CanvasMemento] = []
        self.current_index = -1
        self.max_history = max_history
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.auto_save_enabled = True
        self.auto_save_interval = 30  # 30秒
        self.last_auto_save = datetime.now()
    
    def save_state(self, memento: CanvasMemento) -> None:
        """保存状态"""
        # 删除当前位置之后的历史
        if self.current_index < len(self.history) - 1:
            removed_count = len(self.history) - self.current_index - 1
            self.history = self.history[:self.current_index + 1]
            print(f"🗑️ 删除 {removed_count} 个后续历史记录")
        
        # 添加新状态
        self.history.append(memento)
        self.current_index += 1
        
        # 管理内存和数量限制
        self._manage_history()
        
        print(f"📚 保存历史: {memento} ({self.current_index + 1}/{len(self.history)})")
    
    def _manage_history(self) -> None:
        """管理历史记录"""
        # 计算总内存使用
        total_memory = sum(m.get_memory_size() for m in self.history)
        
        # 删除最旧的记录直到满足限制
        while ((len(self.history) > self.max_history or total_memory > self.max_memory_bytes) 
               and len(self.history) > 1):
            removed = self.history.pop(0)
            self.current_index -= 1
            total_memory -= removed.get_memory_size()
            print(f"🗑️ 删除旧历史: {removed.get_operation()}")
    
    def undo(self) -> Optional[CanvasMemento]:
        """撤销"""
        if self.current_index > 0:
            self.current_index -= 1
            memento = self.history[self.current_index]
            print(f"↶ 撤销到: {memento}")
            return memento
        else:
            print("⚠️ 无法撤销：已到达历史起点")
            return None
    
    def redo(self) -> Optional[CanvasMemento]:
        """重做"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            memento = self.history[self.current_index]
            print(f"↷ 重做到: {memento}")
            return memento
        else:
            print("⚠️ 无法重做：已到达历史终点")
            return None
    
    def auto_save_check(self, editor: GraphicsEditor) -> bool:
        """检查是否需要自动保存"""
        if not self.auto_save_enabled:
            return False
        
        now = datetime.now()
        if (now - self.last_auto_save).total_seconds() >= self.auto_save_interval:
            auto_save_memento = editor.create_memento("自动保存")
            self.save_state(auto_save_memento)
            self.last_auto_save = now
            return True
        return False
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """获取内存使用情况"""
        total_memory = sum(m.get_memory_size() for m in self.history)
        return {
            'total_memory_bytes': total_memory,
            'total_memory_mb': total_memory / (1024 * 1024),
            'history_count': len(self.history),
            'max_count': self.max_history,
            'max_memory_mb': self.max_memory_bytes / (1024 * 1024),
            'memory_usage_percent': (total_memory / self.max_memory_bytes) * 100
        }


# ==================== 工作流状态管理示例 ====================

class WorkflowStatus(Enum):
    """工作流状态"""
    DRAFT = "草稿"
    SUBMITTED = "已提交"
    REVIEWING = "审核中"
    APPROVED = "已批准"
    REJECTED = "已拒绝"
    COMPLETED = "已完成"


@dataclass
class WorkflowStep:
    """工作流步骤"""
    step_id: str
    name: str
    assignee: str
    status: str = "pending"
    completed_at: Optional[datetime] = None
    comments: str = ""


class WorkflowMemento:
    """工作流备忘录"""
    
    def __init__(self, workflow_state: Dict[str, Any], checkpoint_name: str):
        self._state = copy.deepcopy(workflow_state)
        self._checkpoint_name = checkpoint_name
        self._timestamp = datetime.now()
    
    def get_state(self) -> Dict[str, Any]:
        return copy.deepcopy(self._state)
    
    def get_checkpoint_name(self) -> str:
        return self._checkpoint_name
    
    def get_timestamp(self) -> datetime:
        return self._timestamp
    
    def __str__(self) -> str:
        return f"工作流检查点: {self._checkpoint_name} [{self._timestamp.strftime('%H:%M:%S')}]"


class Workflow:
    """工作流系统"""
    
    def __init__(self, workflow_id: str, title: str):
        self.workflow_id = workflow_id
        self.title = title
        self.status = WorkflowStatus.DRAFT
        self.steps: List[WorkflowStep] = []
        self.current_step_index = 0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.data: Dict[str, Any] = {}
    
    def add_step(self, step: WorkflowStep) -> None:
        """添加步骤"""
        self.steps.append(step)
        print(f"📋 添加工作流步骤: {step.name}")
    
    def start_workflow(self) -> bool:
        """启动工作流"""
        if self.status != WorkflowStatus.DRAFT:
            print("❌ 工作流已启动")
            return False
        
        self.status = WorkflowStatus.SUBMITTED
        self.updated_at = datetime.now()
        print(f"🚀 启动工作流: {self.title}")
        return True
    
    def complete_current_step(self, assignee: str, comments: str = "") -> bool:
        """完成当前步骤"""
        if self.current_step_index >= len(self.steps):
            print("❌ 没有更多步骤")
            return False
        
        current_step = self.steps[self.current_step_index]
        if current_step.assignee != assignee:
            print(f"❌ 当前步骤分配给 {current_step.assignee}，不是 {assignee}")
            return False
        
        current_step.status = "completed"
        current_step.completed_at = datetime.now()
        current_step.comments = comments
        
        self.current_step_index += 1
        self.updated_at = datetime.now()
        
        # 检查是否完成所有步骤
        if self.current_step_index >= len(self.steps):
            self.status = WorkflowStatus.COMPLETED
            print(f"🎉 工作流完成: {self.title}")
        else:
            print(f"✅ 完成步骤: {current_step.name}")
        
        return True
    
    def reject_workflow(self, assignee: str, reason: str) -> bool:
        """拒绝工作流"""
        if self.current_step_index >= len(self.steps):
            return False
        
        current_step = self.steps[self.current_step_index]
        if current_step.assignee != assignee:
            return False
        
        self.status = WorkflowStatus.REJECTED
        current_step.status = "rejected"
        current_step.comments = reason
        self.updated_at = datetime.now()
        
        print(f"❌ 工作流被拒绝: {reason}")
        return True
    
    def create_checkpoint(self, checkpoint_name: str) -> WorkflowMemento:
        """创建检查点"""
        state = {
            'workflow_id': self.workflow_id,
            'title': self.title,
            'status': self.status.value,
            'steps': [
                {
                    'step_id': step.step_id,
                    'name': step.name,
                    'assignee': step.assignee,
                    'status': step.status,
                    'completed_at': step.completed_at.isoformat() if step.completed_at else None,
                    'comments': step.comments
                }
                for step in self.steps
            ],
            'current_step_index': self.current_step_index,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'data': copy.deepcopy(self.data)
        }
        
        memento = WorkflowMemento(state, checkpoint_name)
        print(f"💾 创建工作流检查点: {checkpoint_name}")
        return memento
    
    def restore_from_checkpoint(self, memento: WorkflowMemento) -> None:
        """从检查点恢复"""
        state = memento.get_state()
        
        self.workflow_id = state['workflow_id']
        self.title = state['title']
        self.status = WorkflowStatus(state['status'])
        self.current_step_index = state['current_step_index']
        self.created_at = datetime.fromisoformat(state['created_at'])
        self.updated_at = datetime.fromisoformat(state['updated_at'])
        self.data = state['data']
        
        # 恢复步骤
        self.steps = []
        for step_data in state['steps']:
            step = WorkflowStep(
                step_id=step_data['step_id'],
                name=step_data['name'],
                assignee=step_data['assignee'],
                status=step_data['status'],
                completed_at=datetime.fromisoformat(step_data['completed_at']) if step_data['completed_at'] else None,
                comments=step_data['comments']
            )
            self.steps.append(step)
        
        print(f"🔄 恢复工作流: {memento.get_checkpoint_name()}")
    
    def get_progress(self) -> Dict[str, Any]:
        """获取进度信息"""
        completed_steps = sum(1 for step in self.steps if step.status == "completed")
        total_steps = len(self.steps)
        progress_percent = (completed_steps / total_steps * 100) if total_steps > 0 else 0
        
        return {
            'workflow_id': self.workflow_id,
            'title': self.title,
            'status': self.status.value,
            'completed_steps': completed_steps,
            'total_steps': total_steps,
            'progress_percent': progress_percent,
            'current_step': self.steps[self.current_step_index].name if self.current_step_index < len(self.steps) else None
        }


def demo_graphics_editor():
    """演示图形编辑器"""
    print("=" * 50)
    print("🎨 图形编辑器备忘录演示")
    print("=" * 50)
    
    # 创建编辑器和历史管理器
    editor = GraphicsEditor()
    history = EditorHistoryManager(max_history=10, max_memory_mb=10)
    
    # 保存初始状态
    initial_memento = editor.create_memento("初始画布")
    history.save_state(initial_memento)
    
    print("\n🎨 开始绘制:")
    
    # 添加一些图形
    rect1 = Shape("", ShapeType.RECTANGLE, 10, 10, 100, 50, "#FF0000")
    editor.add_shape(rect1)
    memento1 = editor.create_memento("添加矩形")
    history.save_state(memento1)
    
    circle1 = Shape("", ShapeType.CIRCLE, 150, 20, 60, 60, "#00FF00")
    editor.add_shape(circle1)
    memento2 = editor.create_memento("添加圆形")
    history.save_state(memento2)
    
    # 移动图形
    editor.move_shape("shape_1", 20, 30)
    memento3 = editor.create_memento("移动矩形")
    history.save_state(memento3)
    
    # 改变颜色
    editor.change_color("shape_2", "#0000FF")
    memento4 = editor.create_memento("改变圆形颜色")
    history.save_state(memento4)
    
    print(f"\n📊 当前画布: {editor.get_canvas_info()}")
    print(f"💾 内存使用: {history.get_memory_usage()}")
    
    # 撤销操作
    print("\n↶ 执行撤销:")
    for _ in range(2):
        memento = history.undo()
        if memento:
            editor.restore_from_memento(memento)
            print(f"📊 画布状态: {editor.get_canvas_info()}")
    
    # 重做操作
    print("\n↷ 执行重做:")
    memento = history.redo()
    if memento:
        editor.restore_from_memento(memento)
        print(f"📊 画布状态: {editor.get_canvas_info()}")


def demo_workflow_system():
    """演示工作流系统"""
    print("\n" + "=" * 50)
    print("📋 工作流系统备忘录演示")
    print("=" * 50)
    
    # 创建工作流
    workflow = Workflow("WF_001", "采购申请审批")
    
    # 添加步骤
    steps = [
        WorkflowStep("step1", "部门经理审批", "manager1"),
        WorkflowStep("step2", "财务审核", "finance1"),
        WorkflowStep("step3", "总经理批准", "ceo"),
        WorkflowStep("step4", "采购执行", "procurement")
    ]
    
    for step in steps:
        workflow.add_step(step)
    
    # 创建初始检查点
    checkpoint1 = workflow.create_checkpoint("工作流创建")
    
    # 启动工作流
    workflow.start_workflow()
    checkpoint2 = workflow.create_checkpoint("工作流启动")
    
    print(f"\n📊 工作流进度: {workflow.get_progress()}")
    
    # 完成第一步
    workflow.complete_current_step("manager1", "同意采购申请")
    checkpoint3 = workflow.create_checkpoint("部门经理审批完成")
    
    # 完成第二步
    workflow.complete_current_step("finance1", "预算充足，财务审核通过")
    checkpoint4 = workflow.create_checkpoint("财务审核完成")
    
    print(f"\n📊 当前进度: {workflow.get_progress()}")
    
    # 模拟回滚到之前的检查点
    print("\n🔄 回滚到财务审核前:")
    workflow.restore_from_checkpoint(checkpoint2)
    print(f"📊 回滚后进度: {workflow.get_progress()}")
    
    # 重新执行
    print("\n🔄 重新执行审批流程:")
    workflow.complete_current_step("manager1", "重新审批通过")
    workflow.complete_current_step("finance1", "重新财务审核通过")
    workflow.complete_current_step("ceo", "总经理批准")
    workflow.complete_current_step("procurement", "采购完成")
    
    print(f"\n📊 最终进度: {workflow.get_progress()}")


if __name__ == "__main__":
    print("🎯 备忘录模式实际应用演示")
    
    # 运行图形编辑器演示
    demo_graphics_editor()
    
    # 运行工作流系统演示
    demo_workflow_system()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 备忘录模式在复杂应用中提供了强大的状态管理能力")
    print("=" * 50)
