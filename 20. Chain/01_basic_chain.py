"""
01_basic_chain.py - 责任链模式基础实现

这个示例展示了责任链模式的基本概念和实现方式。
包括基本的处理者接口、简单的请求处理链和链的构建使用演示。
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, List
from enum import Enum


class RequestType(Enum):
    """请求类型枚举"""
    HELP = "help"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Request:
    """请求对象"""
    
    def __init__(self, request_type: RequestType, message: str, data: Dict[str, Any] = None):
        self.request_type = request_type
        self.message = message
        self.data = data or {}
        self.handled = False
        self.handler_chain = []  # 记录处理链路
    
    def add_to_chain(self, handler_name: str):
        """添加到处理链路记录"""
        self.handler_chain.append(handler_name)
    
    def mark_handled(self, handler_name: str):
        """标记为已处理"""
        self.handled = True
        self.handler_chain.append(f"{handler_name} (已处理)")
    
    def get_info(self) -> str:
        """获取请求信息"""
        return f"请求类型: {self.request_type.value}, 消息: {self.message}"


# ==================== 抽象处理者 ====================
class Handler(ABC):
    """抽象处理者"""
    
    def __init__(self, name: str):
        self.name = name
        self._next_handler: Optional[Handler] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        """设置下一个处理者"""
        self._next_handler = handler
        return handler  # 返回下一个处理者，支持链式调用
    
    def handle(self, request: Request) -> Optional[str]:
        """处理请求"""
        request.add_to_chain(self.name)
        
        # 尝试处理请求
        result = self._handle_request(request)
        
        if result is not None:
            # 当前处理者能够处理请求
            request.mark_handled(self.name)
            return result
        elif self._next_handler:
            # 传递给下一个处理者
            print(f"{self.name}: 无法处理，传递给下一个处理者")
            return self._next_handler.handle(request)
        else:
            # 链的末端，没有处理者能处理
            print(f"{self.name}: 链的末端，请求未被处理")
            return None
    
    @abstractmethod
    def _handle_request(self, request: Request) -> Optional[str]:
        """具体的请求处理逻辑，由子类实现"""
        pass


# ==================== 具体处理者 ====================
class HelpHandler(Handler):
    """帮助请求处理者"""
    
    def __init__(self):
        super().__init__("帮助处理器")
    
    def _handle_request(self, request: Request) -> Optional[str]:
        """处理帮助请求"""
        if request.request_type == RequestType.HELP:
            print(f"{self.name}: 处理帮助请求")
            return f"帮助信息: {request.message} - 这里是相关的帮助文档"
        return None


class InfoHandler(Handler):
    """信息请求处理者"""
    
    def __init__(self):
        super().__init__("信息处理器")
    
    def _handle_request(self, request: Request) -> Optional[str]:
        """处理信息请求"""
        if request.request_type == RequestType.INFO:
            print(f"{self.name}: 处理信息请求")
            return f"信息响应: {request.message} - 请求已记录"
        return None


class WarningHandler(Handler):
    """警告请求处理者"""
    
    def __init__(self):
        super().__init__("警告处理器")
    
    def _handle_request(self, request: Request) -> Optional[str]:
        """处理警告请求"""
        if request.request_type == RequestType.WARNING:
            print(f"{self.name}: 处理警告请求")
            return f"警告处理: {request.message} - 已发送警告通知"
        return None


class ErrorHandler(Handler):
    """错误请求处理者"""
    
    def __init__(self):
        super().__init__("错误处理器")
    
    def _handle_request(self, request: Request) -> Optional[str]:
        """处理错误请求"""
        if request.request_type in [RequestType.ERROR, RequestType.CRITICAL]:
            print(f"{self.name}: 处理{request.request_type.value}请求")
            
            if request.request_type == RequestType.CRITICAL:
                return f"紧急处理: {request.message} - 已启动紧急响应程序"
            else:
                return f"错误处理: {request.message} - 错误已记录并通知相关人员"
        return None


class DefaultHandler(Handler):
    """默认处理者 - 处理所有未被处理的请求"""
    
    def __init__(self):
        super().__init__("默认处理器")
    
    def _handle_request(self, request: Request) -> Optional[str]:
        """处理所有类型的请求"""
        print(f"{self.name}: 处理未知类型请求")
        return f"默认处理: {request.message} - 请求已转发给系统管理员"


# ==================== 链构建器 ====================
class ChainBuilder:
    """责任链构建器"""
    
    def __init__(self):
        self.handlers: List[Handler] = []
    
    def add_handler(self, handler: Handler) -> 'ChainBuilder':
        """添加处理者"""
        self.handlers.append(handler)
        return self
    
    def build(self) -> Optional[Handler]:
        """构建责任链"""
        if not self.handlers:
            return None
        
        # 连接处理者
        for i in range(len(self.handlers) - 1):
            self.handlers[i].set_next(self.handlers[i + 1])
        
        print(f"责任链构建完成，包含 {len(self.handlers)} 个处理者:")
        for i, handler in enumerate(self.handlers):
            print(f"  {i + 1}. {handler.name}")
        
        return self.handlers[0]  # 返回链的第一个处理者


# ==================== 客户端 ====================
class Client:
    """客户端 - 使用责任链处理请求"""
    
    def __init__(self, chain: Handler):
        self.chain = chain
        self.processed_requests = []
    
    def send_request(self, request: Request) -> Optional[str]:
        """发送请求到责任链"""
        print(f"\n客户端: 发送请求 - {request.get_info()}")
        
        result = self.chain.handle(request)
        
        # 记录处理结果
        self.processed_requests.append({
            "request": request,
            "result": result,
            "handled": request.handled,
            "chain": request.handler_chain
        })
        
        if result:
            print(f"客户端: 请求处理成功 - {result}")
        else:
            print(f"客户端: 请求未被处理")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取处理统计信息"""
        total_requests = len(self.processed_requests)
        handled_requests = sum(1 for req in self.processed_requests if req["handled"])
        
        return {
            "total_requests": total_requests,
            "handled_requests": handled_requests,
            "unhandled_requests": total_requests - handled_requests,
            "success_rate": round(handled_requests / total_requests * 100, 1) if total_requests > 0 else 0
        }
    
    def show_request_history(self):
        """显示请求历史"""
        print(f"\n📋 请求处理历史:")
        for i, record in enumerate(self.processed_requests, 1):
            request = record["request"]
            print(f"\n{i}. {request.get_info()}")
            print(f"   处理链路: {' -> '.join(record['chain'])}")
            print(f"   处理结果: {'成功' if record['handled'] else '失败'}")
            if record["result"]:
                print(f"   响应: {record['result']}")


