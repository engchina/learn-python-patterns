"""
02_database_factory.py - 数据库抽象工厂模式

数据库访问层示例
这个示例展示了如何使用抽象工厂模式来创建不同数据库的访问组件。
在企业应用中，经常需要支持多种数据库（如MySQL、PostgreSQL、MongoDB），
抽象工厂模式可以确保同一数据库的所有组件协同工作。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


# ==================== 抽象产品类 ====================
class Connection(ABC):
    """数据库连接抽象基类"""
    
    @abstractmethod
    def connect(self) -> bool:
        """连接数据库"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """断开连接"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """检查连接状态"""
        pass


class Query(ABC):
    """查询构建器抽象基类"""
    
    @abstractmethod
    def select(self, fields: List[str]) -> 'Query':
        """选择字段"""
        pass
    
    @abstractmethod
    def from_table(self, table: str) -> 'Query':
        """指定表名"""
        pass
    
    @abstractmethod
    def where(self, condition: str) -> 'Query':
        """添加WHERE条件"""
        pass
    
    @abstractmethod
    def execute(self) -> List[Dict[str, Any]]:
        """执行查询"""
        pass


class Transaction(ABC):
    """事务管理器抽象基类"""
    
    @abstractmethod
    def begin(self) -> bool:
        """开始事务"""
        pass
    
    @abstractmethod
    def commit(self) -> bool:
        """提交事务"""
        pass
    
    @abstractmethod
    def rollback(self) -> bool:
        """回滚事务"""
        pass


# ==================== MySQL产品族 ====================
class MySQLConnection(Connection):
    """MySQL连接"""
    
    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.connected = False
        self.connection_id = None
    
    def connect(self) -> bool:
        """连接MySQL数据库"""
        try:
            # 模拟连接过程
            self.connection_id = f"mysql_conn_{datetime.now().timestamp()}"
            self.connected = True
            print(f"MySQL连接成功: {self.host}:{self.port}/{self.database}")
            return True
        except Exception as e:
            print(f"MySQL连接失败: {e}")
            return False
    
    def disconnect(self) -> bool:
        """断开MySQL连接"""
        if self.connected:
            self.connected = False
            self.connection_id = None
            print("MySQL连接已断开")
            return True
        return False
    
    def is_connected(self) -> bool:
        """检查MySQL连接状态"""
        return self.connected


class MySQLQuery(Query):
    """MySQL查询构建器"""
    
    def __init__(self, connection: MySQLConnection):
        self.connection = connection
        self.query_parts = {
            "select": [],
            "from": "",
            "where": []
        }
    
    def select(self, fields: List[str]) -> 'MySQLQuery':
        """选择字段"""
        self.query_parts["select"] = fields
        return self
    
    def from_table(self, table: str) -> 'MySQLQuery':
        """指定表名"""
        self.query_parts["from"] = table
        return self
    
    def where(self, condition: str) -> 'MySQLQuery':
        """添加WHERE条件"""
        self.query_parts["where"].append(condition)
        return self
    
    def build_sql(self) -> str:
        """构建SQL语句"""
        fields = ", ".join(self.query_parts["select"]) if self.query_parts["select"] else "*"
        sql = f"SELECT {fields} FROM {self.query_parts['from']}"
        
        if self.query_parts["where"]:
            sql += " WHERE " + " AND ".join(self.query_parts["where"])
        
        return sql
    
    def execute(self) -> List[Dict[str, Any]]:
        """执行MySQL查询"""
        if not self.connection.is_connected():
            raise Exception("数据库未连接")
        
        sql = self.build_sql()
        print(f"执行MySQL查询: {sql}")
        
        # 模拟查询结果
        return [
            {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
            {"id": 2, "name": "李四", "email": "lisi@example.com"}
        ]


class MySQLTransaction(Transaction):
    """MySQL事务管理器"""
    
    def __init__(self, connection: MySQLConnection):
        self.connection = connection
        self.in_transaction = False
    
    def begin(self) -> bool:
        """开始MySQL事务"""
        if not self.connection.is_connected():
            return False
        
        self.in_transaction = True
        print("MySQL事务已开始")
        return True
    
    def commit(self) -> bool:
        """提交MySQL事务"""
        if self.in_transaction:
            self.in_transaction = False
            print("MySQL事务已提交")
            return True
        return False
    
    def rollback(self) -> bool:
        """回滚MySQL事务"""
        if self.in_transaction:
            self.in_transaction = False
            print("MySQL事务已回滚")
            return True
        return False


# ==================== PostgreSQL产品族 ====================
class PostgreSQLConnection(Connection):
    """PostgreSQL连接"""
    
    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.connected = False
        self.connection_id = None
    
    def connect(self) -> bool:
        """连接PostgreSQL数据库"""
        try:
            self.connection_id = f"pg_conn_{datetime.now().timestamp()}"
            self.connected = True
            print(f"PostgreSQL连接成功: {self.host}:{self.port}/{self.database}")
            return True
        except Exception as e:
            print(f"PostgreSQL连接失败: {e}")
            return False
    
    def disconnect(self) -> bool:
        """断开PostgreSQL连接"""
        if self.connected:
            self.connected = False
            self.connection_id = None
            print("PostgreSQL连接已断开")
            return True
        return False
    
    def is_connected(self) -> bool:
        """检查PostgreSQL连接状态"""
        return self.connected


class PostgreSQLQuery(Query):
    """PostgreSQL查询构建器"""
    
    def __init__(self, connection: PostgreSQLConnection):
        self.connection = connection
        self.query_parts = {
            "select": [],
            "from": "",
            "where": []
        }
    
    def select(self, fields: List[str]) -> 'PostgreSQLQuery':
        """选择字段"""
        self.query_parts["select"] = fields
        return self
    
    def from_table(self, table: str) -> 'PostgreSQLQuery':
        """指定表名"""
        self.query_parts["from"] = table
        return self
    
    def where(self, condition: str) -> 'PostgreSQLQuery':
        """添加WHERE条件"""
        self.query_parts["where"].append(condition)
        return self
    
    def build_sql(self) -> str:
        """构建PostgreSQL SQL语句"""
        fields = ", ".join(self.query_parts["select"]) if self.query_parts["select"] else "*"
        sql = f'SELECT {fields} FROM "{self.query_parts["from"]}"'  # PostgreSQL使用双引号
        
        if self.query_parts["where"]:
            sql += " WHERE " + " AND ".join(self.query_parts["where"])
        
        return sql
    
    def execute(self) -> List[Dict[str, Any]]:
        """执行PostgreSQL查询"""
        if not self.connection.is_connected():
            raise Exception("数据库未连接")
        
        sql = self.build_sql()
        print(f"执行PostgreSQL查询: {sql}")
        
        # 模拟查询结果
        return [
            {"id": 1, "name": "王五", "email": "wangwu@example.com"},
            {"id": 2, "name": "赵六", "email": "zhaoliu@example.com"}
        ]


class PostgreSQLTransaction(Transaction):
    """PostgreSQL事务管理器"""
    
    def __init__(self, connection: PostgreSQLConnection):
        self.connection = connection
        self.in_transaction = False
    
    def begin(self) -> bool:
        """开始PostgreSQL事务"""
        if not self.connection.is_connected():
            return False
        
        self.in_transaction = True
        print("PostgreSQL事务已开始")
        return True
    
    def commit(self) -> bool:
        """提交PostgreSQL事务"""
        if self.in_transaction:
            self.in_transaction = False
            print("PostgreSQL事务已提交")
            return True
        return False
    
    def rollback(self) -> bool:
        """回滚PostgreSQL事务"""
        if self.in_transaction:
            self.in_transaction = False
            print("PostgreSQL事务已回滚")
            return True
        return False


# ==================== 抽象工厂类 ====================
class DatabaseFactory(ABC):
    """数据库抽象工厂"""
    
    @abstractmethod
    def create_connection(self, host: str, port: int, database: str, 
                         username: str, password: str) -> Connection:
        """创建数据库连接"""
        pass
    
    @abstractmethod
    def create_query(self, connection: Connection) -> Query:
        """创建查询构建器"""
        pass
    
    @abstractmethod
    def create_transaction(self, connection: Connection) -> Transaction:
        """创建事务管理器"""
        pass


# ==================== 具体工厂类 ====================
class MySQLFactory(DatabaseFactory):
    """MySQL工厂"""
    
    def create_connection(self, host: str, port: int, database: str, 
                         username: str, password: str) -> Connection:
        """创建MySQL连接"""
        return MySQLConnection(host, port, database, username, password)
    
    def create_query(self, connection: Connection) -> Query:
        """创建MySQL查询构建器"""
        return MySQLQuery(connection)
    
    def create_transaction(self, connection: Connection) -> Transaction:
        """创建MySQL事务管理器"""
        return MySQLTransaction(connection)


class PostgreSQLFactory(DatabaseFactory):
    """PostgreSQL工厂"""
    
    def create_connection(self, host: str, port: int, database: str, 
                         username: str, password: str) -> Connection:
        """创建PostgreSQL连接"""
        return PostgreSQLConnection(host, port, database, username, password)
    
    def create_query(self, connection: Connection) -> Query:
        """创建PostgreSQL查询构建器"""
        return PostgreSQLQuery(connection)
    
    def create_transaction(self, connection: Connection) -> Transaction:
        """创建PostgreSQL事务管理器"""
        return PostgreSQLTransaction(connection)


# ==================== 数据访问层 ====================
class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, factory: DatabaseFactory):
        self.factory = factory
        self.connection = None
    
    def connect(self, host: str, port: int, database: str, username: str, password: str):
        """连接数据库"""
        self.connection = self.factory.create_connection(host, port, database, username, password)
        return self.connection.connect()
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            return self.connection.disconnect()
        return False
    
    def execute_query(self, table: str, fields: List[str] = None, conditions: List[str] = None):
        """执行查询"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("数据库未连接")
        
        query = self.factory.create_query(self.connection)
        
        if fields:
            query.select(fields)
        
        query.from_table(table)
        
        if conditions:
            for condition in conditions:
                query.where(condition)
        
        return query.execute()
    
    def execute_transaction(self, operations: List[str]):
        """执行事务"""
        if not self.connection or not self.connection.is_connected():
            raise Exception("数据库未连接")
        
        transaction = self.factory.create_transaction(self.connection)
        
        try:
            transaction.begin()
            
            # 模拟执行操作
            for operation in operations:
                print(f"执行操作: {operation}")
            
            transaction.commit()
            return True
        except Exception as e:
            transaction.rollback()
            print(f"事务执行失败: {e}")
            return False


