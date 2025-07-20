#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
事件总线中介者实现

本模块演示了中介者模式在事件总线中的应用，包括：
1. 发布-订阅机制
2. 事件路由和过滤
3. 异步消息处理
4. 现代事件驱动架构

作者: Assistant
日期: 2024-01-20
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Any, Callable, Optional
from enum import Enum
from datetime import datetime
import threading
import queue
import time
import uuid
from dataclasses import dataclass, field


class EventPriority(Enum):
    """事件优先级枚举"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Event:
    """事件类"""
    event_type: str
    data: Any
    source: str
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    priority: EventPriority = EventPriority.NORMAL
    tags: Set[str] = field(default_factory=set)

    def add_tag(self, tag: str) -> None:
        """添加标签"""
        self.tags.add(tag)

    def has_tag(self, tag: str) -> bool:
        """检查是否有指定标签"""
        return tag in self.tags

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'data': self.data,
            'source': self.source,
            'timestamp': self.timestamp.isoformat(),
            'priority': self.priority.value,
            'tags': list(self.tags)
        }


class EventFilter:
    """事件过滤器"""

    def __init__(self, filter_func: Callable[[Event], bool]):
        self.filter_func = filter_func

    def matches(self, event: Event) -> bool:
        """检查事件是否匹配过滤条件"""
        try:
            return self.filter_func(event)
        except Exception:
            return False

    @staticmethod
    def by_type(event_type: str) -> 'EventFilter':
        """按事件类型过滤"""
        return EventFilter(lambda event: event.event_type == event_type)

    @staticmethod
    def by_source(source: str) -> 'EventFilter':
        """按事件源过滤"""
        return EventFilter(lambda event: event.source == source)

    @staticmethod
    def by_priority(min_priority: EventPriority) -> 'EventFilter':
        """按优先级过滤"""
        return EventFilter(lambda event: event.priority.value >= min_priority.value)

    @staticmethod
    def by_tag(tag: str) -> 'EventFilter':
        """按标签过滤"""
        return EventFilter(lambda event: event.has_tag(tag))

    @staticmethod
    def combine_and(*filters: 'EventFilter') -> 'EventFilter':
        """组合多个过滤器（AND逻辑）"""
        return EventFilter(lambda event: all(f.matches(event) for f in filters))

    @staticmethod
    def combine_or(*filters: 'EventFilter') -> 'EventFilter':
        """组合多个过滤器（OR逻辑）"""
        return EventFilter(lambda event: any(f.matches(event) for f in filters))


class EventSubscriber(ABC):
    """事件订阅者接口"""

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        """处理事件"""
        pass

    @abstractmethod
    def get_subscriber_id(self) -> str:
        """获取订阅者ID"""
        pass


class EventSubscription:
    """事件订阅"""

    def __init__(self, subscriber: EventSubscriber, event_filter: EventFilter = None):
        self.subscriber = subscriber
        self.event_filter = event_filter or EventFilter(lambda e: True)  # 默认接受所有事件
        self.subscription_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.event_count = 0
        self.last_event_time: Optional[datetime] = None

    def matches(self, event: Event) -> bool:
        """检查事件是否匹配订阅条件"""
        return self.event_filter.matches(event)

    def deliver_event(self, event: Event) -> bool:
        """投递事件给订阅者"""
        try:
            if self.matches(event):
                self.subscriber.handle_event(event)
                self.event_count += 1
                self.last_event_time = datetime.now()
                return True
        except Exception as e:
            print(f"❌ 事件投递失败: {self.subscriber.get_subscriber_id()} - {e}")
        return False


class EventBus:
    """事件总线中介者"""

    def __init__(self, name: str = "EventBus", async_processing: bool = True):
        self.name = name
        self.async_processing = async_processing
        self.subscriptions: Dict[str, EventSubscription] = {}
        self.event_history: List[Event] = []
        self.processing_queue = queue.PriorityQueue()
        self.is_running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.stats = {
            'events_published': 0,
            'events_delivered': 0,
            'subscribers_count': 0
        }

        if async_processing:
            self._start_worker()

    def _start_worker(self) -> None:
        """启动工作线程"""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._process_events, daemon=True)
        self.worker_thread.start()
        print(f"🚀 事件总线 {self.name} 异步处理已启动")

    def _process_events(self) -> None:
        """处理事件队列"""
        while self.is_running:
            try:
                # 获取事件（优先级队列，数字越小优先级越高）
                priority, event = self.processing_queue.get(timeout=1.0)
                self._deliver_event(event)
                self.processing_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ 事件处理异常: {e}")

    def subscribe(self, subscriber: EventSubscriber, event_filter: EventFilter = None) -> str:
        """订阅事件"""
        subscription = EventSubscription(subscriber, event_filter)
        self.subscriptions[subscription.subscription_id] = subscription
        self.stats['subscribers_count'] = len(self.subscriptions)

        print(f"📝 新订阅者: {subscriber.get_subscriber_id()}")
        return subscription.subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """取消订阅"""
        if subscription_id in self.subscriptions:
            subscription = self.subscriptions[subscription_id]
            del self.subscriptions[subscription_id]
            self.stats['subscribers_count'] = len(self.subscriptions)

            print(f"🗑️ 取消订阅: {subscription.subscriber.get_subscriber_id()}")
            return True
        return False

    def publish(self, event: Event) -> None:
        """发布事件"""
        self.event_history.append(event)
        self.stats['events_published'] += 1

        print(f"📢 发布事件: {event.event_type} (来源: {event.source})")

        if self.async_processing:
            # 异步处理：加入队列
            priority = 5 - event.priority.value  # 转换为队列优先级（数字越小优先级越高）
            self.processing_queue.put((priority, event))
        else:
            # 同步处理：立即投递
            self._deliver_event(event)

    def _deliver_event(self, event: Event) -> None:
        """投递事件给订阅者"""
        delivered_count = 0

        for subscription in self.subscriptions.values():
            if subscription.deliver_event(event):
                delivered_count += 1

        self.stats['events_delivered'] += delivered_count

        if delivered_count > 0:
            print(f"📬 事件已投递给 {delivered_count} 个订阅者")

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'name': self.name,
            'async_processing': self.async_processing,
            'events_published': self.stats['events_published'],
            'events_delivered': self.stats['events_delivered'],
            'subscribers_count': self.stats['subscribers_count'],
            'queue_size': self.processing_queue.qsize() if self.async_processing else 0,
            'history_size': len(self.event_history)
        }

    def get_recent_events(self, count: int = 10) -> List[Event]:
        """获取最近的事件"""
        return self.event_history[-count:]

    def shutdown(self) -> None:
        """关闭事件总线"""
        if self.async_processing and self.is_running:
            self.is_running = False
            if self.worker_thread:
                self.worker_thread.join(timeout=2.0)
            print(f"🛑 事件总线 {self.name} 已关闭")


# 具体的事件订阅者实现
class LoggingSubscriber(EventSubscriber):
    """日志记录订阅者"""

    def __init__(self, name: str):
        self.name = name
        self.logged_events: List[Event] = []

    def handle_event(self, event: Event) -> None:
        """处理事件 - 记录日志"""
        self.logged_events.append(event)
        timestamp = event.timestamp.strftime("%H:%M:%S")
        print(f"📝 [{self.name}] [{timestamp}] {event.event_type}: {event.data}")

    def get_subscriber_id(self) -> str:
        return f"Logger_{self.name}"


class EmailNotificationSubscriber(EventSubscriber):
    """邮件通知订阅者"""

    def __init__(self, email: str):
        self.email = email
        self.sent_count = 0

    def handle_event(self, event: Event) -> None:
        """处理事件 - 发送邮件"""
        self.sent_count += 1
        print(f"📧 发送邮件到 {self.email}: {event.event_type} - {event.data}")

    def get_subscriber_id(self) -> str:
        return f"Email_{self.email}"


class MetricsSubscriber(EventSubscriber):
    """指标统计订阅者"""

    def __init__(self):
        self.metrics: Dict[str, int] = {}

    def handle_event(self, event: Event) -> None:
        """处理事件 - 统计指标"""
        event_type = event.event_type
        self.metrics[event_type] = self.metrics.get(event_type, 0) + 1
        print(f"📊 指标更新: {event_type} = {self.metrics[event_type]}")

    def get_subscriber_id(self) -> str:
        return "MetricsCollector"

    def get_metrics(self) -> Dict[str, int]:
        return self.metrics.copy()


class AlertSubscriber(EventSubscriber):
    """告警订阅者"""

    def __init__(self, alert_threshold: int = 3):
        self.alert_threshold = alert_threshold
        self.error_count = 0

    def handle_event(self, event: Event) -> None:
        """处理事件 - 告警检查"""
        if event.priority == EventPriority.CRITICAL:
            self.error_count += 1
            print(f"🚨 严重告警: {event.data} (累计: {self.error_count})")

            if self.error_count >= self.alert_threshold:
                print(f"🔥 告警升级: 严重错误已达到 {self.error_count} 次！")

    def get_subscriber_id(self) -> str:
        return "AlertManager"


def demo_event_bus():
    """演示事件总线"""
    print("=" * 50)
    print("🚌 事件总线中介者演示")
    print("=" * 50)

    # 创建事件总线
    event_bus = EventBus("MainEventBus", async_processing=True)

    # 创建订阅者
    logger = LoggingSubscriber("SystemLogger")
    email_notifier = EmailNotificationSubscriber("admin@example.com")
    metrics_collector = MetricsSubscriber()
    alert_manager = AlertSubscriber(alert_threshold=2)

    # 订阅事件
    print("\n📝 设置事件订阅:")

    # 日志记录器订阅所有事件
    event_bus.subscribe(logger)

    # 邮件通知只订阅高优先级事件
    email_filter = EventFilter.by_priority(EventPriority.HIGH)
    event_bus.subscribe(email_notifier, email_filter)

    # 指标收集器订阅所有事件
    event_bus.subscribe(metrics_collector)

    # 告警管理器只订阅严重事件
    alert_filter = EventFilter.by_priority(EventPriority.CRITICAL)
    event_bus.subscribe(alert_manager, alert_filter)

    # 发布各种事件
    print("\n📢 发布事件:")

    # 普通事件
    user_login = Event(
        event_type="user_login",
        data={"user_id": "user123", "ip": "192.168.1.100"},
        source="AuthService",
        priority=EventPriority.NORMAL
    )
    user_login.add_tag("security")
    event_bus.publish(user_login)

    time.sleep(0.1)  # 等待异步处理

    # 高优先级事件
    payment_failed = Event(
        event_type="payment_failed",
        data={"order_id": "ORD123", "amount": 299.99, "reason": "insufficient_funds"},
        source="PaymentService",
        priority=EventPriority.HIGH
    )
    payment_failed.add_tag("payment")
    payment_failed.add_tag("error")
    event_bus.publish(payment_failed)

    time.sleep(0.1)

    # 严重事件
    system_error = Event(
        event_type="system_error",
        data={"error": "Database connection lost", "service": "UserService"},
        source="SystemMonitor",
        priority=EventPriority.CRITICAL
    )
    system_error.add_tag("system")
    system_error.add_tag("critical")
    event_bus.publish(system_error)

    time.sleep(0.1)

    # 再发布一个严重事件触发告警升级
    another_error = Event(
        event_type="system_error",
        data={"error": "Memory usage critical", "service": "DataProcessor"},
        source="SystemMonitor",
        priority=EventPriority.CRITICAL
    )
    event_bus.publish(another_error)

    time.sleep(0.2)  # 等待所有事件处理完成

    # 显示统计信息
    print("\n📊 事件总线统计:")
    stats = event_bus.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n📈 指标统计:")
    metrics = metrics_collector.get_metrics()
    for event_type, count in metrics.items():
        print(f"  {event_type}: {count}")

    # 演示事件过滤
    print("\n🔍 演示复杂事件过滤:")

    # 创建一个只订阅支付相关高优先级事件的订阅者
    payment_monitor = LoggingSubscriber("PaymentMonitor")
    payment_filter = EventFilter.combine_and(
        EventFilter.by_tag("payment"),
        EventFilter.by_priority(EventPriority.HIGH)
    )
    event_bus.subscribe(payment_monitor, payment_filter)

    # 发布一些测试事件
    normal_payment = Event(
        event_type="payment_success",
        data={"order_id": "ORD124", "amount": 99.99},
        source="PaymentService",
        priority=EventPriority.NORMAL
    )
    normal_payment.add_tag("payment")
    event_bus.publish(normal_payment)  # 不会被PaymentMonitor接收（优先级不够）

    time.sleep(0.1)

    high_payment = Event(
        event_type="large_payment",
        data={"order_id": "ORD125", "amount": 9999.99},
        source="PaymentService",
        priority=EventPriority.HIGH
    )
    high_payment.add_tag("payment")
    event_bus.publish(high_payment)  # 会被PaymentMonitor接收

    time.sleep(0.2)

    # 最终统计
    print("\n📋 最终统计:")
    final_stats = event_bus.get_stats()
    for key, value in final_stats.items():
        print(f"  {key}: {value}")

    # 关闭事件总线
    event_bus.shutdown()


if __name__ == "__main__":
    print("🎯 事件总线中介者模式演示")

    demo_event_bus()

    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 事件总线是中介者模式在现代架构中的重要应用")
    print("=" * 50)
