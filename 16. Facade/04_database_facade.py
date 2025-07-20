"""
04_database_facade.py - 数据库访问外观

这个示例展示了如何使用外观模式来简化复杂的数据库操作。
数据库系统包含连接管理、查询构建、结果处理、事务管理等多个子系统，
外观模式提供了统一的数据访问接口，隐藏了底层的复杂性。
"""

import sqlite3
from typing import Dict, List, Any, Optional, Union
from contextlib import contextmanager


# ==================== 子系统：连接管理 ====================
class ConnectionManager:
    """数据库连接管理子系统"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        self.is_connected = False
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # 使结果可以按列名访问
            self.is_connected = True
            return "连接管理器: 数据库连接已建立"
        except Exception as e:
            return f"连接管理器: 连接失败 - {str(e)}"
    
    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.is_connected = False
            return "连接管理器: 数据库连接已断开"
        return "连接管理器: 没有活动连接"
    
    def get_connection(self):
        """获取数据库连接"""
        if not self.is_connected:
            self.connect()
        return self.connection


# ==================== 子系统：查询构建器 ====================
class QueryBuilder:
    """SQL查询构建子系统"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置查询构建器"""
        self._select_fields = []
        self._from_table = ""
        self._where_conditions = []
        self._order_by = []
        self._limit_count = None
        self._parameters = []
    
    def select(self, fields: Union[str, List[str]]):
        """设置SELECT字段"""
        if isinstance(fields, str):
            self._select_fields = [fields]
        else:
            self._select_fields = fields
        return self
    
    def from_table(self, table: str):
        """设置FROM表"""
        self._from_table = table
        return self
    
    def where(self, condition: str, *params):
        """添加WHERE条件"""
        self._where_conditions.append(condition)
        self._parameters.extend(params)
        return self
    
    def order_by(self, field: str, direction: str = "ASC"):
        """添加ORDER BY"""
        self._order_by.append(f"{field} {direction}")
        return self
    
    def limit(self, count: int):
        """设置LIMIT"""
        self._limit_count = count
        return self
    
    def build_select(self):
        """构建SELECT查询"""
        if not self._select_fields or not self._from_table:
            raise ValueError("SELECT字段和FROM表是必需的")
        
        query_parts = []
        
        # SELECT
        query_parts.append(f"SELECT {', '.join(self._select_fields)}")
        
        # FROM
        query_parts.append(f"FROM {self._from_table}")
        
        # WHERE
        if self._where_conditions:
            query_parts.append(f"WHERE {' AND '.join(self._where_conditions)}")
        
        # ORDER BY
        if self._order_by:
            query_parts.append(f"ORDER BY {', '.join(self._order_by)}")
        
        # LIMIT
        if self._limit_count:
            query_parts.append(f"LIMIT {self._limit_count}")
        
        return " ".join(query_parts), self._parameters
    
    def build_insert(self, table: str, data: Dict[str, Any]):
        """构建INSERT查询"""
        columns = list(data.keys())
        placeholders = ["?" for _ in columns]
        values = list(data.values())
        
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        return query, values
    
    def build_update(self, table: str, data: Dict[str, Any], conditions: Dict[str, Any]):
        """构建UPDATE查询"""
        set_clauses = [f"{column} = ?" for column in data.keys()]
        where_clauses = [f"{column} = ?" for column in conditions.keys()]
        
        query = f"UPDATE {table} SET {', '.join(set_clauses)}"
        if where_clauses:
            query += f" WHERE {' AND '.join(where_clauses)}"
        
        values = list(data.values()) + list(conditions.values())
        return query, values
    
    def build_delete(self, table: str, conditions: Dict[str, Any]):
        """构建DELETE查询"""
        where_clauses = [f"{column} = ?" for column in conditions.keys()]
        
        query = f"DELETE FROM {table}"
        if where_clauses:
            query += f" WHERE {' AND '.join(where_clauses)}"
        
        values = list(conditions.values())
        return query, values


