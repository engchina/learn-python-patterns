"""
05_real_world_examples.py - 享元模式的实际应用示例

这个文件展示了享元模式在实际开发中的常见应用场景，
包括图标缓存系统、数据库连接池、线程池管理等实际场景。
"""

import time
import threading
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum
import uuid


# ==================== 示例1：图标缓存系统 ====================
class IconType(Enum):
    """图标类型枚举"""
    FILE = "file"
    FOLDER = "folder"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


class Icon:
    """图标享元"""
    
    def __init__(self, icon_type: IconType, size: str, theme: str):
        """
        初始化图标享元
        
        Args:
            icon_type: 图标类型（内在状态）
            size: 图标大小（内在状态）
            theme: 图标主题（内在状态）
        """
        self.icon_type = icon_type
        self.size = size
        self.theme = theme
        self.image_data = self._load_icon_data()  # 模拟加载图标数据
        print(f"加载图标: {icon_type.value}-{size}-{theme}")
    
    def _load_icon_data(self) -> bytes:
        """模拟加载图标数据"""
        # 模拟从文件系统或网络加载图标数据
        time.sleep(0.01)  # 模拟加载时间
        return f"icon_data_{self.icon_type.value}_{self.size}_{self.theme}".encode()
    
    def render(self, position: tuple, label: str = "") -> str:
        """
        渲染图标
        
        Args:
            position: 图标位置（外在状态）
            label: 图标标签（外在状态）
            
        Returns:
            渲染结果描述
        """
        return (f"渲染{self.theme}主题{self.size}大小的{self.icon_type.value}图标 "
                f"位置:{position} 标签:'{label}' 数据大小:{len(self.image_data)}字节")


class IconFactory:
    """图标工厂"""
    
    def __init__(self):
        self._icons: Dict[str, Icon] = {}
        self._load_count = 0
        self._access_count = 0
    
    def get_icon(self, icon_type: IconType, size: str = "medium", 
                 theme: str = "default") -> Icon:
        """获取图标享元"""
        key = f"{icon_type.value}-{size}-{theme}"
        self._access_count += 1
        
        if key not in self._icons:
            self._icons[key] = Icon(icon_type, size, theme)
            self._load_count += 1
            print(f"✓ 创建新图标: {key}")
        else:
            print(f"♻️ 复用缓存图标: {key}")
        
        return self._icons[key]
    
    def get_cache_info(self) -> Dict[str, int]:
        """获取缓存信息"""
        return {
            "cached_icons": len(self._icons),
            "load_count": self._load_count,
            "access_count": self._access_count,
            "cache_hit_rate": round((self._access_count - self._load_count) / self._access_count * 100, 1) if self._access_count > 0 else 0
        }


class FileSystemItem:
    """文件系统项目"""
    
    def __init__(self, name: str, icon: Icon, position: tuple):
        self.name = name
        self.icon = icon
        self.position = position
    
    def render(self) -> str:
        """渲染文件系统项目"""
        return self.icon.render(self.position, self.name)


class FileExplorer:
    """文件浏览器"""
    
    def __init__(self):
        self.icon_factory = IconFactory()
        self.items: List[FileSystemItem] = []
    
    def add_file(self, name: str, file_type: str, position: tuple):
        """添加文件"""
        # 根据文件类型选择图标
        icon_type_map = {
            "txt": IconType.DOCUMENT,
            "doc": IconType.DOCUMENT,
            "jpg": IconType.IMAGE,
            "png": IconType.IMAGE,
            "mp4": IconType.VIDEO,
            "mp3": IconType.AUDIO,
            "folder": IconType.FOLDER
        }
        
        icon_type = icon_type_map.get(file_type, IconType.FILE)
        icon = self.icon_factory.get_icon(icon_type)
        
        item = FileSystemItem(name, icon, position)
        self.items.append(item)
    
    def render_view(self, max_items: int = 10):
        """渲染文件浏览器视图"""
        print(f"\n📁 文件浏览器视图")
        print("=" * 60)
        
        items_to_show = min(max_items, len(self.items))
        for i in range(items_to_show):
            render_result = self.items[i].render()
            print(f"  {i+1:2d}. {render_result}")
        
        if len(self.items) > max_items:
            print(f"  ... 还有 {len(self.items) - max_items} 个项目")
    
    def get_statistics(self):
        """获取统计信息"""
        cache_info = self.icon_factory.get_cache_info()
        
        print(f"\n📊 文件浏览器统计:")
        print(f"  • 文件项目数: {len(self.items)}")
        print(f"  • 缓存图标数: {cache_info['cached_icons']}")
        print(f"  • 图标加载次数: {cache_info['load_count']}")
        print(f"  • 图标访问次数: {cache_info['access_count']}")
        print(f"  • 缓存命中率: {cache_info['cache_hit_rate']}%")


