"""
03_cache_proxy.py - 缓存代理示例

这个示例展示了缓存代理在性能优化中的应用。
包括缓存机制的实现、性能优化策略和缓存失效处理。
"""

import time
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class CacheStrategy(Enum):
    """缓存策略枚举"""
    LRU = "LRU"  # 最近最少使用
    LFU = "LFU"  # 最少使用频率
    TTL = "TTL"  # 生存时间


# ==================== 数据服务接口 ====================
class DataService(ABC):
    """数据服务抽象接口"""

    @abstractmethod
    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """获取用户数据"""
        pass

    @abstractmethod
    def search_products(self, query: str, category: str = "") -> List[Dict[str, Any]]:
        """搜索商品"""
        pass

    @abstractmethod
    def get_analytics_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """获取分析报告"""
        pass

    @abstractmethod
    def calculate_recommendation(self, user_id: str) -> List[str]:
        """计算推荐"""
        pass


# ==================== 真实数据服务 ====================
class DatabaseService(DataService):
    """数据库服务 - 真实的数据服务"""

    def __init__(self, name: str):
        self.name = name
        self.query_count = 0
        self.total_query_time = 0
        print(f"数据库服务 '{name}' 初始化完成")

    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """获取用户数据"""
        self._simulate_database_query(0.5)  # 模拟数据库查询时间

        return {
            "user_id": user_id,
            "name": f"用户{user_id}",
            "email": f"user{user_id}@example.com",
            "age": 25 + int(user_id) % 50,
            "preferences": ["科技", "阅读", "旅行"],
            "last_login": datetime.now().isoformat()
        }

    def search_products(self, query: str, category: str = "") -> List[Dict[str, Any]]:
        """搜索商品"""
        self._simulate_database_query(1.0)  # 搜索操作更耗时

        # 模拟搜索结果
        products = []
        for i in range(5):
            products.append({
                "product_id": f"P{i+1:03d}",
                "name": f"{query}相关商品{i+1}",
                "category": category or "通用",
                "price": 99.99 + i * 10,
                "rating": 4.0 + (i % 5) * 0.2
            })

        return products

    def get_analytics_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """获取分析报告"""
        self._simulate_database_query(2.0)  # 分析报告非常耗时

        return {
            "period": f"{start_date} 到 {end_date}",
            "total_users": 10000 + int(start_date.replace("-", "")) % 5000,
            "total_orders": 5000 + int(end_date.replace("-", "")) % 2000,
            "revenue": 100000.0 + (int(start_date.replace("-", "")) % 50000),
            "generated_at": datetime.now().isoformat()
        }

    def calculate_recommendation(self, user_id: str) -> List[str]:
        """计算推荐"""
        self._simulate_database_query(1.5)  # 推荐计算耗时

        # 模拟推荐结果
        base_products = ["手机", "笔记本", "耳机", "平板", "手表"]
        user_factor = int(user_id) % len(base_products)

        recommendations = []
        for i in range(3):
            product_index = (user_factor + i) % len(base_products)
            recommendations.append(f"{base_products[product_index]}{i+1}")

        return recommendations

    def _simulate_database_query(self, duration: float):
        """模拟数据库查询"""
        self.query_count += 1
        start_time = time.time()
        time.sleep(duration)
        end_time = time.time()
        actual_duration = end_time - start_time
        self.total_query_time += actual_duration

        print(f"数据库查询 #{self.query_count}: 耗时 {actual_duration:.2f} 秒")

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        avg_query_time = self.total_query_time / self.query_count if self.query_count > 0 else 0
        return {
            "service_name": self.name,
            "total_queries": self.query_count,
            "total_query_time": round(self.total_query_time, 2),
            "average_query_time": round(avg_query_time, 2)
        }


# ==================== 缓存项 ====================
class CacheItem:
    """缓存项"""

    def __init__(self, key: str, value: Any, ttl_seconds: int = 300):
        self.key = key
        self.value = value
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(seconds=ttl_seconds)
        self.access_count = 0
        self.last_accessed = self.created_at

    def is_expired(self) -> bool:
        """检查是否过期"""
        return datetime.now() > self.expires_at

    def access(self) -> Any:
        """访问缓存项"""
        self.access_count += 1
        self.last_accessed = datetime.now()
        return self.value

    def get_age_seconds(self) -> float:
        """获取缓存项年龄（秒）"""
        return (datetime.now() - self.created_at).total_seconds()


