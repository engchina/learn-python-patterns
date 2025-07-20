"""
03_logging_chain.py - 日志处理链示例

这个示例展示了责任链模式在日志系统中的应用。
包括多级日志处理器、不同输出目标的日志链和日志级别的过滤机制。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, TextIO
from datetime import datetime
from enum import Enum
import sys
import json


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    
    def __str__(self):
        return self.name


class LogRecord:
    """日志记录对象"""
    
    def __init__(self, level: LogLevel, message: str, logger_name: str = "root",
                 extra: Dict[str, Any] = None):
        self.level = level
        self.message = message
        self.logger_name = logger_name
        self.timestamp = datetime.now()
        self.extra = extra or {}
        self.handler_chain = []  # 处理器链记录
    
    def add_handler_record(self, handler_name: str):
        """添加处理器记录"""
        self.handler_chain.append(handler_name)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.name,
            "logger": self.logger_name,
            "message": self.message,
            "extra": self.extra
        }


# ==================== 抽象日志处理器 ====================
class LogHandler(ABC):
    """抽象日志处理器"""
    
    def __init__(self, name: str, level: LogLevel = LogLevel.DEBUG):
        self.name = name
        self.level = level
        self._next_handler: Optional['LogHandler'] = None
        self.processed_count = 0
        self.filtered_count = 0
    
    def set_next(self, handler: 'LogHandler') -> 'LogHandler':
        """设置下一个处理器"""
        self._next_handler = handler
        return handler
    
    def handle(self, record: LogRecord):
        """处理日志记录"""
        record.add_handler_record(self.name)
        
        # 检查日志级别
        if record.level.value >= self.level.value:
            # 当前处理器处理日志
            self.processed_count += 1
            self._handle_record(record)
            print(f"{self.name}: 处理日志 [{record.level.name}] {record.message}")
        else:
            # 级别不够，过滤掉
            self.filtered_count += 1
            print(f"{self.name}: 过滤日志 [{record.level.name}] (级别不够)")
        
        # 传递给下一个处理器
        if self._next_handler:
            self._next_handler.handle(record)
    
    @abstractmethod
    def _handle_record(self, record: LogRecord):
        """具体的日志处理逻辑"""
        pass
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取处理统计"""
        return {
            "name": self.name,
            "level": self.level.name,
            "processed_count": self.processed_count,
            "filtered_count": self.filtered_count
        }


# ==================== 具体日志处理器 ====================
class ConsoleHandler(LogHandler):
    """控制台日志处理器"""
    
    def __init__(self, level: LogLevel = LogLevel.DEBUG, stream: TextIO = None):
        super().__init__("控制台处理器", level)
        self.stream = stream or sys.stdout
        self.color_map = {
            LogLevel.DEBUG: "\033[36m",    # 青色
            LogLevel.INFO: "\033[32m",     # 绿色
            LogLevel.WARNING: "\033[33m",  # 黄色
            LogLevel.ERROR: "\033[31m",    # 红色
            LogLevel.CRITICAL: "\033[35m"  # 紫色
        }
        self.reset_color = "\033[0m"
    
    def _handle_record(self, record: LogRecord):
        """输出到控制台"""
        # 格式化日志消息
        timestamp = record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        color = self.color_map.get(record.level, "")
        
        formatted_message = (f"{color}[{timestamp}] [{record.level.name:8}] "
                           f"{record.logger_name}: {record.message}{self.reset_color}")
        
        # 添加额外信息
        if record.extra:
            extra_str = " | ".join([f"{k}={v}" for k, v in record.extra.items()])
            formatted_message += f" | {extra_str}"
        
        # 输出到流
        self.stream.write(formatted_message + "\n")
        self.stream.flush()