# ==================== 示例2：数据库连接池 ====================
class DatabaseConnection:
    """数据库连接享元"""
    
    def __init__(self, host: str, port: int, database: str):
        """
        初始化数据库连接
        
        Args:
            host: 数据库主机（内在状态）
            port: 数据库端口（内在状态）
            database: 数据库名称（内在状态）
        """
        self.host = host
        self.port = port
        self.database = database
        self.connection_id = str(uuid.uuid4())[:8]
        self.is_busy = False
        self._establish_connection()
    
    def _establish_connection(self):
        """建立数据库连接"""
        print(f"建立数据库连接: {self.host}:{self.port}/{self.database} [{self.connection_id}]")
        time.sleep(0.1)  # 模拟连接建立时间
    
    def execute_query(self, sql: str, params: tuple = ()) -> str:
        """
        执行查询
        
        Args:
            sql: SQL语句（外在状态）
            params: 查询参数（外在状态）
            
        Returns:
            查询结果描述
        """
        if self.is_busy:
            return "连接忙碌中"
        
        self.is_busy = True
        try:
            # 模拟查询执行
            time.sleep(0.05)
            result = f"连接[{self.connection_id}]执行: {sql} 参数:{params}"
            return result
        finally:
            self.is_busy = False
    
    def get_connection_info(self) -> str:
        """获取连接信息"""
        return f"{self.host}:{self.port}/{self.database}"


class ConnectionPool:
    """数据库连接池"""
    
    def __init__(self, max_connections: int = 5):
        self.max_connections = max_connections
        self._connections: Dict[str, List[DatabaseConnection]] = {}
        self._creation_count = 0
        self._borrow_count = 0
    
    def get_connection(self, host: str, port: int, database: str) -> Optional[DatabaseConnection]:
        """获取数据库连接"""
        key = f"{host}:{port}/{database}"
        self._borrow_count += 1
        
        # 检查是否有可用连接
        if key in self._connections:
            for conn in self._connections[key]:
                if not conn.is_busy:
                    print(f"♻️ 复用数据库连接: {key} [{conn.connection_id}]")
                    return conn
        
        # 创建新连接
        if key not in self._connections:
            self._connections[key] = []
        
        if len(self._connections[key]) < self.max_connections:
            new_conn = DatabaseConnection(host, port, database)
            self._connections[key].append(new_conn)
            self._creation_count += 1
            print(f"✓ 创建新数据库连接: {key} [{new_conn.connection_id}]")
            return new_conn
        
        print(f"❌ 连接池已满: {key}")
        return None
    
    def get_pool_statistics(self) -> Dict[str, Any]:
        """获取连接池统计信息"""
        total_connections = sum(len(conns) for conns in self._connections.values())
        busy_connections = sum(1 for conns in self._connections.values() 
                             for conn in conns if conn.is_busy)
        
        return {
            "total_connections": total_connections,
            "busy_connections": busy_connections,
            "available_connections": total_connections - busy_connections,
            "creation_count": self._creation_count,
            "borrow_count": self._borrow_count,
            "reuse_rate": round((self._borrow_count - self._creation_count) / self._borrow_count * 100, 1) if self._borrow_count > 0 else 0
        }


# ==================== 示例3：线程池管理 ====================
class WorkerThread:
    """工作线程享元"""
    
    def __init__(self, thread_type: str, priority: int):
        """
        初始化工作线程
        
        Args:
            thread_type: 线程类型（内在状态）
            priority: 线程优先级（内在状态）
        """
        self.thread_type = thread_type
        self.priority = priority
        self.thread_id = str(uuid.uuid4())[:8]
        self.is_busy = False
        print(f"创建工作线程: {thread_type} 优先级:{priority} [{self.thread_id}]")
    
    def execute_task(self, task_name: str, task_data: Any) -> str:
        """
        执行任务
        
        Args:
            task_name: 任务名称（外在状态）
            task_data: 任务数据（外在状态）
            
        Returns:
            执行结果描述
        """
        if self.is_busy:
            return "线程忙碌中"
        
        self.is_busy = True
        try:
            # 模拟任务执行
            execution_time = 0.1 / self.priority  # 高优先级执行更快
            time.sleep(execution_time)
            result = f"线程[{self.thread_id}]({self.thread_type})执行任务: {task_name}"
            return result
        finally:
            self.is_busy = False


class ThreadPool:
    """线程池"""
    
    def __init__(self):
        self._threads: Dict[str, List[WorkerThread]] = {}
        self._creation_count = 0
        self._task_count = 0
    
    def get_thread(self, thread_type: str, priority: int = 1) -> Optional[WorkerThread]:
        """获取工作线程"""
        key = f"{thread_type}-{priority}"
        self._task_count += 1
        
        # 查找可用线程
        if key in self._threads:
            for thread in self._threads[key]:
                if not thread.is_busy:
                    print(f"♻️ 复用工作线程: {key} [{thread.thread_id}]")
                    return thread
        
        # 创建新线程
        if key not in self._threads:
            self._threads[key] = []
        
        new_thread = WorkerThread(thread_type, priority)
        self._threads[key].append(new_thread)
        self._creation_count += 1
        print(f"✓ 创建新工作线程: {key} [{new_thread.thread_id}]")
        return new_thread
    
    def get_thread_statistics(self) -> Dict[str, Any]:
        """获取线程池统计信息"""
        total_threads = sum(len(threads) for threads in self._threads.values())
        busy_threads = sum(1 for threads in self._threads.values() 
                          for thread in threads if thread.is_busy)
        
        return {
            "total_threads": total_threads,
            "busy_threads": busy_threads,
            "available_threads": total_threads - busy_threads,
            "creation_count": self._creation_count,
            "task_count": self._task_count,
            "reuse_rate": round((self._task_count - self._creation_count) / self._task_count * 100, 1) if self._task_count > 0 else 0
        }