# ==================== 缓存管理器 ====================
class CacheManager:
    """缓存管理器"""

    def __init__(self, max_size: int = 100, default_ttl: int = 300, strategy: CacheStrategy = CacheStrategy.LRU):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.strategy = strategy
        self.cache: Dict[str, CacheItem] = {}
        self.hit_count = 0
        self.miss_count = 0
        print(f"缓存管理器初始化: 最大容量={max_size}, 默认TTL={default_ttl}秒, 策略={strategy.value}")

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key in self.cache:
            item = self.cache[key]

            # 检查是否过期
            if item.is_expired():
                del self.cache[key]
                self.miss_count += 1
                print(f"缓存过期: {key}")
                return None

            # 缓存命中
            self.hit_count += 1
            print(f"缓存命中: {key} (访问次数: {item.access_count + 1})")
            return item.access()

        # 缓存未命中
        self.miss_count += 1
        print(f"缓存未命中: {key}")
        return None

    def put(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """存储缓存值"""
        ttl = ttl_seconds or self.default_ttl

        # 如果缓存已满，根据策略清理
        if len(self.cache) >= self.max_size and key not in self.cache:
            self._evict_item()

        self.cache[key] = CacheItem(key, value, ttl)
        print(f"缓存存储: {key} (TTL: {ttl}秒)")

    def invalidate(self, key: str) -> bool:
        """使缓存失效"""
        if key in self.cache:
            del self.cache[key]
            print(f"缓存失效: {key}")
            return True
        return False

    def clear(self) -> None:
        """清空缓存"""
        count = len(self.cache)
        self.cache.clear()
        print(f"缓存已清空: 清理了 {count} 个项目")

    def _evict_item(self) -> None:
        """根据策略清理缓存项"""
        if not self.cache:
            return

        if self.strategy == CacheStrategy.LRU:
            # 最近最少使用
            oldest_key = min(self.cache.keys(),
                           key=lambda k: self.cache[k].last_accessed)
            del self.cache[oldest_key]
            print(f"LRU清理: {oldest_key}")

        elif self.strategy == CacheStrategy.LFU:
            # 最少使用频率
            least_used_key = min(self.cache.keys(),
                               key=lambda k: self.cache[k].access_count)
            del self.cache[least_used_key]
            print(f"LFU清理: {least_used_key}")

        elif self.strategy == CacheStrategy.TTL:
            # 最早过期的
            earliest_expire_key = min(self.cache.keys(),
                                    key=lambda k: self.cache[k].expires_at)
            del self.cache[earliest_expire_key]
            print(f"TTL清理: {earliest_expire_key}")

    def get_statistics(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0

        return {
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": round(hit_rate, 1),
            "strategy": self.strategy.value
        }


# ==================== 缓存代理 ====================
class CacheProxy(DataService):
    """缓存代理"""

    def __init__(self, data_service: DataService, cache_manager: CacheManager):
        self.data_service = data_service
        self.cache_manager = cache_manager
        print(f"缓存代理已创建")

    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """获取用户数据 - 带缓存"""
        cache_key = f"user_data:{user_id}"

        # 尝试从缓存获取
        cached_data = self.cache_manager.get(cache_key)
        if cached_data is not None:
            return cached_data

        # 缓存未命中，从真实服务获取
        print(f"从数据服务获取用户数据: {user_id}")
        data = self.data_service.get_user_data(user_id)

        # 存储到缓存
        self.cache_manager.put(cache_key, data, ttl_seconds=600)  # 10分钟TTL

        return data

    def search_products(self, query: str, category: str = "") -> List[Dict[str, Any]]:
        """搜索商品 - 带缓存"""
        cache_key = self._generate_cache_key("search", query, category)

        # 尝试从缓存获取
        cached_data = self.cache_manager.get(cache_key)
        if cached_data is not None:
            return cached_data

        # 缓存未命中，从真实服务获取
        print(f"从数据服务搜索商品: query='{query}', category='{category}'")
        data = self.data_service.search_products(query, category)

        # 存储到缓存
        self.cache_manager.put(cache_key, data, ttl_seconds=300)  # 5分钟TTL

        return data

    def get_analytics_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """获取分析报告 - 带缓存"""
        cache_key = f"analytics:{start_date}:{end_date}"

        # 尝试从缓存获取
        cached_data = self.cache_manager.get(cache_key)
        if cached_data is not None:
            return cached_data

        # 缓存未命中，从真实服务获取
        print(f"从数据服务获取分析报告: {start_date} 到 {end_date}")
        data = self.data_service.get_analytics_report(start_date, end_date)

        # 存储到缓存
        self.cache_manager.put(cache_key, data, ttl_seconds=1800)  # 30分钟TTL

        return data

    def calculate_recommendation(self, user_id: str) -> List[str]:
        """计算推荐 - 带缓存"""
        cache_key = f"recommendation:{user_id}"

        # 尝试从缓存获取
        cached_data = self.cache_manager.get(cache_key)
        if cached_data is not None:
            return cached_data

        # 缓存未命中，从真实服务获取
        print(f"从数据服务计算推荐: {user_id}")
        data = self.data_service.calculate_recommendation(user_id)

        # 存储到缓存
        self.cache_manager.put(cache_key, data, ttl_seconds=900)  # 15分钟TTL

        return data

    def invalidate_user_cache(self, user_id: str):
        """使用户相关缓存失效"""
        keys_to_invalidate = [
            f"user_data:{user_id}",
            f"recommendation:{user_id}"
        ]

        for key in keys_to_invalidate:
            self.cache_manager.invalidate(key)

        print(f"用户 {user_id} 相关缓存已失效")

    def _generate_cache_key(self, prefix: str, *args) -> str:
        """生成缓存键"""
        key_data = f"{prefix}:" + ":".join(str(arg) for arg in args)
        return hashlib.md5(key_data.encode()).hexdigest()[:16]


# ==================== 使用示例 ====================
def demo_cache_proxy():
    """缓存代理演示"""
    print("=" * 60)
    print("🚀 缓存代理演示 - 性能优化")
    print("=" * 60)

    # 创建系统组件
    database_service = DatabaseService("主数据库")
    cache_manager = CacheManager(max_size=50, default_ttl=300, strategy=CacheStrategy.LRU)
    cache_proxy = CacheProxy(database_service, cache_manager)

    print("\n📊 测试用户数据缓存:")

    # 第一次访问 - 缓存未命中
    print("\n--- 第一次获取用户数据 ---")
    start_time = time.time()
    user_data = cache_proxy.get_user_data("123")
    end_time = time.time()
    print(f"耗时: {end_time - start_time:.2f} 秒")
    print(f"用户数据: {user_data['name']}, {user_data['email']}")

    # 第二次访问 - 缓存命中
    print("\n--- 第二次获取用户数据 ---")
    start_time = time.time()
    user_data = cache_proxy.get_user_data("123")
    end_time = time.time()
    print(f"耗时: {end_time - start_time:.2f} 秒")
    print(f"用户数据: {user_data['name']}, {user_data['email']}")

    print("\n🔍 测试商品搜索缓存:")

    # 搜索商品
    print("\n--- 第一次搜索商品 ---")
    start_time = time.time()
    products = cache_proxy.search_products("手机", "电子产品")
    end_time = time.time()
    print(f"耗时: {end_time - start_time:.2f} 秒")
    print(f"找到 {len(products)} 个商品")

    # 再次搜索相同商品
    print("\n--- 第二次搜索相同商品 ---")
    start_time = time.time()
    products = cache_proxy.search_products("手机", "电子产品")
    end_time = time.time()
    print(f"耗时: {end_time - start_time:.2f} 秒")
    print(f"找到 {len(products)} 个商品")

    # 显示统计信息
    print("\n📈 性能统计:")
    db_stats = database_service.get_statistics()
    cache_stats = cache_manager.get_statistics()

    print(f"数据库统计: {db_stats}")
    print(f"缓存统计: {cache_stats}")


def demo_cache_strategies():
    """缓存策略演示"""
    print("\n" + "=" * 60)
    print("📋 缓存策略对比演示")
    print("=" * 60)

    strategies = [CacheStrategy.LRU, CacheStrategy.LFU, CacheStrategy.TTL]

    for strategy in strategies:
        print(f"\n--- 测试 {strategy.value} 策略 ---")

        database_service = DatabaseService(f"数据库-{strategy.value}")
        cache_manager = CacheManager(max_size=3, default_ttl=60, strategy=strategy)
        cache_proxy = CacheProxy(database_service, cache_manager)

        # 添加多个缓存项，触发清理
        users = ["001", "002", "003", "004", "005"]

        for user_id in users:
            print(f"\n获取用户 {user_id} 数据:")
            cache_proxy.get_user_data(user_id)

            # 显示当前缓存状态
            stats = cache_manager.get_statistics()
            print(f"缓存状态: 大小={stats['cache_size']}/{stats['max_size']}")


def demo_cache_invalidation():
    """缓存失效演示"""
    print("\n" + "=" * 60)
    print("🗑️ 缓存失效演示")
    print("=" * 60)

    database_service = DatabaseService("用户数据库")
    cache_manager = CacheManager(max_size=10, default_ttl=300)
    cache_proxy = CacheProxy(database_service, cache_manager)

    user_id = "999"

    # 获取用户数据并缓存
    print("\n📖 获取用户数据:")
    user_data = cache_proxy.get_user_data(user_id)
    print(f"用户数据: {user_data['name']}")

    # 再次获取（应该从缓存获取）
    print("\n📖 再次获取用户数据:")
    user_data = cache_proxy.get_user_data(user_id)
    print(f"用户数据: {user_data['name']}")

    # 使缓存失效
    print("\n🗑️ 使用户缓存失效:")
    cache_proxy.invalidate_user_cache(user_id)

    # 再次获取（应该从数据库获取）
    print("\n📖 失效后再次获取用户数据:")
    user_data = cache_proxy.get_user_data(user_id)
    print(f"用户数据: {user_data['name']}")

    # 显示最终统计
    print("\n📊 最终统计:")
    db_stats = database_service.get_statistics()
    cache_stats = cache_manager.get_statistics()
    print(f"数据库统计: {db_stats}")
    print(f"缓存统计: {cache_stats}")


def main():
    """主演示函数"""
    demo_cache_proxy()
    demo_cache_strategies()
    demo_cache_invalidation()

    print("\n" + "=" * 60)
    print("🎉 缓存代理演示完成！")
    print("💡 关键要点:")
    print("   • 缓存代理透明地添加缓存功能")
    print("   • 显著提高重复请求的响应速度")
    print("   • 支持多种缓存策略和TTL机制")
    print("   • 提供缓存失效和统计功能")
    print("   • 在高并发场景下效果显著")
    print("=" * 60)


if __name__ == "__main__":
    main()