class FileHandler(LogHandler):
    """文件日志处理器"""
    
    def __init__(self, filename: str, level: LogLevel = LogLevel.DEBUG, 
                 max_size: int = 1024*1024):  # 1MB
        super().__init__(f"文件处理器({filename})", level)
        self.filename = filename
        self.max_size = max_size
        self.current_size = 0
        self.file_handle = None
        self._open_file()
    
    def _open_file(self):
        """打开日志文件"""
        try:
            self.file_handle = open(self.filename, 'a', encoding='utf-8')
            print(f"{self.name}: 日志文件已打开")
        except Exception as e:
            print(f"{self.name}: 无法打开日志文件 - {e}")
    
    def _handle_record(self, record: LogRecord):
        """写入到文件"""
        if not self.file_handle:
            return
        
        # 格式化日志消息
        timestamp = record.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_message = (f"[{timestamp}] [{record.level.name:8}] "
                           f"{record.logger_name}: {record.message}")
        
        # 添加额外信息
        if record.extra:
            extra_str = " | ".join([f"{k}={v}" for k, v in record.extra.items()])
            formatted_message += f" | {extra_str}"
        
        formatted_message += "\n"
        
        # 写入文件
        try:
            self.file_handle.write(formatted_message)
            self.file_handle.flush()
            self.current_size += len(formatted_message.encode('utf-8'))
            
            # 检查文件大小
            if self.current_size > self.max_size:
                self._rotate_file()
                
        except Exception as e:
            print(f"{self.name}: 写入文件失败 - {e}")
    
    def _rotate_file(self):
        """轮转日志文件"""
        if self.file_handle:
            self.file_handle.close()
        
        # 重命名当前文件
        backup_filename = f"{self.filename}.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            import os
            os.rename(self.filename, backup_filename)
            print(f"{self.name}: 日志文件已轮转到 {backup_filename}")
        except Exception as e:
            print(f"{self.name}: 文件轮转失败 - {e}")
        
        # 重新打开文件
        self.current_size = 0
        self._open_file()
    
    def close(self):
        """关闭文件处理器"""
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
            print(f"{self.name}: 日志文件已关闭")


class JsonHandler(LogHandler):
    """JSON格式日志处理器"""
    
    def __init__(self, filename: str, level: LogLevel = LogLevel.DEBUG):
        super().__init__(f"JSON处理器({filename})", level)
        self.filename = filename
        self.file_handle = None
        self._open_file()
    
    def _open_file(self):
        """打开JSON日志文件"""
        try:
            self.file_handle = open(self.filename, 'a', encoding='utf-8')
            print(f"{self.name}: JSON日志文件已打开")
        except Exception as e:
            print(f"{self.name}: 无法打开JSON日志文件 - {e}")
    
    def _handle_record(self, record: LogRecord):
        """写入JSON格式日志"""
        if not self.file_handle:
            return
        
        try:
            json_record = record.to_dict()
            json_line = json.dumps(json_record, ensure_ascii=False) + "\n"
            self.file_handle.write(json_line)
            self.file_handle.flush()
        except Exception as e:
            print(f"{self.name}: 写入JSON失败 - {e}")
    
    def close(self):
        """关闭JSON处理器"""
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
            print(f"{self.name}: JSON日志文件已关闭")


class EmailHandler(LogHandler):
    """邮件日志处理器（模拟）"""
    
    def __init__(self, level: LogLevel = LogLevel.ERROR, recipients: List[str] = None):
        super().__init__("邮件处理器", level)
        self.recipients = recipients or ["admin@example.com"]
        self.sent_count = 0
    
    def _handle_record(self, record: LogRecord):
        """发送邮件通知（模拟）"""
        self.sent_count += 1
        
        # 模拟发送邮件
        subject = f"[{record.level.name}] 系统日志告警"
        body = f"""
时间: {record.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
级别: {record.level.name}
日志器: {record.logger_name}
消息: {record.message}

额外信息: {record.extra}
        """
        
        print(f"{self.name}: 发送邮件到 {self.recipients}")
        print(f"  主题: {subject}")
        print(f"  内容: {record.message}")
        print(f"  已发送邮件总数: {self.sent_count}")