# ==================== 使用示例 ====================
def demo_basic_chain():
    """基础责任链演示"""
    print("=" * 60)
    print("🔗 责任链模式基础演示")
    print("=" * 60)
    
    # 构建责任链
    chain = (ChainBuilder()
             .add_handler(HelpHandler())
             .add_handler(InfoHandler())
             .add_handler(WarningHandler())
             .add_handler(ErrorHandler())
             .build())
    
    # 创建客户端
    client = Client(chain)
    
    # 创建各种类型的请求
    requests = [
        Request(RequestType.HELP, "如何使用系统？"),
        Request(RequestType.INFO, "用户登录成功", {"user_id": "123", "ip": "192.168.1.1"}),
        Request(RequestType.WARNING, "内存使用率过高", {"memory_usage": "85%"}),
        Request(RequestType.ERROR, "数据库连接失败", {"error_code": "DB001"}),
        Request(RequestType.CRITICAL, "系统即将崩溃", {"cpu_usage": "99%"})
    ]
    
    # 处理所有请求
    print(f"\n🚀 开始处理 {len(requests)} 个请求:")
    for request in requests:
        client.send_request(request)
    
    # 显示统计信息
    print(f"\n📊 处理统计:")
    stats = client.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 显示请求历史
    client.show_request_history()


def demo_chain_modification():
    """责任链修改演示"""
    print("\n" + "=" * 60)
    print("🔧 责任链动态修改演示")
    print("=" * 60)
    
    # 创建基础链
    help_handler = HelpHandler()
    info_handler = InfoHandler()
    error_handler = ErrorHandler()
    
    # 手动构建链
    help_handler.set_next(info_handler).set_next(error_handler)
    
    client = Client(help_handler)
    
    print("\n📝 原始链处理:")
    client.send_request(Request(RequestType.WARNING, "这是一个警告"))
    
    # 动态添加警告处理器
    print("\n🔧 动态添加警告处理器:")
    warning_handler = WarningHandler()
    
    # 重新组织链：help -> info -> warning -> error
    help_handler.set_next(info_handler)
    info_handler.set_next(warning_handler)
    warning_handler.set_next(error_handler)
    
    print("新的链结构已建立")
    
    print("\n📝 修改后的链处理:")
    client.send_request(Request(RequestType.WARNING, "这是一个警告"))
    
    # 显示统计
    stats = client.get_statistics()
    print(f"\n📊 最终统计: {stats}")


def demo_default_handler():
    """默认处理者演示"""
    print("\n" + "=" * 60)
    print("🛡️ 默认处理者演示")
    print("=" * 60)
    
    # 构建包含默认处理者的链
    chain = (ChainBuilder()
             .add_handler(HelpHandler())
             .add_handler(InfoHandler())
             .add_handler(DefaultHandler())  # 默认处理者放在最后
             .build())
    
    client = Client(chain)
    
    # 创建一些无法被特定处理者处理的请求
    unknown_requests = [
        Request(RequestType.WARNING, "未知警告类型"),
        Request(RequestType.ERROR, "未知错误类型"),
        Request(RequestType.CRITICAL, "未知紧急情况")
    ]
    
    print(f"\n🔍 处理未知类型请求:")
    for request in unknown_requests:
        client.send_request(request)
    
    # 显示处理历史
    client.show_request_history()


def main():
    """主演示函数"""
    demo_basic_chain()
    demo_chain_modification()
    demo_default_handler()
    
    print("\n" + "=" * 60)
    print("🎉 责任链模式基础演示完成！")
    print("💡 关键要点:")
    print("   • 责任链将请求发送者和接收者解耦")
    print("   • 每个处理者只关注自己能处理的请求")
    print("   • 可以动态地组合和修改处理链")
    print("   • 请求沿着链传递直到被处理或到达末端")
    print("   • 适用于多级处理和过滤场景")
    print("=" * 60)


if __name__ == "__main__":
    main()
