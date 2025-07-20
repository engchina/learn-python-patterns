"""
02_decorator_singleton.py - 装饰器实现单例模式

配置管理系统示例
这个示例展示了如何使用装饰器来实现单例模式。
装饰器方式实现单例模式更加简洁和优雅，
适合用于配置管理、缓存管理等场景。
"""

import threading
import json
from typing import Dict, Any, List
from functools import wraps


# ==================== 单例装饰器实现 ====================
def singleton(cls):
    """单例装饰器"""
    instances = {}
    lock = threading.Lock()
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


def thread_safe_singleton(cls):
    """线程安全的单例装饰器（增强版）"""
    instances = {}
    locks = {}
    main_lock = threading.Lock()
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        # 为每个类创建独立的锁
        if cls not in locks:
            with main_lock:
                if cls not in locks:
                    locks[cls] = threading.Lock()
        
        if cls not in instances:
            with locks[cls]:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    # 添加一些有用的方法
    def reset_instance():
        """重置实例（主要用于测试）"""
        with locks.get(cls, threading.Lock()):
            if cls in instances:
                del instances[cls]
    
    def get_instance_count():
        """获取实例数量"""
        return len([k for k in instances.keys() if k == cls])
    
    get_instance.reset_instance = reset_instance
    get_instance.get_instance_count = get_instance_count
    
    return get_instance


