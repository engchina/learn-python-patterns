"""
04_module_singleton.py - 模块级单例模式

系统监控器示例
这个示例展示了如何使用Python模块的特性来实现单例模式。
在Python中，模块本身就是单例的，这是最简单和最Pythonic的单例实现方式，
适合用于系统监控、全局状态管理等场景。
"""

import threading
import time
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable
from collections import deque


# ==================== 模块级变量（单例数据） ====================
_system_monitor = None
_performance_tracker = None
_event_dispatcher = None
_lock = threading.Lock()


# ==================== 系统监控器类 ====================
class SystemMonitor:
    """系统监控器"""
    
    def __init__(self):
        self.is_monitoring = False
        self.monitor_thread = None
        self.metrics_history = deque(maxlen=1000)  # 保留最近1000条记录
        self.alert_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0
        }
        self.alert_callbacks = []
        self.start_time = datetime.now()
        print("系统监控器已初始化")
    
    def start_monitoring(self, interval: float = 1.0):
        """开始监控"""
        if self.is_monitoring:
            print("监控已经在运行")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        print(f"系统监控已启动，监控间隔: {interval}秒")
    
    def stop_monitoring(self):
        """停止监控"""
        if not self.is_monitoring:
            print("监控未运行")
            return
        
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        print("系统监控已停止")
    
    def _monitor_loop(self, interval: float):
        """监控循环"""
        while self.is_monitoring:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                self._check_alerts(metrics)
                time.sleep(interval)
            except Exception as e:
                print(f"监控过程中发生错误: {e}")
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """收集系统指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            
            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            
            # 网络IO
            net_io = psutil.net_io_counters()
            
            # 进程数量
            process_count = len(psutil.pids())
            
            metrics = {
                "timestamp": datetime.now(),
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available,
                "memory_total": memory.total,
                "disk_usage": (disk.used / disk.total) * 100,
                "disk_free": disk.free,
                "disk_total": disk.total,
                "network_bytes_sent": net_io.bytes_sent,
                "network_bytes_recv": net_io.bytes_recv,
                "process_count": process_count,
                "load_average": os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
            }
            
            return metrics
        except Exception as e:
            print(f"收集系统指标时发生错误: {e}")
            return {}
    
    def _check_alerts(self, metrics: Dict[str, Any]):
        """检查告警条件"""
        alerts = []
        
        # 检查CPU使用率
        if metrics.get("cpu_usage", 0) > self.alert_thresholds["cpu_usage"]:
            alerts.append({
                "type": "cpu_high",
                "message": f"CPU使用率过高: {metrics['cpu_usage']:.1f}%",
                "value": metrics["cpu_usage"],
                "threshold": self.alert_thresholds["cpu_usage"]
            })
        
        # 检查内存使用率
        if metrics.get("memory_usage", 0) > self.alert_thresholds["memory_usage"]:
            alerts.append({
                "type": "memory_high",
                "message": f"内存使用率过高: {metrics['memory_usage']:.1f}%",
                "value": metrics["memory_usage"],
                "threshold": self.alert_thresholds["memory_usage"]
            })
        
        # 检查磁盘使用率
        if metrics.get("disk_usage", 0) > self.alert_thresholds["disk_usage"]:
            alerts.append({
                "type": "disk_high",
                "message": f"磁盘使用率过高: {metrics['disk_usage']:.1f}%",
                "value": metrics["disk_usage"],
                "threshold": self.alert_thresholds["disk_usage"]
            })
        
        # 触发告警回调
        for alert in alerts:
            self._trigger_alert(alert)
    
    def _trigger_alert(self, alert: Dict[str, Any]):
        """触发告警"""
        alert["timestamp"] = datetime.now()
        print(f"告警: {alert['message']}")
        
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"执行告警回调时发生错误: {e}")
    
    def add_alert_callback(self, callback: Callable):
        """添加告警回调函数"""
        self.alert_callbacks.append(callback)
    
    def set_alert_threshold(self, metric: str, threshold: float):
        """设置告警阈值"""
        self.alert_thresholds[metric] = threshold
        print(f"告警阈值已设置: {metric} = {threshold}")
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """获取当前系统指标"""
        return self._collect_metrics()
    
    def get_metrics_history(self, minutes: int = 10) -> List[Dict[str, Any]]:
        """获取历史指标数据"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            metrics for metrics in self.metrics_history
            if metrics.get("timestamp", datetime.min) >= cutoff_time
        ]
    
    def get_average_metrics(self, minutes: int = 5) -> Dict[str, float]:
        """获取平均指标"""
        history = self.get_metrics_history(minutes)
        if not history:
            return {}
        
        metrics_sum = {}
        count = len(history)
        
        for metrics in history:
            for key, value in metrics.items():
                if isinstance(value, (int, float)) and key != "timestamp":
                    metrics_sum[key] = metrics_sum.get(key, 0) + value
        
        return {key: value / count for key, value in metrics_sum.items()}
    
    def get_status(self) -> Dict[str, Any]:
        """获取监控器状态"""
        return {
            "is_monitoring": self.is_monitoring,
            "start_time": self.start_time.isoformat(),
            "uptime": str(datetime.now() - self.start_time),
            "metrics_count": len(self.metrics_history),
            "alert_thresholds": self.alert_thresholds,
            "alert_callbacks_count": len(self.alert_callbacks)
        }


