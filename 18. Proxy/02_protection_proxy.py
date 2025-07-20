"""
02_protection_proxy.py - 保护代理示例

这个示例展示了保护代理在权限控制系统中的应用。
包括用户角色管理、访问权限验证和安全访问机制。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Optional
from enum import Enum
from datetime import datetime, timedelta
import hashlib


class UserRole(Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"


class Permission(Enum):
    """权限枚举"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"


# ==================== 用户和会话管理 ====================
class User:
    """用户类"""
    
    def __init__(self, username: str, role: UserRole, permissions: Set[Permission]):
        self.username = username
        self.role = role
        self.permissions = permissions
        self.created_at = datetime.now()
        self.last_login = None
    
    def login(self):
        """用户登录"""
        self.last_login = datetime.now()
        print(f"用户 {self.username} ({self.role.value}) 登录成功")
    
    def has_permission(self, permission: Permission) -> bool:
        """检查用户是否有指定权限"""
        return permission in self.permissions
    
    def get_info(self) -> str:
        """获取用户信息"""
        return f"用户: {self.username}, 角色: {self.role.value}, 权限: {[p.value for p in self.permissions]}"


class Session:
    """会话类"""
    
    def __init__(self, user: User, session_id: str):
        self.user = user
        self.session_id = session_id
        self.created_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(hours=2)  # 2小时过期
        self.is_active = True
    
    def is_valid(self) -> bool:
        """检查会话是否有效"""
        return self.is_active and datetime.now() < self.expires_at
    
    def extend_session(self):
        """延长会话时间"""
        if self.is_valid():
            self.expires_at = datetime.now() + timedelta(hours=2)
            print(f"会话 {self.session_id} 已延长")
    
    def invalidate(self):
        """使会话失效"""
        self.is_active = False
        print(f"会话 {self.session_id} 已失效")


# ==================== 敏感资源接口 ====================
class SensitiveResource(ABC):
    """敏感资源抽象接口"""
    
    @abstractmethod
    def read_data(self) -> str:
        """读取数据"""
        pass
    
    @abstractmethod
    def write_data(self, data: str) -> str:
        """写入数据"""
        pass
    
    @abstractmethod
    def delete_data(self, data_id: str) -> str:
        """删除数据"""
        pass
    
    @abstractmethod
    def execute_command(self, command: str) -> str:
        """执行命令"""
        pass
    
    @abstractmethod
    def get_admin_info(self) -> str:
        """获取管理员信息"""
        pass


# ==================== 真实敏感资源 ====================
class DatabaseResource(SensitiveResource):
    """数据库资源 - 真实的敏感资源"""
    
    def __init__(self, name: str):
        self.name = name
        self.data = {
            "user_001": "张三的个人信息",
            "user_002": "李四的个人信息",
            "user_003": "王五的个人信息"
        }
        self.access_log = []
        print(f"数据库资源 '{name}' 初始化完成")
    
    def read_data(self) -> str:
        """读取数据"""
        self._log_access("READ")
        data_list = [f"{key}: {value}" for key, value in self.data.items()]
        return f"数据库 {self.name} 数据: {data_list}"
    
    def write_data(self, data: str) -> str:
        """写入数据"""
        self._log_access("WRITE")
        data_id = f"user_{len(self.data) + 1:03d}"
        self.data[data_id] = data
        return f"数据库 {self.name}: 数据已写入，ID: {data_id}"
    
    def delete_data(self, data_id: str) -> str:
        """删除数据"""
        self._log_access("DELETE")
        if data_id in self.data:
            deleted_data = self.data.pop(data_id)
            return f"数据库 {self.name}: 已删除数据 {data_id}: {deleted_data}"
        return f"数据库 {self.name}: 数据 {data_id} 不存在"
    
    def execute_command(self, command: str) -> str:
        """执行命令"""
        self._log_access("EXECUTE")
        return f"数据库 {self.name}: 执行命令 '{command}' 完成"
    
    def get_admin_info(self) -> str:
        """获取管理员信息"""
        self._log_access("ADMIN")
        return f"数据库 {self.name} 管理信息: 总记录数 {len(self.data)}, 访问日志 {len(self.access_log)} 条"
    
    def _log_access(self, operation: str):
        """记录访问日志"""
        self.access_log.append({
            "operation": operation,
            "timestamp": datetime.now(),
            "count": len(self.access_log) + 1
        })


