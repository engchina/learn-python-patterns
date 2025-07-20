"""
05_real_world_examples.py - 责任链模式的实际应用示例

这个文件展示了责任链模式在实际开发中的常见应用场景，
包括审批流程系统、异常处理链、事件处理系统等实际场景。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import json


# ==================== 示例1：审批流程系统 ====================
class ApprovalStatus(Enum):
    """审批状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"


class ApprovalRequest:
    """审批请求"""
    
    def __init__(self, request_id: str, requester: str, amount: float, 
                 description: str, category: str):
        self.request_id = request_id
        self.requester = requester
        self.amount = amount
        self.description = description
        self.category = category
        self.status = ApprovalStatus.PENDING
        self.created_at = datetime.now()
        self.approval_history: List[Dict[str, Any]] = []
        self.current_approver = None
    
    def add_approval_record(self, approver: str, action: str, comment: str = ""):
        """添加审批记录"""
        record = {
            "approver": approver,
            "action": action,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        self.approval_history.append(record)
    
    def get_info(self) -> str:
        """获取请求信息"""
        return f"请求ID: {self.request_id}, 申请人: {self.requester}, 金额: ¥{self.amount:,.2f}"


class Approver(ABC):
    """抽象审批者"""
    
    def __init__(self, name: str, title: str, approval_limit: float):
        self.name = name
        self.title = title
        self.approval_limit = approval_limit
        self._next_approver: Optional['Approver'] = None
        self.processed_requests = 0
        self.approved_count = 0
        self.rejected_count = 0
    
    def set_next(self, approver: 'Approver') -> 'Approver':
        """设置下一级审批者"""
        self._next_approver = approver
        return approver
    
    def process_request(self, request: ApprovalRequest) -> ApprovalStatus:
        """处理审批请求"""
        self.processed_requests += 1
        request.current_approver = self.name
        
        print(f"\n{self.title} {self.name}: 处理审批请求")
        print(f"  {request.get_info()}")
        print(f"  审批权限: ¥{self.approval_limit:,.2f}")
        
        # 检查是否在审批权限范围内
        if request.amount <= self.approval_limit:
            # 在权限范围内，进行审批决策
            decision = self._make_decision(request)
            
            if decision == ApprovalStatus.APPROVED:
                self.approved_count += 1
                request.status = ApprovalStatus.APPROVED
                request.add_approval_record(self.name, "approved", "审批通过")
                print(f"  决策: ✅ 审批通过")
            elif decision == ApprovalStatus.REJECTED:
                self.rejected_count += 1
                request.status = ApprovalStatus.REJECTED
                request.add_approval_record(self.name, "rejected", "审批拒绝")
                print(f"  决策: ❌ 审批拒绝")
            
            return decision
        else:
            # 超出权限，上报给上级
            if self._next_approver:
                print(f"  决策: ⬆️ 超出权限，上报给 {self._next_approver.title}")
                request.add_approval_record(self.name, "escalated", "超出权限，上报上级")
                return self._next_approver.process_request(request)
            else:
                # 没有上级了，自动拒绝
                print(f"  决策: ❌ 超出所有审批权限，自动拒绝")
                self.rejected_count += 1
                request.status = ApprovalStatus.REJECTED
                request.add_approval_record(self.name, "rejected", "超出所有审批权限")
                return ApprovalStatus.REJECTED
    
    @abstractmethod
    def _make_decision(self, request: ApprovalRequest) -> ApprovalStatus:
        """做出审批决策"""
        pass
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取审批统计"""
        approval_rate = (self.approved_count / self.processed_requests * 100) if self.processed_requests > 0 else 0
        return {
            "name": self.name,
            "title": self.title,
            "approval_limit": self.approval_limit,
            "processed_requests": self.processed_requests,
            "approved_count": self.approved_count,
            "rejected_count": self.rejected_count,
            "approval_rate": round(approval_rate, 1)
        }


class TeamLeader(Approver):
    """团队主管"""
    
    def __init__(self, name: str):
        super().__init__(name, "团队主管", 10000.0)  # 1万元审批权限
    
    def _make_decision(self, request: ApprovalRequest) -> ApprovalStatus:
        """团队主管的审批逻辑"""
        # 简单的审批逻辑
        if request.category in ["办公用品", "培训费用"] and request.amount <= 5000:
            return ApprovalStatus.APPROVED
        elif request.amount <= 3000:
            return ApprovalStatus.APPROVED
        else:
            # 需要更仔细的审查
            if "紧急" in request.description:
                return ApprovalStatus.APPROVED
            return ApprovalStatus.REJECTED


class DepartmentManager(Approver):
    """部门经理"""
    
    def __init__(self, name: str):
        super().__init__(name, "部门经理", 50000.0)  # 5万元审批权限
    
    def _make_decision(self, request: ApprovalRequest) -> ApprovalStatus:
        """部门经理的审批逻辑"""
        # 更复杂的审批逻辑
        if request.category == "设备采购" and request.amount <= 30000:
            return ApprovalStatus.APPROVED
        elif request.category in ["差旅费", "会议费"] and request.amount <= 20000:
            return ApprovalStatus.APPROVED
        elif request.amount <= 15000:
            return ApprovalStatus.APPROVED
        else:
            return ApprovalStatus.REJECTED


class GeneralManager(Approver):
    """总经理"""
    
    def __init__(self, name: str):
        super().__init__(name, "总经理", 200000.0)  # 20万元审批权限
    
    def _make_decision(self, request: ApprovalRequest) -> ApprovalStatus:
        """总经理的审批逻辑"""
        # 总经理级别的审批逻辑
        if request.category == "战略投资" and request.amount <= 150000:
            return ApprovalStatus.APPROVED
        elif request.amount <= 100000:
            return ApprovalStatus.APPROVED
        else:
            # 超过20万需要董事会审批
            return ApprovalStatus.REJECTED


class CEO(Approver):
    """首席执行官"""
    
    def __init__(self, name: str):
        super().__init__(name, "首席执行官", 1000000.0)  # 100万元审批权限
    
    def _make_decision(self, request: ApprovalRequest) -> ApprovalStatus:
        """CEO的审批逻辑"""
        # CEO几乎可以审批所有请求
        if request.amount <= 500000:
            return ApprovalStatus.APPROVED
        else:
            # 超过50万需要董事会审批
            return ApprovalStatus.REJECTED


# ==================== 示例2：异常处理链 ====================
class ExceptionSeverity(Enum):
    """异常严重程度"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class SystemException:
    """系统异常"""
    
    def __init__(self, exception_type: str, message: str, severity: ExceptionSeverity,
                 context: Dict[str, Any] = None):
        self.exception_type = exception_type
        self.message = message
        self.severity = severity
        self.context = context or {}
        self.timestamp = datetime.now()
        self.handled = False
        self.handler_chain: List[str] = []
    
    def add_handler_record(self, handler_name: str):
        """添加处理器记录"""
        self.handler_chain.append(handler_name)
    
    def mark_handled(self, handler_name: str):
        """标记为已处理"""
        self.handled = True
        self.handler_chain.append(f"{handler_name} (已处理)")


class ExceptionHandler(ABC):
    """抽象异常处理器"""
    
    def __init__(self, name: str, max_severity: ExceptionSeverity):
        self.name = name
        self.max_severity = max_severity
        self._next_handler: Optional['ExceptionHandler'] = None
        self.handled_count = 0
    
    def set_next(self, handler: 'ExceptionHandler') -> 'ExceptionHandler':
        """设置下一个处理器"""
        self._next_handler = handler
        return handler
    
    def handle_exception(self, exception: SystemException) -> bool:
        """处理异常"""
        exception.add_handler_record(self.name)
        
        print(f"\n{self.name}: 接收到异常")
        print(f"  类型: {exception.exception_type}")
        print(f"  严重程度: {exception.severity.name}")
        print(f"  消息: {exception.message}")
        
        # 检查是否能处理该异常
        if exception.severity.value <= self.max_severity.value:
            # 可以处理
            self.handled_count += 1
            success = self._handle_exception(exception)
            
            if success:
                exception.mark_handled(self.name)
                print(f"  结果: ✅ 异常已处理")
                return True
            else:
                print(f"  结果: ❌ 处理失败，传递给下一个处理器")
        else:
            print(f"  结果: ⬆️ 严重程度超出处理能力，传递给下一个处理器")
        
        # 传递给下一个处理器
        if self._next_handler:
            return self._next_handler.handle_exception(exception)
        else:
            print(f"  结果: 💥 没有更多处理器，异常未被处理")
            return False
    
    @abstractmethod
    def _handle_exception(self, exception: SystemException) -> bool:
        """具体的异常处理逻辑"""
        pass


class LoggingHandler(ExceptionHandler):
    """日志记录处理器"""
    
    def __init__(self):
        super().__init__("日志记录处理器", ExceptionSeverity.MEDIUM)
    
    def _handle_exception(self, exception: SystemException) -> bool:
        """记录异常日志"""
        log_entry = {
            "timestamp": exception.timestamp.isoformat(),
            "type": exception.exception_type,
            "severity": exception.severity.name,
            "message": exception.message,
            "context": exception.context
        }
        
        print(f"    📝 异常已记录到日志: {json.dumps(log_entry, ensure_ascii=False)}")
        return True


class NotificationHandler(ExceptionHandler):
    """通知处理器"""
    
    def __init__(self):
        super().__init__("通知处理器", ExceptionSeverity.HIGH)
        self.notification_count = 0
    
    def _handle_exception(self, exception: SystemException) -> bool:
        """发送通知"""
        self.notification_count += 1
        
        # 模拟发送通知
        recipients = ["admin@company.com", "ops@company.com"]
        subject = f"[{exception.severity.name}] 系统异常告警"
        
        print(f"    📧 发送通知到: {recipients}")
        print(f"    主题: {subject}")
        print(f"    通知编号: #{self.notification_count}")
        
        return True


class EmergencyHandler(ExceptionHandler):
    """紧急处理器"""
    
    def __init__(self):
        super().__init__("紧急处理器", ExceptionSeverity.CRITICAL)
        self.emergency_count = 0
    
    def _handle_exception(self, exception: SystemException) -> bool:
        """紧急处理"""
        self.emergency_count += 1
        
        print(f"    🚨 启动紧急响应程序")
        print(f"    📞 呼叫值班人员")
        print(f"    🔧 尝试自动恢复")
        print(f"    紧急处理编号: #{self.emergency_count}")
        
        # 模拟紧急处理逻辑
        if "数据库" in exception.message:
            print(f"    💾 重启数据库连接")
        elif "网络" in exception.message:
            print(f"    🌐 检查网络连接")
        
        return True


# ==================== 示例3：事件处理系统 ====================
class Event:
    """事件对象"""
    
    def __init__(self, event_type: str, data: Dict[str, Any], priority: int = 1):
        self.event_type = event_type
        self.data = data
        self.priority = priority
        self.timestamp = datetime.now()
        self.processed = False
        self.processor_chain: List[str] = []
    
    def add_processor_record(self, processor_name: str):
        """添加处理器记录"""
        self.processor_chain.append(processor_name)


class EventProcessor(ABC):
    """抽象事件处理器"""
    
    def __init__(self, name: str, event_types: List[str]):
        self.name = name
        self.event_types = event_types
        self._next_processor: Optional['EventProcessor'] = None
        self.processed_count = 0
    
    def set_next(self, processor: 'EventProcessor') -> 'EventProcessor':
        """设置下一个处理器"""
        self._next_processor = processor
        return processor
    
    def process_event(self, event: Event):
        """处理事件"""
        event.add_processor_record(self.name)
        
        # 检查是否能处理该事件类型
        if event.event_type in self.event_types:
            print(f"\n{self.name}: 处理事件 '{event.event_type}'")
            self.processed_count += 1
            self._process_event(event)
            event.processed = True
        else:
            print(f"\n{self.name}: 跳过事件 '{event.event_type}' (不在处理范围内)")
        
        # 传递给下一个处理器
        if self._next_processor:
            self._next_processor.process_event(event)
    
    @abstractmethod
    def _process_event(self, event: Event):
        """具体的事件处理逻辑"""
        pass


class UserEventProcessor(EventProcessor):
    """用户事件处理器"""
    
    def __init__(self):
        super().__init__("用户事件处理器", ["user_login", "user_logout", "user_register"])
    
    def _process_event(self, event: Event):
        """处理用户事件"""
        if event.event_type == "user_login":
            user_id = event.data.get("user_id")
            print(f"    👤 用户 {user_id} 登录，更新最后登录时间")
        elif event.event_type == "user_logout":
            user_id = event.data.get("user_id")
            session_duration = event.data.get("session_duration", 0)
            print(f"    👤 用户 {user_id} 登出，会话时长: {session_duration} 分钟")
        elif event.event_type == "user_register":
            user_id = event.data.get("user_id")
            print(f"    👤 新用户 {user_id} 注册，发送欢迎邮件")


class OrderEventProcessor(EventProcessor):
    """订单事件处理器"""
    
    def __init__(self):
        super().__init__("订单事件处理器", ["order_created", "order_paid", "order_shipped"])
    
    def _process_event(self, event: Event):
        """处理订单事件"""
        order_id = event.data.get("order_id")
        
        if event.event_type == "order_created":
            print(f"    🛒 订单 {order_id} 已创建，发送确认邮件")
        elif event.event_type == "order_paid":
            amount = event.data.get("amount", 0)
            print(f"    💰 订单 {order_id} 已支付 ¥{amount}，更新库存")
        elif event.event_type == "order_shipped":
            tracking_number = event.data.get("tracking_number")
            print(f"    📦 订单 {order_id} 已发货，快递单号: {tracking_number}")


class AnalyticsEventProcessor(EventProcessor):
    """分析事件处理器"""
    
    def __init__(self):
        super().__init__("分析事件处理器", 
                        ["user_login", "user_register", "order_created", "order_paid"])
        self.analytics_data = {}
    
    def _process_event(self, event: Event):
        """处理分析事件"""
        event_type = event.event_type
        
        if event_type not in self.analytics_data:
            self.analytics_data[event_type] = 0
        
        self.analytics_data[event_type] += 1
        
        print(f"    📊 更新分析数据: {event_type} 事件计数 +1")
        print(f"    📈 当前统计: {self.analytics_data}")


# ==================== 使用示例 ====================
def demo_approval_system():
    """审批流程系统演示"""
    print("=" * 60)
    print("📋 审批流程系统演示")
    print("=" * 60)
    
    # 构建审批链
    team_leader = TeamLeader("张三")
    dept_manager = DepartmentManager("李四")
    general_manager = GeneralManager("王五")
    ceo = CEO("赵六")
    
    # 连接审批链
    team_leader.set_next(dept_manager).set_next(general_manager).set_next(ceo)
    
    # 创建各种审批请求
    requests = [
        ApprovalRequest("REQ001", "员工A", 3000, "购买办公用品", "办公用品"),
        ApprovalRequest("REQ002", "员工B", 15000, "参加技术培训", "培训费用"),
        ApprovalRequest("REQ003", "员工C", 45000, "购买服务器设备", "设备采购"),
        ApprovalRequest("REQ004", "员工D", 120000, "市场推广活动", "营销费用"),
        ApprovalRequest("REQ005", "员工E", 800000, "收购小公司", "战略投资")
    ]
    
    print(f"\n🚀 处理 {len(requests)} 个审批请求:")
    
    # 处理所有请求
    for i, request in enumerate(requests, 1):
        print(f"\n{'='*20} 审批请求 {i} {'='*20}")
        status = team_leader.process_request(request)
        
        print(f"\n📋 最终结果: {status.value.upper()}")
        print(f"📝 审批历史:")
        for record in request.approval_history:
            print(f"    {record['timestamp'][:19]} | {record['approver']} | {record['action']} | {record['comment']}")
    
    # 显示审批者统计
    print(f"\n📊 审批者统计:")
    approvers = [team_leader, dept_manager, general_manager, ceo]
    for approver in approvers:
        stats = approver.get_statistics()
        print(f"\n{stats['title']} {stats['name']}:")
        print(f"  审批权限: ¥{stats['approval_limit']:,.2f}")
        print(f"  处理请求: {stats['processed_requests']} 个")
        print(f"  通过率: {stats['approval_rate']}%")


def demo_exception_handling():
    """异常处理链演示"""
    print("\n" + "=" * 60)
    print("🚨 异常处理链演示")
    print("=" * 60)
    
    # 构建异常处理链
    logging_handler = LoggingHandler()
    notification_handler = NotificationHandler()
    emergency_handler = EmergencyHandler()
    
    # 连接处理链
    logging_handler.set_next(notification_handler).set_next(emergency_handler)
    
    # 创建各种异常
    exceptions = [
        SystemException("ValidationError", "用户输入验证失败", ExceptionSeverity.LOW,
                       {"field": "email", "value": "invalid"}),
        SystemException("DatabaseError", "数据库查询超时", ExceptionSeverity.MEDIUM,
                       {"query": "SELECT * FROM users", "timeout": 30}),
        SystemException("NetworkError", "外部API调用失败", ExceptionSeverity.HIGH,
                       {"api": "payment_gateway", "status_code": 500}),
        SystemException("SystemCrash", "系统内存不足即将崩溃", ExceptionSeverity.CRITICAL,
                       {"memory_usage": "98%", "available_memory": "50MB"})
    ]
    
    print(f"\n🚀 处理 {len(exceptions)} 个异常:")
    
    # 处理所有异常
    for i, exception in enumerate(exceptions, 1):
        print(f"\n{'='*20} 异常 {i} {'='*20}")
        handled = logging_handler.handle_exception(exception)
        
        print(f"\n📋 处理结果: {'✅ 已处理' if handled else '❌ 未处理'}")
        print(f"🔗 处理链路: {' -> '.join(exception.handler_chain)}")


def demo_event_processing():
    """事件处理系统演示"""
    print("\n" + "=" * 60)
    print("🎯 事件处理系统演示")
    print("=" * 60)
    
    # 构建事件处理链
    user_processor = UserEventProcessor()
    order_processor = OrderEventProcessor()
    analytics_processor = AnalyticsEventProcessor()
    
    # 连接处理链
    user_processor.set_next(order_processor).set_next(analytics_processor)
    
    # 创建各种事件
    events = [
        Event("user_register", {"user_id": "U001", "email": "user1@example.com"}),
        Event("user_login", {"user_id": "U001", "ip": "192.168.1.1"}),
        Event("order_created", {"order_id": "O001", "user_id": "U001", "amount": 299.99}),
        Event("order_paid", {"order_id": "O001", "amount": 299.99, "payment_method": "credit_card"}),
        Event("order_shipped", {"order_id": "O001", "tracking_number": "SF1234567890"}),
        Event("user_logout", {"user_id": "U001", "session_duration": 45})
    ]
    
    print(f"\n🚀 处理 {len(events)} 个事件:")
    
    # 处理所有事件
    for i, event in enumerate(events, 1):
        print(f"\n{'='*15} 事件 {i}: {event.event_type} {'='*15}")
        user_processor.process_event(event)
        
        print(f"🔗 处理链路: {' -> '.join(event.processor_chain)}")
    
    # 显示处理器统计
    print(f"\n📊 事件处理器统计:")
    processors = [user_processor, order_processor, analytics_processor]
    for processor in processors:
        print(f"  {processor.name}: 处理了 {processor.processed_count} 个事件")


def main():
    """主演示函数"""
    demo_approval_system()
    demo_exception_handling()
    demo_event_processing()
    
    print("\n" + "=" * 60)
    print("🎉 责任链模式实际应用演示完成！")
    print("💡 关键要点:")
    print("   • 审批系统：实现多级审批流程")
    print("   • 异常处理：按严重程度分层处理")
    print("   • 事件系统：多处理器协同工作")
    print("   • 责任链模式在企业系统中应用广泛")
    print("   • 提供了灵活的处理流程组织方式")
    print("=" * 60)


if __name__ == "__main__":
    main()