# ==================== 性能跟踪器类 ====================
class PerformanceTracker:
    """性能跟踪器"""
    
    def __init__(self):
        self.function_stats = {}
        self.request_stats = {}
        self.lock = threading.Lock()
        print("性能跟踪器已初始化")
    
    def track_function(self, func_name: str, execution_time: float):
        """跟踪函数执行时间"""
        with self.lock:
            if func_name not in self.function_stats:
                self.function_stats[func_name] = {
                    "call_count": 0,
                    "total_time": 0.0,
                    "min_time": float('inf'),
                    "max_time": 0.0,
                    "avg_time": 0.0
                }
            
            stats = self.function_stats[func_name]
            stats["call_count"] += 1
            stats["total_time"] += execution_time
            stats["min_time"] = min(stats["min_time"], execution_time)
            stats["max_time"] = max(stats["max_time"], execution_time)
            stats["avg_time"] = stats["total_time"] / stats["call_count"]
    
    def track_request(self, endpoint: str, method: str, status_code: int, response_time: float):
        """跟踪HTTP请求"""
        key = f"{method} {endpoint}"
        
        with self.lock:
            if key not in self.request_stats:
                self.request_stats[key] = {
                    "request_count": 0,
                    "total_time": 0.0,
                    "min_time": float('inf'),
                    "max_time": 0.0,
                    "avg_time": 0.0,
                    "status_codes": {}
                }
            
            stats = self.request_stats[key]
            stats["request_count"] += 1
            stats["total_time"] += response_time
            stats["min_time"] = min(stats["min_time"], response_time)
            stats["max_time"] = max(stats["max_time"], response_time)
            stats["avg_time"] = stats["total_time"] / stats["request_count"]
            
            # 统计状态码
            stats["status_codes"][status_code] = stats["status_codes"].get(status_code, 0) + 1
    
    def get_function_stats(self, func_name: str = None) -> Dict[str, Any]:
        """获取函数统计信息"""
        with self.lock:
            if func_name:
                return self.function_stats.get(func_name, {})
            return self.function_stats.copy()
    
    def get_request_stats(self, endpoint: str = None) -> Dict[str, Any]:
        """获取请求统计信息"""
        with self.lock:
            if endpoint:
                return self.request_stats.get(endpoint, {})
            return self.request_stats.copy()
    
    def get_top_slow_functions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最慢的函数"""
        with self.lock:
            functions = [
                {"name": name, **stats}
                for name, stats in self.function_stats.items()
            ]
            return sorted(functions, key=lambda x: x["avg_time"], reverse=True)[:limit]
    
    def get_top_slow_requests(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最慢的请求"""
        with self.lock:
            requests = [
                {"endpoint": endpoint, **stats}
                for endpoint, stats in self.request_stats.items()
            ]
            return sorted(requests, key=lambda x: x["avg_time"], reverse=True)[:limit]
    
    def reset_stats(self):
        """重置统计信息"""
        with self.lock:
            self.function_stats.clear()
            self.request_stats.clear()
        print("性能统计信息已重置")