# ==================== 配置管理器 ====================
@singleton
class ConfigManager:
    """配置管理器（使用装饰器实现单例）"""
    
    def __init__(self):
        self.config = {
            "app_name": "MyApplication",
            "version": "1.0.0",
            "debug": True,
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "myapp_db",
                "user": "admin"
            },
            "cache": {
                "enabled": True,
                "ttl": 3600,
                "max_size": 1000
            },
            "logging": {
                "level": "INFO",
                "file": "app.log",
                "max_size": "10MB"
            }
        }
        self.observers = []  # 配置变更观察者
        print("配置管理器已初始化")
    
    def get_config(self, key: str, default=None):
        """获取配置项（支持嵌套键，如 'database.host'）"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_config(self, key: str, value: Any):
        """设置配置项（支持嵌套键）"""
        keys = key.split('.')
        config = self.config
        
        # 导航到最后一级的父级
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置最终值
        old_value = config.get(keys[-1])
        config[keys[-1]] = value
        
        print(f"配置已更新: {key} = {value}")
        
        # 通知观察者
        self._notify_observers(key, old_value, value)
    
    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self.config.copy()
    
    def load_from_file(self, filename: str):
        """从文件加载配置"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                self.config.update(file_config)
                print(f"配置已从文件加载: {filename}")
        except FileNotFoundError:
            print(f"配置文件不存在: {filename}")
        except json.JSONDecodeError:
            print(f"配置文件格式错误: {filename}")
    
    def save_to_file(self, filename: str):
        """保存配置到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
                print(f"配置已保存到文件: {filename}")
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def add_observer(self, observer):
        """添加配置变更观察者"""
        self.observers.append(observer)
    
    def remove_observer(self, observer):
        """移除配置变更观察者"""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def _notify_observers(self, key: str, old_value: Any, new_value: Any):
        """通知所有观察者配置已变更"""
        for observer in self.observers:
            try:
                observer.on_config_changed(key, old_value, new_value)
            except Exception as e:
                print(f"通知观察者失败: {e}")
    
    def reset_to_defaults(self):
        """重置为默认配置"""
        self.config = {
            "app_name": "MyApplication",
            "version": "1.0.0",
            "debug": True,
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "myapp_db",
                "user": "admin"
            }
        }
        print("配置已重置为默认值")


# ==================== 缓存管理器 ====================
@thread_safe_singleton
class CacheManager:
    """缓存管理器（使用增强版装饰器实现单例）"""
    
    def __init__(self):
        self.cache = {}
        self.access_count = {}
        self.max_size = 1000
        self.hit_count = 0
        self.miss_count = 0
        print("缓存管理器已初始化")
    
    def get(self, key: str):
        """获取缓存值"""
        if key in self.cache:
            self.hit_count += 1
            self.access_count[key] = self.access_count.get(key, 0) + 1
            print(f"缓存命中: {key}")
            return self.cache[key]
        else:
            self.miss_count += 1
            print(f"缓存未命中: {key}")
            return None
    
    def set(self, key: str, value: Any):
        """设置缓存值"""
        # 如果缓存已满，移除最少使用的项
        if len(self.cache) >= self.max_size and key not in self.cache:
            self._evict_least_used()
        
        self.cache[key] = value
        self.access_count[key] = self.access_count.get(key, 0) + 1
        print(f"缓存已设置: {key}")
    
    def delete(self, key: str):
        """删除缓存项"""
        if key in self.cache:
            del self.cache[key]
            if key in self.access_count:
                del self.access_count[key]
            print(f"缓存已删除: {key}")
            return True
        return False
    
    def clear(self):
        """清空所有缓存"""
        self.cache.clear()
        self.access_count.clear()
        self.hit_count = 0
        self.miss_count = 0
        print("缓存已清空")
    
    def _evict_least_used(self):
        """移除最少使用的缓存项"""
        if not self.access_count:
            return
        
        least_used_key = min(self.access_count, key=self.access_count.get)
        self.delete(least_used_key)
        print(f"移除最少使用的缓存项: {least_used_key}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": f"{hit_rate:.2f}%",
            "total_requests": total_requests
        }
    
    def set_max_size(self, size: int):
        """设置最大缓存大小"""
        self.max_size = size
        # 如果当前缓存超过新的最大大小，进行清理
        while len(self.cache) > self.max_size:
            self._evict_least_used()
        print(f"缓存最大大小已设置为: {size}")


# ==================== 配置观察者示例 ====================
class DatabaseConfigObserver:
    """数据库配置观察者"""
    
    def on_config_changed(self, key: str, old_value: Any, new_value: Any):
        """配置变更回调"""
        if key.startswith('database.'):
            print(f"数据库配置变更: {key} 从 {old_value} 改为 {new_value}")
            # 这里可以重新连接数据库等操作
            self._reconnect_database()
    
    def _reconnect_database(self):
        """重新连接数据库"""
        print("正在重新连接数据库...")


class LoggingConfigObserver:
    """日志配置观察者"""
    
    def on_config_changed(self, key: str, old_value: Any, new_value: Any):
        """配置变更回调"""
        if key.startswith('logging.'):
            print(f"日志配置变更: {key} 从 {old_value} 改为 {new_value}")
            # 这里可以重新配置日志系统
            self._reconfigure_logging()
    
    def _reconfigure_logging(self):
        """重新配置日志系统"""
        print("正在重新配置日志系统...")


# ==================== 演示函数 ====================
def demonstrate_config_manager():
    """演示配置管理器"""
    print("=" * 60)
    print("配置管理器单例演示")
    print("=" * 60)
    
    # 创建配置管理器实例
    config1 = ConfigManager()
    config2 = ConfigManager()
    
    print(f"config1 和 config2 是同一个对象: {config1 is config2}")
    
    # 添加观察者
    db_observer = DatabaseConfigObserver()
    log_observer = LoggingConfigObserver()
    config1.add_observer(db_observer)
    config1.add_observer(log_observer)
    
    # 获取配置
    print(f"应用名称: {config1.get_config('app_name')}")
    print(f"数据库主机: {config1.get_config('database.host')}")
    print(f"缓存TTL: {config1.get_config('cache.ttl')}")
    
    # 设置配置
    config1.set_config("database.host", "192.168.1.100")
    config1.set_config("logging.level", "DEBUG")
    config1.set_config("new_feature.enabled", True)
    
    # 从另一个实例获取配置
    print(f"从 config2 获取数据库主机: {config2.get_config('database.host')}")


def demonstrate_cache_manager():
    """演示缓存管理器"""
    print("\n" + "=" * 60)
    print("缓存管理器单例演示")
    print("=" * 60)
    
    # 创建缓存管理器实例
    cache1 = CacheManager()
    cache2 = CacheManager()
    
    print(f"cache1 和 cache2 是同一个对象: {cache1 is cache2}")
    
    # 设置缓存
    cache1.set("user:1001", {"name": "张三", "age": 25})
    cache1.set("user:1002", {"name": "李四", "age": 30})
    cache1.set("config:theme", "dark")
    
    # 从另一个实例获取缓存
    user_data = cache2.get("user:1001")
    print(f"从 cache2 获取用户数据: {user_data}")
    
    # 测试缓存命中和未命中
    cache2.get("user:1001")  # 命中
    cache2.get("user:9999")  # 未命中
    
    # 获取缓存统计
    stats = cache1.get_stats()
    print(f"缓存统计: {stats}")


def demonstrate_thread_safety():
    """演示线程安全性"""
    print("\n" + "=" * 60)
    print("线程安全性演示")
    print("=" * 60)
    
    instances = []
    
    def create_config_instance():
        """在线程中创建配置管理器实例"""
        config = ConfigManager()
        instances.append(config)
    
    # 创建多个线程同时创建实例
    threads = []
    for i in range(5):
        thread = threading.Thread(target=create_config_instance)
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 验证所有实例都是同一个对象
    print(f"创建了 {len(instances)} 个配置管理器实例")
    first_instance = instances[0]
    all_same = all(instance is first_instance for instance in instances)
    print(f"所有实例都是同一个对象: {all_same}")


def main():
    """主函数"""
    print("装饰器单例模式演示")
    
    demonstrate_config_manager()
    demonstrate_cache_manager()
    demonstrate_thread_safety()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
