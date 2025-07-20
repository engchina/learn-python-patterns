"""
05_real_world_examples.py - 代理模式的实际应用示例

这个文件展示了代理模式在实际开发中的常见应用场景，
包括数据库连接代理、图片加载代理、日志记录代理等实际场景。
"""

import time
import threading
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from enum import Enum
import base64


# ==================== 示例1：数据库连接代理 ====================
class DatabaseConnection(ABC):
    """数据库连接抽象接口"""
    
    @abstractmethod
    def execute_query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询"""
        pass
    
    @abstractmethod
    def execute_update(self, sql: str, params: tuple = ()) -> int:
        """执行更新"""
        pass
    
    @abstractmethod
    def begin_transaction(self):
        """开始事务"""
        pass
    
    @abstractmethod
    def commit(self):
        """提交事务"""
        pass
    
    @abstractmethod
    def rollback(self):
        """回滚事务"""
        pass


class RealDatabaseConnection(DatabaseConnection):
    """真实数据库连接"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.is_connected = False
        self.transaction_active = False
        self.query_count = 0
        self._connect()
    
    def _connect(self):
        """建立数据库连接"""
        print(f"建立数据库连接: {self.connection_string}")
        time.sleep(0.5)  # 模拟连接时间
        self.is_connected = True
    
    def execute_query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询"""
        if not self.is_connected:
            raise Exception("数据库未连接")
        
        self.query_count += 1
        print(f"执行查询: {sql} 参数: {params}")
        time.sleep(0.1)  # 模拟查询时间
        
        # 模拟查询结果
        return [
            {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
            {"id": 2, "name": "李四", "email": "lisi@example.com"}
        ]
    
    def execute_update(self, sql: str, params: tuple = ()) -> int:
        """执行更新"""
        if not self.is_connected:
            raise Exception("数据库未连接")
        
        self.query_count += 1
        print(f"执行更新: {sql} 参数: {params}")
        time.sleep(0.1)  # 模拟更新时间
        return 1  # 模拟影响行数
    
    def begin_transaction(self):
        """开始事务"""
        print("开始事务")
        self.transaction_active = True
    
    def commit(self):
        """提交事务"""
        print("提交事务")
        self.transaction_active = False
    
    def rollback(self):
        """回滚事务"""
        print("回滚事务")
        self.transaction_active = False


class DatabaseConnectionProxy(DatabaseConnection):
    """数据库连接代理"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._real_connection: Optional[RealDatabaseConnection] = None
        self._lock = threading.Lock()
        self.access_count = 0
        self.last_access_time = None
        print(f"数据库连接代理已创建: {connection_string}")
    
    def execute_query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询 - 延迟连接"""
        with self._lock:
            self._ensure_connection()
            self._record_access()
            return self._real_connection.execute_query(sql, params)
    
    def execute_update(self, sql: str, params: tuple = ()) -> int:
        """执行更新 - 延迟连接"""
        with self._lock:
            self._ensure_connection()
            self._record_access()
            return self._real_connection.execute_update(sql, params)
    
    def begin_transaction(self):
        """开始事务"""
        with self._lock:
            self._ensure_connection()
            self._real_connection.begin_transaction()
    
    def commit(self):
        """提交事务"""
        if self._real_connection:
            self._real_connection.commit()
    
    def rollback(self):
        """回滚事务"""
        if self._real_connection:
            self._real_connection.rollback()
    
    def _ensure_connection(self):
        """确保连接存在（延迟连接）"""
        if self._real_connection is None:
            print("代理: 首次访问，创建真实数据库连接")
            self._real_connection = RealDatabaseConnection(self.connection_string)
    
    def _record_access(self):
        """记录访问"""
        self.access_count += 1
        self.last_access_time = datetime.now()
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "access_count": self.access_count,
            "last_access_time": self.last_access_time.isoformat() if self.last_access_time else None,
            "connection_created": self._real_connection is not None,
            "query_count": self._real_connection.query_count if self._real_connection else 0
        }


# ==================== 示例2：图片加载代理 ====================
class Image(ABC):
    """图片抽象接口"""
    
    @abstractmethod
    def display(self) -> str:
        """显示图片"""
        pass
    
    @abstractmethod
    def get_size(self) -> tuple:
        """获取图片尺寸"""
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """获取图片信息"""
        pass


class RealImage(Image):
    """真实图片"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.width = 0
        self.height = 0
        self.data = None
        self._load_from_disk()
    
    def _load_from_disk(self):
        """从磁盘加载图片"""
        print(f"从磁盘加载图片: {self.filename}")
        time.sleep(1.0)  # 模拟加载时间
        
        # 模拟图片数据
        self.width = 800
        self.height = 600
        self.data = f"图片数据_{self.filename}".encode()
        print(f"图片加载完成: {self.filename} ({self.width}x{self.height})")
    
    def display(self) -> str:
        """显示图片"""
        return f"显示图片: {self.filename} ({self.width}x{self.height})"
    
    def get_size(self) -> tuple:
        """获取图片尺寸"""
        return (self.width, self.height)
    
    def get_info(self) -> Dict[str, Any]:
        """获取图片信息"""
        return {
            "filename": self.filename,
            "width": self.width,
            "height": self.height,
            "size_bytes": len(self.data) if self.data else 0
        }