# ==================== 保护代理 ====================
class DatabaseProtectionProxy(SensitiveResource):
    """数据库保护代理"""
    
    def __init__(self, database: DatabaseResource):
        self._database = database
        self._current_session: Optional[Session] = None
        self._failed_attempts = {}  # 记录失败尝试
        self._max_failed_attempts = 3
        print(f"数据库保护代理已创建")
    
    def authenticate(self, session: Session) -> bool:
        """认证用户会话"""
        if not session.is_valid():
            print(f"认证失败: 会话已过期或无效")
            return False
        
        username = session.user.username
        
        # 检查是否被锁定
        if self._is_user_locked(username):
            print(f"认证失败: 用户 {username} 已被锁定")
            return False
        
        self._current_session = session
        self._reset_failed_attempts(username)
        print(f"认证成功: 用户 {session.user.username} ({session.user.role.value})")
        return True
    
    def logout(self):
        """用户登出"""
        if self._current_session:
            username = self._current_session.user.username
            self._current_session.invalidate()
            self._current_session = None
            print(f"用户 {username} 已登出")
        else:
            print("没有活跃的会话")
    
    def read_data(self) -> str:
        """读取数据"""
        if not self._check_permission(Permission.READ):
            return "访问被拒绝: 没有读取权限"
        
        print("保护代理: 读取权限验证通过")
        return self._database.read_data()
    
    def write_data(self, data: str) -> str:
        """写入数据"""
        if not self._check_permission(Permission.WRITE):
            return "访问被拒绝: 没有写入权限"
        
        print("保护代理: 写入权限验证通过")
        return self._database.write_data(data)
    
    def delete_data(self, data_id: str) -> str:
        """删除数据"""
        if not self._check_permission(Permission.DELETE):
            return "访问被拒绝: 没有删除权限"
        
        print("保护代理: 删除权限验证通过")
        return self._database.delete_data(data_id)
    
    def execute_command(self, command: str) -> str:
        """执行命令"""
        if not self._check_permission(Permission.EXECUTE):
            return "访问被拒绝: 没有执行权限"
        
        print("保护代理: 执行权限验证通过")
        return self._database.execute_command(command)
    
    def get_admin_info(self) -> str:
        """获取管理员信息"""
        if not self._check_permission(Permission.ADMIN):
            return "访问被拒绝: 没有管理员权限"
        
        print("保护代理: 管理员权限验证通过")
        return self._database.get_admin_info()
    
    def _check_permission(self, required_permission: Permission) -> bool:
        """检查权限"""
        if not self._current_session:
            print("权限检查失败: 用户未认证")
            return False
        
        if not self._current_session.is_valid():
            print("权限检查失败: 会话已过期")
            self._current_session = None
            return False
        
        user = self._current_session.user
        has_permission = user.has_permission(required_permission)
        
        if not has_permission:
            self._record_failed_attempt(user.username)
            print(f"权限检查失败: 用户 {user.username} 没有 {required_permission.value} 权限")
        
        return has_permission
    
    def _record_failed_attempt(self, username: str):
        """记录失败尝试"""
        if username not in self._failed_attempts:
            self._failed_attempts[username] = []
        
        self._failed_attempts[username].append(datetime.now())
        
        # 清理过期的失败记录（1小时内）
        cutoff_time = datetime.now() - timedelta(hours=1)
        self._failed_attempts[username] = [
            attempt for attempt in self._failed_attempts[username]
            if attempt > cutoff_time
        ]
        
        attempts_count = len(self._failed_attempts[username])
        print(f"记录失败尝试: 用户 {username} 在1小时内失败 {attempts_count} 次")
    
    def _is_user_locked(self, username: str) -> bool:
        """检查用户是否被锁定"""
        if username not in self._failed_attempts:
            return False
        
        # 清理过期的失败记录
        cutoff_time = datetime.now() - timedelta(hours=1)
        self._failed_attempts[username] = [
            attempt for attempt in self._failed_attempts[username]
            if attempt > cutoff_time
        ]
        
        return len(self._failed_attempts[username]) >= self._max_failed_attempts
    
    def _reset_failed_attempts(self, username: str):
        """重置失败尝试记录"""
        if username in self._failed_attempts:
            self._failed_attempts[username] = []


