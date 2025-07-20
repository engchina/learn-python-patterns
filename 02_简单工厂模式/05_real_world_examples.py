"""
05_real_world_examples.py - 简单工厂模式实际应用示例

实际应用场景演示
这个文件展示了简单工厂模式在实际开发中的多种应用场景：
1. 连接池工厂 - 不同类型的连接池创建
2. 验证器工厂 - 不同验证规则的验证器
3. 缓存工厂 - 不同缓存策略的缓存器
4. 序列化器工厂 - 不同格式的序列化器
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
import time
import hashlib
import json
import pickle
from datetime import datetime, timedelta


# ==================== 连接池工厂 ====================
class ConnectionPool(ABC):
    """连接池抽象基类"""
    
    def __init__(self, name: str, max_connections: int = 10):
        self.name = name
        self.max_connections = max_connections
        self.active_connections = 0
        self.created_time = datetime.now()
    
    @abstractmethod
    def get_connection(self) -> Dict[str, Any]:
        """获取连接"""
        pass
    
    @abstractmethod
    def release_connection(self, connection: Dict[str, Any]) -> bool:
        """释放连接"""
        pass
    
    @abstractmethod
    def close_all(self) -> bool:
        """关闭所有连接"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """获取连接池状态"""
        return {
            "name": self.name,
            "max_connections": self.max_connections,
            "active_connections": self.active_connections,
            "usage_rate": round(self.active_connections / self.max_connections * 100, 2),
            "created_time": self.created_time.isoformat()
        }


class DatabaseConnectionPool(ConnectionPool):
    """数据库连接池"""
    
    def __init__(self, host: str = "localhost", port: int = 5432, max_connections: int = 10):
        super().__init__("数据库连接池", max_connections)
        self.host = host
        self.port = port
        self.connections = []
    
    def get_connection(self) -> Dict[str, Any]:
        """获取数据库连接"""
        if self.active_connections >= self.max_connections:
            raise Exception("连接池已满，无法创建新连接")
        
        connection = {
            "id": f"db_conn_{self.active_connections + 1}",
            "host": self.host,
            "port": self.port,
            "created_at": datetime.now().isoformat(),
            "type": "database"
        }
        
        self.connections.append(connection)
        self.active_connections += 1
        
        print(f"🔗 获取数据库连接: {connection['id']} ({self.host}:{self.port})")
        return connection
    
    def release_connection(self, connection: Dict[str, Any]) -> bool:
        """释放数据库连接"""
        if connection in self.connections:
            self.connections.remove(connection)
            self.active_connections -= 1
            print(f"🔓 释放数据库连接: {connection['id']}")
            return True
        return False
    
    def close_all(self) -> bool:
        """关闭所有数据库连接"""
        count = len(self.connections)
        self.connections.clear()
        self.active_connections = 0
        print(f"🔒 关闭所有数据库连接，共 {count} 个")
        return True


class RedisConnectionPool(ConnectionPool):
    """Redis连接池"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, max_connections: int = 20):
        super().__init__("Redis连接池", max_connections)
        self.host = host
        self.port = port
        self.connections = []
    
    def get_connection(self) -> Dict[str, Any]:
        """获取Redis连接"""
        if self.active_connections >= self.max_connections:
            raise Exception("Redis连接池已满")
        
        connection = {
            "id": f"redis_conn_{self.active_connections + 1}",
            "host": self.host,
            "port": self.port,
            "created_at": datetime.now().isoformat(),
            "type": "redis"
        }
        
        self.connections.append(connection)
        self.active_connections += 1
        
        print(f"🔗 获取Redis连接: {connection['id']} ({self.host}:{self.port})")
        return connection
    
    def release_connection(self, connection: Dict[str, Any]) -> bool:
        """释放Redis连接"""
        if connection in self.connections:
            self.connections.remove(connection)
            self.active_connections -= 1
            print(f"🔓 释放Redis连接: {connection['id']}")
            return True
        return False
    
    def close_all(self) -> bool:
        """关闭所有Redis连接"""
        count = len(self.connections)
        self.connections.clear()
        self.active_connections = 0
        print(f"🔒 关闭所有Redis连接，共 {count} 个")
        return True