# ==================== 演示函数 ====================
def demonstrate_mysql():
    """演示MySQL数据库操作"""
    print("=" * 60)
    print("MySQL数据库操作演示")
    print("=" * 60)
    
    # 创建MySQL工厂
    mysql_factory = MySQLFactory()
    
    # 创建数据库管理器
    db_manager = DatabaseManager(mysql_factory)
    
    # 连接数据库
    db_manager.connect("localhost", 3306, "testdb", "root", "password")
    
    # 执行查询
    results = db_manager.execute_query("users", ["id", "name", "email"], ["status = 'active'"])
    print(f"查询结果: {results}")
    
    # 执行事务
    operations = ["INSERT INTO users (name, email) VALUES ('新用户', 'new@example.com')",
                 "UPDATE users SET status = 'active' WHERE id = 3"]
    db_manager.execute_transaction(operations)
    
    # 断开连接
    db_manager.disconnect()


def demonstrate_postgresql():
    """演示PostgreSQL数据库操作"""
    print("\n" + "=" * 60)
    print("PostgreSQL数据库操作演示")
    print("=" * 60)
    
    # 创建PostgreSQL工厂
    pg_factory = PostgreSQLFactory()
    
    # 创建数据库管理器
    db_manager = DatabaseManager(pg_factory)
    
    # 连接数据库
    db_manager.connect("localhost", 5432, "testdb", "postgres", "password")
    
    # 执行查询
    results = db_manager.execute_query("users", ["id", "name", "email"], ["created_at > '2023-01-01'"])
    print(f"查询结果: {results}")
    
    # 执行事务
    operations = ["INSERT INTO users (name, email) VALUES ('PostgreSQL用户', 'pg@example.com')",
                 "UPDATE users SET last_login = NOW() WHERE id = 1"]
    db_manager.execute_transaction(operations)
    
    # 断开连接
    db_manager.disconnect()


def main():
    """主函数"""
    print("抽象工厂模式演示 - 数据库访问层")
    
    demonstrate_mysql()
    demonstrate_postgresql()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