class ImageProxy(Image):
    """图片代理 - 延迟加载"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image: Optional[RealImage] = None
        self.access_count = 0
        print(f"图片代理已创建: {filename}")
    
    def display(self) -> str:
        """显示图片 - 延迟加载"""
        self._ensure_loaded()
        self.access_count += 1
        return self._real_image.display()
    
    def get_size(self) -> tuple:
        """获取图片尺寸 - 可能需要加载"""
        self._ensure_loaded()
        return self._real_image.get_size()
    
    def get_info(self) -> Dict[str, Any]:
        """获取图片信息"""
        if self._real_image is None:
            # 返回基本信息，不触发加载
            return {
                "filename": self.filename,
                "loaded": False,
                "access_count": self.access_count
            }
        else:
            info = self._real_image.get_info()
            info["loaded"] = True
            info["access_count"] = self.access_count
            return info
    
    def _ensure_loaded(self):
        """确保图片已加载"""
        if self._real_image is None:
            print(f"代理: 首次访问，加载图片 {self.filename}")
            self._real_image = RealImage(self.filename)


# ==================== 示例3：日志记录代理 ====================
class Logger(ABC):
    """日志记录器抽象接口"""
    
    @abstractmethod
    def log(self, level: str, message: str, **kwargs):
        """记录日志"""
        pass


class FileLogger(Logger):
    """文件日志记录器"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.log_count = 0
        print(f"文件日志记录器初始化: {filename}")
    
    def log(self, level: str, message: str, **kwargs):
        """记录日志到文件"""
        self.log_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        if kwargs:
            log_entry += f" | 额外信息: {kwargs}"
        
        print(f"写入日志文件 {self.filename}: {log_entry}")
        time.sleep(0.05)  # 模拟文件写入时间


