#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工作流系统中介者

本模块演示了中介者模式在工作流系统中的应用，包括：
1. 任务节点协调
2. 流程状态管理
3. 条件分支处理
4. 业务流程建模

作者: Assistant
日期: 2024-01-20
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Optional, Any, Callable
from enum import Enum
from datetime import datetime, timedelta
import uuid


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "待处理"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    FAILED = "失败"
    CANCELLED = "已取消"
    WAITING = "等待中"


class WorkflowStatus(Enum):
    """工作流状态枚举"""
    CREATED = "已创建"
    RUNNING = "运行中"
    COMPLETED = "已完成"
    FAILED = "失败"
    CANCELLED = "已取消"
    PAUSED = "已暂停"


class TaskType(Enum):
    """任务类型枚举"""
    MANUAL = "手动任务"
    AUTOMATIC = "自动任务"
    APPROVAL = "审批任务"
    NOTIFICATION = "通知任务"
    CONDITION = "条件判断"
    PARALLEL = "并行任务"


class WorkflowMediator(ABC):
    """工作流中介者接口"""
    
    @abstractmethod
    def notify_task_completed(self, task_id: str, result: Any) -> None:
        """通知任务完成"""
        pass
    
    @abstractmethod
    def notify_task_failed(self, task_id: str, error: str) -> None:
        """通知任务失败"""
        pass
    
    @abstractmethod
    def get_task_data(self, task_id: str) -> Dict[str, Any]:
        """获取任务数据"""
        pass
    
    @abstractmethod
    def set_workflow_data(self, key: str, value: Any) -> None:
        """设置工作流数据"""
        pass


