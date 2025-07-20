"""
适配器模式实际应用案例集合

这个文件包含了多个实际项目中适配器模式的应用案例，展示了
不同场景下适配器模式的变体和最佳实践。

作者: Adapter Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
import time
import json
from datetime import datetime
from enum import Enum


# ==================== 案例1: 日志系统适配器 ====================

class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger(ABC):
    """统一日志接口"""

    @abstractmethod
    def log(self, level: LogLevel, message: str, **kwargs) -> None:
        """记录日志"""
        pass

    @abstractmethod
    def get_logger_info(self) -> str:
        """获取日志器信息"""
        pass


class PythonLoggingModule:
    """Python标准日志模块 - 被适配者"""

    def __init__(self, name: str):
        self.name = name
        self.log_count = 0
        self.level_mapping = {
            "DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50
        }

    def debug(self, msg: str) -> None:
        """调试日志"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] DEBUG:{self.name}: {msg}")
        self.log_count += 1

    def info(self, msg: str) -> None:
        """信息日志"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] INFO:{self.name}: {msg}")
        self.log_count += 1

    def warning(self, msg: str) -> None:
        """警告日志"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] WARNING:{self.name}: {msg}")
        self.log_count += 1

    def error(self, msg: str) -> None:
        """错误日志"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR:{self.name}: {msg}")
        self.log_count += 1

    def critical(self, msg: str) -> None:
        """严重错误日志"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] CRITICAL:{self.name}: {msg}")
        self.log_count += 1