class LoggingProxy(Logger):
    """日志记录代理 - 添加过滤和缓冲功能"""
    
    def __init__(self, logger: Logger, min_level: str = "INFO", buffer_size: int = 5):
        self.logger = logger
        self.min_level = min_level
        self.buffer_size = buffer_size
        self.buffer = []
        self.level_priority = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
        self.filtered_count = 0
        self.buffered_count = 0
        print(f"日志代理已创建: 最小级别={min_level}, 缓冲大小={buffer_size}")
    
    def log(self, level: str, message: str, **kwargs):
        """记录日志 - 带过滤和缓冲"""
        # 级别过滤
        if not self._should_log(level):
            self.filtered_count += 1
            print(f"日志代理: 过滤低级别日志 [{level}] {message}")
            return
        
        # 添加到缓冲区
        log_entry = {
            "level": level,
            "message": message,
            "timestamp": datetime.now(),
            "kwargs": kwargs
        }
        
        self.buffer.append(log_entry)
        self.buffered_count += 1
        print(f"日志代理: 添加到缓冲区 [{level}] {message} (缓冲区: {len(self.buffer)}/{self.buffer_size})")
        
        # 检查是否需要刷新缓冲区
        if len(self.buffer) >= self.buffer_size or level in ["ERROR", "CRITICAL"]:
            self._flush_buffer()
    
    def _should_log(self, level: str) -> bool:
        """检查是否应该记录日志"""
        return self.level_priority.get(level, 0) >= self.level_priority.get(self.min_level, 1)
    
    def _flush_buffer(self):
        """刷新缓冲区"""
        if not self.buffer:
            return
        
        print(f"日志代理: 刷新缓冲区 ({len(self.buffer)} 条日志)")
        
        for entry in self.buffer:
            self.logger.log(
                entry["level"],
                entry["message"],
                **entry["kwargs"]
            )
        
        self.buffer.clear()
    
    def force_flush(self):
        """强制刷新缓冲区"""
        print("日志代理: 强制刷新缓冲区")
        self._flush_buffer()
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "buffered_count": self.buffered_count,
            "filtered_count": self.filtered_count,
            "current_buffer_size": len(self.buffer),
            "max_buffer_size": self.buffer_size,
            "min_level": self.min_level
        }


# ==================== 使用示例 ====================
def demo_database_proxy():
    """数据库连接代理演示"""
    print("=" * 60)
    print("🗄️ 数据库连接代理演示")
    print("=" * 60)
    
    # 创建数据库连接代理
    db_proxy = DatabaseConnectionProxy("mysql://localhost:3306/testdb")
    
    print("\n📋 获取代理信息（不会创建真实连接）:")
    stats = db_proxy.get_statistics()
    print(f"统计信息: {stats}")
    
    print("\n🔍 第一次查询（会创建真实连接）:")
    users = db_proxy.execute_query("SELECT * FROM users WHERE age > ?", (18,))
    print(f"查询结果: {len(users)} 个用户")
    
    print("\n✏️ 执行更新操作:")
    affected_rows = db_proxy.execute_update("UPDATE users SET status = ? WHERE id = ?", ("active", 1))
    print(f"影响行数: {affected_rows}")
    
    print("\n🔄 事务操作:")
    db_proxy.begin_transaction()
    db_proxy.execute_update("INSERT INTO users (name, email) VALUES (?, ?)", ("新用户", "new@example.com"))
    db_proxy.commit()
    
    print("\n📊 最终统计:")
    final_stats = db_proxy.get_statistics()
    print(f"统计信息: {final_stats}")


def demo_image_proxy():
    """图片加载代理演示"""
    print("\n" + "=" * 60)
    print("🖼️ 图片加载代理演示")
    print("=" * 60)
    
    # 创建图片代理
    images = [
        ImageProxy("photo1.jpg"),
        ImageProxy("photo2.png"),
        ImageProxy("photo3.gif")
    ]
    
    print("\n📋 获取图片信息（不会加载图片）:")
    for i, image in enumerate(images):
        info = image.get_info()
        print(f"图片 {i+1}: {info}")
    
    print("\n🖼️ 显示第一张图片（会触发加载）:")
    result = images[0].display()
    print(f"显示结果: {result}")
    
    print("\n📏 获取第二张图片尺寸（会触发加载）:")
    size = images[1].get_size()
    print(f"图片尺寸: {size}")
    
    print("\n📋 再次获取图片信息:")
    for i, image in enumerate(images):
        info = image.get_info()
        print(f"图片 {i+1}: 已加载={info.get('loaded', False)}, 访问次数={info.get('access_count', 0)}")


