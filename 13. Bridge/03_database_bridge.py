"""
桥接模式数据库应用 - 统一数据库访问系统

这个示例展示了桥接模式在数据库访问中的应用，演示如何将
数据访问层（抽象）与具体数据库驱动（实现）分离。

作者: Bridge Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json
import time
from datetime import datetime


# ==================== 实现层接口 ====================

class DatabaseDriver(ABC):
    """数据库驱动接口 - 实现层"""
    
    @abstractmethod
    def connect(self, connection_string: str) -> bool:
        """连接数据库"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """断开连接"""
        pass
    
    @abstractmethod
    def execute_query(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """执行查询"""
        pass
    
    @abstractmethod
    def execute_command(self, sql: str, params: List[Any] = None) -> int:
        """执行命令（INSERT, UPDATE, DELETE）"""
        pass
    
    @abstractmethod
    def begin_transaction(self) -> None:
        """开始事务"""
        pass
    
    @abstractmethod
    def commit_transaction(self) -> None:
        """提交事务"""
        pass
    
    @abstractmethod
    def rollback_transaction(self) -> None:
        """回滚事务"""
        pass
    
    @abstractmethod
    def get_driver_info(self) -> str:
        """获取驱动信息"""
        pass


# ==================== 具体实现 ====================

class MySQLDriver(DatabaseDriver):
    """MySQL数据库驱动 - 具体实现A"""
    
    def __init__(self):
        self.connected = False
        self.connection_string = ""
        self.query_count = 0
        self.in_transaction = False
    
    def connect(self, connection_string: str) -> bool:
        """连接MySQL数据库"""
        print(f"🐬 连接MySQL数据库: {connection_string}")
        self.connection_string = connection_string
        self.connected = True
        print(f"   ✅ MySQL连接成功")
        return True
    
    def disconnect(self) -> None:
        """断开MySQL连接"""
        if self.connected:
            print(f"🐬 断开MySQL连接")
            self.connected = False
    
    def execute_query(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """执行MySQL查询"""
        if not self.connected:
            raise Exception("数据库未连接")
        
        print(f"🐬 MySQL执行查询: {sql}")
        if params:
            print(f"   参数: {params}")
        
        # 模拟查询延迟
        time.sleep(0.1)
        self.query_count += 1
        
        # 模拟返回结果
        if "users" in sql.lower():
            return [
                {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
                {"id": 2, "name": "李四", "email": "lisi@example.com"}
            ]
        return []
    
    def execute_command(self, sql: str, params: List[Any] = None) -> int:
        """执行MySQL命令"""
        if not self.connected:
            raise Exception("数据库未连接")
        
        print(f"🐬 MySQL执行命令: {sql}")
        if params:
            print(f"   参数: {params}")
        
        time.sleep(0.05)
        self.query_count += 1
        
        # 模拟影响行数
        return 1
    
    def begin_transaction(self) -> None:
        """开始MySQL事务"""
        print(f"🐬 MySQL开始事务")
        self.in_transaction = True
    
    def commit_transaction(self) -> None:
        """提交MySQL事务"""
        print(f"🐬 MySQL提交事务")
        self.in_transaction = False
    
    def rollback_transaction(self) -> None:
        """回滚MySQL事务"""
        print(f"🐬 MySQL回滚事务")
        self.in_transaction = False
    
    def get_driver_info(self) -> str:
        return f"MySQL驱动 (连接: {self.connected}, 查询次数: {self.query_count})"


class PostgreSQLDriver(DatabaseDriver):
    """PostgreSQL数据库驱动 - 具体实现B"""
    
    def __init__(self):
        self.connected = False
        self.connection_string = ""
        self.query_count = 0
        self.in_transaction = False
    
    def connect(self, connection_string: str) -> bool:
        """连接PostgreSQL数据库"""
        print(f"🐘 连接PostgreSQL数据库: {connection_string}")
        self.connection_string = connection_string
        self.connected = True
        print(f"   ✅ PostgreSQL连接成功")
        return True
    
    def disconnect(self) -> None:
        """断开PostgreSQL连接"""
        if self.connected:
            print(f"🐘 断开PostgreSQL连接")
            self.connected = False
    
    def execute_query(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """执行PostgreSQL查询"""
        if not self.connected:
            raise Exception("数据库未连接")
        
        print(f"🐘 PostgreSQL执行查询: {sql}")
        if params:
            print(f"   参数: {params}")
        
        time.sleep(0.08)
        self.query_count += 1
        
        # 模拟返回结果
        if "products" in sql.lower():
            return [
                {"id": 1, "name": "笔记本电脑", "price": 5999.00},
                {"id": 2, "name": "智能手机", "price": 2999.00}
            ]
        return []
    
    def execute_command(self, sql: str, params: List[Any] = None) -> int:
        """执行PostgreSQL命令"""
        if not self.connected:
            raise Exception("数据库未连接")
        
        print(f"🐘 PostgreSQL执行命令: {sql}")
        if params:
            print(f"   参数: {params}")
        
        time.sleep(0.04)
        self.query_count += 1
        return 1
    
    def begin_transaction(self) -> None:
        """开始PostgreSQL事务"""
        print(f"🐘 PostgreSQL开始事务")
        self.in_transaction = True
    
    def commit_transaction(self) -> None:
        """提交PostgreSQL事务"""
        print(f"🐘 PostgreSQL提交事务")
        self.in_transaction = False
    
    def rollback_transaction(self) -> None:
        """回滚PostgreSQL事务"""
        print(f"🐘 PostgreSQL回滚事务")
        self.in_transaction = False
    
    def get_driver_info(self) -> str:
        return f"PostgreSQL驱动 (连接: {self.connected}, 查询次数: {self.query_count})"


class MongoDBDriver(DatabaseDriver):
    """MongoDB数据库驱动 - 具体实现C"""
    
    def __init__(self):
        self.connected = False
        self.connection_string = ""
        self.query_count = 0
        self.in_transaction = False
    
    def connect(self, connection_string: str) -> bool:
        """连接MongoDB数据库"""
        print(f"🍃 连接MongoDB数据库: {connection_string}")
        self.connection_string = connection_string
        self.connected = True
        print(f"   ✅ MongoDB连接成功")
        return True
    
    def disconnect(self) -> None:
        """断开MongoDB连接"""
        if self.connected:
            print(f"🍃 断开MongoDB连接")
            self.connected = False
    
    def execute_query(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """执行MongoDB查询（转换为MongoDB查询）"""
        if not self.connected:
            raise Exception("数据库未连接")
        
        # 将SQL转换为MongoDB查询（简化示例）
        mongo_query = self._sql_to_mongo(sql)
        print(f"🍃 MongoDB执行查询: {mongo_query}")
        if params:
            print(f"   参数: {params}")
        
        time.sleep(0.06)
        self.query_count += 1
        
        # 模拟返回结果
        if "orders" in sql.lower():
            return [
                {"_id": "507f1f77bcf86cd799439011", "user_id": 1, "total": 299.99},
                {"_id": "507f1f77bcf86cd799439012", "user_id": 2, "total": 199.99}
            ]
        return []
    
    def execute_command(self, sql: str, params: List[Any] = None) -> int:
        """执行MongoDB命令"""
        if not self.connected:
            raise Exception("数据库未连接")
        
        mongo_command = self._sql_to_mongo(sql)
        print(f"🍃 MongoDB执行命令: {mongo_command}")
        if params:
            print(f"   参数: {params}")
        
        time.sleep(0.03)
        self.query_count += 1
        return 1
    
    def begin_transaction(self) -> None:
        """开始MongoDB事务"""
        print(f"🍃 MongoDB开始事务")
        self.in_transaction = True
    
    def commit_transaction(self) -> None:
        """提交MongoDB事务"""
        print(f"🍃 MongoDB提交事务")
        self.in_transaction = False
    
    def rollback_transaction(self) -> None:
        """回滚MongoDB事务"""
        print(f"🍃 MongoDB回滚事务")
        self.in_transaction = False
    
    def _sql_to_mongo(self, sql: str) -> str:
        """简化的SQL到MongoDB查询转换"""
        if "SELECT" in sql.upper():
            return f"db.collection.find({{}})"
        elif "INSERT" in sql.upper():
            return f"db.collection.insertOne({{}})"
        elif "UPDATE" in sql.upper():
            return f"db.collection.updateOne({{}}, {{}})"
        elif "DELETE" in sql.upper():
            return f"db.collection.deleteOne({{}})"
        return sql
    
    def get_driver_info(self) -> str:
        return f"MongoDB驱动 (连接: {self.connected}, 查询次数: {self.query_count})"


# ==================== 抽象层 ====================

class Database:
    """数据库抽象类 - 抽象层"""
    
    def __init__(self, driver: DatabaseDriver):
        self.driver = driver
        self.connected = False
    
    def connect(self, connection_string: str) -> bool:
        """连接数据库"""
        self.connected = self.driver.connect(connection_string)
        return self.connected
    
    def disconnect(self) -> None:
        """断开连接"""
        self.driver.disconnect()
        self.connected = False
    
    def query(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """执行查询"""
        return self.driver.execute_query(sql, params)
    
    def execute(self, sql: str, params: List[Any] = None) -> int:
        """执行命令"""
        return self.driver.execute_command(sql, params)
    
    def set_driver(self, driver: DatabaseDriver) -> None:
        """切换数据库驱动"""
        if self.connected:
            self.disconnect()
        self.driver = driver
        print(f"🔄 数据库驱动已切换为: {driver.get_driver_info()}")
    
    def get_info(self) -> str:
        """获取数据库信息"""
        return self.driver.get_driver_info()


# ==================== 扩展抽象层 ====================

class TransactionalDatabase(Database):
    """事务数据库 - 扩展抽象层"""
    
    def __init__(self, driver: DatabaseDriver):
        super().__init__(driver)
        self.auto_commit = True
    
    def begin_transaction(self) -> None:
        """开始事务"""
        self.driver.begin_transaction()
        self.auto_commit = False
    
    def commit(self) -> None:
        """提交事务"""
        self.driver.commit_transaction()
        self.auto_commit = True
    
    def rollback(self) -> None:
        """回滚事务"""
        self.driver.rollback_transaction()
        self.auto_commit = True
    
    def execute_transaction(self, operations: List[tuple]) -> bool:
        """执行事务操作"""
        try:
            self.begin_transaction()
            print(f"📦 开始执行事务 (包含 {len(operations)} 个操作)")
            
            for i, (sql, params) in enumerate(operations, 1):
                print(f"   操作 {i}: {sql}")
                self.execute(sql, params)
            
            self.commit()
            print(f"✅ 事务执行成功")
            return True
            
        except Exception as e:
            print(f"❌ 事务执行失败: {e}")
            self.rollback()
            return False


class CachedDatabase(Database):
    """缓存数据库 - 扩展抽象层"""
    
    def __init__(self, driver: DatabaseDriver):
        super().__init__(driver)
        self.cache: Dict[str, List[Dict[str, Any]]] = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def query(self, sql: str, params: List[Any] = None) -> List[Dict[str, Any]]:
        """带缓存的查询"""
        cache_key = self._get_cache_key(sql, params)
        
        if cache_key in self.cache:
            print(f"💾 缓存命中: {sql}")
            self.cache_hits += 1
            return self.cache[cache_key]
        
        print(f"🔍 缓存未命中，执行查询: {sql}")
        self.cache_misses += 1
        result = self.driver.execute_query(sql, params)
        
        # 缓存结果
        self.cache[cache_key] = result
        return result
    
    def _get_cache_key(self, sql: str, params: List[Any] = None) -> str:
        """生成缓存键"""
        return f"{sql}:{json.dumps(params) if params else 'None'}"
    
    def clear_cache(self) -> None:
        """清空缓存"""
        self.cache.clear()
        print(f"🗑️  缓存已清空")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """获取缓存统计"""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "hit_rate": hit_rate
        }


def demo_database_bridge():
    """数据库桥接模式演示"""
    print("=" * 60)
    print("🗄️  统一数据库访问系统 - 桥接模式演示")
    print("=" * 60)
    
    # 创建不同的数据库驱动
    mysql_driver = MySQLDriver()
    postgresql_driver = PostgreSQLDriver()
    mongodb_driver = MongoDBDriver()
    
    # 创建数据库对象
    db = Database(mysql_driver)
    
    print("\n🔹 使用MySQL数据库:")
    db.connect("mysql://localhost:3306/testdb")
    users = db.query("SELECT * FROM users")
    print(f"   查询结果: {users}")
    
    print(f"\n🔄 切换到PostgreSQL:")
    db.set_driver(postgresql_driver)
    db.connect("postgresql://localhost:5432/testdb")
    products = db.query("SELECT * FROM products")
    print(f"   查询结果: {products}")
    
    print(f"\n🔄 切换到MongoDB:")
    db.set_driver(mongodb_driver)
    db.connect("mongodb://localhost:27017/testdb")
    orders = db.query("SELECT * FROM orders")
    print(f"   查询结果: {orders}")


def demo_transactional_database():
    """事务数据库演示"""
    print("\n" + "=" * 60)
    print("📦 事务数据库演示")
    print("=" * 60)
    
    # 创建事务数据库
    mysql_driver = MySQLDriver()
    trans_db = TransactionalDatabase(mysql_driver)
    trans_db.connect("mysql://localhost:3306/testdb")
    
    # 执行事务操作
    operations = [
        ("INSERT INTO users (name, email) VALUES (?, ?)", ["王五", "wangwu@example.com"]),
        ("UPDATE users SET email = ? WHERE name = ?", ["newemail@example.com", "张三"]),
        ("DELETE FROM users WHERE name = ?", ["临时用户"])
    ]
    
    trans_db.execute_transaction(operations)


def demo_cached_database():
    """缓存数据库演示"""
    print("\n" + "=" * 60)
    print("💾 缓存数据库演示")
    print("=" * 60)
    
    # 创建缓存数据库
    postgresql_driver = PostgreSQLDriver()
    cached_db = CachedDatabase(postgresql_driver)
    cached_db.connect("postgresql://localhost:5432/testdb")
    
    # 执行相同查询多次
    sql = "SELECT * FROM products WHERE price > ?"
    params = [1000]
    
    print(f"第一次查询:")
    cached_db.query(sql, params)
    
    print(f"\n第二次查询 (应该命中缓存):")
    cached_db.query(sql, params)
    
    print(f"\n第三次查询 (应该命中缓存):")
    cached_db.query(sql, params)
    
    # 显示缓存统计
    stats = cached_db.get_cache_stats()
    print(f"\n📊 缓存统计: 命中 {stats['hits']} 次, 未命中 {stats['misses']} 次, 命中率 {stats['hit_rate']:.1f}%")


if __name__ == "__main__":
    demo_database_bridge()
    demo_transactional_database()
    demo_cached_database()
