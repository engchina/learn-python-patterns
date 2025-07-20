"""
03_macro_command.py - 宏命令和批量操作实现

这个示例展示了如何使用命令模式实现宏命令（组合命令）和批量操作。
宏命令可以将多个命令组合成一个复合命令，支持批量执行和批量撤销。
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time


# ==================== 基础命令接口 ====================
class Command(ABC):
    """抽象命令接口"""
    
    @abstractmethod
    def execute(self) -> str:
        """执行命令"""
        pass
    
    @abstractmethod
    def undo(self) -> str:
        """撤销命令"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取命令描述"""
        pass


# ==================== 接收者：数据库操作 ====================
class DatabaseConnection:
    """模拟数据库连接"""
    
    def __init__(self):
        self.users: Dict[int, Dict[str, Any]] = {}
        self.next_id = 1
        self.transaction_log: List[str] = []
    
    def create_user(self, name: str, email: str, age: int) -> tuple[int, str]:
        """创建用户"""
        user_id = self.next_id
        self.users[user_id] = {
            'name': name,
            'email': email,
            'age': age,
            'created_at': time.time()
        }
        self.next_id += 1
        log_msg = f"创建用户: ID={user_id}, 姓名={name}, 邮箱={email}, 年龄={age}"
        self.transaction_log.append(log_msg)
        return user_id, log_msg
    
    def update_user(self, user_id: int, **kwargs) -> tuple[Dict[str, Any], str]:
        """更新用户信息"""
        if user_id not in self.users:
            return {}, f"错误: 用户ID {user_id} 不存在"
        
        old_data = self.users[user_id].copy()
        for key, value in kwargs.items():
            if key in self.users[user_id]:
                self.users[user_id][key] = value
        
        log_msg = f"更新用户: ID={user_id}, 更新字段={list(kwargs.keys())}"
        self.transaction_log.append(log_msg)
        return old_data, log_msg
    
    def delete_user(self, user_id: int) -> tuple[Dict[str, Any], str]:
        """删除用户"""
        if user_id not in self.users:
            return {}, f"错误: 用户ID {user_id} 不存在"
        
        deleted_user = self.users.pop(user_id)
        log_msg = f"删除用户: ID={user_id}, 姓名={deleted_user['name']}"
        self.transaction_log.append(log_msg)
        return deleted_user, log_msg
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """获取用户信息"""
        return self.users.get(user_id, {})
    
    def get_all_users(self) -> Dict[int, Dict[str, Any]]:
        """获取所有用户"""
        return self.users.copy()
    
    def get_transaction_log(self) -> List[str]:
        """获取事务日志"""
        return self.transaction_log.copy()


# ==================== 具体命令实现 ====================
class CreateUserCommand(Command):
    """创建用户命令"""
    
    def __init__(self, db: DatabaseConnection, name: str, email: str, age: int):
        self.db = db
        self.name = name
        self.email = email
        self.age = age
        self.created_user_id = None
    
    def execute(self) -> str:
        self.created_user_id, result = self.db.create_user(self.name, self.email, self.age)
        return result
    
    def undo(self) -> str:
        if self.created_user_id:
            _, result = self.db.delete_user(self.created_user_id)
            return f"撤销创建用户: {result}"
        return "无法撤销: 用户未创建"
    
    def get_description(self) -> str:
        return f"创建用户: {self.name} ({self.email})"


class UpdateUserCommand(Command):
    """更新用户命令"""
    
    def __init__(self, db: DatabaseConnection, user_id: int, **kwargs):
        self.db = db
        self.user_id = user_id
        self.update_data = kwargs
        self.old_data = {}
    
    def execute(self) -> str:
        self.old_data, result = self.db.update_user(self.user_id, **self.update_data)
        return result
    
    def undo(self) -> str:
        if self.old_data:
            # 恢复原始数据（排除时间戳等系统字段）
            restore_data = {k: v for k, v in self.old_data.items() 
                          if k in self.update_data}
            _, result = self.db.update_user(self.user_id, **restore_data)
            return f"撤销更新用户: {result}"
        return "无法撤销: 没有原始数据"
    
    def get_description(self) -> str:
        return f"更新用户ID {self.user_id}: {self.update_data}"