# ==================== 使用示例 ====================
def demo_icon_cache_system():
    """图标缓存系统演示"""
    print("=" * 60)
    print("🎨 图标缓存系统享元模式演示")
    print("=" * 60)
    
    # 创建文件浏览器
    explorer = FileExplorer()
    
    # 添加各种文件
    files = [
        ("document.txt", "txt", (10, 20)),
        ("image1.jpg", "jpg", (50, 20)),
        ("image2.png", "png", (90, 20)),
        ("video.mp4", "mp4", (130, 20)),
        ("music.mp3", "mp3", (170, 20)),
        ("report.doc", "doc", (10, 60)),
        ("photo.jpg", "jpg", (50, 60)),  # 复用jpg图标
        ("folder1", "folder", (90, 60)),
        ("folder2", "folder", (130, 60)),  # 复用folder图标
        ("data.txt", "txt", (170, 60)),  # 复用txt图标
    ]
    
    print("\n📁 添加文件到浏览器...")
    for name, file_type, position in files:
        explorer.add_file(name, file_type, position)
    
    # 渲染文件浏览器
    explorer.render_view()
    
    # 显示统计信息
    explorer.get_statistics()


def demo_database_connection_pool():
    """数据库连接池演示"""
    print("\n" + "=" * 60)
    print("🗄️ 数据库连接池享元模式演示")
    print("=" * 60)
    
    # 创建连接池
    pool = ConnectionPool(max_connections=3)
    
    print("\n💾 执行数据库操作...")
    
    # 模拟多个数据库操作
    operations = [
        ("localhost", 5432, "app_db", "SELECT * FROM users", ()),
        ("localhost", 5432, "app_db", "SELECT * FROM orders", ()),
        ("localhost", 3306, "log_db", "INSERT INTO logs VALUES (?)", ("info",)),
        ("localhost", 5432, "app_db", "UPDATE users SET status = ?", ("active",)),
        ("localhost", 3306, "log_db", "SELECT * FROM errors", ()),
        ("localhost", 5432, "app_db", "DELETE FROM temp_data", ()),
    ]
    
    for host, port, database, sql, params in operations:
        conn = pool.get_connection(host, port, database)
        if conn:
            result = conn.execute_query(sql, params)
            print(f"  ✓ {result}")
        else:
            print(f"  ❌ 无法获取连接: {host}:{port}/{database}")
    
    # 显示连接池统计
    stats = pool.get_pool_statistics()
    print(f"\n📊 连接池统计:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")


def demo_thread_pool():
    """线程池演示"""
    print("\n" + "=" * 60)
    print("🧵 线程池享元模式演示")
    print("=" * 60)
    
    # 创建线程池
    thread_pool = ThreadPool()
    
    print("\n⚡ 执行并发任务...")
    
    # 模拟多个任务
    tasks = [
        ("计算任务", "compute", 3, {"data": "math_calculation"}),
        ("IO任务", "io", 1, {"file": "data.txt"}),
        ("网络任务", "network", 2, {"url": "api.example.com"}),
        ("计算任务", "compute", 3, {"data": "image_processing"}),
        ("IO任务", "io", 1, {"file": "log.txt"}),
        ("计算任务", "compute", 3, {"data": "data_analysis"}),
    ]
    
    for task_name, thread_type, priority, task_data in tasks:
        thread = thread_pool.get_thread(thread_type, priority)
        if thread:
            result = thread.execute_task(task_name, task_data)
            print(f"  ✓ {result}")
        else:
            print(f"  ❌ 无法获取线程: {thread_type}")
    
    # 显示线程池统计
    stats = thread_pool.get_thread_statistics()
    print(f"\n📊 线程池统计:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")


def main():
    """主演示函数"""
    demo_icon_cache_system()
    demo_database_connection_pool()
    demo_thread_pool()
    
    print("\n" + "=" * 60)
    print("🎉 享元模式实际应用演示完成！")
    print("💡 关键要点:")
    print("   • 图标缓存：相同类型的图标共享同一个对象")
    print("   • 连接池：相同配置的数据库连接可以复用")
    print("   • 线程池：相同类型的工作线程可以复用")
    print("   • 享元模式在资源管理中非常有用")
    print("=" * 60)


if __name__ == "__main__":
    main()