class DatabaseHandler(LogHandler):
    """数据库日志处理器（模拟）"""
    
    def __init__(self, level: LogLevel = LogLevel.WARNING):
        super().__init__("数据库处理器", level)
        self.records = []  # 模拟数据库存储
    
    def _handle_record(self, record: LogRecord):
        """存储到数据库（模拟）"""
        # 模拟数据库插入
        db_record = {
            "id": len(self.records) + 1,
            "timestamp": record.timestamp,
            "level": record.level.name,
            "logger_name": record.logger_name,
            "message": record.message,
            "extra": json.dumps(record.extra),
            "created_at": datetime.now()
        }
        
        self.records.append(db_record)
        print(f"{self.name}: 日志已存储到数据库，记录ID: {db_record['id']}")
    
    def query_records(self, level: LogLevel = None, limit: int = 10) -> List[Dict]:
        """查询日志记录"""
        filtered_records = self.records
        
        if level:
            filtered_records = [r for r in self.records if r["level"] == level.name]
        
        return filtered_records[-limit:]


# ==================== 日志器 ====================
class Logger:
    """日志器"""
    
    def __init__(self, name: str = "root"):
        self.name = name
        self.handlers: List[LogHandler] = []
        self.level = LogLevel.DEBUG
        self.log_count = 0
    
    def add_handler(self, handler: LogHandler):
        """添加处理器"""
        self.handlers.append(handler)
        print(f"日志器 '{self.name}': 添加处理器 {handler.name}")
    
    def set_level(self, level: LogLevel):
        """设置日志级别"""
        self.level = level
        print(f"日志器 '{self.name}': 设置级别为 {level.name}")
    
    def _log(self, level: LogLevel, message: str, **kwargs):
        """记录日志"""
        if level.value < self.level.value:
            return  # 级别不够，不处理
        
        self.log_count += 1
        record = LogRecord(level, message, self.name, kwargs)
        
        # 发送到所有处理器
        for handler in self.handlers:
            handler.handle(record)
    
    def debug(self, message: str, **kwargs):
        """调试日志"""
        self._log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """信息日志"""
        self._log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """警告日志"""
        self._log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """错误日志"""
        self._log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """严重错误日志"""
        self._log(LogLevel.CRITICAL, message, **kwargs)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        handler_stats = [handler.get_statistics() for handler in self.handlers]
        
        return {
            "logger_name": self.name,
            "logger_level": self.level.name,
            "total_logs": self.log_count,
            "handlers": handler_stats
        }


# ==================== 日志管理器 ====================
class LogManager:
    """日志管理器"""
    
    def __init__(self):
        self.loggers: Dict[str, Logger] = {}
    
    def get_logger(self, name: str = "root") -> Logger:
        """获取日志器"""
        if name not in self.loggers:
            self.loggers[name] = Logger(name)
            print(f"日志管理器: 创建新日志器 '{name}'")
        
        return self.loggers[name]
    
    def setup_default_logging(self) -> Logger:
        """设置默认日志配置"""
        root_logger = self.get_logger("root")
        
        # 添加控制台处理器
        console_handler = ConsoleHandler(LogLevel.INFO)
        root_logger.add_handler(console_handler)
        
        # 添加文件处理器
        file_handler = FileHandler("application.log", LogLevel.DEBUG)
        root_logger.add_handler(file_handler)
        
        # 添加错误邮件处理器
        email_handler = EmailHandler(LogLevel.ERROR)
        root_logger.add_handler(email_handler)
        
        print("默认日志配置已设置")
        return root_logger
    
    def setup_chain_logging(self) -> Logger:
        """设置链式日志配置"""
        logger = self.get_logger("chain_demo")
        
        # 创建处理器链
        console = ConsoleHandler(LogLevel.DEBUG)
        file_handler = FileHandler("chain_demo.log", LogLevel.INFO)
        json_handler = JsonHandler("chain_demo.json", LogLevel.WARNING)
        db_handler = DatabaseHandler(LogLevel.ERROR)
        email_handler = EmailHandler(LogLevel.CRITICAL)
        
        # 构建处理器链
        console.set_next(file_handler).set_next(json_handler).set_next(db_handler).set_next(email_handler)
        
        # 添加链的第一个处理器
        logger.add_handler(console)
        
        print("链式日志配置已设置")
        return logger