class HTTPConnectionPool(ConnectionPool):
    """HTTP连接池"""
    
    def __init__(self, base_url: str = "https://api.example.com", max_connections: int = 15):
        super().__init__("HTTP连接池", max_connections)
        self.base_url = base_url
        self.connections = []
    
    def get_connection(self) -> Dict[str, Any]:
        """获取HTTP连接"""
        if self.active_connections >= self.max_connections:
            raise Exception("HTTP连接池已满")
        
        connection = {
            "id": f"http_conn_{self.active_connections + 1}",
            "base_url": self.base_url,
            "created_at": datetime.now().isoformat(),
            "type": "http",
            "session_id": hashlib.md5(f"{self.base_url}_{time.time()}".encode()).hexdigest()[:8]
        }
        
        self.connections.append(connection)
        self.active_connections += 1
        
        print(f"🔗 获取HTTP连接: {connection['id']} ({self.base_url})")
        return connection
    
    def release_connection(self, connection: Dict[str, Any]) -> bool:
        """释放HTTP连接"""
        if connection in self.connections:
            self.connections.remove(connection)
            self.active_connections -= 1
            print(f"🔓 释放HTTP连接: {connection['id']}")
            return True
        return False
    
    def close_all(self) -> bool:
        """关闭所有HTTP连接"""
        count = len(self.connections)
        self.connections.clear()
        self.active_connections = 0
        print(f"🔒 关闭所有HTTP连接，共 {count} 个")
        return True


class ConnectionPoolFactory:
    """连接池工厂"""
    
    SUPPORTED_POOLS = {
        "database": ("数据库", DatabaseConnectionPool),
        "redis": ("Redis", RedisConnectionPool),
        "http": ("HTTP", HTTPConnectionPool),
        # 别名
        "db": ("数据库", DatabaseConnectionPool),
        "cache": ("Redis", RedisConnectionPool),
        "api": ("HTTP", HTTPConnectionPool),
    }
    
    @staticmethod
    def create_pool(pool_type: str, **kwargs) -> ConnectionPool:
        """创建连接池"""
        pool_type = pool_type.lower().strip()
        
        if pool_type in ConnectionPoolFactory.SUPPORTED_POOLS:
            pool_name, pool_class = ConnectionPoolFactory.SUPPORTED_POOLS[pool_type]
            print(f"🏭 连接池工厂正在创建 {pool_name} 连接池...")
            pool = pool_class(**kwargs)
            print(f"✅ {pool.name} 创建成功")
            return pool
        else:
            supported = list(set([name for name, _ in ConnectionPoolFactory.SUPPORTED_POOLS.values()]))
            raise ValueError(f"不支持的连接池类型: {pool_type}。支持的类型: {supported}")


# ==================== 验证器工厂 ====================
class Validator(ABC):
    """验证器抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.validation_count = 0
    
    @abstractmethod
    def validate(self, value: Any) -> bool:
        """验证值"""
        pass
    
    @abstractmethod
    def get_error_message(self, value: Any) -> str:
        """获取错误消息"""
        pass
    
    def is_valid(self, value: Any) -> tuple[bool, str]:
        """验证并返回结果和错误消息"""
        self.validation_count += 1
        is_valid = self.validate(value)
        error_msg = "" if is_valid else self.get_error_message(value)
        return is_valid, error_msg


class EmailValidator(Validator):
    """邮箱验证器"""
    
    def __init__(self):
        super().__init__("邮箱验证器")
    
    def validate(self, value: Any) -> bool:
        """验证邮箱格式"""
        if not isinstance(value, str):
            return False
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, value))
    
    def get_error_message(self, value: Any) -> str:
        return f"无效的邮箱格式: {value}"


class PhoneValidator(Validator):
    """手机号验证器"""
    
    def __init__(self):
        super().__init__("手机号验证器")
    
    def validate(self, value: Any) -> bool:
        """验证手机号格式"""
        if not isinstance(value, str):
            return False
        
        import re
        # 简单的中国手机号验证
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, value))
    
    def get_error_message(self, value: Any) -> str:
        return f"无效的手机号格式: {value}"


class PasswordValidator(Validator):
    """密码验证器"""
    
    def __init__(self, min_length: int = 8, require_special: bool = True):
        super().__init__("密码验证器")
        self.min_length = min_length
        self.require_special = require_special
    
    def validate(self, value: Any) -> bool:
        """验证密码强度"""
        if not isinstance(value, str):
            return False
        
        if len(value) < self.min_length:
            return False
        
        has_upper = any(c.isupper() for c in value)
        has_lower = any(c.islower() for c in value)
        has_digit = any(c.isdigit() for c in value)
        
        if not (has_upper and has_lower and has_digit):
            return False
        
        if self.require_special:
            import re
            has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', value))
            if not has_special:
                return False
        
        return True
    
    def get_error_message(self, value: Any) -> str:
        if not isinstance(value, str):
            return "密码必须是字符串"
        
        if len(value) < self.min_length:
            return f"密码长度至少 {self.min_length} 位"
        
        requirements = ["大写字母", "小写字母", "数字"]
        if self.require_special:
            requirements.append("特殊字符")
        
        return f"密码必须包含: {', '.join(requirements)}"


class ValidatorFactory:
    """验证器工厂"""
    
    SUPPORTED_VALIDATORS = {
        "email": ("邮箱", EmailValidator),
        "phone": ("手机号", PhoneValidator),
        "password": ("密码", PasswordValidator),
    }
    
    @staticmethod
    def create_validator(validator_type: str, **kwargs) -> Validator:
        """创建验证器"""
        validator_type = validator_type.lower().strip()
        
        if validator_type in ValidatorFactory.SUPPORTED_VALIDATORS:
            validator_name, validator_class = ValidatorFactory.SUPPORTED_VALIDATORS[validator_type]
            print(f"🏭 验证器工厂正在创建 {validator_name} 验证器...")
            validator = validator_class(**kwargs)
            print(f"✅ {validator.name} 创建成功")
            return validator
        else:
            supported = list(set([name for name, _ in ValidatorFactory.SUPPORTED_VALIDATORS.values()]))
            raise ValueError(f"不支持的验证器类型: {validator_type}。支持的类型: {supported}")


# ==================== 缓存工厂 ====================
class Cache(ABC):
    """缓存抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.hit_count = 0
        self.miss_count = 0
    
    @abstractmethod
    def get(self, key: str) -> Any:
        """获取缓存值"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """删除缓存"""
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """清空缓存"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self.hit_count + self.miss_count
        hit_rate = round(self.hit_count / total * 100, 2) if total > 0 else 0
        
        return {
            "name": self.name,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate
        }


