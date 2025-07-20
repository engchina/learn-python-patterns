"""
01_basic_proxy.py - 代理模式基础实现

这个示例展示了代理模式的基本概念和实现方式。
包括虚拟代理的延迟加载和代理的透明性演示。
"""

from abc import ABC, abstractmethod
import time
from typing import Optional


# ==================== 抽象主题接口 ====================
class Subject(ABC):
    """抽象主题接口"""
    
    @abstractmethod
    def request(self) -> str:
        """处理请求"""
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        """获取信息"""
        pass


# ==================== 真实主题 ====================
class RealSubject(Subject):
    """真实主题 - 实际执行业务逻辑的对象"""
    
    def __init__(self, name: str):
        self.name = name
        self._initialize()
    
    def _initialize(self):
        """初始化真实对象（模拟耗时操作）"""
        print(f"正在初始化真实对象: {self.name}")
        time.sleep(1)  # 模拟初始化耗时
        print(f"真实对象 {self.name} 初始化完成")
    
    def request(self) -> str:
        """处理请求"""
        print(f"真实对象 {self.name} 正在处理请求...")
        time.sleep(0.5)  # 模拟处理时间
        return f"真实对象 {self.name} 的处理结果"
    
    def get_info(self) -> str:
        """获取信息"""
        return f"真实对象信息: {self.name}"


# ==================== 虚拟代理 ====================
class VirtualProxy(Subject):
    """虚拟代理 - 延迟创建真实对象"""
    
    def __init__(self, name: str):
        self.name = name
        self._real_subject: Optional[RealSubject] = None
        self._access_count = 0
        print(f"创建虚拟代理: {self.name}")
    
    def request(self) -> str:
        """处理请求 - 延迟创建真实对象"""
        self._access_count += 1
        print(f"代理 {self.name}: 收到第 {self._access_count} 次请求")
        
        # 延迟创建真实对象
        if self._real_subject is None:
            print(f"代理 {self.name}: 首次访问，创建真实对象")
            self._real_subject = RealSubject(self.name)
        else:
            print(f"代理 {self.name}: 复用现有真实对象")
        
        # 委托给真实对象
        return self._real_subject.request()
    
    def get_info(self) -> str:
        """获取信息 - 不需要创建真实对象"""
        return f"代理对象信息: {self.name} (访问次数: {self._access_count})"


# ==================== 保护代理 ====================
class ProtectionProxy(Subject):
    """保护代理 - 控制访问权限"""
    
    def __init__(self, real_subject: RealSubject, user_role: str):
        self._real_subject = real_subject
        self._user_role = user_role
        self._allowed_roles = {"admin", "user"}
        print(f"创建保护代理，用户角色: {user_role}")
    
    def request(self) -> str:
        """处理请求 - 检查权限"""
        if not self._check_access():
            return f"访问被拒绝: 用户角色 '{self._user_role}' 没有访问权限"
        
        print(f"保护代理: 权限验证通过，转发请求")
        return self._real_subject.request()
    
    def get_info(self) -> str:
        """获取信息"""
        if not self._check_access():
            return f"访问被拒绝: 用户角色 '{self._user_role}' 没有访问权限"
        
        return self._real_subject.get_info()
    
    def _check_access(self) -> bool:
        """检查访问权限"""
        has_access = self._user_role in self._allowed_roles
        print(f"保护代理: 检查权限 - 角色 '{self._user_role}' {'有' if has_access else '无'}访问权限")
        return has_access


# ==================== 日志代理 ====================
class LoggingProxy(Subject):
    """日志代理 - 记录访问日志"""
    
    def __init__(self, real_subject: RealSubject):
        self._real_subject = real_subject
        self._request_count = 0
        print(f"创建日志代理")
    
    def request(self) -> str:
        """处理请求 - 记录日志"""
        self._request_count += 1
        start_time = time.time()
        
        print(f"日志代理: [请求开始] 第 {self._request_count} 次请求")
        
        try:
            result = self._real_subject.request()
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"日志代理: [请求成功] 耗时 {duration:.2f} 秒")
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"日志代理: [请求失败] 耗时 {duration:.2f} 秒，错误: {e}")
            raise
    
    def get_info(self) -> str:
        """获取信息"""
        print(f"日志代理: 获取信息请求")
        return self._real_subject.get_info() + f" (总请求次数: {self._request_count})"


