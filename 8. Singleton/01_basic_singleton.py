"""
01_basic_singleton.py - 单例模式基础实现

日志管理系统示例
这个示例展示了如何使用单例模式来实现日志管理系统。
在应用程序中，通常只需要一个日志管理器来统一处理所有的日志记录，
单例模式确保整个应用程序使用同一个日志实例。
"""

import threading
import time
from datetime import datetime
from typing import List
from enum import Enum


# ==================== 日志级别枚举 ====================
class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# ==================== 基础单例实现 ====================
class BasicSingleton:
    """基础单例模式实现"""
    
    _instance = None
    
    def __new__(cls):
        """重写 __new__ 方法实现单例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化方法"""
        if not hasattr(self, 'initialized'):
            self.value = 0
            self.initialized = True
    
    def set_value(self, value: int):
        """设置值"""
        self.value = value
    
    def get_value(self) -> int:
        """获取值"""
        return self.value


# ==================== 线程安全的单例实现 ====================
class ThreadSafeSingleton:
    """线程安全的单例模式实现"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """使用双重检查锁定确保线程安全"""
        if cls._instance is None:
            with cls._lock:
                # 双重检查：再次检查实例是否已创建
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化方法"""
        if not hasattr(self, 'initialized'):
            self.data = {}
            self.initialized = True
    
    def set_data(self, key: str, value: any):
        """设置数据"""
        with self._lock:
            self.data[key] = value
    
    def get_data(self, key: str) -> any:
        """获取数据"""
        with self._lock:
            return self.data.get(key)


# ==================== 日志管理器单例 ====================
class Logger:
    """日志管理器单例类"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """确保只有一个日志管理器实例"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化日志管理器"""
        if not hasattr(self, 'initialized'):
            self.log_level = LogLevel.INFO
            self.log_file = "application.log"
            self.logs = []
            self.max_logs = 1000  # 最大日志条数
            self.initialized = True
            print("日志管理器已初始化")
    
    def set_log_level(self, level: LogLevel):
        """设置日志级别"""
        self.log_level = level
        print(f"日志级别已设置为: {level.value}")
    
    def set_log_file(self, filename: str):
        """设置日志文件"""
        self.log_file = filename
        print(f"日志文件已设置为: {filename}")
    
    def _should_log(self, level: LogLevel) -> bool:
        """判断是否应该记录该级别的日志"""
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 4
        }
        return level_order[level] >= level_order[self.log_level]
    
    def _add_log(self, level: LogLevel, message: str, module: str = ""):
        """添加日志记录"""
        if not self._should_log(level):
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level.value,
            "module": module,
            "message": message
        }
        
        with self._lock:
            self.logs.append(log_entry)
            # 保持日志数量在限制范围内
            if len(self.logs) > self.max_logs:
                self.logs.pop(0)
        
        # 输出到控制台
        module_info = f"[{module}] " if module else ""
        print(f"{timestamp} [{level.value}] {module_info}{message}")
    
    def debug(self, message: str, module: str = ""):
        """记录调试日志"""
        self._add_log(LogLevel.DEBUG, message, module)
    
    def info(self, message: str, module: str = ""):
        """记录信息日志"""
        self._add_log(LogLevel.INFO, message, module)
    
    def warning(self, message: str, module: str = ""):
        """记录警告日志"""
        self._add_log(LogLevel.WARNING, message, module)
    
    def error(self, message: str, module: str = ""):
        """记录错误日志"""
        self._add_log(LogLevel.ERROR, message, module)
    
    def critical(self, message: str, module: str = ""):
        """记录严重错误日志"""
        self._add_log(LogLevel.CRITICAL, message, module)
    
    def get_logs(self, level: LogLevel = None, limit: int = None) -> List[dict]:
        """获取日志记录"""
        with self._lock:
            logs = self.logs.copy()
        
        # 按级别过滤
        if level:
            logs = [log for log in logs if log["level"] == level.value]
        
        # 限制数量
        if limit:
            logs = logs[-limit:]
        
        return logs
    
    def clear_logs(self):
        """清空日志"""
        with self._lock:
            self.logs.clear()
        print("日志已清空")
    
    def get_log_count(self) -> int:
        """获取日志总数"""
        return len(self.logs)


# ==================== 演示函数 ====================
def demonstrate_basic_singleton():
    """演示基础单例模式"""
    print("=" * 60)
    print("基础单例模式演示")
    print("=" * 60)
    
    # 创建两个实例，验证它们是同一个对象
    singleton1 = BasicSingleton()
    singleton2 = BasicSingleton()
    
    print(f"singleton1 id: {id(singleton1)}")
    print(f"singleton2 id: {id(singleton2)}")
    print(f"是否为同一个对象: {singleton1 is singleton2}")
    
    # 修改一个实例的值，另一个实例也会受影响
    singleton1.set_value(100)
    print(f"singleton1 的值: {singleton1.get_value()}")
    print(f"singleton2 的值: {singleton2.get_value()}")


def demonstrate_thread_safe_singleton():
    """演示线程安全的单例模式"""
    print("\n" + "=" * 60)
    print("线程安全单例模式演示")
    print("=" * 60)
    
    instances = []
    
    def create_instance():
        """在线程中创建实例"""
        instance = ThreadSafeSingleton()
        instances.append(instance)
        time.sleep(0.1)  # 模拟一些处理时间
    
    # 创建多个线程同时创建实例
    threads = []
    for i in range(5):
        thread = threading.Thread(target=create_instance)
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 验证所有实例都是同一个对象
    print(f"创建了 {len(instances)} 个实例")
    first_instance = instances[0]
    all_same = all(instance is first_instance for instance in instances)
    print(f"所有实例都是同一个对象: {all_same}")
    
    # 显示所有实例的ID
    for i, instance in enumerate(instances):
        print(f"实例 {i+1} ID: {id(instance)}")


def demonstrate_logger_singleton():
    """演示日志管理器单例"""
    print("\n" + "=" * 60)
    print("日志管理器单例演示")
    print("=" * 60)
    
    # 获取日志管理器实例
    logger1 = Logger()
    logger2 = Logger()
    
    print(f"logger1 和 logger2 是同一个对象: {logger1 is logger2}")
    
    # 设置日志级别
    logger1.set_log_level(LogLevel.DEBUG)
    
    # 记录不同级别的日志
    logger1.debug("这是一条调试信息", "用户模块")
    logger1.info("用户登录成功", "认证模块")
    logger1.warning("内存使用率较高", "系统监控")
    logger1.error("数据库连接失败", "数据库模块")
    logger1.critical("系统即将崩溃", "系统核心")
    
    # 从另一个实例记录日志
    logger2.info("这是从 logger2 记录的日志", "测试模块")
    
    # 获取日志统计
    print(f"\n总日志数量: {logger1.get_log_count()}")
    
    # 获取错误级别的日志
    error_logs = logger1.get_logs(LogLevel.ERROR)
    print(f"错误日志数量: {len(error_logs)}")


# ==================== 主函数 ====================
def main():
    """主函数 - 演示各种单例模式实现"""
    print("单例模式演示 - 日志管理系统")
    
    # 演示基础单例
    demonstrate_basic_singleton()
    
    # 演示线程安全单例
    demonstrate_thread_safe_singleton()
    
    # 演示日志管理器单例
    demonstrate_logger_singleton()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