# ==================== 事件分发器类 ====================
class EventDispatcher:
    """事件分发器"""
    
    def __init__(self):
        self.listeners = {}
        self.event_history = deque(maxlen=1000)
        self.lock = threading.Lock()
        print("事件分发器已初始化")
    
    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件"""
        with self.lock:
            if event_type not in self.listeners:
                self.listeners[event_type] = []
            self.listeners[event_type].append(callback)
        print(f"已订阅事件: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """取消订阅事件"""
        with self.lock:
            if event_type in self.listeners:
                if callback in self.listeners[event_type]:
                    self.listeners[event_type].remove(callback)
                    print(f"已取消订阅事件: {event_type}")
    
    def emit(self, event_type: str, data: Any = None):
        """发布事件"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now()
        }
        
        with self.lock:
            self.event_history.append(event)
            listeners = self.listeners.get(event_type, []).copy()
        
        print(f"发布事件: {event_type}")
        
        # 异步执行监听器
        for listener in listeners:
            try:
                threading.Thread(target=listener, args=(event,), daemon=True).start()
            except Exception as e:
                print(f"执行事件监听器时发生错误: {e}")
    
    def get_event_history(self, event_type: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """获取事件历史"""
        with self.lock:
            events = list(self.event_history)
        
        if event_type:
            events = [event for event in events if event["type"] == event_type]
        
        return events[-limit:]
    
    def get_listener_count(self, event_type: str = None) -> int:
        """获取监听器数量"""
        with self.lock:
            if event_type:
                return len(self.listeners.get(event_type, []))
            return sum(len(listeners) for listeners in self.listeners.values())


# ==================== 模块级单例获取函数 ====================
def get_system_monitor() -> SystemMonitor:
    """获取系统监控器单例"""
    global _system_monitor
    if _system_monitor is None:
        with _lock:
            if _system_monitor is None:
                _system_monitor = SystemMonitor()
    return _system_monitor


def get_performance_tracker() -> PerformanceTracker:
    """获取性能跟踪器单例"""
    global _performance_tracker
    if _performance_tracker is None:
        with _lock:
            if _performance_tracker is None:
                _performance_tracker = PerformanceTracker()
    return _performance_tracker


def get_event_dispatcher() -> EventDispatcher:
    """获取事件分发器单例"""
    global _event_dispatcher
    if _event_dispatcher is None:
        with _lock:
            if _event_dispatcher is None:
                _event_dispatcher = EventDispatcher()
    return _event_dispatcher


# ==================== 装饰器工具 ====================
def performance_monitor(func):
    """性能监控装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            tracker = get_performance_tracker()
            tracker.track_function(func.__name__, execution_time)
    
    return wrapper


# ==================== 演示函数 ====================
def demonstrate_system_monitor():
    """演示系统监控器"""
    print("=" * 60)
    print("系统监控器模块单例演示")
    print("=" * 60)
    
    # 获取监控器实例
    monitor1 = get_system_monitor()
    monitor2 = get_system_monitor()
    
    print(f"monitor1 和 monitor2 是同一个对象: {monitor1 is monitor2}")
    
    # 添加告警回调
    def alert_handler(alert):
        print(f"收到告警: {alert['type']} - {alert['message']}")
    
    monitor1.add_alert_callback(alert_handler)
    
    # 设置告警阈值
    monitor1.set_alert_threshold("cpu_usage", 50.0)  # 降低阈值以便演示
    
    # 获取当前系统指标
    current_metrics = monitor1.get_current_metrics()
    print(f"当前系统指标: CPU={current_metrics.get('cpu_usage', 0):.1f}%, "
          f"内存={current_metrics.get('memory_usage', 0):.1f}%")
    
    # 启动监控（短时间演示）
    monitor1.start_monitoring(0.5)
    time.sleep(2)
    monitor1.stop_monitoring()
    
    # 获取平均指标
    avg_metrics = monitor1.get_average_metrics(1)
    print(f"平均指标: {avg_metrics}")


def demonstrate_performance_tracker():
    """演示性能跟踪器"""
    print("\n" + "=" * 60)
    print("性能跟踪器模块单例演示")
    print("=" * 60)
    
    # 获取跟踪器实例
    tracker1 = get_performance_tracker()
    tracker2 = get_performance_tracker()
    
    print(f"tracker1 和 tracker2 是同一个对象: {tracker1 is tracker2}")
    
    # 使用装饰器监控函数性能
    @performance_monitor
    def slow_function():
        time.sleep(0.1)
        return "完成"
    
    @performance_monitor
    def fast_function():
        time.sleep(0.01)
        return "完成"
    
    # 执行函数多次
    for _ in range(3):
        slow_function()
        fast_function()
    
    # 手动跟踪请求
    tracker1.track_request("/api/users", "GET", 200, 0.05)
    tracker1.track_request("/api/users", "GET", 200, 0.03)
    tracker1.track_request("/api/orders", "POST", 201, 0.15)
    
    # 获取统计信息
    function_stats = tracker1.get_function_stats()
    print(f"函数统计: {function_stats}")
    
    request_stats = tracker1.get_request_stats()
    print(f"请求统计: {request_stats}")
    
    # 获取最慢的函数
    slow_functions = tracker1.get_top_slow_functions(5)
    print(f"最慢的函数: {slow_functions}")


def demonstrate_event_dispatcher():
    """演示事件分发器"""
    print("\n" + "=" * 60)
    print("事件分发器模块单例演示")
    print("=" * 60)
    
    # 获取分发器实例
    dispatcher1 = get_event_dispatcher()
    dispatcher2 = get_event_dispatcher()
    
    print(f"dispatcher1 和 dispatcher2 是同一个对象: {dispatcher1 is dispatcher2}")
    
    # 定义事件监听器
    def user_login_handler(event):
        print(f"用户登录事件处理: {event['data']}")
    
    def system_alert_handler(event):
        print(f"系统告警事件处理: {event['data']}")
    
    # 订阅事件
    dispatcher1.subscribe("user_login", user_login_handler)
    dispatcher1.subscribe("system_alert", system_alert_handler)
    
    # 发布事件
    dispatcher1.emit("user_login", {"user_id": 1001, "username": "张三"})
    dispatcher1.emit("system_alert", {"level": "warning", "message": "内存使用率过高"})
    
    time.sleep(0.1)  # 等待异步事件处理完成
    
    # 获取事件历史
    history = dispatcher1.get_event_history(limit=5)
    print(f"事件历史数量: {len(history)}")
    
    # 获取监听器数量
    listener_count = dispatcher1.get_listener_count()
    print(f"总监听器数量: {listener_count}")


def main():
    """主函数"""
    print("模块级单例模式演示")
    
    demonstrate_system_monitor()
    demonstrate_performance_tracker()
    demonstrate_event_dispatcher()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