class DeleteUserCommand(Command):
    """删除用户命令"""
    
    def __init__(self, db: DatabaseConnection, user_id: int):
        self.db = db
        self.user_id = user_id
        self.deleted_user_data = {}
    
    def execute(self) -> str:
        self.deleted_user_data, result = self.db.delete_user(self.user_id)
        return result
    
    def undo(self) -> str:
        if self.deleted_user_data:
            # 重新创建用户（需要手动设置ID）
            self.db.users[self.user_id] = self.deleted_user_data
            result = f"恢复用户: ID={self.user_id}, 姓名={self.deleted_user_data['name']}"
            self.db.transaction_log.append(f"撤销删除: {result}")
            return result
        return "无法撤销: 没有用户数据"
    
    def get_description(self) -> str:
        return f"删除用户ID: {self.user_id}"


# ==================== 宏命令实现 ====================
class MacroCommand(Command):
    """宏命令 - 组合多个命令"""
    
    def __init__(self, commands: List[Command], description: str = "宏命令"):
        self.commands = commands
        self.description = description
        self.executed_commands: List[Command] = []
    
    def execute(self) -> str:
        """按顺序执行所有命令"""
        results = []
        self.executed_commands.clear()
        
        for command in self.commands:
            try:
                result = command.execute()
                results.append(result)
                self.executed_commands.append(command)
            except Exception as e:
                # 如果某个命令失败，撤销已执行的命令
                self._rollback()
                return f"宏命令执行失败: {str(e)}"
        
        return f"宏命令执行成功，共执行{len(results)}个命令:\n" + "\n".join(f"  - {r}" for r in results)
    
    def undo(self) -> str:
        """逆序撤销所有已执行的命令"""
        if not self.executed_commands:
            return "宏命令未执行，无法撤销"
        
        results = []
        # 逆序撤销
        for command in reversed(self.executed_commands):
            try:
                result = command.undo()
                results.append(result)
            except Exception as e:
                results.append(f"撤销失败: {str(e)}")
        
        self.executed_commands.clear()
        return f"宏命令撤销完成，共撤销{len(results)}个命令:\n" + "\n".join(f"  - {r}" for r in results)
    
    def _rollback(self):
        """回滚已执行的命令"""
        for command in reversed(self.executed_commands):
            try:
                command.undo()
            except:
                pass  # 忽略回滚过程中的错误
        self.executed_commands.clear()
    
    def get_description(self) -> str:
        return f"{self.description} (包含{len(self.commands)}个子命令)"
    
    def add_command(self, command: Command):
        """添加命令到宏命令"""
        self.commands.append(command)
    
    def get_sub_commands(self) -> List[str]:
        """获取子命令描述"""
        return [cmd.get_description() for cmd in self.commands]


# ==================== 批量操作命令 ====================
class BatchUserCreationCommand(MacroCommand):
    """批量用户创建命令"""
    
    def __init__(self, db: DatabaseConnection, users_data: List[Dict[str, Any]]):
        commands = []
        for user_data in users_data:
            cmd = CreateUserCommand(
                db, 
                user_data['name'], 
                user_data['email'], 
                user_data['age']
            )
            commands.append(cmd)
        
        super().__init__(commands, f"批量创建{len(users_data)}个用户")
        self.db = db


class UserMigrationCommand(MacroCommand):
    """用户数据迁移命令"""
    
    def __init__(self, db: DatabaseConnection, migration_data: List[Dict[str, Any]]):
        commands = []
        
        for data in migration_data:
            if data['action'] == 'create':
                cmd = CreateUserCommand(db, data['name'], data['email'], data['age'])
            elif data['action'] == 'update':
                cmd = UpdateUserCommand(db, data['user_id'], **data['updates'])
            elif data['action'] == 'delete':
                cmd = DeleteUserCommand(db, data['user_id'])
            else:
                continue
            commands.append(cmd)
        
        super().__init__(commands, f"用户数据迁移 (共{len(commands)}个操作)")


# ==================== 调用者：事务管理器 ====================
class TransactionManager:
    """事务管理器 - 支持事务性操作"""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.transaction_stack: List[Command] = []
    
    def execute_transaction(self, command: Command) -> str:
        """执行事务性命令"""
        try:
            result = command.execute()
            self.transaction_stack.append(command)
            return f"事务执行成功: {result}"
        except Exception as e:
            return f"事务执行失败: {str(e)}"
    
    def rollback_last_transaction(self) -> str:
        """回滚最后一个事务"""
        if self.transaction_stack:
            command = self.transaction_stack.pop()
            return f"事务回滚: {command.undo()}"
        return "没有可回滚的事务"
    
    def rollback_all_transactions(self) -> str:
        """回滚所有事务"""
        if not self.transaction_stack:
            return "没有可回滚的事务"
        
        results = []
        while self.transaction_stack:
            command = self.transaction_stack.pop()
            result = command.undo()
            results.append(result)
        
        return f"回滚所有事务完成:\n" + "\n".join(f"  - {r}" for r in results)
    
    def get_transaction_count(self) -> int:
        """获取事务数量"""
        return len(self.transaction_stack)


