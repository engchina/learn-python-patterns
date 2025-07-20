"""
03_event_system.py - 事件驱动系统的观察者模式

这个示例展示了如何使用观察者模式构建事件驱动系统。
包括事件管理器、事件类型分类、异步事件处理等高级特性。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
from datetime import datetime
import threading
import time


# ==================== 事件类型定义 ====================

class EventType(Enum):
    """事件类型枚举"""
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    ORDER_CREATED = "order_created"
    ORDER_PAID = "order_paid"
    ORDER_SHIPPED = "order_shipped"
    SYSTEM_ERROR = "system_error"
    DATA_UPDATED = "data_updated"


class Event:
    """事件数据类"""
    
    def __init__(self, event_type: EventType, data: Dict[str, Any], source: str = "unknown"):
        self.event_type = event_type
        self.data = data
        self.source = source
        self.timestamp = datetime.now()
        self.event_id = f"{event_type.value}_{int(time.time() * 1000)}"
    
    def __str__(self) -> str:
        return f"Event({self.event_type.value}, {self.source}, {self.timestamp.strftime('%H:%M:%S')})"


# ==================== 事件监听器接口 ====================

class EventListener(ABC):
    """抽象事件监听器"""
    
    @abstractmethod
    def handle_event(self, event: Event) -> None:
        """处理事件"""
        pass
    
    @abstractmethod
    def get_interested_events(self) -> List[EventType]:
        """返回感兴趣的事件类型"""
        pass


# ==================== 事件管理器 ====================

class EventManager:
    """事件管理器 - 实现发布订阅模式"""
    
    def __init__(self):
        # 存储事件监听器
        self._listeners: Dict[EventType, List[EventListener]] = {}
        # 存储函数式监听器
        self._function_listeners: Dict[EventType, List[Callable[[Event], None]]] = {}
        # 事件历史
        self._event_history: List[Event] = []
        # 异步处理开关
        self._async_mode = False
        # 线程池
        self._thread_pool: List[threading.Thread] = []
    
    def subscribe(self, event_type: EventType, listener: EventListener) -> None:
        """订阅事件 - 类监听器"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        
        if listener not in self._listeners[event_type]:
            self._listeners[event_type].append(listener)
            print(f"📝 监听器 {listener.__class__.__name__} 订阅了事件 {event_type.value}")
    
    def subscribe_function(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """订阅事件 - 函数监听器"""
        if event_type not in self._function_listeners:
            self._function_listeners[event_type] = []
        
        if handler not in self._function_listeners[event_type]:
            self._function_listeners[event_type].append(handler)
            print(f"📝 函数监听器 {handler.__name__} 订阅了事件 {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, listener: EventListener) -> None:
        """取消订阅 - 类监听器"""
        if event_type in self._listeners and listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)
            print(f"❌ 监听器 {listener.__class__.__name__} 取消订阅事件 {event_type.value}")
    
    def unsubscribe_function(self, event_type: EventType, handler: Callable[[Event], None]) -> None:
        """取消订阅 - 函数监听器"""
        if event_type in self._function_listeners and handler in self._function_listeners[event_type]:
            self._function_listeners[event_type].remove(handler)
            print(f"❌ 函数监听器 {handler.__name__} 取消订阅事件 {event_type.value}")
    
    def publish(self, event: Event) -> None:
        """发布事件"""
        # 记录事件历史
        self._event_history.append(event)
        
        print(f"\n📢 发布事件: {event}")
        
        # 通知类监听器
        if event.event_type in self._listeners:
            for listener in self._listeners[event.event_type]:
                if self._async_mode:
                    self._handle_async(listener.handle_event, event)
                else:
                    listener.handle_event(event)
        
        # 通知函数监听器
        if event.event_type in self._function_listeners:
            for handler in self._function_listeners[event.event_type]:
                if self._async_mode:
                    self._handle_async(handler, event)
                else:
                    handler(event)
    
    def _handle_async(self, handler: Callable, event: Event) -> None:
        """异步处理事件"""
        thread = threading.Thread(target=handler, args=(event,))
        thread.daemon = True
        thread.start()
        self._thread_pool.append(thread)
    
    def set_async_mode(self, async_mode: bool) -> None:
        """设置异步模式"""
        self._async_mode = async_mode
        print(f"🔄 事件处理模式: {'异步' if async_mode else '同步'}")
    
    def get_event_history(self, event_type: Optional[EventType] = None) -> List[Event]:
        """获取事件历史"""
        if event_type:
            return [event for event in self._event_history if event.event_type == event_type]
        return self._event_history.copy()
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取事件统计"""
        stats = {}
        for event in self._event_history:
            event_type = event.event_type.value
            if event_type not in stats:
                stats[event_type] = 0
            stats[event_type] += 1
        return stats


# ==================== 具体事件监听器 ====================

class UserActivityLogger(EventListener):
    """用户活动日志记录器"""
    
    def __init__(self):
        self._log_entries: List[str] = []
    
    def handle_event(self, event: Event) -> None:
        """记录用户活动"""
        if event.event_type in [EventType.USER_LOGIN, EventType.USER_LOGOUT]:
            user_id = event.data.get('user_id', 'unknown')
            action = "登录" if event.event_type == EventType.USER_LOGIN else "登出"
            log_entry = f"[{event.timestamp.strftime('%H:%M:%S')}] 用户 {user_id} {action}"
            self._log_entries.append(log_entry)
            print(f"📝 用户活动日志: {log_entry}")
    
    def get_interested_events(self) -> List[EventType]:
        return [EventType.USER_LOGIN, EventType.USER_LOGOUT]
    
    def get_logs(self) -> List[str]:
        return self._log_entries.copy()


class OrderProcessor(EventListener):
    """订单处理器"""
    
    def __init__(self):
        self._orders: Dict[str, Dict[str, Any]] = {}
    
    def handle_event(self, event: Event) -> None:
        """处理订单相关事件"""
        if event.event_type == EventType.ORDER_CREATED:
            order_id = event.data.get('order_id')
            self._orders[order_id] = {
                'status': 'created',
                'created_time': event.timestamp,
                'data': event.data
            }
            print(f"📦 订单处理: 创建订单 {order_id}")
        
        elif event.event_type == EventType.ORDER_PAID:
            order_id = event.data.get('order_id')
            if order_id in self._orders:
                self._orders[order_id]['status'] = 'paid'
                self._orders[order_id]['paid_time'] = event.timestamp
                print(f"💳 订单处理: 订单 {order_id} 已支付")
        
        elif event.event_type == EventType.ORDER_SHIPPED:
            order_id = event.data.get('order_id')
            if order_id in self._orders:
                self._orders[order_id]['status'] = 'shipped'
                self._orders[order_id]['shipped_time'] = event.timestamp
                print(f"🚚 订单处理: 订单 {order_id} 已发货")
    
    def get_interested_events(self) -> List[EventType]:
        return [EventType.ORDER_CREATED, EventType.ORDER_PAID, EventType.ORDER_SHIPPED]
    
    def get_order_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        return self._orders.get(order_id)


class SystemMonitor(EventListener):
    """系统监控器"""
    
    def __init__(self):
        self._error_count = 0
        self._last_error_time = None
    
    def handle_event(self, event: Event) -> None:
        """监控系统错误"""
        if event.event_type == EventType.SYSTEM_ERROR:
            self._error_count += 1
            self._last_error_time = event.timestamp
            error_msg = event.data.get('error_message', 'Unknown error')
            print(f"🚨 系统监控: 检测到错误 #{self._error_count} - {error_msg}")
            
            # 错误频率检查
            if self._error_count > 3:
                print(f"⚠️ 系统监控: 错误频率过高，建议检查系统状态")
    
    def get_interested_events(self) -> List[EventType]:
        return [EventType.SYSTEM_ERROR]
    
    def get_error_stats(self) -> Dict[str, Any]:
        return {
            'error_count': self._error_count,
            'last_error_time': self._last_error_time
        }


# ==================== 函数式事件处理器 ====================

def send_email_notification(event: Event) -> None:
    """发送邮件通知"""
    if event.event_type == EventType.ORDER_PAID:
        order_id = event.data.get('order_id')
        user_email = event.data.get('user_email', 'user@example.com')
        print(f"📧 邮件通知: 向 {user_email} 发送订单 {order_id} 支付确认邮件")
    
    elif event.event_type == EventType.SYSTEM_ERROR:
        print(f"📧 邮件通知: 向管理员发送系统错误警报")


def update_analytics(event: Event) -> None:
    """更新分析数据"""
    print(f"📊 分析系统: 记录事件 {event.event_type.value} 到分析数据库")
    # 模拟数据库更新延迟
    time.sleep(0.1)


def cache_invalidation(event: Event) -> None:
    """缓存失效处理"""
    if event.event_type == EventType.DATA_UPDATED:
        cache_key = event.data.get('cache_key', 'default')
        print(f"🗄️ 缓存管理: 清除缓存键 {cache_key}")


# ==================== 演示函数 ====================

def demo_event_system():
    """事件系统演示"""
    print("=" * 60)
    print("🎯 事件驱动系统观察者模式演示")
    print("=" * 60)
    
    # 创建事件管理器
    event_manager = EventManager()
    
    # 创建监听器
    user_logger = UserActivityLogger()
    order_processor = OrderProcessor()
    system_monitor = SystemMonitor()
    
    # 订阅事件
    print("\n📋 订阅事件:")
    event_manager.subscribe(EventType.USER_LOGIN, user_logger)
    event_manager.subscribe(EventType.USER_LOGOUT, user_logger)
    event_manager.subscribe(EventType.ORDER_CREATED, order_processor)
    event_manager.subscribe(EventType.ORDER_PAID, order_processor)
    event_manager.subscribe(EventType.ORDER_SHIPPED, order_processor)
    event_manager.subscribe(EventType.SYSTEM_ERROR, system_monitor)
    
    # 订阅函数式监听器
    event_manager.subscribe_function(EventType.ORDER_PAID, send_email_notification)
    event_manager.subscribe_function(EventType.SYSTEM_ERROR, send_email_notification)
    event_manager.subscribe_function(EventType.DATA_UPDATED, update_analytics)
    event_manager.subscribe_function(EventType.DATA_UPDATED, cache_invalidation)
    
    # 发布事件序列
    print("\n" + "=" * 40)
    print("模拟用户和订单流程:")
    
    # 用户登录
    event_manager.publish(Event(
        EventType.USER_LOGIN,
        {'user_id': 'user123', 'ip_address': '192.168.1.100'},
        'auth_service'
    ))
    
    # 创建订单
    event_manager.publish(Event(
        EventType.ORDER_CREATED,
        {'order_id': 'order456', 'user_id': 'user123', 'amount': 99.99},
        'order_service'
    ))
    
    # 支付订单
    event_manager.publish(Event(
        EventType.ORDER_PAID,
        {'order_id': 'order456', 'user_email': 'user123@example.com', 'payment_method': 'credit_card'},
        'payment_service'
    ))
    
    # 发货
    event_manager.publish(Event(
        EventType.ORDER_SHIPPED,
        {'order_id': 'order456', 'tracking_number': 'TN789'},
        'shipping_service'
    ))
    
    # 系统错误
    event_manager.publish(Event(
        EventType.SYSTEM_ERROR,
        {'error_message': 'Database connection timeout', 'severity': 'high'},
        'database_service'
    ))
    
    # 数据更新
    event_manager.publish(Event(
        EventType.DATA_UPDATED,
        {'table': 'users', 'cache_key': 'user_list'},
        'data_service'
    ))
    
    # 用户登出
    event_manager.publish(Event(
        EventType.USER_LOGOUT,
        {'user_id': 'user123'},
        'auth_service'
    ))
    
    # 显示统计信息
    print("\n" + "=" * 40)
    print("📊 事件统计:")
    stats = event_manager.get_statistics()
    for event_type, count in stats.items():
        print(f"   {event_type}: {count} 次")
    
    # 显示订单状态
    print("\n📦 订单状态:")
    order_status = order_processor.get_order_status('order456')
    if order_status:
        print(f"   订单 order456: {order_status['status']}")
    
    # 显示错误统计
    print("\n🚨 错误统计:")
    error_stats = system_monitor.get_error_stats()
    print(f"   错误次数: {error_stats['error_count']}")


def demo_async_events():
    """异步事件处理演示"""
    print("\n" + "=" * 60)
    print("🔄 异步事件处理演示")
    print("=" * 60)
    
    event_manager = EventManager()
    event_manager.set_async_mode(True)
    
    # 订阅需要时间的处理器
    event_manager.subscribe_function(EventType.DATA_UPDATED, update_analytics)
    
    print("\n发布多个数据更新事件:")
    for i in range(3):
        event_manager.publish(Event(
            EventType.DATA_UPDATED,
            {'table': f'table_{i}', 'cache_key': f'key_{i}'},
            'data_service'
        ))
    
    print("主线程继续执行其他任务...")
    time.sleep(0.5)  # 等待异步处理完成


if __name__ == "__main__":
    # 运行基础演示
    demo_event_system()
    
    # 运行异步演示
    demo_async_events()
    
    print("\n" + "=" * 60)
    print("✅ 事件系统演示完成")
    print("💡 学习要点:")
    print("   - 事件驱动架构的松耦合设计")
    print("   - 支持类和函数两种监听器")
    print("   - 异步事件处理提高性能")
    print("   - 事件历史和统计分析")
    print("=" * 60)