# ==================== 用户管理系统 ====================
class UserManager:
    """用户管理系统"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Session] = {}
        self._init_default_users()
    
    def _init_default_users(self):
        """初始化默认用户"""
        # 管理员用户
        admin_user = User("admin", UserRole.ADMIN, {
            Permission.READ, Permission.WRITE, Permission.DELETE, 
            Permission.EXECUTE, Permission.ADMIN
        })
        
        # 管理者用户
        manager_user = User("manager", UserRole.MANAGER, {
            Permission.READ, Permission.WRITE, Permission.DELETE
        })
        
        # 普通用户
        normal_user = User("user", UserRole.USER, {
            Permission.READ, Permission.WRITE
        })
        
        # 访客用户
        guest_user = User("guest", UserRole.GUEST, {
            Permission.READ
        })
        
        self.users = {
            "admin": admin_user,
            "manager": manager_user,
            "user": normal_user,
            "guest": guest_user
        }
        
        print("用户管理系统: 默认用户已初始化")
    
    def login(self, username: str, password: str) -> Optional[Session]:
        """用户登录"""
        if username not in self.users:
            print(f"登录失败: 用户 {username} 不存在")
            return None
        
        # 简化的密码验证（实际应用中应该使用安全的哈希验证）
        expected_password = f"{username}_password"
        if password != expected_password:
            print(f"登录失败: 密码错误")
            return None
        
        user = self.users[username]
        user.login()
        
        # 创建会话
        session_id = self._generate_session_id(username)
        session = Session(user, session_id)
        self.sessions[session_id] = session
        
        print(f"会话创建成功: {session_id}")
        return session
    
    def _generate_session_id(self, username: str) -> str:
        """生成会话ID"""
        timestamp = str(datetime.now().timestamp())
        raw_id = f"{username}_{timestamp}"
        return hashlib.md5(raw_id.encode()).hexdigest()[:16]


# ==================== 使用示例 ====================
def demo_protection_proxy():
    """保护代理演示"""
    print("=" * 60)
    print("🛡️ 保护代理演示 - 权限控制系统")
    print("=" * 60)
    
    # 创建系统组件
    database = DatabaseResource("用户数据库")
    proxy = DatabaseProtectionProxy(database)
    user_manager = UserManager()
    
    # 测试不同用户的访问
    test_users = [
        ("admin", "admin_password"),
        ("manager", "manager_password"),
        ("user", "user_password"),
        ("guest", "guest_password")
    ]
    
    for username, password in test_users:
        print(f"\n{'='*20} 测试用户: {username} {'='*20}")
        
        # 用户登录
        session = user_manager.login(username, password)
        if not session:
            continue
        
        # 认证到代理
        if not proxy.authenticate(session):
            continue
        
        print(f"\n用户信息: {session.user.get_info()}")
        
        # 测试各种操作
        operations = [
            ("读取数据", lambda: proxy.read_data()),
            ("写入数据", lambda: proxy.write_data(f"{username}的新数据")),
            ("删除数据", lambda: proxy.delete_data("user_001")),
            ("执行命令", lambda: proxy.execute_command("BACKUP DATABASE")),
            ("获取管理信息", lambda: proxy.get_admin_info())
        ]
        
        for op_name, op_func in operations:
            print(f"\n--- {op_name} ---")
            result = op_func()
            print(f"结果: {result}")
        
        # 用户登出
        proxy.logout()


def demo_session_management():
    """会话管理演示"""
    print("\n" + "=" * 60)
    print("⏰ 会话管理演示")
    print("=" * 60)
    
    database = DatabaseResource("测试数据库")
    proxy = DatabaseProtectionProxy(database)
    user_manager = UserManager()
    
    # 用户登录
    session = user_manager.login("admin", "admin_password")
    proxy.authenticate(session)
    
    print("\n📖 正常访问:")
    result = proxy.read_data()
    print(f"结果: {result}")
    
    print("\n⏰ 模拟会话过期:")
    # 手动使会话过期
    session.expires_at = datetime.now() - timedelta(minutes=1)
    
    result = proxy.read_data()
    print(f"结果: {result}")
    
    print("\n🔄 重新登录:")
    new_session = user_manager.login("admin", "admin_password")
    proxy.authenticate(new_session)
    
    result = proxy.read_data()
    print(f"结果: {result}")


def demo_failed_attempts():
    """失败尝试演示"""
    print("\n" + "=" * 60)
    print("🚫 失败尝试锁定演示")
    print("=" * 60)
    
    database = DatabaseResource("安全数据库")
    proxy = DatabaseProtectionProxy(database)
    user_manager = UserManager()
    
    # 用户登录为普通用户（没有删除权限）
    session = user_manager.login("user", "user_password")
    proxy.authenticate(session)
    
    print(f"\n用户信息: {session.user.get_info()}")
    
    print("\n🚫 多次尝试无权限操作:")
    for i in range(4):
        print(f"\n--- 第 {i+1} 次尝试删除操作 ---")
        result = proxy.delete_data("user_001")
        print(f"结果: {result}")
    
    print("\n📖 尝试正常操作:")
    result = proxy.read_data()
    print(f"结果: {result}")


def main():
    """主演示函数"""
    demo_protection_proxy()
    demo_session_management()
    demo_failed_attempts()
    
    print("\n" + "=" * 60)
    print("🎉 保护代理演示完成！")
    print("💡 关键要点:")
    print("   • 保护代理控制对敏感资源的访问")
    print("   • 基于用户角色和权限进行访问控制")
    print("   • 会话管理确保访问的安全性")
    print("   • 失败尝试记录防止恶意访问")
    print("   • 代理透明地添加安全功能")
    print("=" * 60)


if __name__ == "__main__":
    main()