class StructuredLogger:
    """结构化日志器 - 被适配者"""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.log_count = 0

    def write_log(self, severity: str, event: str, context: Dict[str, Any] = None) -> None:
        """写入结构化日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "service": self.service_name,
            "severity": severity,
            "event": event,
            "context": context or {}
        }
        print(f"📋 结构化日志: {json.dumps(log_entry, ensure_ascii=False)}")
        self.log_count += 1


class PythonLoggingAdapter(Logger):
    """Python日志模块适配器"""

    def __init__(self, python_logger: PythonLoggingModule):
        self.python_logger = python_logger

    def log(self, level: LogLevel, message: str, **kwargs) -> None:
        """记录日志"""
        # 将统一接口转换为Python日志接口
        if level == LogLevel.DEBUG:
            self.python_logger.debug(message)
        elif level == LogLevel.INFO:
            self.python_logger.info(message)
        elif level == LogLevel.WARNING:
            self.python_logger.warning(message)
        elif level == LogLevel.ERROR:
            self.python_logger.error(message)
        elif level == LogLevel.CRITICAL:
            self.python_logger.critical(message)

    def get_logger_info(self) -> str:
        return f"Python日志适配器 -> {self.python_logger.name} (记录数: {self.python_logger.log_count})"


class StructuredLoggerAdapter(Logger):
    """结构化日志器适配器"""

    def __init__(self, structured_logger: StructuredLogger):
        self.structured_logger = structured_logger

    def log(self, level: LogLevel, message: str, **kwargs) -> None:
        """记录日志"""
        # 将统一接口转换为结构化日志接口
        context = kwargs.copy()
        context["original_level"] = level.value

        self.structured_logger.write_log(
            severity=level.value,
            event=message,
            context=context
        )

    def get_logger_info(self) -> str:
        return f"结构化日志适配器 -> {self.structured_logger.service_name} (记录数: {self.structured_logger.log_count})"


# ==================== 案例2: 缓存系统适配器 ====================

class CacheInterface(ABC):
    """统一缓存接口"""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """设置缓存值"""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """删除缓存"""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        pass

    @abstractmethod
    def get_cache_info(self) -> str:
        """获取缓存信息"""
        pass


class MemoryCache:
    """内存缓存 - 被适配者"""

    def __init__(self):
        self.data = {}
        self.expiry = {}
        self.hit_count = 0
        self.miss_count = 0

    def store(self, key: str, value: Any, expire_seconds: int = 3600) -> None:
        """存储数据"""
        self.data[key] = value
        self.expiry[key] = time.time() + expire_seconds
        print(f"💾 内存缓存存储: {key}")

    def retrieve(self, key: str) -> Optional[Any]:
        """检索数据"""
        if key in self.data:
            if time.time() < self.expiry[key]:
                self.hit_count += 1
                print(f"💾 内存缓存命中: {key}")
                return self.data[key]
            else:
                # 过期删除
                del self.data[key]
                del self.expiry[key]

        self.miss_count += 1
        print(f"💾 内存缓存未命中: {key}")
        return None

    def remove(self, key: str) -> bool:
        """移除数据"""
        if key in self.data:
            del self.data[key]
            del self.expiry[key]
            print(f"💾 内存缓存删除: {key}")
            return True
        return False

    def has_key(self, key: str) -> bool:
        """检查键是否存在"""
        return key in self.data and time.time() < self.expiry[key]


class RedisLikeCache:
    """类Redis缓存 - 被适配者"""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.storage = {}
        self.ttl_data = {}
        self.operation_count = 0

    def redis_get(self, key: str) -> Optional[str]:
        """Redis GET命令"""
        self.operation_count += 1
        if key in self.storage:
            if key not in self.ttl_data or time.time() < self.ttl_data[key]:
                print(f"🔴 Redis GET: {key}")
                return self.storage[key]
            else:
                # TTL过期
                del self.storage[key]
                if key in self.ttl_data:
                    del self.ttl_data[key]

        print(f"🔴 Redis GET: {key} (NULL)")
        return None

    def redis_set(self, key: str, value: str) -> bool:
        """Redis SET命令"""
        self.operation_count += 1
        self.storage[key] = value
        print(f"🔴 Redis SET: {key} = {value}")
        return True

    def redis_setex(self, key: str, seconds: int, value: str) -> bool:
        """Redis SETEX命令"""
        self.operation_count += 1
        self.storage[key] = value
        self.ttl_data[key] = time.time() + seconds
        print(f"🔴 Redis SETEX: {key} = {value} (TTL: {seconds}s)")
        return True

    def redis_del(self, key: str) -> int:
        """Redis DEL命令"""
        self.operation_count += 1
        if key in self.storage:
            del self.storage[key]
            if key in self.ttl_data:
                del self.ttl_data[key]
            print(f"🔴 Redis DEL: {key}")
            return 1
        return 0

    def redis_exists(self, key: str) -> int:
        """Redis EXISTS命令"""
        self.operation_count += 1
        exists = key in self.storage and (key not in self.ttl_data or time.time() < self.ttl_data[key])
        print(f"🔴 Redis EXISTS: {key} = {1 if exists else 0}")
        return 1 if exists else 0


class MemoryCacheAdapter(CacheInterface):
    """内存缓存适配器"""

    def __init__(self, memory_cache: MemoryCache):
        self.memory_cache = memory_cache

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        return self.memory_cache.retrieve(key)

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """设置缓存值"""
        self.memory_cache.store(key, value, ttl)
        return True

    def delete(self, key: str) -> bool:
        """删除缓存"""
        return self.memory_cache.remove(key)

    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return self.memory_cache.has_key(key)

    def get_cache_info(self) -> str:
        total = self.memory_cache.hit_count + self.memory_cache.miss_count
        hit_rate = (self.memory_cache.hit_count / total * 100) if total > 0 else 0
        return f"内存缓存适配器 (命中率: {hit_rate:.1f}%, 总操作: {total})"


class RedisCacheAdapter(CacheInterface):
    """Redis缓存适配器"""

    def __init__(self, redis_cache: RedisLikeCache):
        self.redis_cache = redis_cache

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        result = self.redis_cache.redis_get(key)
        if result is not None:
            try:
                # 尝试反序列化JSON
                return json.loads(result)
            except json.JSONDecodeError:
                return result
        return None

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """设置缓存值"""
        # 序列化为JSON字符串
        serialized_value = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value

        if ttl > 0:
            return self.redis_cache.redis_setex(key, ttl, serialized_value)
        else:
            return self.redis_cache.redis_set(key, serialized_value)

    def delete(self, key: str) -> bool:
        """删除缓存"""
        return self.redis_cache.redis_del(key) > 0

    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return self.redis_cache.redis_exists(key) > 0

    def get_cache_info(self) -> str:
        return f"Redis缓存适配器 -> {self.redis_cache.host}:{self.redis_cache.port} (操作数: {self.redis_cache.operation_count})"


# ==================== 案例3: 消息队列适配器 ====================

class MessageQueue(ABC):
    """统一消息队列接口"""

    @abstractmethod
    def send_message(self, queue_name: str, message: Dict[str, Any]) -> bool:
        """发送消息"""
        pass

    @abstractmethod
    def receive_message(self, queue_name: str) -> Optional[Dict[str, Any]]:
        """接收消息"""
        pass

    @abstractmethod
    def get_queue_size(self, queue_name: str) -> int:
        """获取队列大小"""
        pass

    @abstractmethod
    def get_queue_info(self) -> str:
        """获取队列信息"""
        pass


class SimpleQueue:
    """简单队列实现 - 被适配者"""

    def __init__(self):
        self.queues: Dict[str, List[Any]] = {}
        self.message_count = 0

    def enqueue(self, queue_name: str, item: Any) -> None:
        """入队"""
        if queue_name not in self.queues:
            self.queues[queue_name] = []

        self.queues[queue_name].append(item)
        self.message_count += 1
        print(f"📤 简单队列入队: {queue_name} (大小: {len(self.queues[queue_name])})")

    def dequeue(self, queue_name: str) -> Optional[Any]:
        """出队"""
        if queue_name in self.queues and self.queues[queue_name]:
            item = self.queues[queue_name].pop(0)
            print(f"📥 简单队列出队: {queue_name} (剩余: {len(self.queues[queue_name])})")
            return item

        print(f"📥 简单队列出队: {queue_name} (空队列)")
        return None

    def size(self, queue_name: str) -> int:
        """获取队列大小"""
        return len(self.queues.get(queue_name, []))


class RabbitMQLike:
    """类RabbitMQ消息队列 - 被适配者"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.exchanges = {}
        self.queues = {}
        self.published_count = 0
        self.consumed_count = 0

    def publish(self, exchange: str, routing_key: str, body: str,
               properties: Dict[str, Any] = None) -> None:
        """发布消息"""
        if exchange not in self.exchanges:
            self.exchanges[exchange] = {}

        if routing_key not in self.queues:
            self.queues[routing_key] = []

        message = {
            "body": body,
            "properties": properties or {},
            "timestamp": datetime.now().isoformat(),
            "exchange": exchange,
            "routing_key": routing_key
        }

        self.queues[routing_key].append(message)
        self.published_count += 1
        print(f"🐰 RabbitMQ发布: {exchange}/{routing_key} (队列大小: {len(self.queues[routing_key])})")

    def consume(self, queue: str) -> Optional[Dict[str, Any]]:
        """消费消息"""
        if queue in self.queues and self.queues[queue]:
            message = self.queues[queue].pop(0)
            self.consumed_count += 1
            print(f"🐰 RabbitMQ消费: {queue} (剩余: {len(self.queues[queue])})")
            return message

        print(f"🐰 RabbitMQ消费: {queue} (无消息)")
        return None

    def queue_declare(self, queue: str, durable: bool = True) -> None:
        """声明队列"""
        if queue not in self.queues:
            self.queues[queue] = []
        print(f"🐰 RabbitMQ声明队列: {queue}")

    def get_queue_length(self, queue: str) -> int:
        """获取队列长度"""
        return len(self.queues.get(queue, []))