# ==================== 使用示例 ====================
def demo_logging_chain():
    """日志处理链演示"""
    print("=" * 60)
    print("📝 日志处理链演示")
    print("=" * 60)
    
    # 创建日志管理器
    log_manager = LogManager()
    
    # 设置链式日志配置
    logger = log_manager.setup_chain_logging()
    
    # 记录不同级别的日志
    log_messages = [
        (LogLevel.DEBUG, "调试信息：用户点击了按钮", {"user_id": "123", "button": "submit"}),
        (LogLevel.INFO, "用户登录成功", {"user": "张三", "ip": "192.168.1.1"}),
        (LogLevel.WARNING, "内存使用率较高", {"memory_usage": "85%", "threshold": "80%"}),
        (LogLevel.ERROR, "数据库连接失败", {"error_code": "DB001", "retry_count": 3}),
        (LogLevel.CRITICAL, "系统即将崩溃", {"cpu_usage": "99%", "memory_usage": "95%"})
    ]
    
    print(f"\n📝 记录 {len(log_messages)} 条不同级别的日志:")
    for level, message, extra in log_messages:
        print(f"\n--- 记录 {level.name} 级别日志 ---")
        logger._log(level, message, **extra)
    
    # 显示统计信息
    print(f"\n📊 日志统计:")
    stats = logger.get_statistics()
    print(f"日志器: {stats['logger_name']}, 级别: {stats['logger_level']}, 总日志数: {stats['total_logs']}")
    
    for handler_stat in stats['handlers']:
        print(f"  处理器: {handler_stat['name']}")
        print(f"    级别: {handler_stat['level']}")
        print(f"    处理数: {handler_stat['processed_count']}")
        print(f"    过滤数: {handler_stat['filtered_count']}")


def demo_multiple_loggers():
    """多日志器演示"""
    print("\n" + "=" * 60)
    print("🔄 多日志器演示")
    print("=" * 60)
    
    log_manager = LogManager()
    
    # 创建不同的日志器
    app_logger = log_manager.get_logger("app")
    db_logger = log_manager.get_logger("database")
    api_logger = log_manager.get_logger("api")
    
    # 为每个日志器配置不同的处理器
    # 应用日志器 - 只输出到控制台和文件
    app_logger.add_handler(ConsoleHandler(LogLevel.INFO))
    app_logger.add_handler(FileHandler("app.log", LogLevel.DEBUG))
    
    # 数据库日志器 - 输出到文件和数据库
    db_logger.add_handler(FileHandler("database.log", LogLevel.DEBUG))
    db_logger.add_handler(DatabaseHandler(LogLevel.WARNING))
    
    # API日志器 - 输出到JSON和邮件
    api_logger.add_handler(JsonHandler("api.json", LogLevel.INFO))
    api_logger.add_handler(EmailHandler(LogLevel.ERROR))
    
    # 记录不同类型的日志
    print(f"\n📝 使用不同的日志器记录日志:")
    
    print(f"\n--- 应用日志 ---")
    app_logger.info("应用启动成功", version="1.0.0", port=8080)
    app_logger.warning("配置文件缺少某些选项", missing_keys=["debug", "timeout"])
    
    print(f"\n--- 数据库日志 ---")
    db_logger.info("数据库连接已建立", host="localhost", database="myapp")
    db_logger.error("查询执行失败", sql="SELECT * FROM users", error="Table not found")
    
    print(f"\n--- API日志 ---")
    api_logger.info("API请求处理", method="GET", path="/users", status=200)
    api_logger.error("API认证失败", token="invalid_token", ip="192.168.1.100")
    
    # 显示所有日志器的统计
    print(f"\n📊 所有日志器统计:")
    for name, logger in log_manager.loggers.items():
        stats = logger.get_statistics()
        print(f"\n日志器 '{name}': {stats['total_logs']} 条日志")


def main():
    """主演示函数"""
    demo_logging_chain()
    demo_multiple_loggers()
    
    print("\n" + "=" * 60)
    print("🎉 日志处理链演示完成！")
    print("💡 关键要点:")
    print("   • 日志处理器链实现了多目标输出")
    print("   • 每个处理器可以有不同的级别过滤")
    print("   • 支持多种输出格式和目标")
    print("   • 可以灵活组合不同的处理器")
    print("   • 广泛应用于日志系统和监控系统")
    print("=" * 60)


if __name__ == "__main__":
    main()
