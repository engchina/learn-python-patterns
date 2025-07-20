"""
05_real_world_examples.py - 实际项目中的策略模式应用

这个示例展示了策略模式在实际项目中的复杂应用场景，
包括文件压缩、图像处理、缓存管理等系统。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union
import os
import time
import random
import hashlib
from datetime import datetime, timedelta
from enum import Enum
import threading


# ==================== 文件压缩策略系统 ====================

class CompressionStrategy(ABC):
    """文件压缩策略抽象类"""
    
    @abstractmethod
    def compress(self, data: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """压缩数据，返回压缩后的数据和统计信息"""
        pass
    
    @abstractmethod
    def decompress(self, compressed_data: bytes) -> bytes:
        """解压数据"""
        pass
    
    @abstractmethod
    def get_algorithm_name(self) -> str:
        """获取算法名称"""
        pass
    
    @abstractmethod
    def get_compression_level(self) -> int:
        """获取压缩级别 (1-10)"""
        pass
    
    @abstractmethod
    def is_suitable_for_file_type(self, file_extension: str) -> bool:
        """判断是否适合特定文件类型"""
        pass


class ZipCompressionStrategy(CompressionStrategy):
    """ZIP压缩策略"""
    
    def __init__(self, compression_level: int = 6):
        self.compression_level = min(10, max(1, compression_level))
    
    def compress(self, data: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """模拟ZIP压缩"""
        start_time = time.time()
        
        # 模拟压缩过程
        time.sleep(0.01)  # 模拟压缩时间
        
        # 模拟压缩效果（根据压缩级别）
        compression_ratio = 0.3 + (self.compression_level / 10) * 0.4  # 30%-70%压缩率
        compressed_size = int(len(data) * compression_ratio)
        compressed_data = data[:compressed_size]  # 模拟压缩数据
        
        compression_time = time.time() - start_time
        
        stats = {
            'original_size': len(data),
            'compressed_size': compressed_size,
            'compression_ratio': (len(data) - compressed_size) / len(data) * 100,
            'compression_time': compression_time,
            'algorithm': self.get_algorithm_name()
        }
        
        return compressed_data, stats
    
    def decompress(self, compressed_data: bytes) -> bytes:
        """模拟ZIP解压"""
        time.sleep(0.005)  # 模拟解压时间
        # 模拟解压过程，实际应该恢复原始数据
        return compressed_data * 2  # 简单模拟
    
    def get_algorithm_name(self) -> str:
        return f"ZIP (级别 {self.compression_level})"
    
    def get_compression_level(self) -> int:
        return self.compression_level
    
    def is_suitable_for_file_type(self, file_extension: str) -> bool:
        """ZIP适合大多数文件类型"""
        return file_extension.lower() in ['.txt', '.doc', '.pdf', '.html', '.xml', '.csv']


class GzipCompressionStrategy(CompressionStrategy):
    """GZIP压缩策略"""
    
    def compress(self, data: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """模拟GZIP压缩"""
        start_time = time.time()
        time.sleep(0.008)
        
        # GZIP通常有更好的压缩率但速度稍慢
        compression_ratio = 0.25
        compressed_size = int(len(data) * compression_ratio)
        compressed_data = data[:compressed_size]
        
        compression_time = time.time() - start_time
        
        stats = {
            'original_size': len(data),
            'compressed_size': compressed_size,
            'compression_ratio': (len(data) - compressed_size) / len(data) * 100,
            'compression_time': compression_time,
            'algorithm': self.get_algorithm_name()
        }
        
        return compressed_data, stats
    
    def decompress(self, compressed_data: bytes) -> bytes:
        time.sleep(0.004)
        return compressed_data * 3  # 简单模拟
    
    def get_algorithm_name(self) -> str:
        return "GZIP"
    
    def get_compression_level(self) -> int:
        return 8  # GZIP默认级别
    
    def is_suitable_for_file_type(self, file_extension: str) -> bool:
        """GZIP特别适合文本文件"""
        return file_extension.lower() in ['.txt', '.log', '.json', '.xml', '.html', '.css', '.js']


class LZ4CompressionStrategy(CompressionStrategy):
    """LZ4压缩策略 - 高速压缩"""
    
    def compress(self, data: bytes) -> Tuple[bytes, Dict[str, Any]]:
        """模拟LZ4压缩"""
        start_time = time.time()
        time.sleep(0.003)  # LZ4速度很快
        
        # LZ4压缩率较低但速度很快
        compression_ratio = 0.5
        compressed_size = int(len(data) * compression_ratio)
        compressed_data = data[:compressed_size]
        
        compression_time = time.time() - start_time
        
        stats = {
            'original_size': len(data),
            'compressed_size': compressed_size,
            'compression_ratio': (len(data) - compressed_size) / len(data) * 100,
            'compression_time': compression_time,
            'algorithm': self.get_algorithm_name()
        }
        
        return compressed_data, stats
    
    def decompress(self, compressed_data: bytes) -> bytes:
        time.sleep(0.001)  # 解压也很快
        return compressed_data * 2
    
    def get_algorithm_name(self) -> str:
        return "LZ4 (高速)"
    
    def get_compression_level(self) -> int:
        return 3  # 低压缩级别，高速度
    
    def is_suitable_for_file_type(self, file_extension: str) -> bool:
        """LZ4适合需要快速压缩的场景"""
        return file_extension.lower() in ['.log', '.tmp', '.cache', '.db']


# ==================== 文件压缩管理器 ====================

class FileCompressionManager:
    """文件压缩管理器"""
    
    def __init__(self):
        self._strategies: Dict[str, CompressionStrategy] = {
            'zip': ZipCompressionStrategy(),
            'zip_fast': ZipCompressionStrategy(compression_level=3),
            'zip_best': ZipCompressionStrategy(compression_level=9),
            'gzip': GzipCompressionStrategy(),
            'lz4': LZ4CompressionStrategy()
        }
        self._compression_history: List[Dict[str, Any]] = []
    
    def compress_file(self, file_path: str, strategy_name: str = None) -> Dict[str, Any]:
        """压缩文件"""
        if not os.path.exists(file_path):
            return {'success': False, 'error': '文件不存在'}
        
        # 自动选择策略
        if strategy_name is None:
            strategy_name = self._auto_select_strategy(file_path)
        
        if strategy_name not in self._strategies:
            return {'success': False, 'error': f'不支持的压缩策略: {strategy_name}'}
        
        strategy = self._strategies[strategy_name]
        
        try:
            # 读取文件（模拟）
            file_size = random.randint(1024, 1024*1024)  # 1KB-1MB
            file_data = b'x' * file_size  # 模拟文件数据
            
            print(f"📁 压缩文件: {file_path}")
            print(f"🔧 使用策略: {strategy.get_algorithm_name()}")
            print(f"📊 原始大小: {file_size:,} 字节")
            
            # 执行压缩
            compressed_data, stats = strategy.compress(file_data)
            
            # 记录历史
            history_record = {
                'file_path': file_path,
                'strategy': strategy_name,
                'timestamp': datetime.now(),
                **stats
            }
            self._compression_history.append(history_record)
            
            print(f"✅ 压缩完成:")
            print(f"   压缩后大小: {stats['compressed_size']:,} 字节")
            print(f"   压缩率: {stats['compression_ratio']:.1f}%")
            print(f"   压缩时间: {stats['compression_time']:.3f} 秒")
            
            return {
                'success': True,
                'compressed_data': compressed_data,
                'stats': stats
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _auto_select_strategy(self, file_path: str) -> str:
        """自动选择压缩策略"""
        file_extension = os.path.splitext(file_path)[1]
        file_size = random.randint(1024, 1024*1024)  # 模拟文件大小
        
        # 根据文件类型和大小选择策略
        if file_size > 100 * 1024 * 1024:  # 大于100MB
            return 'lz4'  # 大文件优先考虑速度
        elif file_extension.lower() in ['.txt', '.log', '.json']:
            return 'gzip'  # 文本文件用GZIP
        elif file_extension.lower() in ['.tmp', '.cache']:
            return 'lz4'  # 临时文件用高速压缩
        else:
            return 'zip'  # 默认使用ZIP
    
    def get_compression_statistics(self) -> Dict[str, Any]:
        """获取压缩统计信息"""
        if not self._compression_history:
            return {}
        
        total_files = len(self._compression_history)
        total_original_size = sum(h['original_size'] for h in self._compression_history)
        total_compressed_size = sum(h['compressed_size'] for h in self._compression_history)
        total_time = sum(h['compression_time'] for h in self._compression_history)
        
        # 按策略统计
        strategy_stats = {}
        for record in self._compression_history:
            strategy = record['strategy']
            if strategy not in strategy_stats:
                strategy_stats[strategy] = {
                    'count': 0,
                    'total_ratio': 0,
                    'total_time': 0
                }
            strategy_stats[strategy]['count'] += 1
            strategy_stats[strategy]['total_ratio'] += record['compression_ratio']
            strategy_stats[strategy]['total_time'] += record['compression_time']
        
        # 计算平均值
        for strategy, stats in strategy_stats.items():
            stats['avg_ratio'] = stats['total_ratio'] / stats['count']
            stats['avg_time'] = stats['total_time'] / stats['count']
        
        return {
            'total_files': total_files,
            'total_original_size': total_original_size,
            'total_compressed_size': total_compressed_size,
            'overall_compression_ratio': (total_original_size - total_compressed_size) / total_original_size * 100,
            'total_time': total_time,
            'average_time': total_time / total_files,
            'strategy_statistics': strategy_stats
        }


# ==================== 缓存策略系统 ====================

class CacheStrategy(ABC):
    """缓存策略抽象类"""
    
    @abstractmethod
    def should_cache(self, key: str, data: Any, metadata: Dict[str, Any]) -> bool:
        """判断是否应该缓存"""
        pass
    
    @abstractmethod
    def get_ttl(self, key: str, data: Any, metadata: Dict[str, Any]) -> int:
        """获取缓存过期时间（秒）"""
        pass
    
    @abstractmethod
    def get_priority(self, key: str, data: Any, metadata: Dict[str, Any]) -> int:
        """获取缓存优先级 (1-10, 10最高)"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """获取策略名称"""
        pass


class LRUCacheStrategy(CacheStrategy):
    """LRU缓存策略"""
    
    def should_cache(self, key: str, data: Any, metadata: Dict[str, Any]) -> bool:
        """总是缓存，由LRU算法决定淘汰"""
        return True
    
    def get_ttl(self, key: str, data: Any, metadata: Dict[str, Any]) -> int:
        """根据数据大小设置TTL"""
        data_size = metadata.get('size', 0)
        if data_size > 1024 * 1024:  # 大于1MB
            return 300  # 5分钟
        elif data_size > 1024:  # 大于1KB
            return 1800  # 30分钟
        else:
            return 3600  # 1小时
    
    def get_priority(self, key: str, data: Any, metadata: Dict[str, Any]) -> int:
        """根据访问频率设置优先级"""
        access_count = metadata.get('access_count', 0)
        if access_count > 100:
            return 9
        elif access_count > 10:
            return 6
        else:
            return 3
    
    def get_strategy_name(self) -> str:
        return "LRU缓存策略"


class TTLCacheStrategy(CacheStrategy):
    """TTL缓存策略"""
    
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
    
    def should_cache(self, key: str, data: Any, metadata: Dict[str, Any]) -> bool:
        """根据数据类型决定是否缓存"""
        data_type = metadata.get('type', '')
        # 不缓存敏感数据
        return data_type not in ['password', 'token', 'secret']
    
    def get_ttl(self, key: str, data: Any, metadata: Dict[str, Any]) -> int:
        """根据数据类型设置不同的TTL"""
        data_type = metadata.get('type', '')
        
        ttl_mapping = {
            'user_profile': 1800,    # 30分钟
            'product_info': 3600,    # 1小时
            'static_content': 86400, # 24小时
            'api_response': 300,     # 5分钟
            'search_result': 600     # 10分钟
        }
        
        return ttl_mapping.get(data_type, self.default_ttl)
    
    def get_priority(self, key: str, data: Any, metadata: Dict[str, Any]) -> int:
        """根据数据重要性设置优先级"""
        importance = metadata.get('importance', 'normal')
        
        priority_mapping = {
            'critical': 10,
            'high': 8,
            'normal': 5,
            'low': 2
        }
        
        return priority_mapping.get(importance, 5)
    
    def get_strategy_name(self) -> str:
        return f"TTL缓存策略 (默认{self.default_ttl}秒)"


class AdaptiveCacheStrategy(CacheStrategy):
    """自适应缓存策略"""
    
    def __init__(self):
        self._access_patterns: Dict[str, List[datetime]] = {}
    
    def should_cache(self, key: str, data: Any, metadata: Dict[str, Any]) -> bool:
        """根据访问模式决定是否缓存"""
        # 记录访问时间
        if key not in self._access_patterns:
            self._access_patterns[key] = []
        
        self._access_patterns[key].append(datetime.now())
        
        # 保留最近1小时的访问记录
        cutoff_time = datetime.now() - timedelta(hours=1)
        self._access_patterns[key] = [
            t for t in self._access_patterns[key] if t > cutoff_time
        ]
        
        # 如果1小时内访问超过3次，则缓存
        return len(self._access_patterns[key]) >= 3
    
    def get_ttl(self, key: str, data: Any, metadata: Dict[str, Any]) -> int:
        """根据访问频率动态调整TTL"""
        access_count = len(self._access_patterns.get(key, []))
        
        if access_count > 20:
            return 7200  # 2小时
        elif access_count > 10:
            return 3600  # 1小时
        elif access_count > 5:
            return 1800  # 30分钟
        else:
            return 600   # 10分钟
    
    def get_priority(self, key: str, data: Any, metadata: Dict[str, Any]) -> int:
        """根据访问频率设置优先级"""
        access_count = len(self._access_patterns.get(key, []))
        return min(10, max(1, access_count // 2))
    
    def get_strategy_name(self) -> str:
        return "自适应缓存策略"


# ==================== 缓存管理器 ====================

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, strategy: CacheStrategy):
        self._strategy = strategy
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_requests': 0
        }
    
    def set_strategy(self, strategy: CacheStrategy) -> None:
        """设置缓存策略"""
        self._strategy = strategy
        print(f"🔄 切换缓存策略: {strategy.get_strategy_name()}")
    
    def get(self, key: str) -> Tuple[Any, bool]:
        """获取缓存数据"""
        self._cache_stats['total_requests'] += 1
        
        if key in self._cache:
            cache_entry = self._cache[key]
            
            # 检查是否过期
            if datetime.now() < cache_entry['expires_at']:
                self._cache_stats['hits'] += 1
                cache_entry['access_count'] += 1
                cache_entry['last_accessed'] = datetime.now()
                return cache_entry['data'], True
            else:
                # 过期，删除
                del self._cache[key]
        
        self._cache_stats['misses'] += 1
        return None, False
    
    def set(self, key: str, data: Any, metadata: Dict[str, Any] = None) -> bool:
        """设置缓存数据"""
        if metadata is None:
            metadata = {}
        
        # 添加数据大小信息
        if 'size' not in metadata:
            metadata['size'] = len(str(data))
        
        # 检查是否应该缓存
        if not self._strategy.should_cache(key, data, metadata):
            return False
        
        # 获取TTL和优先级
        ttl = self._strategy.get_ttl(key, data, metadata)
        priority = self._strategy.get_priority(key, data, metadata)
        
        # 创建缓存条目
        cache_entry = {
            'data': data,
            'metadata': metadata,
            'priority': priority,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=ttl),
            'last_accessed': datetime.now(),
            'access_count': 1,
            'ttl': ttl
        }
        
        self._cache[key] = cache_entry
        
        # 检查缓存大小限制（简单实现）
        if len(self._cache) > 1000:  # 最大1000个条目
            self._evict_entries()
        
        return True
    
    def _evict_entries(self) -> None:
        """淘汰缓存条目"""
        # 按优先级和最后访问时间排序
        sorted_entries = sorted(
            self._cache.items(),
            key=lambda x: (x[1]['priority'], x[1]['last_accessed']),
            reverse=False
        )
        
        # 删除优先级最低的10%条目
        evict_count = len(self._cache) // 10
        for i in range(evict_count):
            key, _ = sorted_entries[i]
            del self._cache[key]
            self._cache_stats['evictions'] += 1
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        total_requests = self._cache_stats['total_requests']
        hit_rate = (self._cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'strategy': self._strategy.get_strategy_name(),
            'cache_size': len(self._cache),
            'hit_rate': hit_rate,
            **self._cache_stats
        }


# ==================== 演示函数 ====================

def demo_file_compression():
    """文件压缩演示"""
    print("=" * 60)
    print("📁 文件压缩策略系统演示")
    print("=" * 60)
    
    manager = FileCompressionManager()
    
    # 模拟压缩不同类型的文件
    test_files = [
        "document.txt",
        "data.json",
        "image.jpg",
        "archive.zip",
        "log.log",
        "cache.tmp"
    ]
    
    for file_path in test_files:
        print(f"\n" + "=" * 40)
        result = manager.compress_file(file_path)
        
        if not result['success']:
            print(f"❌ 压缩失败: {result['error']}")
    
    # 显示统计信息
    print(f"\n" + "=" * 40)
    print("📊 压缩统计信息:")
    stats = manager.get_compression_statistics()
    
    if stats:
        print(f"   总文件数: {stats['total_files']}")
        print(f"   总压缩率: {stats['overall_compression_ratio']:.1f}%")
        print(f"   平均压缩时间: {stats['average_time']:.3f} 秒")
        
        print(f"\n   各策略统计:")
        for strategy, strategy_stats in stats['strategy_statistics'].items():
            print(f"     {strategy}: {strategy_stats['count']} 个文件, "
                  f"平均压缩率 {strategy_stats['avg_ratio']:.1f}%")


def demo_cache_strategies():
    """缓存策略演示"""
    print("\n" + "=" * 60)
    print("🗄️ 缓存策略系统演示")
    print("=" * 60)
    
    # 测试不同缓存策略
    strategies = [
        LRUCacheStrategy(),
        TTLCacheStrategy(default_ttl=1800),
        AdaptiveCacheStrategy()
    ]
    
    for strategy in strategies:
        print(f"\n测试 {strategy.get_strategy_name()}:")
        manager = CacheManager(strategy)
        
        # 模拟缓存操作
        test_data = [
            ('user:123', {'name': 'Alice', 'age': 25}, {'type': 'user_profile', 'importance': 'high'}),
            ('product:456', {'name': 'iPhone', 'price': 999}, {'type': 'product_info', 'importance': 'normal'}),
            ('search:python', ['result1', 'result2'], {'type': 'search_result', 'importance': 'low'}),
            ('api:weather', {'temp': 25, 'humidity': 60}, {'type': 'api_response', 'importance': 'normal'}),
        ]
        
        # 设置缓存
        for key, data, metadata in test_data:
            success = manager.set(key, data, metadata)
            print(f"   设置缓存 {key}: {'成功' if success else '失败'}")
        
        # 获取缓存
        for key, _, _ in test_data:
            data, hit = manager.get(key)
            print(f"   获取缓存 {key}: {'命中' if hit else '未命中'}")
        
        # 显示统计
        stats = manager.get_cache_stats()
        print(f"   缓存统计: 命中率 {stats['hit_rate']:.1f}%, 大小 {stats['cache_size']}")


if __name__ == "__main__":
    # 运行文件压缩演示
    demo_file_compression()
    
    # 运行缓存策略演示
    demo_cache_strategies()
    
    print("\n" + "=" * 60)
    print("✅ 实际项目应用演示完成")
    print("💡 学习要点:")
    print("   - 策略模式在文件处理系统中的应用")
    print("   - 根据文件特征自动选择最优策略")
    print("   - 缓存策略的多样化实现")
    print("   - 策略模式提高了系统的可扩展性")
    print("=" * 60)