# ==================== 子系统：结果处理器 ====================
class ResultProcessor:
    """查询结果处理子系统"""
    
    @staticmethod
    def to_dict_list(cursor) -> List[Dict[str, Any]]:
        """将查询结果转换为字典列表"""
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def to_single_dict(cursor) -> Optional[Dict[str, Any]]:
        """将查询结果转换为单个字典"""
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def format_results(results: List[Dict[str, Any]], max_width: int = 20) -> str:
        """格式化结果为表格字符串"""
        if not results:
            return "没有结果"
        
        # 获取所有列名
        columns = list(results[0].keys())
        
        # 计算每列的最大宽度
        col_widths = {}
        for col in columns:
            col_widths[col] = min(max_width, max(
                len(str(col)),
                max(len(str(row.get(col, ""))) for row in results)
            ))
        
        # 构建表格
        lines = []
        
        # 表头
        header = " | ".join(str(col).ljust(col_widths[col]) for col in columns)
        lines.append(header)
        lines.append("-" * len(header))
        
        # 数据行
        for row in results:
            line = " | ".join(
                str(row.get(col, "")).ljust(col_widths[col])[:col_widths[col]]
                for col in columns
            )
            lines.append(line)
        
        return "\n".join(lines)


# ==================== 子系统：事务管理器 ====================
class TransactionManager:
    """事务管理子系统"""
    
    def __init__(self, connection):
        self.connection = connection
        self.in_transaction = False
    
    def begin_transaction(self):
        """开始事务"""
        if not self.in_transaction:
            self.connection.execute("BEGIN")
            self.in_transaction = True
            return "事务管理器: 事务已开始"
        return "事务管理器: 已在事务中"
    
    def commit_transaction(self):
        """提交事务"""
        if self.in_transaction:
            self.connection.commit()
            self.in_transaction = False
            return "事务管理器: 事务已提交"
        return "事务管理器: 没有活动事务"
    
    def rollback_transaction(self):
        """回滚事务"""
        if self.in_transaction:
            self.connection.rollback()
            self.in_transaction = False
            return "事务管理器: 事务已回滚"
        return "事务管理器: 没有活动事务"
    
    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        self.begin_transaction()
        try:
            yield
            self.commit_transaction()
        except Exception as e:
            self.rollback_transaction()
            raise e