class SimpleQueueAdapter(MessageQueue):
    """简单队列适配器"""

    def __init__(self, simple_queue: SimpleQueue):
        self.simple_queue = simple_queue

    def send_message(self, queue_name: str, message: Dict[str, Any]) -> bool:
        """发送消息"""
        # 添加元数据
        wrapped_message = {
            "id": f"msg_{int(time.time() * 1000)}",
            "timestamp": datetime.now().isoformat(),
            "payload": message
        }

        self.simple_queue.enqueue(queue_name, wrapped_message)
        return True

    def receive_message(self, queue_name: str) -> Optional[Dict[str, Any]]:
        """接收消息"""
        message = self.simple_queue.dequeue(queue_name)
        if message:
            return message.get("payload", message)
        return None

    def get_queue_size(self, queue_name: str) -> int:
        """获取队列大小"""
        return self.simple_queue.size(queue_name)

    def get_queue_info(self) -> str:
        return f"简单队列适配器 (总消息数: {self.simple_queue.message_count})"


class RabbitMQAdapter(MessageQueue):
    """RabbitMQ适配器"""

    def __init__(self, rabbitmq: RabbitMQLike):
        self.rabbitmq = rabbitmq
        self.default_exchange = "amq.direct"

    def send_message(self, queue_name: str, message: Dict[str, Any]) -> bool:
        """发送消息"""
        # 确保队列存在
        self.rabbitmq.queue_declare(queue_name)

        # 序列化消息
        body = json.dumps(message, ensure_ascii=False)
        properties = {
            "content_type": "application/json",
            "delivery_mode": 2  # 持久化
        }

        self.rabbitmq.publish(self.default_exchange, queue_name, body, properties)
        return True

    def receive_message(self, queue_name: str) -> Optional[Dict[str, Any]]:
        """接收消息"""
        message = self.rabbitmq.consume(queue_name)
        if message:
            try:
                return json.loads(message["body"])
            except json.JSONDecodeError:
                return {"raw_body": message["body"]}
        return None

    def get_queue_size(self, queue_name: str) -> int:
        """获取队列大小"""
        return self.rabbitmq.get_queue_length(queue_name)

    def get_queue_info(self) -> str:
        return f"RabbitMQ适配器 -> {self.rabbitmq.connection_string} (发布: {self.rabbitmq.published_count}, 消费: {self.rabbitmq.consumed_count})"


# ==================== 统一服务管理器 ====================