# ==================== 客户端代码 ====================
class Client:
    """客户端 - 使用代理对象"""
    
    def __init__(self):
        self.subjects = []
    
    def add_subject(self, subject: Subject, name: str):
        """添加主题对象"""
        self.subjects.append((subject, name))
        print(f"客户端: 添加主题对象 '{name}'")
    
    def execute_requests(self):
        """执行请求"""
        print(f"\n客户端: 开始执行请求...")
        
        for subject, name in self.subjects:
            print(f"\n--- 处理 {name} ---")
            
            # 获取信息
            info = subject.get_info()
            print(f"信息: {info}")
            
            # 执行请求
            result = subject.request()
            print(f"结果: {result}")


# ==================== 使用示例 ====================
def demo_virtual_proxy():
    """虚拟代理演示"""
    print("=" * 60)
    print("🔄 虚拟代理演示 - 延迟加载")
    print("=" * 60)
    
    # 创建虚拟代理
    proxy = VirtualProxy("重要服务")
    
    print("\n📋 获取代理信息（不会创建真实对象）:")
    info = proxy.get_info()
    print(f"信息: {info}")
    
    print("\n🚀 第一次请求（会创建真实对象）:")
    result1 = proxy.request()
    print(f"结果: {result1}")
    
    print("\n🚀 第二次请求（复用真实对象）:")
    result2 = proxy.request()
    print(f"结果: {result2}")


def demo_protection_proxy():
    """保护代理演示"""
    print("\n" + "=" * 60)
    print("🛡️ 保护代理演示 - 权限控制")
    print("=" * 60)
    
    # 创建真实对象
    real_subject = RealSubject("敏感服务")
    
    # 创建不同权限的代理
    admin_proxy = ProtectionProxy(real_subject, "admin")
    user_proxy = ProtectionProxy(real_subject, "user")
    guest_proxy = ProtectionProxy(real_subject, "guest")
    
    proxies = [
        (admin_proxy, "管理员代理"),
        (user_proxy, "用户代理"),
        (guest_proxy, "访客代理")
    ]
    
    for proxy, name in proxies:
        print(f"\n--- {name} ---")
        info = proxy.get_info()
        print(f"信息: {info}")
        
        result = proxy.request()
        print(f"结果: {result}")


def demo_logging_proxy():
    """日志代理演示"""
    print("\n" + "=" * 60)
    print("📝 日志代理演示 - 访问记录")
    print("=" * 60)
    
    # 创建真实对象和日志代理
    real_subject = RealSubject("业务服务")
    logging_proxy = LoggingProxy(real_subject)
    
    print("\n🔍 执行多次请求:")
    for i in range(3):
        print(f"\n--- 第 {i+1} 次请求 ---")
        result = logging_proxy.request()
        print(f"结果: {result}")
    
    print(f"\n📊 最终信息:")
    info = logging_proxy.get_info()
    print(f"信息: {info}")


def demo_proxy_chain():
    """代理链演示 - 多个代理组合使用"""
    print("\n" + "=" * 60)
    print("🔗 代理链演示 - 组合使用")
    print("=" * 60)
    
    # 创建真实对象
    real_subject = RealSubject("核心服务")
    
    # 创建代理链：日志代理 -> 保护代理 -> 真实对象
    protection_proxy = ProtectionProxy(real_subject, "admin")
    logging_proxy = LoggingProxy(protection_proxy)
    
    print("\n🔗 通过代理链访问:")
    
    # 获取信息
    info = logging_proxy.get_info()
    print(f"信息: {info}")
    
    # 执行请求
    result = logging_proxy.request()
    print(f"结果: {result}")


def demo_client_usage():
    """客户端使用演示"""
    print("\n" + "=" * 60)
    print("👤 客户端使用演示 - 透明性")
    print("=" * 60)
    
    client = Client()
    
    # 添加不同类型的主题对象
    real_subject = RealSubject("直接服务")
    virtual_proxy = VirtualProxy("虚拟服务")
    protection_proxy = ProtectionProxy(RealSubject("保护服务"), "admin")
    
    client.add_subject(real_subject, "真实对象")
    client.add_subject(virtual_proxy, "虚拟代理")
    client.add_subject(protection_proxy, "保护代理")
    
    # 客户端透明地使用所有对象
    client.execute_requests()


def main():
    """主演示函数"""
    demo_virtual_proxy()
    demo_protection_proxy()
    demo_logging_proxy()
    demo_proxy_chain()
    demo_client_usage()
    
    print("\n" + "=" * 60)
    print("🎉 代理模式基础演示完成！")
    print("💡 关键要点:")
    print("   • 代理对象与真实对象实现相同接口")
    print("   • 虚拟代理可以延迟创建昂贵的对象")
    print("   • 保护代理可以控制访问权限")
    print("   • 代理可以添加额外功能而不修改真实对象")
    print("   • 多个代理可以组合使用形成代理链")
    print("=" * 60)


if __name__ == "__main__":
    main()