# ==================== 外观类：数据库访问器 ====================
class DatabaseFacade:
    """数据库访问外观类
    
    提供简化的接口来处理复杂的数据库操作，
    将连接管理、查询构建、结果处理、事务管理等子系统整合起来。
    """
    
    def __init__(self, db_path: str):
        # 初始化所有子系统
        self.connection_manager = ConnectionManager(db_path)
        self.query_builder = QueryBuilder()
        self.result_processor = ResultProcessor()
        self.transaction_manager = None
        
        # 建立连接并初始化事务管理器
        self.connection_manager.connect()
        self.transaction_manager = TransactionManager(
            self.connection_manager.get_connection()
        )
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询并返回结果"""
        conn = self.connection_manager.get_connection()
        cursor = conn.execute(query, params)
        return self.result_processor.to_dict_list(cursor)
    
    def execute_single(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """执行查询并返回单个结果"""
        conn = self.connection_manager.get_connection()
        cursor = conn.execute(query, params)
        return self.result_processor.to_single_dict(cursor)
    
    def find_all(self, table: str, columns: List[str] = None, 
                 conditions: Dict[str, Any] = None, order_by: str = None) -> List[Dict[str, Any]]:
        """查找所有记录"""
        builder = self.query_builder
        builder.reset()
        
        # 设置字段
        if columns:
            builder.select(columns)
        else:
            builder.select("*")
        
        builder.from_table(table)
        
        # 添加条件
        if conditions:
            for column, value in conditions.items():
                builder.where(f"{column} = ?", value)
        
        # 添加排序
        if order_by:
            builder.order_by(order_by)
        
        query, params = builder.build_select()
        return self.execute_query(query, params)
    
    def find_by_id(self, table: str, id_value: Any, id_column: str = "id") -> Optional[Dict[str, Any]]:
        """根据ID查找记录"""
        builder = self.query_builder
        builder.reset()
        
        query, params = (builder
                        .select("*")
                        .from_table(table)
                        .where(f"{id_column} = ?", id_value)
                        .build_select())
        
        return self.execute_single(query, params)
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """插入记录"""
        query, params = self.query_builder.build_insert(table, data)
        
        conn = self.connection_manager.get_connection()
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    
    def update(self, table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> int:
        """更新记录"""
        query, params = self.query_builder.build_update(table, data, conditions)
        
        conn = self.connection_manager.get_connection()
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.rowcount
    
    def delete(self, table: str, conditions: Dict[str, Any]) -> int:
        """删除记录"""
        query, params = self.query_builder.build_delete(table, conditions)
        
        conn = self.connection_manager.get_connection()
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.rowcount
    
    def create_table(self, table_name: str, columns: Dict[str, str]):
        """创建表"""
        column_definitions = []
        for column_name, column_type in columns.items():
            column_definitions.append(f"{column_name} {column_type}")
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
        
        conn = self.connection_manager.get_connection()
        conn.execute(query)
        conn.commit()
        return f"数据库外观: 表 '{table_name}' 创建成功"
    
    def batch_insert(self, table: str, data_list: List[Dict[str, Any]]):
        """批量插入"""
        if not data_list:
            return 0
        
        # 使用事务确保数据一致性
        with self.transaction_manager.transaction():
            inserted_count = 0
            for data in data_list:
                self.insert(table, data)
                inserted_count += 1
        
        return inserted_count
    
    def close(self):
        """关闭数据库连接"""
        return self.connection_manager.disconnect()


# ==================== 使用示例 ====================
def demo_database_facade():
    """数据库外观模式演示"""
    print("=" * 60)
    print("🗄️ 数据库访问系统演示 - 外观模式应用")
    print("=" * 60)
    
    # 创建数据库外观
    db = DatabaseFacade(":memory:")  # 使用内存数据库
    
    print("📋 创建用户表...")
    # 创建用户表
    table_msg = db.create_table("users", {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "email": "TEXT UNIQUE NOT NULL",
        "age": "INTEGER"
    })
    print(f"  ✓ {table_msg}")
    
    print("\n📝 插入用户数据...")
    # 批量插入用户
    users_data = [
        {"name": "张三", "email": "zhangsan@example.com", "age": 25},
        {"name": "李四", "email": "lisi@example.com", "age": 30},
        {"name": "王五", "email": "wangwu@example.com", "age": 28}
    ]
    
    inserted_count = db.batch_insert("users", users_data)
    print(f"  ✓ 批量插入 {inserted_count} 个用户")
    
    print("\n🔍 查询用户数据...")
    # 查找所有用户
    all_users = db.find_all("users", order_by="age")
    print("  ✓ 所有用户（按年龄排序）:")
    print(db.result_processor.format_results(all_users))
    
    print("\n🔍 根据条件查询...")
    # 根据条件查找
    young_users = db.find_all("users", conditions={"age": 25})
    print("  ✓ 25岁的用户:")
    print(db.result_processor.format_results(young_users))
    
    print("\n✏️ 更新用户数据...")
    # 更新用户
    updated_rows = db.update("users", {"age": 26}, {"name": "张三"})
    print(f"  ✓ 更新了 {updated_rows} 行")
    
    print("\n🗑️ 删除用户数据...")
    # 删除用户
    deleted_rows = db.delete("users", {"name": "王五"})
    print(f"  ✓ 删除了 {deleted_rows} 行")
    
    print("\n📊 最终用户列表...")
    final_users = db.find_all("users", order_by="id")
    print(db.result_processor.format_results(final_users))
    
    # 关闭数据库连接
    close_msg = db.close()
    print(f"\n🔒 {close_msg}")
    
    print("\n" + "="*60)
    print("🎯 演示完成！外观模式成功简化了复杂的数据库操作！")
    print("="*60)


if __name__ == "__main__":
    demo_database_facade()