# ==================== 演示函数 ====================
def demonstrate_macro_commands():
    """演示宏命令功能"""
    print("=" * 60)
    print("宏命令和批量操作演示")
    print("=" * 60)
    
    # 创建数据库连接
    db = DatabaseConnection()
    transaction_manager = TransactionManager(db)
    
    print("1. 批量创建用户:")
    users_data = [
        {'name': '张三', 'email': 'zhangsan@example.com', 'age': 25},
        {'name': '李四', 'email': 'lisi@example.com', 'age': 30},
        {'name': '王五', 'email': 'wangwu@example.com', 'age': 28}
    ]
    
    batch_create = BatchUserCreationCommand(db, users_data)
    result = transaction_manager.execute_transaction(batch_create)
    print(f"  {result}")
    
    print(f"\n2. 当前用户列表:")
    for user_id, user_data in db.get_all_users().items():
        print(f"  ID: {user_id}, 姓名: {user_data['name']}, 邮箱: {user_data['email']}, 年龄: {user_data['age']}")
    
    print(f"\n3. 执行复杂的数据迁移操作:")
    migration_data = [
        {'action': 'update', 'user_id': 1, 'updates': {'age': 26, 'email': 'zhangsan_new@example.com'}},
        {'action': 'create', 'name': '赵六', 'email': 'zhaoliu@example.com', 'age': 35},
        {'action': 'delete', 'user_id': 2}
    ]
    
    migration = UserMigrationCommand(db, migration_data)
    result = transaction_manager.execute_transaction(migration)
    print(f"  {result}")
    
    print(f"\n4. 迁移后的用户列表:")
    for user_id, user_data in db.get_all_users().items():
        print(f"  ID: {user_id}, 姓名: {user_data['name']}, 邮箱: {user_data['email']}, 年龄: {user_data['age']}")
    
    print(f"\n5. 回滚最后一个事务:")
    result = transaction_manager.rollback_last_transaction()
    print(f"  {result}")
    
    print(f"\n6. 回滚后的用户列表:")
    for user_id, user_data in db.get_all_users().items():
        print(f"  ID: {user_id}, 姓名: {user_data['name']}, 邮箱: {user_data['email']}, 年龄: {user_data['age']}")
    
    print(f"\n7. 事务日志:")
    for i, log_entry in enumerate(db.get_transaction_log(), 1):
        print(f"  {i}. {log_entry}")


def demonstrate_nested_macro_commands():
    """演示嵌套宏命令"""
    print("\n" + "=" * 60)
    print("嵌套宏命令演示")
    print("=" * 60)
    
    db = DatabaseConnection()
    
    # 创建基础命令
    create_admin = CreateUserCommand(db, "管理员", "admin@example.com", 30)
    create_user1 = CreateUserCommand(db, "用户1", "user1@example.com", 25)
    create_user2 = CreateUserCommand(db, "用户2", "user2@example.com", 28)
    
    # 创建子宏命令
    create_users_macro = MacroCommand([create_user1, create_user2], "创建普通用户")
    
    # 创建主宏命令（包含子宏命令）
    setup_system_macro = MacroCommand([create_admin, create_users_macro], "系统初始化")
    
    print("1. 执行嵌套宏命令:")
    result = setup_system_macro.execute()
    print(f"  {result}")
    
    print(f"\n2. 系统初始化后的用户:")
    for user_id, user_data in db.get_all_users().items():
        print(f"  ID: {user_id}, 姓名: {user_data['name']}, 角色: {'管理员' if '管理员' in user_data['name'] else '普通用户'}")
    
    print(f"\n3. 撤销整个系统初始化:")
    result = setup_system_macro.undo()
    print(f"  {result}")
    
    print(f"\n4. 撤销后的用户数量: {len(db.get_all_users())}")


if __name__ == "__main__":
    demonstrate_macro_commands()
    demonstrate_nested_macro_commands()