def demo_logging_proxy():
    """日志记录代理演示"""
    print("\n" + "=" * 60)
    print("📝 日志记录代理演示")
    print("=" * 60)
    
    # 创建日志系统
    file_logger = FileLogger("application.log")
    log_proxy = LoggingProxy(file_logger, min_level="INFO", buffer_size=3)
    
    print("\n📝 记录各种级别的日志:")
    
    # 记录不同级别的日志
    log_entries = [
        ("DEBUG", "调试信息", {"user_id": 123}),
        ("INFO", "用户登录", {"user": "张三", "ip": "192.168.1.1"}),
        ("DEBUG", "详细调试信息", {}),
        ("WARNING", "警告信息", {"memory_usage": "85%"}),
        ("INFO", "数据保存成功", {"records": 100}),
        ("ERROR", "数据库连接失败", {"error_code": 1001}),
        ("INFO", "系统启动完成", {})
    ]
    
    for level, message, kwargs in log_entries:
        log_proxy.log(level, message, **kwargs)
        time.sleep(0.1)
    
    print("\n🔄 强制刷新缓冲区:")
    log_proxy.force_flush()
    
    print("\n📊 日志统计:")
    stats = log_proxy.get_statistics()
    print(f"统计信息: {stats}")


def demo_proxy_chain():
    """代理链演示"""
    print("\n" + "=" * 60)
    print("🔗 代理链演示 - 多层代理组合")
    print("=" * 60)
    
    # 创建代理链：日志代理 -> 数据库代理
    class LoggingDatabaseProxy(DatabaseConnection):
        """带日志的数据库代理"""
        
        def __init__(self, db_proxy: DatabaseConnectionProxy, logger: Logger):
            self.db_proxy = db_proxy
            self.logger = logger
        
        def execute_query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
            self.logger.log("INFO", f"执行查询: {sql}", params=params)
            try:
                result = self.db_proxy.execute_query(sql, params)
                self.logger.log("INFO", f"查询成功，返回 {len(result)} 行")
                return result
            except Exception as e:
                self.logger.log("ERROR", f"查询失败: {e}")
                raise
        
        def execute_update(self, sql: str, params: tuple = ()) -> int:
            self.logger.log("INFO", f"执行更新: {sql}", params=params)
            try:
                result = self.db_proxy.execute_update(sql, params)
                self.logger.log("INFO", f"更新成功，影响 {result} 行")
                return result
            except Exception as e:
                self.logger.log("ERROR", f"更新失败: {e}")
                raise
        
        def begin_transaction(self):
            self.logger.log("INFO", "开始事务")
            self.db_proxy.begin_transaction()
        
        def commit(self):
            self.logger.log("INFO", "提交事务")
            self.db_proxy.commit()
        
        def rollback(self):
            self.logger.log("WARNING", "回滚事务")
            self.db_proxy.rollback()
    
    # 创建代理链
    db_proxy = DatabaseConnectionProxy("postgresql://localhost:5432/app")
    file_logger = FileLogger("db_operations.log")
    log_proxy = LoggingProxy(file_logger, min_level="INFO", buffer_size=2)
    logging_db_proxy = LoggingDatabaseProxy(db_proxy, log_proxy)
    
    print("\n🔗 通过代理链执行数据库操作:")
    
    # 执行操作
    users = logging_db_proxy.execute_query("SELECT * FROM users")
    logging_db_proxy.execute_update("UPDATE users SET last_login = NOW()")
    
    # 强制刷新日志
    log_proxy.force_flush()


def main():
    """主演示函数"""
    demo_database_proxy()
    demo_image_proxy()
    demo_logging_proxy()
    demo_proxy_chain()
    
    print("\n" + "=" * 60)
    print("🎉 代理模式实际应用演示完成！")
    print("💡 关键要点:")
    print("   • 数据库代理：延迟连接，节省资源")
    print("   • 图片代理：延迟加载，提高性能")
    print("   • 日志代理：过滤缓冲，优化I/O")
    print("   • 代理链：多层代理，功能组合")
    print("   • 代理模式在实际项目中应用广泛")
    print("=" * 60)


if __name__ == "__main__":
    main()