class Task(ABC):
    """任务基类"""
    
    def __init__(self, task_id: str, name: str, task_type: TaskType, mediator: WorkflowMediator = None):
        self.task_id = task_id
        self.name = name
        self.task_type = task_type
        self.status = TaskStatus.PENDING
        self.mediator = mediator
        self.dependencies: Set[str] = set()  # 依赖的任务ID
        self.next_tasks: Set[str] = set()    # 后续任务ID
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Any = None
        self.error_message: str = ""
        self.assignee: str = ""
        self.timeout_minutes: Optional[int] = None
    
    def set_mediator(self, mediator: WorkflowMediator) -> None:
        """设置中介者"""
        self.mediator = mediator
    
    def add_dependency(self, task_id: str) -> None:
        """添加依赖任务"""
        self.dependencies.add(task_id)
    
    def add_next_task(self, task_id: str) -> None:
        """添加后续任务"""
        self.next_tasks.add(task_id)
    
    def can_start(self) -> bool:
        """检查是否可以开始执行"""
        if self.status != TaskStatus.PENDING:
            return False
        
        # 检查所有依赖任务是否已完成
        for dep_task_id in self.dependencies:
            dep_data = self.mediator.get_task_data(dep_task_id) if self.mediator else {}
            if dep_data.get('status') != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def start(self) -> bool:
        """开始执行任务"""
        if not self.can_start():
            return False
        
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        print(f"🚀 任务开始: {self.name} ({self.task_id})")
        
        try:
            self.execute()
            return True
        except Exception as e:
            self.fail(str(e))
            return False
    
    @abstractmethod
    def execute(self) -> None:
        """执行任务逻辑"""
        pass
    
    def complete(self, result: Any = None) -> None:
        """完成任务"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result
        
        duration = (self.completed_at - self.started_at).total_seconds()
        print(f"✅ 任务完成: {self.name} (耗时: {duration:.1f}秒)")
        
        if self.mediator:
            self.mediator.notify_task_completed(self.task_id, result)
    
    def fail(self, error_message: str) -> None:
        """任务失败"""
        self.status = TaskStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.now()
        
        print(f"❌ 任务失败: {self.name} - {error_message}")
        
        if self.mediator:
            self.mediator.notify_task_failed(self.task_id, error_message)
    
    def cancel(self) -> None:
        """取消任务"""
        self.status = TaskStatus.CANCELLED
        print(f"🚫 任务取消: {self.name}")
    
    def get_info(self) -> Dict[str, Any]:
        """获取任务信息"""
        return {
            'task_id': self.task_id,
            'name': self.name,
            'type': self.task_type.value,
            'status': self.status.value,
            'assignee': self.assignee,
            'dependencies': list(self.dependencies),
            'next_tasks': list(self.next_tasks),
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'result': self.result,
            'error_message': self.error_message
        }


class ManualTask(Task):
    """手动任务"""
    
    def __init__(self, task_id: str, name: str, assignee: str, mediator: WorkflowMediator = None):
        super().__init__(task_id, name, TaskType.MANUAL, mediator)
        self.assignee = assignee
        self.instructions = ""
    
    def set_instructions(self, instructions: str) -> None:
        """设置任务说明"""
        self.instructions = instructions
    
    def execute(self) -> None:
        """执行手动任务"""
        print(f"👤 手动任务分配给: {self.assignee}")
        print(f"📋 任务说明: {self.instructions}")
        
        # 模拟手动任务处理
        import time
        time.sleep(0.1)  # 模拟处理时间
        
        # 手动任务需要外部调用complete()方法
        self.status = TaskStatus.WAITING
        print(f"⏳ 等待 {self.assignee} 完成任务...")


class AutomaticTask(Task):
    """自动任务"""
    
    def __init__(self, task_id: str, name: str, action: Callable, mediator: WorkflowMediator = None):
        super().__init__(task_id, name, TaskType.AUTOMATIC, mediator)
        self.action = action
    
    def execute(self) -> None:
        """执行自动任务"""
        print(f"🤖 执行自动任务: {self.name}")
        
        try:
            result = self.action()
            self.complete(result)
        except Exception as e:
            self.fail(str(e))


class ApprovalTask(Task):
    """审批任务"""
    
    def __init__(self, task_id: str, name: str, approver: str, mediator: WorkflowMediator = None):
        super().__init__(task_id, name, TaskType.APPROVAL, mediator)
        self.approver = approver
        self.approval_result: Optional[bool] = None
        self.approval_comment = ""
    
    def execute(self) -> None:
        """执行审批任务"""
        print(f"📝 审批任务分配给: {self.approver}")
        
        # 模拟审批处理
        self.status = TaskStatus.WAITING
        print(f"⏳ 等待 {self.approver} 审批...")
    
    def approve(self, comment: str = "") -> None:
        """批准"""
        self.approval_result = True
        self.approval_comment = comment
        print(f"✅ {self.approver} 批准了任务: {self.name}")
        if comment:
            print(f"💬 审批意见: {comment}")
        self.complete({"approved": True, "comment": comment})
    
    def reject(self, comment: str = "") -> None:
        """拒绝"""
        self.approval_result = False
        self.approval_comment = comment
        print(f"❌ {self.approver} 拒绝了任务: {self.name}")
        if comment:
            print(f"💬 拒绝理由: {comment}")
        self.complete({"approved": False, "comment": comment})


class ConditionTask(Task):
    """条件判断任务"""
    
    def __init__(self, task_id: str, name: str, condition: Callable, mediator: WorkflowMediator = None):
        super().__init__(task_id, name, TaskType.CONDITION, mediator)
        self.condition = condition
        self.true_tasks: Set[str] = set()   # 条件为真时执行的任务
        self.false_tasks: Set[str] = set()  # 条件为假时执行的任务
    
    def add_true_task(self, task_id: str) -> None:
        """添加条件为真时的任务"""
        self.true_tasks.add(task_id)
    
    def add_false_task(self, task_id: str) -> None:
        """添加条件为假时的任务"""
        self.false_tasks.add(task_id)
    
    def execute(self) -> None:
        """执行条件判断"""
        print(f"🔍 执行条件判断: {self.name}")
        
        try:
            result = self.condition()
            print(f"📊 条件结果: {result}")
            
            # 根据条件结果设置后续任务
            if result:
                self.next_tasks = self.true_tasks.copy()
            else:
                self.next_tasks = self.false_tasks.copy()
            
            self.complete(result)
        except Exception as e:
            self.fail(str(e))


class WorkflowEngine(WorkflowMediator):
    """工作流引擎"""
    
    def __init__(self, workflow_id: str, name: str):
        self.workflow_id = workflow_id
        self.name = name
        self.status = WorkflowStatus.CREATED
        self.tasks: Dict[str, Task] = {}
        self.workflow_data: Dict[str, Any] = {}
        self.execution_log: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
    
    def add_task(self, task: Task) -> None:
        """添加任务"""
        task.set_mediator(self)
        self.tasks[task.task_id] = task
        print(f"📋 添加任务: {task.name} ({task.task_id})")
    
    def start_workflow(self) -> None:
        """启动工作流"""
        if self.status != WorkflowStatus.CREATED:
            print(f"⚠️ 工作流状态不正确: {self.status.value}")
            return
        
        self.status = WorkflowStatus.RUNNING
        self.started_at = datetime.now()
        
        print(f"🚀 启动工作流: {self.name}")
        self._log_event("workflow_started", {"workflow_id": self.workflow_id})
        
        # 启动所有可以开始的任务
        self._start_ready_tasks()
    
    def _start_ready_tasks(self) -> None:
        """启动所有准备就绪的任务"""
        ready_tasks = [task for task in self.tasks.values() if task.can_start()]
        
        for task in ready_tasks:
            task.start()
    
    def notify_task_completed(self, task_id: str, result: Any) -> None:
        """处理任务完成通知"""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        self._log_event("task_completed", {
            "task_id": task_id,
            "task_name": task.name,
            "result": result
        })
        
        # 检查是否有新的任务可以开始
        self._start_ready_tasks()
        
        # 检查工作流是否完成
        self._check_workflow_completion()
    
    def notify_task_failed(self, task_id: str, error: str) -> None:
        """处理任务失败通知"""
        task = self.tasks.get(task_id)
        if not task:
            return
        
        self._log_event("task_failed", {
            "task_id": task_id,
            "task_name": task.name,
            "error": error
        })
        
        # 工作流失败
        self.status = WorkflowStatus.FAILED
        self.completed_at = datetime.now()
        print(f"💥 工作流失败: {self.name} - 任务 {task.name} 失败")
    
    def get_task_data(self, task_id: str) -> Dict[str, Any]:
        """获取任务数据"""
        task = self.tasks.get(task_id)
        if task:
            return task.get_info()
        return {}
    
    def set_workflow_data(self, key: str, value: Any) -> None:
        """设置工作流数据"""
        self.workflow_data[key] = value
        print(f"💾 设置工作流数据: {key} = {value}")
    
    def get_workflow_data(self, key: str) -> Any:
        """获取工作流数据"""
        return self.workflow_data.get(key)
    
    def _check_workflow_completion(self) -> None:
        """检查工作流是否完成"""
        if self.status != WorkflowStatus.RUNNING:
            return
        
        # 检查是否所有任务都已完成
        all_completed = all(
            task.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED, TaskStatus.FAILED]
            for task in self.tasks.values()
        )
        
        if all_completed:
            self.status = WorkflowStatus.COMPLETED
            self.completed_at = datetime.now()
            
            duration = (self.completed_at - self.started_at).total_seconds()
            print(f"🎉 工作流完成: {self.name} (总耗时: {duration:.1f}秒)")
            
            self._log_event("workflow_completed", {"workflow_id": self.workflow_id})
    
    def _log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """记录事件"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        self.execution_log.append(log_entry)
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """获取工作流状态"""
        task_summary = {}
        for status in TaskStatus:
            count = sum(1 for task in self.tasks.values() if task.status == status)
            if count > 0:
                task_summary[status.value] = count
        
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "status": self.status.value,
            "task_count": len(self.tasks),
            "task_summary": task_summary,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """获取执行日志"""
        return self.execution_log.copy()


