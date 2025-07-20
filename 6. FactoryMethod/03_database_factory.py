"""
03_database_factory.py - 数据库连接工厂方法模式

数据库连接示例
这个示例展示了工厂方法模式在数据库访问层的应用。
我们有不同类型的数据库（MySQL、PostgreSQL、SQLite），每种数据库都有对应的连接工厂。
通过配置可以动态选择数据库类型，体现了工厂方法模式在基础设施层的价值。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import time
import json


# ==================== 抽象产品 ====================
class DatabaseConnection(ABC):
    """数据库连接抽象基类"""

    def __init__(self, host: str, port: int, database: str, username: str):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.connected = False
        self.connection_time: Optional[str] = None

    @abstractmethod
    def connect(self) -> bool:
        """连接数据库"""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """断开连接"""
        pass

    @abstractmethod
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """执行查询"""
        pass

    @abstractmethod
    def execute_update(self, sql: str) -> int:
        """执行更新操作"""
        pass

    @abstractmethod
    def get_connection_info(self) -> Dict[str, Any]:
        """获取连接信息"""
        pass

    def is_connected(self) -> bool:
        """检查连接状态"""
        return self.connected


# ==================== 具体产品 ====================
class MySQLConnection(DatabaseConnection):
    """MySQL数据库连接"""

    def connect(self) -> bool:
        """连接MySQL数据库"""
        print(f"🔗 正在连接MySQL数据库...")
        print(f"   主机: {self.host}:{self.port}")
        print(f"   数据库: {self.database}")
        print(f"   用户: {self.username}")

        # 模拟连接过程
        time.sleep(0.3)

        self.connected = True
        self.connection_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"   ✓ MySQL连接成功")
        return True

    def disconnect(self) -> bool:
        """断开MySQL连接"""
        if self.connected:
            print(f"🔌 断开MySQL连接")
            self.connected = False
            return True
        return False

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """执行MySQL查询"""
        if not self.connected:
            raise Exception("数据库未连接")

        print(f"📊 执行MySQL查询: {sql}")
        # 模拟查询结果
        if "users" in sql.lower():
            return [
                {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
                {"id": 2, "name": "李四", "email": "lisi@example.com"}
            ]
        return []

    def execute_update(self, sql: str) -> int:
        """执行MySQL更新操作"""
        if not self.connected:
            raise Exception("数据库未连接")

        print(f"✏️  执行MySQL更新: {sql}")
        # 模拟影响行数
        return 1

    def get_connection_info(self) -> Dict[str, Any]:
        return {
            "type": "MySQL",
            "version": "8.0.25",
            "driver": "mysql-connector-python",
            "charset": "utf8mb4",
            "engine": "InnoDB"
        }


class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL数据库连接"""

    def connect(self) -> bool:
        """连接PostgreSQL数据库"""
        print(f"🔗 正在连接PostgreSQL数据库...")
        print(f"   主机: {self.host}:{self.port}")
        print(f"   数据库: {self.database}")
        print(f"   用户: {self.username}")

        # 模拟连接过程
        time.sleep(0.4)

        self.connected = True
        self.connection_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"   ✓ PostgreSQL连接成功")
        return True

    def disconnect(self) -> bool:
        """断开PostgreSQL连接"""
        if self.connected:
            print(f"🔌 断开PostgreSQL连接")
            self.connected = False
            return True
        return False

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """执行PostgreSQL查询"""
        if not self.connected:
            raise Exception("数据库未连接")

        print(f"📊 执行PostgreSQL查询: {sql}")
        # 模拟查询结果
        if "products" in sql.lower():
            return [
                {"id": 1, "name": "笔记本电脑", "price": 5999.00},
                {"id": 2, "name": "智能手机", "price": 2999.00}
            ]
        return []

    def execute_update(self, sql: str) -> int:
        """执行PostgreSQL更新操作"""
        if not self.connected:
            raise Exception("数据库未连接")

        print(f"✏️  执行PostgreSQL更新: {sql}")
        # 模拟影响行数
        return 1

    def get_connection_info(self) -> Dict[str, Any]:
        return {
            "type": "PostgreSQL",
            "version": "13.4",
            "driver": "psycopg2",
            "charset": "UTF8",
            "collation": "zh_CN.UTF-8"
        }


