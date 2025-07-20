"""
03_metaclass_singleton.py - 元类实现单例模式

数据库连接池系统示例
这个示例展示了如何使用元类来实现单例模式。
元类方式实现单例模式更加底层和强大，
适合用于数据库连接池、资源管理等需要严格控制实例的场景。
"""

import threading
import time
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


# ==================== 单例元类实现 ====================
class SingletonMeta(type):
    """单例元类"""
    
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        """控制类的实例化过程"""
        if cls not in cls._instances:
            with cls._lock:
                # 双重检查锁定
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
    def reset_instance(cls):
        """重置实例（主要用于测试）"""
        with cls._lock:
            if cls in cls._instances:
                del cls._instances[cls]
    
    def get_instance_count(cls):
        """获取实例数量"""
        return len([k for k in cls._instances.keys() if k == cls])


class ThreadSafeSingletonMeta(type):
    """线程安全的单例元类（增强版）"""
    
    _instances = {}
    _locks = {}
    _main_lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        """控制类的实例化过程"""
        # 为每个类创建独立的锁
        if cls not in cls._locks:
            with cls._main_lock:
                if cls not in cls._locks:
                    cls._locks[cls] = threading.Lock()
        
        if cls not in cls._instances:
            with cls._locks[cls]:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
                    print(f"创建了新的 {cls.__name__} 实例")
        
        return cls._instances[cls]
    
    def reset_instance(cls):
        """重置实例"""
        with cls._locks.get(cls, threading.Lock()):
            if cls in cls._instances:
                instance = cls._instances[cls]
                if hasattr(instance, 'cleanup'):
                    instance.cleanup()
                del cls._instances[cls]
                print(f"重置了 {cls.__name__} 实例")
    
    def get_all_instances(cls):
        """获取所有实例"""
        return dict(cls._instances)