class ServiceManager:
    """服务管理器"""

    def __init__(self):
        self.loggers: Dict[str, Logger] = {}
        self.caches: Dict[str, CacheInterface] = {}
        self.queues: Dict[str, MessageQueue] = {}

    def register_logger(self, name: str, logger: Logger) -> None:
        """注册日志器"""
        self.loggers[name] = logger
        print(f"✅ 已注册日志器: {name}")

    def register_cache(self, name: str, cache: CacheInterface) -> None:
        """注册缓存"""
        self.caches[name] = cache
        print(f"✅ 已注册缓存: {name}")

    def register_queue(self, name: str, queue: MessageQueue) -> None:
        """注册消息队列"""
        self.queues[name] = queue
        print(f"✅ 已注册消息队列: {name}")

    def log_message(self, logger_name: str, level: LogLevel, message: str, **kwargs) -> None:
        """记录日志"""
        if logger_name in self.loggers:
            self.loggers[logger_name].log(level, message, **kwargs)

    def cache_data(self, cache_name: str, key: str, value: Any, ttl: int = 3600) -> bool:
        """缓存数据"""
        if cache_name in self.caches:
            return self.caches[cache_name].set(key, value, ttl)
        return False

    def get_cached_data(self, cache_name: str, key: str) -> Optional[Any]:
        """获取缓存数据"""
        if cache_name in self.caches:
            return self.caches[cache_name].get(key)
        return None

    def send_message(self, queue_name: str, message: Dict[str, Any]) -> bool:
        """发送消息"""
        if queue_name in self.queues:
            return self.queues[queue_name].send_message("default", message)
        return False

    def get_service_status(self) -> Dict[str, List[str]]:
        """获取服务状态"""
        return {
            "loggers": [logger.get_logger_info() for logger in self.loggers.values()],
            "caches": [cache.get_cache_info() for cache in self.caches.values()],
            "queues": [queue.get_queue_info() for queue in self.queues.values()]
        }


def demo_real_world_adapters():
    """实际应用适配器演示"""
    print("=" * 60)
    print("🌍 实际应用案例 - 适配器模式演示")
    print("=" * 60)

    # 创建服务管理器
    service_manager = ServiceManager()

    # 创建并注册日志适配器
    print("\n📝 配置日志系统:")
    python_logger = PythonLoggingModule("WebApp")
    structured_logger = StructuredLogger("UserService")

    service_manager.register_logger("python", PythonLoggingAdapter(python_logger))
    service_manager.register_logger("structured", StructuredLoggerAdapter(structured_logger))

    # 创建并注册缓存适配器
    print("\n💾 配置缓存系统:")
    memory_cache = MemoryCache()
    redis_cache = RedisLikeCache("localhost", 6379)

    service_manager.register_cache("memory", MemoryCacheAdapter(memory_cache))
    service_manager.register_cache("redis", RedisCacheAdapter(redis_cache))

    # 创建并注册消息队列适配器
    print("\n📨 配置消息队列:")
    simple_queue = SimpleQueue()
    rabbitmq = RabbitMQLike("amqp://localhost:5672")

    service_manager.register_queue("simple", SimpleQueueAdapter(simple_queue))
    service_manager.register_queue("rabbitmq", RabbitMQAdapter(rabbitmq))

    # 测试日志系统
    print(f"\n📝 测试日志系统:")
    service_manager.log_message("python", LogLevel.INFO, "应用程序启动")
    service_manager.log_message("structured", LogLevel.WARNING, "内存使用率过高", memory_usage=85.5, threshold=80.0)

    # 测试缓存系统
    print(f"\n💾 测试缓存系统:")
    user_data = {"id": 123, "name": "Alice", "email": "alice@example.com"}

    service_manager.cache_data("memory", "user:123", user_data, 1800)
    service_manager.cache_data("redis", "user:123", user_data, 3600)

    # 获取缓存数据
    cached_user_memory = service_manager.get_cached_data("memory", "user:123")
    cached_user_redis = service_manager.get_cached_data("redis", "user:123")

    print(f"   内存缓存结果: {cached_user_memory}")
    print(f"   Redis缓存结果: {cached_user_redis}")

    # 测试消息队列
    print(f"\n📨 测试消息队列:")
    order_message = {
        "order_id": "ORD-001",
        "user_id": 123,
        "amount": 99.99,
        "status": "pending"
    }

    service_manager.send_message("simple", order_message)
    service_manager.send_message("rabbitmq", order_message)

    # 显示服务状态
    print(f"\n📊 服务状态:")
    status = service_manager.get_service_status()

    for service_type, services in status.items():
        print(f"  {service_type.upper()}:")
        for service_info in services:
            print(f"    - {service_info}")


if __name__ == "__main__":
    demo_real_world_adapters()