class SQLiteConnection(DatabaseConnection):
    """SQLite数据库连接"""

    def connect(self) -> bool:
        """连接SQLite数据库"""
        print(f"🔗 正在连接SQLite数据库...")
        print(f"   文件路径: {self.database}")

        # 模拟连接过程
        time.sleep(0.1)

        self.connected = True
        self.connection_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"   ✓ SQLite连接成功")
        return True

    def disconnect(self) -> bool:
        """断开SQLite连接"""
        if self.connected:
            print(f"🔌 断开SQLite连接")
            self.connected = False
            return True
        return False

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """执行SQLite查询"""
        if not self.connected:
            raise Exception("数据库未连接")

        print(f"📊 执行SQLite查询: {sql}")
        # 模拟查询结果
        if "orders" in sql.lower():
            return [
                {"id": 1, "user_id": 1, "total": 299.00, "status": "已完成"},
                {"id": 2, "user_id": 2, "total": 599.00, "status": "处理中"}
            ]
        return []

    def execute_update(self, sql: str) -> int:
        """执行SQLite更新操作"""
        if not self.connected:
            raise Exception("数据库未连接")

        print(f"✏️  执行SQLite更新: {sql}")
        # 模拟影响行数
        return 1

    def get_connection_info(self) -> Dict[str, Any]:
        return {
            "type": "SQLite",
            "version": "3.36.0",
            "driver": "sqlite3",
            "file_based": True,
            "threading": "serialized"
        }


# ==================== 抽象创建者 ====================
class DatabaseFactory(ABC):
    """数据库工厂抽象基类"""

    @abstractmethod
    def create_connection(self, host: str, port: int, database: str,
                         username: str, password: str) -> DatabaseConnection:
        """工厂方法：创建数据库连接"""
        pass

    def get_connection(self, config: Dict[str, Any]) -> DatabaseConnection:
        """获取数据库连接（业务逻辑）"""
        print(f"🏭 使用 {self.__class__.__name__} 创建数据库连接...")

        # 1. 创建连接对象（使用工厂方法）
        connection = self.create_connection(
            host=config.get("host", "localhost"),
            port=config.get("port", 3306),
            database=config["database"],
            username=config["username"],
            password=config.get("password", "")
        )

        # 2. 建立连接
        if connection.connect():
            # 3. 获取连接信息
            info = connection.get_connection_info()
            print(f"📋 数据库类型: {info['type']}")
            print(f"📋 数据库版本: {info['version']}")
            print(f"📋 驱动程序: {info['driver']}")

            return connection
        else:
            raise Exception("数据库连接失败")


# ==================== 具体创建者 ====================
class MySQLFactory(DatabaseFactory):
    """MySQL工厂"""

    def create_connection(self, host: str, port: int, database: str,
                         username: str, password: str) -> DatabaseConnection:
        return MySQLConnection(host, port or 3306, database, username)


class PostgreSQLFactory(DatabaseFactory):
    """PostgreSQL工厂"""

    def create_connection(self, host: str, port: int, database: str,
                         username: str, password: str) -> DatabaseConnection:
        return PostgreSQLConnection(host, port or 5432, database, username)


class SQLiteFactory(DatabaseFactory):
    """SQLite工厂"""

    def create_connection(self, host: str, port: int, database: str,
                         username: str, password: str) -> DatabaseConnection:
        return SQLiteConnection("", 0, database, username or "")