def demo_order_processing_workflow():
    """演示订单处理工作流"""
    print("=" * 50)
    print("📦 订单处理工作流演示")
    print("=" * 50)
    
    # 创建工作流引擎
    workflow = WorkflowEngine("order_001", "订单处理流程")
    
    # 定义自动任务的执行函数
    def validate_order():
        print("🔍 验证订单信息...")
        return {"valid": True, "order_amount": 299.99}
    
    def check_inventory():
        print("📦 检查库存...")
        return {"available": True, "stock_count": 50}
    
    def calculate_shipping():
        print("🚚 计算运费...")
        return {"shipping_cost": 15.00, "estimated_days": 3}
    
    def process_payment():
        print("💳 处理支付...")
        return {"payment_id": "PAY_12345", "status": "success"}
    
    def send_confirmation():
        print("📧 发送确认邮件...")
        return {"email_sent": True}
    
    def prepare_shipment():
        print("📋 准备发货...")
        return {"tracking_number": "TRK_67890"}
    
    # 定义条件判断函数
    def check_high_value_order():
        order_amount = workflow.get_workflow_data("order_amount") or 0
        return order_amount > 200
    
    # 创建任务
    task1 = AutomaticTask("validate", "验证订单", validate_order, workflow)
    task2 = AutomaticTask("inventory", "检查库存", check_inventory, workflow)
    task3 = AutomaticTask("shipping", "计算运费", calculate_shipping, workflow)
    task4 = ConditionTask("check_value", "检查订单金额", check_high_value_order, workflow)
    task5 = ApprovalTask("approval", "高价值订单审批", "财务经理", workflow)
    task6 = AutomaticTask("payment", "处理支付", process_payment, workflow)
    task7 = AutomaticTask("confirmation", "发送确认", send_confirmation, workflow)
    task8 = ManualTask("prepare", "准备发货", "仓库员工", workflow)
    
    # 设置任务依赖关系
    task2.add_dependency("validate")  # 库存检查依赖订单验证
    task3.add_dependency("inventory")  # 运费计算依赖库存检查
    task4.add_dependency("shipping")   # 金额检查依赖运费计算
    
    # 设置条件分支
    task4.add_true_task("approval")    # 高价值订单需要审批
    task4.add_false_task("payment")    # 普通订单直接支付
    
    task6.add_dependency("approval")   # 支付依赖审批（如果需要）
    task7.add_dependency("payment")    # 确认依赖支付
    task8.add_dependency("confirmation")  # 发货依赖确认
    
    # 添加任务到工作流
    for task in [task1, task2, task3, task4, task5, task6, task7, task8]:
        workflow.add_task(task)
    
    # 启动工作流
    print("\n🚀 启动订单处理流程:")
    workflow.start_workflow()
    
    # 模拟一些延迟和手动操作
    import time
    time.sleep(0.5)
    
    # 模拟审批操作
    print("\n📝 模拟审批操作:")
    if task5.status == TaskStatus.WAITING:
        task5.approve("订单金额合理，批准处理")
    
    time.sleep(0.2)
    
    # 模拟手动任务完成
    print("\n👤 模拟手动任务完成:")
    if task8.status == TaskStatus.WAITING:
        task8.complete({"prepared": True, "tracking": "TRK_67890"})
    
    # 显示工作流状态
    print("\n📊 工作流状态:")
    status = workflow.get_workflow_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # 显示执行日志
    print("\n📋 执行日志:")
    for log_entry in workflow.get_execution_log():
        timestamp = log_entry["timestamp"][:19]  # 只显示到秒
        event_type = log_entry["event_type"]
        print(f"  [{timestamp}] {event_type}")


if __name__ == "__main__":
    print("🎯 工作流系统中介者模式演示")
    
    demo_order_processing_workflow()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 中介者模式有效地协调了工作流中各任务间的复杂交互")
    print("=" * 50)
