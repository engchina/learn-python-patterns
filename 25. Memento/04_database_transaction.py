#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库事务回滚模拟

本模块演示了备忘录模式在数据库事务回滚中的应用，包括：
1. 事务状态的保存
2. 回滚机制的实现
3. 嵌套事务处理
4. 原子性操作的保证

作者: Assistant
日期: 2024-01-20
"""

from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import copy
import uuid


class TransactionStatus(Enum):
    """事务状态"""
    ACTIVE = "活跃"
    COMMITTED = "已提交"
    ABORTED = "已中止"
    PREPARING = "准备中"


class OperationType(Enum):
    """操作类型"""
    INSERT = "插入"
    UPDATE = "更新"
    DELETE = "删除"
    CREATE_TABLE = "创建表"
    DROP_TABLE = "删除表"


@dataclass
class DatabaseRecord:
    """数据库记录"""
    id: Any
    data: Dict[str, Any]
    
    def copy(self) -> 'DatabaseRecord':
        return DatabaseRecord(self.id, copy.deepcopy(self.data))
    
    def __str__(self) -> str:
        return f"Record({self.id}: {self.data})"


@dataclass
class DatabaseOperation:
    """数据库操作"""
    operation_type: OperationType
    table_name: str
    record_id: Any = None
    old_record: Optional[DatabaseRecord] = None
    new_record: Optional[DatabaseRecord] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        return f"{self.operation_type.value} on {self.table_name}"


class TransactionMemento:
    """事务备忘录"""
    
    def __init__(self, transaction_id: str, database_state: Dict[str, Dict[Any, DatabaseRecord]]):
        self.transaction_id = transaction_id
        self._database_state = copy.deepcopy(database_state)
        self.timestamp = datetime.now()
        self.operation_count = 0
    
    def get_database_state(self) -> Dict[str, Dict[Any, DatabaseRecord]]:
        """获取数据库状态"""
        return copy.deepcopy(self._database_state)
    
    def get_transaction_id(self) -> str:
        """获取事务ID"""
        return self.transaction_id
    
    def get_timestamp(self) -> datetime:
        """获取时间戳"""
        return self.timestamp
    
    def __str__(self) -> str:
        return f"事务备忘录[{self.transaction_id}] - {self.timestamp.strftime('%H:%M:%S')}"


class Database:
    """模拟数据库 - 发起人"""
    
    def __init__(self):
        # 表结构: {table_name: {record_id: DatabaseRecord}}
        self.tables: Dict[str, Dict[Any, DatabaseRecord]] = {}
        self.current_transaction: Optional['Transaction'] = None
        self.transaction_history: List['Transaction'] = []
        self.auto_commit = True
    
    def create_table(self, table_name: str) -> bool:
        """创建表"""
        if table_name in self.tables:
            print(f"⚠️ 表 {table_name} 已存在")
            return False
        
        self.tables[table_name] = {}
        print(f"📋 创建表: {table_name}")
        
        if self.current_transaction:
            operation = DatabaseOperation(OperationType.CREATE_TABLE, table_name)
            self.current_transaction.add_operation(operation)
        
        return True
    
    def drop_table(self, table_name: str) -> bool:
        """删除表"""
        if table_name not in self.tables:
            print(f"⚠️ 表 {table_name} 不存在")
            return False
        
        old_table = self.tables[table_name].copy()
        del self.tables[table_name]
        print(f"🗑️ 删除表: {table_name}")
        
        if self.current_transaction:
            operation = DatabaseOperation(OperationType.DROP_TABLE, table_name)
            self.current_transaction.add_operation(operation)
        
        return True
    
    def insert(self, table_name: str, record: DatabaseRecord) -> bool:
        """插入记录"""
        if table_name not in self.tables:
            print(f"❌ 表 {table_name} 不存在")
            return False
        
        if record.id in self.tables[table_name]:
            print(f"❌ 记录 {record.id} 已存在")
            return False
        
        self.tables[table_name][record.id] = record.copy()
        print(f"➕ 插入记录: {table_name}.{record}")
        
        if self.current_transaction:
            operation = DatabaseOperation(
                OperationType.INSERT, 
                table_name, 
                record.id, 
                None, 
                record.copy()
            )
            self.current_transaction.add_operation(operation)
        
        return True
    
    def update(self, table_name: str, record_id: Any, new_data: Dict[str, Any]) -> bool:
        """更新记录"""
        if table_name not in self.tables:
            print(f"❌ 表 {table_name} 不存在")
            return False
        
        if record_id not in self.tables[table_name]:
            print(f"❌ 记录 {record_id} 不存在")
            return False
        
        old_record = self.tables[table_name][record_id].copy()
        self.tables[table_name][record_id].data.update(new_data)
        new_record = self.tables[table_name][record_id].copy()
        
        print(f"✏️ 更新记录: {table_name}.{record_id}")
        
        if self.current_transaction:
            operation = DatabaseOperation(
                OperationType.UPDATE, 
                table_name, 
                record_id, 
                old_record, 
                new_record
            )
            self.current_transaction.add_operation(operation)
        
        return True
    
    def delete(self, table_name: str, record_id: Any) -> bool:
        """删除记录"""
        if table_name not in self.tables:
            print(f"❌ 表 {table_name} 不存在")
            return False
        
        if record_id not in self.tables[table_name]:
            print(f"❌ 记录 {record_id} 不存在")
            return False
        
        old_record = self.tables[table_name][record_id].copy()
        del self.tables[table_name][record_id]
        print(f"🗑️ 删除记录: {table_name}.{record_id}")
        
        if self.current_transaction:
            operation = DatabaseOperation(
                OperationType.DELETE, 
                table_name, 
                record_id, 
                old_record, 
                None
            )
            self.current_transaction.add_operation(operation)
        
        return True
    
    def select(self, table_name: str, record_id: Any = None) -> Optional[DatabaseRecord]:
        """查询记录"""
        if table_name not in self.tables:
            return None
        
        if record_id is None:
            # 返回所有记录
            return list(self.tables[table_name].values())
        else:
            return self.tables[table_name].get(record_id)
    
    def create_memento(self, transaction_id: str) -> TransactionMemento:
        """创建备忘录"""
        memento = TransactionMemento(transaction_id, self.tables)
        print(f"💾 创建数据库快照: {transaction_id}")
        return memento
    
    def restore_from_memento(self, memento: TransactionMemento) -> None:
        """从备忘录恢复"""
        self.tables = memento.get_database_state()
        print(f"🔄 恢复数据库状态: {memento.get_transaction_id()}")
    
    def get_table_info(self) -> Dict[str, int]:
        """获取表信息"""
        return {table_name: len(records) for table_name, records in self.tables.items()}


class Transaction:
    """事务类"""
    
    def __init__(self, database: Database, transaction_id: str = None):
        self.transaction_id = transaction_id or str(uuid.uuid4())[:8]
        self.database = database
        self.status = TransactionStatus.ACTIVE
        self.operations: List[DatabaseOperation] = []
        self.savepoints: Dict[str, TransactionMemento] = {}
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        
        # 创建事务开始时的备忘录
        self.initial_memento = database.create_memento(f"{self.transaction_id}_start")
    
    def add_operation(self, operation: DatabaseOperation) -> None:
        """添加操作到事务"""
        if self.status != TransactionStatus.ACTIVE:
            raise Exception(f"事务 {self.transaction_id} 不是活跃状态")
        
        self.operations.append(operation)
        print(f"📝 事务 {self.transaction_id} 记录操作: {operation}")
    
    def create_savepoint(self, savepoint_name: str) -> None:
        """创建保存点"""
        if self.status != TransactionStatus.ACTIVE:
            raise Exception(f"事务 {self.transaction_id} 不是活跃状态")
        
        memento = self.database.create_memento(f"{self.transaction_id}_{savepoint_name}")
        self.savepoints[savepoint_name] = memento
        print(f"📌 创建保存点: {savepoint_name}")
    
    def rollback_to_savepoint(self, savepoint_name: str) -> bool:
        """回滚到保存点"""
        if savepoint_name not in self.savepoints:
            print(f"❌ 保存点 {savepoint_name} 不存在")
            return False
        
        memento = self.savepoints[savepoint_name]
        self.database.restore_from_memento(memento)
        
        # 移除该保存点之后的操作
        savepoint_time = memento.get_timestamp()
        self.operations = [op for op in self.operations if op.timestamp <= savepoint_time]
        
        print(f"↶ 回滚到保存点: {savepoint_name}")
        return True
    
    def commit(self) -> bool:
        """提交事务"""
        if self.status != TransactionStatus.ACTIVE:
            print(f"❌ 事务 {self.transaction_id} 不能提交")
            return False
        
        try:
            self.status = TransactionStatus.COMMITTED
            self.end_time = datetime.now()
            
            # 清理保存点
            self.savepoints.clear()
            
            print(f"✅ 事务 {self.transaction_id} 已提交 ({len(self.operations)} 个操作)")
            return True
            
        except Exception as e:
            print(f"❌ 事务提交失败: {e}")
            self.rollback()
            return False
    
    def rollback(self) -> bool:
        """回滚事务"""
        if self.status == TransactionStatus.COMMITTED:
            print(f"❌ 已提交的事务 {self.transaction_id} 不能回滚")
            return False
        
        try:
            # 恢复到事务开始时的状态
            self.database.restore_from_memento(self.initial_memento)
            
            self.status = TransactionStatus.ABORTED
            self.end_time = datetime.now()
            
            print(f"↶ 事务 {self.transaction_id} 已回滚 (撤销 {len(self.operations)} 个操作)")
            return True
            
        except Exception as e:
            print(f"❌ 事务回滚失败: {e}")
            return False
    
    def get_summary(self) -> Dict[str, Any]:
        """获取事务摘要"""
        duration = None
        if self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            'transaction_id': self.transaction_id,
            'status': self.status.value,
            'operation_count': len(self.operations),
            'savepoint_count': len(self.savepoints),
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_seconds': duration
        }


class TransactionManager:
    """事务管理器 - 管理者"""
    
    def __init__(self, database: Database):
        self.database = database
        self.active_transactions: Dict[str, Transaction] = {}
        self.transaction_history: List[Transaction] = []
    
    def begin_transaction(self, transaction_id: str = None) -> Transaction:
        """开始事务"""
        if self.database.current_transaction:
            print("⚠️ 已有活跃事务，将嵌套执行")
        
        transaction = Transaction(self.database, transaction_id)
        self.active_transactions[transaction.transaction_id] = transaction
        self.database.current_transaction = transaction
        
        print(f"🚀 开始事务: {transaction.transaction_id}")
        return transaction
    
    def commit_transaction(self, transaction_id: str) -> bool:
        """提交事务"""
        if transaction_id not in self.active_transactions:
            print(f"❌ 事务 {transaction_id} 不存在")
            return False
        
        transaction = self.active_transactions[transaction_id]
        success = transaction.commit()
        
        if success:
            # 移动到历史记录
            self.transaction_history.append(transaction)
            del self.active_transactions[transaction_id]
            
            # 清除当前事务
            if self.database.current_transaction == transaction:
                self.database.current_transaction = None
        
        return success
    
    def rollback_transaction(self, transaction_id: str) -> bool:
        """回滚事务"""
        if transaction_id not in self.active_transactions:
            print(f"❌ 事务 {transaction_id} 不存在")
            return False
        
        transaction = self.active_transactions[transaction_id]
        success = transaction.rollback()
        
        if success:
            # 移动到历史记录
            self.transaction_history.append(transaction)
            del self.active_transactions[transaction_id]
            
            # 清除当前事务
            if self.database.current_transaction == transaction:
                self.database.current_transaction = None
        
        return success
    
    def get_active_transactions(self) -> List[Dict[str, Any]]:
        """获取活跃事务列表"""
        return [tx.get_summary() for tx in self.active_transactions.values()]
    
    def get_transaction_history(self) -> List[Dict[str, Any]]:
        """获取事务历史"""
        return [tx.get_summary() for tx in self.transaction_history]


def demo_database_transaction():
    """演示数据库事务"""
    print("=" * 50)
    print("🗄️ 数据库事务回滚演示")
    print("=" * 50)
    
    # 创建数据库和事务管理器
    db = Database()
    tx_manager = TransactionManager(db)
    
    # 创建表
    db.create_table("users")
    db.create_table("orders")
    
    print(f"\n📊 初始表信息: {db.get_table_info()}")
    
    # 开始事务1
    print("\n🚀 开始事务1:")
    tx1 = tx_manager.begin_transaction("tx_001")
    
    # 插入用户数据
    user1 = DatabaseRecord(1, {"name": "张三", "email": "zhangsan@example.com", "age": 25})
    user2 = DatabaseRecord(2, {"name": "李四", "email": "lisi@example.com", "age": 30})
    
    db.insert("users", user1)
    db.insert("users", user2)
    
    # 创建保存点
    tx1.create_savepoint("users_inserted")
    
    # 插入订单数据
    order1 = DatabaseRecord(101, {"user_id": 1, "product": "笔记本电脑", "amount": 5999.00})
    order2 = DatabaseRecord(102, {"user_id": 2, "product": "手机", "amount": 2999.00})
    
    db.insert("orders", order1)
    db.insert("orders", order2)
    
    print(f"\n📊 事务中表信息: {db.get_table_info()}")
    
    # 模拟错误，回滚到保存点
    print("\n❌ 模拟订单处理错误，回滚到保存点:")
    tx1.rollback_to_savepoint("users_inserted")
    
    print(f"📊 回滚后表信息: {db.get_table_info()}")
    
    # 重新插入正确的订单
    print("\n✅ 重新插入正确的订单:")
    order1_fixed = DatabaseRecord(101, {"user_id": 1, "product": "笔记本电脑", "amount": 5999.00, "status": "pending"})
    db.insert("orders", order1_fixed)
    
    # 提交事务
    print("\n✅ 提交事务1:")
    tx_manager.commit_transaction("tx_001")
    
    print(f"📊 提交后表信息: {db.get_table_info()}")
    
    # 开始事务2（演示完整回滚）
    print("\n🚀 开始事务2（演示完整回滚）:")
    tx2 = tx_manager.begin_transaction("tx_002")
    
    # 更新用户信息
    db.update("users", 1, {"age": 26, "city": "北京"})
    
    # 删除订单
    db.delete("orders", 101)
    
    # 插入新用户
    user3 = DatabaseRecord(3, {"name": "王五", "email": "wangwu@example.com", "age": 28})
    db.insert("users", user3)
    
    print(f"\n📊 事务2中表信息: {db.get_table_info()}")
    
    # 回滚整个事务
    print("\n↶ 回滚整个事务2:")
    tx_manager.rollback_transaction("tx_002")
    
    print(f"📊 回滚后表信息: {db.get_table_info()}")
    
    # 显示事务历史
    print("\n📋 事务历史:")
    for tx_summary in tx_manager.get_transaction_history():
        print(f"  {tx_summary}")


if __name__ == "__main__":
    print("🎯 数据库事务备忘录模式演示")
    
    demo_database_transaction()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 备忘录模式在数据库事务中提供了强大的回滚能力")
    print("=" * 50)