# ==================== 数据库管理器 ====================
class DatabaseManager:
    """数据库管理器 - 演示配置驱动的数据库选择"""

    def __init__(self):
        self.factories = {
            "mysql": MySQLFactory(),
            "postgresql": PostgreSQLFactory(),
            "sqlite": SQLiteFactory()
        }
        self.connections: Dict[str, DatabaseConnection] = {}

    def get_connection(self, config: Dict[str, Any]) -> DatabaseConnection:
        """获取数据库连接"""
        db_type = config["type"].lower()
        connection_key = f"{db_type}_{config['database']}"

        # 检查是否已有连接
        if connection_key in self.connections:
            connection = self.connections[connection_key]
            if connection.is_connected():
                print(f"♻️  复用现有连接: {connection_key}")
                return connection

        # 创建新连接
        if db_type in self.factories:
            factory = self.factories[db_type]
            connection = factory.get_connection(config)
            self.connections[connection_key] = connection
            return connection
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")

    def execute_query(self, config: Dict[str, Any], sql: str) -> List[Dict[str, Any]]:
        """执行查询"""
        connection = self.get_connection(config)
        return connection.execute_query(sql)

    def execute_update(self, config: Dict[str, Any], sql: str) -> int:
        """执行更新"""
        connection = self.get_connection(config)
        return connection.execute_update(sql)

    def close_all_connections(self):
        """关闭所有连接"""
        print(f"\n🔒 关闭所有数据库连接...")
        for key, connection in self.connections.items():
            if connection.is_connected():
                connection.disconnect()
                print(f"   ✓ 已关闭: {key}")
        self.connections.clear()


# ==================== 演示函数 ====================
def demo_database_connections():
    """演示不同数据库连接"""
    print("=== 数据库连接工厂演示 ===\n")

    # 数据库配置
    configs = [
        {
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "database": "ecommerce",
            "username": "root",
            "password": "password"
        },
        {
            "type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "database": "analytics",
            "username": "postgres",
            "password": "password"
        },
        {
            "type": "sqlite",
            "database": "local.db",
            "username": "admin"
        }
    ]

    manager = DatabaseManager()

    for config in configs:
        print(f"\n{'='*50}")
        print(f"连接 {config['type'].upper()} 数据库")
        print('='*50)

        try:
            connection = manager.get_connection(config)

            # 执行示例查询
            if config['type'] == 'mysql':
                results = manager.execute_query(config, "SELECT * FROM users")
            elif config['type'] == 'postgresql':
                results = manager.execute_query(config, "SELECT * FROM products")
            else:  # sqlite
                results = manager.execute_query(config, "SELECT * FROM orders")

            print(f"📊 查询结果: {json.dumps(results, ensure_ascii=False, indent=2)}")

        except Exception as e:
            print(f"❌ 连接失败: {e}")

    # 关闭所有连接
    manager.close_all_connections()


def demo_orm_like_usage():
    """演示类似ORM的使用方式"""
    print("\n" + "="*60)
    print("类似ORM的使用方式演示")
    print("="*60)

    # 模拟不同环境的数据库配置
    environments = {
        "development": {
            "type": "sqlite",
            "database": "dev.db",
            "username": "dev"
        },
        "testing": {
            "type": "sqlite",
            "database": ":memory:",
            "username": "test"
        },
        "production": {
            "type": "postgresql",
            "host": "prod-db.example.com",
            "port": 5432,
            "database": "production",
            "username": "app_user",
            "password": "secure_password"
        }
    }

    manager = DatabaseManager()

    # 模拟在不同环境中使用
    current_env = "development"  # 可以通过环境变量设置

    print(f"🌍 当前环境: {current_env}")
    config = environments[current_env]

    try:
        # 执行一些数据库操作
        print(f"\n📝 执行数据库操作...")

        # 创建表（模拟）
        manager.execute_update(config, "CREATE TABLE IF NOT EXISTS users (id, name, email)")
        print("✓ 创建用户表")

        # 插入数据（模拟）
        manager.execute_update(config, "INSERT INTO users VALUES (1, '张三', 'zhangsan@example.com')")
        print("✓ 插入用户数据")

        # 查询数据
        results = manager.execute_query(config, "SELECT * FROM users")
        print(f"✓ 查询用户数据: {json.dumps(results, ensure_ascii=False)}")

    except Exception as e:
        print(f"❌ 操作失败: {e}")

    finally:
        manager.close_all_connections()


def main():
    """主函数"""
    demo_database_connections()
    demo_orm_like_usage()

    print("\n" + "="*60)
    print("工厂方法模式在数据库访问中的优势:")
    print("1. 数据库无关性：可以轻松切换不同的数据库")
    print("2. 配置驱动：通过配置文件动态选择数据库类型")
    print("3. 连接管理：统一的连接创建和管理接口")
    print("4. 易于测试：可以轻松创建测试用的数据库连接")
    print("5. 环境适配：不同环境可以使用不同的数据库")
    print("="*60)


if __name__ == "__main__":
    main()