class MemoryCache(Cache):
    """内存缓存"""
    
    def __init__(self, max_size: int = 1000):
        super().__init__("内存缓存")
        self.max_size = max_size
        self.data = {}
        self.expiry = {}
    
    def get(self, key: str) -> Any:
        """获取缓存值"""
        # 检查是否过期
        if key in self.expiry and datetime.now() > self.expiry[key]:
            del self.data[key]
            del self.expiry[key]
            self.miss_count += 1
            return None
        
        if key in self.data:
            self.hit_count += 1
            print(f"💾 内存缓存命中: {key}")
            return self.data[key]
        else:
            self.miss_count += 1
            print(f"💾 内存缓存未命中: {key}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        # 检查容量
        if len(self.data) >= self.max_size and key not in self.data:
            # 简单的LRU：删除第一个
            first_key = next(iter(self.data))
            del self.data[first_key]
            if first_key in self.expiry:
                del self.expiry[first_key]
        
        self.data[key] = value
        
        if ttl:
            self.expiry[key] = datetime.now() + timedelta(seconds=ttl)
        
        print(f"💾 内存缓存设置: {key} (TTL: {ttl}s)")
        return True
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        if key in self.data:
            del self.data[key]
            if key in self.expiry:
                del self.expiry[key]
            print(f"💾 内存缓存删除: {key}")
            return True
        return False
    
    def clear(self) -> bool:
        """清空缓存"""
        count = len(self.data)
        self.data.clear()
        self.expiry.clear()
        print(f"💾 内存缓存清空，删除 {count} 个项目")
        return True


class FileCache(Cache):
    """文件缓存"""
    
    def __init__(self, cache_dir: str = "./cache"):
        super().__init__("文件缓存")
        self.cache_dir = cache_dir
        import os
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """获取缓存文件路径"""
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return f"{self.cache_dir}/{safe_key}.cache"
    
    def get(self, key: str) -> Any:
        """获取缓存值"""
        file_path = self._get_file_path(key)
        
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                
            # 检查是否过期
            if 'expiry' in data and datetime.now() > data['expiry']:
                import os
                os.remove(file_path)
                self.miss_count += 1
                return None
            
            self.hit_count += 1
            print(f"📁 文件缓存命中: {key}")
            return data['value']
            
        except (FileNotFoundError, pickle.PickleError):
            self.miss_count += 1
            print(f"📁 文件缓存未命中: {key}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        file_path = self._get_file_path(key)
        
        data = {'value': value}
        if ttl:
            data['expiry'] = datetime.now() + timedelta(seconds=ttl)
        
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            print(f"📁 文件缓存设置: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            print(f"📁 文件缓存设置失败: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        file_path = self._get_file_path(key)
        try:
            import os
            os.remove(file_path)
            print(f"📁 文件缓存删除: {key}")
            return True
        except FileNotFoundError:
            return False
    
    def clear(self) -> bool:
        """清空缓存"""
        import os
        import glob
        
        cache_files = glob.glob(f"{self.cache_dir}/*.cache")
        count = len(cache_files)
        
        for file_path in cache_files:
            os.remove(file_path)
        
        print(f"📁 文件缓存清空，删除 {count} 个文件")
        return True


class CacheFactory:
    """缓存工厂"""
    
    SUPPORTED_CACHES = {
        "memory": ("内存", MemoryCache),
        "file": ("文件", FileCache),
        # 别名
        "mem": ("内存", MemoryCache),
        "disk": ("文件", FileCache),
    }
    
    @staticmethod
    def create_cache(cache_type: str, **kwargs) -> Cache:
        """创建缓存"""
        cache_type = cache_type.lower().strip()
        
        if cache_type in CacheFactory.SUPPORTED_CACHES:
            cache_name, cache_class = CacheFactory.SUPPORTED_CACHES[cache_type]
            print(f"🏭 缓存工厂正在创建 {cache_name} 缓存...")
            cache = cache_class(**kwargs)
            print(f"✅ {cache.name} 创建成功")
            return cache
        else:
            supported = list(set([name for name, _ in CacheFactory.SUPPORTED_CACHES.values()]))
            raise ValueError(f"不支持的缓存类型: {cache_type}。支持的类型: {supported}")


# ==================== 演示函数 ====================
def demo_connection_pools():
    """演示连接池工厂"""
    print("=== 连接池工厂演示 ===\n")
    
    # 创建不同类型的连接池
    pools = [
        ("database", {"host": "db.example.com", "port": 5432, "max_connections": 5}),
        ("redis", {"host": "cache.example.com", "port": 6379, "max_connections": 10}),
        ("http", {"base_url": "https://api.example.com", "max_connections": 8})
    ]
    
    for pool_type, config in pools:
        print(f"\n--- {pool_type.upper()} 连接池测试 ---")
        
        try:
            pool = ConnectionPoolFactory.create_pool(pool_type, **config)
            
            # 获取几个连接
            connections = []
            for i in range(3):
                conn = pool.get_connection()
                connections.append(conn)
            
            # 显示状态
            status = pool.get_status()
            print(f"连接池状态: {status}")
            
            # 释放连接
            for conn in connections:
                pool.release_connection(conn)
            
            # 关闭连接池
            pool.close_all()
            
        except Exception as e:
            print(f"❌ 连接池测试失败: {e}")


def demo_validators():
    """演示验证器工厂"""
    print("\n" + "=" * 60)
    print("验证器工厂演示")
    print("=" * 60)
    
    # 测试数据
    test_data = [
        ("email", "test@example.com", {}),
        ("email", "invalid-email", {}),
        ("phone", "13800138000", {}),
        ("phone", "12345", {}),
        ("password", "StrongPass123!", {"min_length": 8, "require_special": True}),
        ("password", "weak", {"min_length": 8, "require_special": True})
    ]
    
    for validator_type, value, config in test_data:
        print(f"\n--- 验证 {validator_type}: {value} ---")
        
        try:
            validator = ValidatorFactory.create_validator(validator_type, **config)
            is_valid, error_msg = validator.is_valid(value)
            
            if is_valid:
                print(f"✅ 验证通过")
            else:
                print(f"❌ 验证失败: {error_msg}")
                
        except Exception as e:
            print(f"❌ 验证器创建失败: {e}")


def demo_caches():
    """演示缓存工厂"""
    print("\n" + "=" * 60)
    print("缓存工厂演示")
    print("=" * 60)
    
    cache_types = ["memory", "file"]
    
    for cache_type in cache_types:
        print(f"\n--- {cache_type.upper()} 缓存测试 ---")
        
        try:
            cache = CacheFactory.create_cache(cache_type)
            
            # 设置缓存
            cache.set("user:1", {"name": "张三", "age": 25}, ttl=60)
            cache.set("config:app", {"debug": True, "version": "1.0"})
            
            # 获取缓存
            user_data = cache.get("user:1")
            config_data = cache.get("config:app")
            missing_data = cache.get("nonexistent")
            
            print(f"用户数据: {user_data}")
            print(f"配置数据: {config_data}")
            print(f"不存在的数据: {missing_data}")
            
            # 显示统计
            stats = cache.get_stats()
            print(f"缓存统计: {stats}")
            
            # 清空缓存
            cache.clear()
            
        except Exception as e:
            print(f"❌ 缓存测试失败: {e}")


def main():
    """主函数"""
    demo_connection_pools()
    demo_validators()
    demo_caches()
    
    print("\n" + "=" * 60)
    print("简单工厂模式在实际项目中的价值:")
    print("1. 资源管理：统一的连接池创建和管理")
    print("2. 数据验证：灵活的验证器创建和配置")
    print("3. 缓存策略：不同缓存实现的统一接口")
    print("4. 配置驱动：根据配置动态选择实现")
    print("5. 易于测试：可以轻松替换实现进行测试")
    print("=" * 60)


if __name__ == "__main__":
    main()