# ==================== 连接状态枚举 ====================
class ConnectionStatus(Enum):
    """连接状态"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"
    CLOSED = "closed"


# ==================== 数据库连接类 ====================
class DatabaseConnection:
    """数据库连接类"""
    
    def __init__(self, connection_id: str, host: str, port: int, database: str):
        self.connection_id = connection_id
        self.host = host
        self.port = port
        self.database = database
        self.status = ConnectionStatus.DISCONNECTED
        self.created_at = datetime.now()
        self.last_used = datetime.now()
        self.query_count = 0
        self.is_in_use = False
    
    def connect(self):
        """连接数据库"""
        self.status = ConnectionStatus.CONNECTING
        # 模拟连接过程
        time.sleep(0.1)
        self.status = ConnectionStatus.CONNECTED
        print(f"连接 {self.connection_id} 已建立")
    
    def disconnect(self):
        """断开连接"""
        self.status = ConnectionStatus.DISCONNECTED
        print(f"连接 {self.connection_id} 已断开")
    
    def execute_query(self, query: str):
        """执行查询"""
        if self.status != ConnectionStatus.CONNECTED:
            raise Exception(f"连接 {self.connection_id} 未建立")
        
        self.query_count += 1
        self.last_used = datetime.now()
        # 模拟查询执行时间
        time.sleep(random.uniform(0.01, 0.05))
        return f"查询结果: {query} (连接: {self.connection_id})"
    
    def is_alive(self) -> bool:
        """检查连接是否存活"""
        return self.status == ConnectionStatus.CONNECTED
    
    def get_info(self) -> Dict[str, Any]:
        """获取连接信息"""
        return {
            "connection_id": self.connection_id,
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat(),
            "query_count": self.query_count,
            "is_in_use": self.is_in_use
        }


# ==================== 数据库连接池 ====================
class DatabaseConnectionPool(metaclass=ThreadSafeSingletonMeta):
    """数据库连接池（使用元类实现单例）"""
    
    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.database = "myapp"
        self.username = "admin"
        self.password = "password"
        self.min_connections = 5
        self.max_connections = 20
        self.connections = []
        self.available_connections = []
        self.in_use_connections = []
        self.connection_counter = 0
        self.lock = threading.Lock()
        self.stats = {
            "total_created": 0,
            "total_destroyed": 0,
            "current_active": 0,
            "peak_usage": 0,
            "total_requests": 0,
            "failed_requests": 0
        }
        print("数据库连接池已初始化")
    
    def configure(self, host: str, port: int, database: str, username: str, password: str):
        """配置连接池"""
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        print(f"连接池已配置: {host}:{port}/{database}")
    
    def initialize(self):
        """初始化连接池"""
        with self.lock:
            # 创建最小数量的连接
            for _ in range(self.min_connections):
                connection = self._create_connection()
                self.available_connections.append(connection)
            print(f"连接池已初始化，创建了 {self.min_connections} 个连接")
    
    def _create_connection(self) -> DatabaseConnection:
        """创建新连接"""
        self.connection_counter += 1
        connection_id = f"conn_{self.connection_counter}"
        connection = DatabaseConnection(connection_id, self.host, self.port, self.database)
        connection.connect()
        
        self.connections.append(connection)
        self.stats["total_created"] += 1
        self.stats["current_active"] += 1
        
        return connection
    
    def get_connection(self) -> Optional[DatabaseConnection]:
        """获取连接"""
        with self.lock:
            self.stats["total_requests"] += 1
            
            # 如果有可用连接，直接返回
            if self.available_connections:
                connection = self.available_connections.pop()
                connection.is_in_use = True
                self.in_use_connections.append(connection)
                
                # 更新峰值使用统计
                if len(self.in_use_connections) > self.stats["peak_usage"]:
                    self.stats["peak_usage"] = len(self.in_use_connections)
                
                print(f"获取连接: {connection.connection_id}")
                return connection
            
            # 如果没有可用连接但未达到最大连接数，创建新连接
            if len(self.connections) < self.max_connections:
                connection = self._create_connection()
                connection.is_in_use = True
                self.in_use_connections.append(connection)
                
                if len(self.in_use_connections) > self.stats["peak_usage"]:
                    self.stats["peak_usage"] = len(self.in_use_connections)
                
                print(f"创建并获取新连接: {connection.connection_id}")
                return connection
            
            # 连接池已满
            self.stats["failed_requests"] += 1
            print("连接池已满，无法获取连接")
            return None
    
    def return_connection(self, connection: DatabaseConnection):
        """归还连接"""
        with self.lock:
            if connection in self.in_use_connections:
                self.in_use_connections.remove(connection)
                connection.is_in_use = False
                
                # 检查连接是否仍然有效
                if connection.is_alive():
                    self.available_connections.append(connection)
                    print(f"归还连接: {connection.connection_id}")
                else:
                    # 连接已失效，移除并创建新连接
                    self._remove_connection(connection)
                    if len(self.connections) < self.min_connections:
                        new_connection = self._create_connection()
                        self.available_connections.append(new_connection)
                        print(f"连接已失效，创建新连接: {new_connection.connection_id}")
    
    def _remove_connection(self, connection: DatabaseConnection):
        """移除连接"""
        if connection in self.connections:
            self.connections.remove(connection)
            connection.disconnect()
            self.stats["total_destroyed"] += 1
            self.stats["current_active"] -= 1
            print(f"移除连接: {connection.connection_id}")
    
    def close_all_connections(self):
        """关闭所有连接"""
        with self.lock:
            all_connections = self.connections.copy()
            for connection in all_connections:
                self._remove_connection(connection)
            
            self.available_connections.clear()
            self.in_use_connections.clear()
            print("所有连接已关闭")
    
    def get_pool_status(self) -> Dict[str, Any]:
        """获取连接池状态"""
        with self.lock:
            return {
                "total_connections": len(self.connections),
                "available_connections": len(self.available_connections),
                "in_use_connections": len(self.in_use_connections),
                "min_connections": self.min_connections,
                "max_connections": self.max_connections,
                "stats": self.stats.copy()
            }
    
    def cleanup(self):
        """清理资源"""
        self.close_all_connections()
        print("连接池已清理")


# ==================== 应用程序管理器 ====================
class ApplicationManager(metaclass=SingletonMeta):
    """应用程序管理器（使用基础元类实现单例）"""
    
    def __init__(self):
        self.app_name = "MyApplication"
        self.version = "1.0.0"
        self.start_time = datetime.now()
        self.is_running = False
        self.modules = {}
        self.event_handlers = {}
        print("应用程序管理器已初始化")
    
    def start(self):
        """启动应用程序"""
        if self.is_running:
            print("应用程序已经在运行")
            return
        
        self.is_running = True
        self.start_time = datetime.now()
        print(f"应用程序 {self.app_name} v{self.version} 已启动")
    
    def stop(self):
        """停止应用程序"""
        if not self.is_running:
            print("应用程序未运行")
            return
        
        self.is_running = False
        print(f"应用程序 {self.app_name} 已停止")
    
    def register_module(self, name: str, module: Any):
        """注册模块"""
        self.modules[name] = module
        print(f"模块已注册: {name}")
    
    def get_module(self, name: str) -> Any:
        """获取模块"""
        return self.modules.get(name)
    
    def get_uptime(self) -> str:
        """获取运行时间"""
        if not self.is_running:
            return "应用程序未运行"
        
        uptime = datetime.now() - self.start_time
        return str(uptime)
    
    def get_status(self) -> Dict[str, Any]:
        """获取应用程序状态"""
        return {
            "app_name": self.app_name,
            "version": self.version,
            "is_running": self.is_running,
            "start_time": self.start_time.isoformat() if self.is_running else None,
            "uptime": self.get_uptime(),
            "modules": list(self.modules.keys())
        }


# ==================== 演示函数 ====================
def demonstrate_database_pool():
    """演示数据库连接池"""
    print("=" * 60)
    print("数据库连接池单例演示")
    print("=" * 60)
    
    # 创建连接池实例
    pool1 = DatabaseConnectionPool()
    pool2 = DatabaseConnectionPool()
    
    print(f"pool1 和 pool2 是同一个对象: {pool1 is pool2}")
    
    # 配置和初始化连接池
    pool1.configure("localhost", 5432, "myapp", "admin", "password")
    pool1.initialize()
    
    # 获取连接并执行查询
    conn1 = pool1.get_connection()
    if conn1:
        result = conn1.execute_query("SELECT * FROM users")
        print(f"查询结果: {result}")
        pool1.return_connection(conn1)
    
    # 从另一个实例获取连接
    conn2 = pool2.get_connection()
    if conn2:
        result = conn2.execute_query("SELECT COUNT(*) FROM orders")
        print(f"查询结果: {result}")
        pool2.return_connection(conn2)
    
    # 显示连接池状态
    status = pool1.get_pool_status()
    print(f"连接池状态: {status}")


def demonstrate_application_manager():
    """演示应用程序管理器"""
    print("\n" + "=" * 60)
    print("应用程序管理器单例演示")
    print("=" * 60)
    
    # 创建应用程序管理器实例
    app1 = ApplicationManager()
    app2 = ApplicationManager()
    
    print(f"app1 和 app2 是同一个对象: {app1 is app2}")
    
    # 启动应用程序
    app1.start()
    
    # 注册模块
    app1.register_module("database", "DatabaseModule")
    app1.register_module("cache", "CacheModule")
    
    # 从另一个实例获取状态
    status = app2.get_status()
    print(f"应用程序状态: {status}")
    
    # 获取运行时间
    time.sleep(1)
    print(f"运行时间: {app2.get_uptime()}")


def demonstrate_thread_safety():
    """演示线程安全性"""
    print("\n" + "=" * 60)
    print("元类单例线程安全性演示")
    print("=" * 60)
    
    pool_instances = []
    app_instances = []
    
    def create_instances():
        """在线程中创建实例"""
        pool = DatabaseConnectionPool()
        app = ApplicationManager()
        pool_instances.append(pool)
        app_instances.append(app)
    
    # 创建多个线程同时创建实例
    threads = []
    for i in range(5):
        thread = threading.Thread(target=create_instances)
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 验证所有实例都是同一个对象
    print(f"创建了 {len(pool_instances)} 个连接池实例")
    print(f"创建了 {len(app_instances)} 个应用管理器实例")
    
    pool_all_same = all(instance is pool_instances[0] for instance in pool_instances)
    app_all_same = all(instance is app_instances[0] for instance in app_instances)
    
    print(f"所有连接池实例都是同一个对象: {pool_all_same}")
    print(f"所有应用管理器实例都是同一个对象: {app_all_same}")


def main():
    """主函数"""
    print("元类单例模式演示")
    
    demonstrate_database_pool()
    demonstrate_application_manager()
    demonstrate_thread_safety()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
