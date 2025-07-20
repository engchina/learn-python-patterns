"""
02_request_processing.py - 请求处理系统示例

这个示例展示了责任链模式在Web开发中的应用。
包括HTTP请求处理链、认证授权、业务逻辑处理和中间件模式的实现。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import json
import time


class HttpMethod(Enum):
    """HTTP方法枚举"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HttpStatus(Enum):
    """HTTP状态码枚举"""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# ==================== HTTP请求和响应 ====================
class HttpRequest:
    """HTTP请求对象"""
    
    def __init__(self, method: HttpMethod, path: str, headers: Dict[str, str] = None,
                 body: str = "", query_params: Dict[str, str] = None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body
        self.query_params = query_params or {}
        self.user = None  # 认证后的用户信息
        self.context = {}  # 请求上下文
        self.start_time = time.time()
        self.middleware_chain = []  # 中间件处理链记录
    
    def get_header(self, name: str, default: str = "") -> str:
        """获取请求头"""
        return self.headers.get(name.lower(), default)
    
    def get_query_param(self, name: str, default: str = "") -> str:
        """获取查询参数"""
        return self.query_params.get(name, default)
    
    def add_middleware_record(self, middleware_name: str):
        """添加中间件处理记录"""
        self.middleware_chain.append(middleware_name)
    
    def get_processing_time(self) -> float:
        """获取处理时间"""
        return time.time() - self.start_time


class HttpResponse:
    """HTTP响应对象"""
    
    def __init__(self, status: HttpStatus = HttpStatus.OK, 
                 body: str = "", headers: Dict[str, str] = None):
        self.status = status
        self.body = body
        self.headers = headers or {}
        self.headers.setdefault("content-type", "text/plain")
    
    def set_json(self, data: Any):
        """设置JSON响应"""
        self.body = json.dumps(data, ensure_ascii=False, indent=2)
        self.headers["content-type"] = "application/json"
    
    def set_header(self, name: str, value: str):
        """设置响应头"""
        self.headers[name] = value


# ==================== 抽象中间件 ====================
class Middleware(ABC):
    """抽象中间件"""
    
    def __init__(self, name: str):
        self.name = name
        self._next_middleware: Optional['Middleware'] = None
    
    def set_next(self, middleware: 'Middleware') -> 'Middleware':
        """设置下一个中间件"""
        self._next_middleware = middleware
        return middleware
    
    def process(self, request: HttpRequest) -> Optional[HttpResponse]:
        """处理请求"""
        request.add_middleware_record(self.name)
        
        # 执行当前中间件的处理逻辑
        response = self._process_request(request)
        
        if response is not None:
            # 当前中间件返回了响应，停止链的传递
            print(f"{self.name}: 处理完成，返回响应")
            return response
        elif self._next_middleware:
            # 传递给下一个中间件
            print(f"{self.name}: 处理完成，传递给下一个中间件")
            return self._next_middleware.process(request)
        else:
            # 链的末端
            print(f"{self.name}: 链的末端，没有更多中间件")
            return HttpResponse(HttpStatus.NOT_FOUND, "未找到处理器")
    
    @abstractmethod
    def _process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """具体的请求处理逻辑"""
        pass


# ==================== 具体中间件实现 ====================
class LoggingMiddleware(Middleware):
    """日志中间件"""
    
    def __init__(self):
        super().__init__("日志中间件")
        self.request_count = 0
    
    def _process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """记录请求日志"""
        self.request_count += 1
        
        print(f"{self.name}: [{self.request_count}] {request.method.value} {request.path}")
        print(f"  请求头: {request.headers}")
        print(f"  查询参数: {request.query_params}")
        
        # 不返回响应，继续传递
        return None


class CorsMiddleware(Middleware):
    """CORS中间件"""
    
    def __init__(self):
        super().__init__("CORS中间件")
    
    def _process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """处理CORS"""
        print(f"{self.name}: 添加CORS头")
        
        # 将CORS信息添加到请求上下文
        request.context["cors_headers"] = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
        
        # 处理预检请求
        if request.method.value == "OPTIONS":
            response = HttpResponse(HttpStatus.OK)
            for key, value in request.context["cors_headers"].items():
                response.set_header(key, value)
            return response
        
        # 不返回响应，继续传递
        return None


class AuthenticationMiddleware(Middleware):
    """认证中间件"""
    
    def __init__(self):
        super().__init__("认证中间件")
        # 模拟用户数据库
        self.users = {
            "token123": {"user_id": "1", "username": "admin", "role": "admin"},
            "token456": {"user_id": "2", "username": "user", "role": "user"},
            "token789": {"user_id": "3", "username": "guest", "role": "guest"}
        }
    
    def _process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """验证用户身份"""
        # 检查是否需要认证
        if self._is_public_path(request.path):
            print(f"{self.name}: 公开路径，跳过认证")
            return None
        
        # 获取认证令牌
        auth_header = request.get_header("authorization")
        if not auth_header.startswith("Bearer "):
            print(f"{self.name}: 缺少认证令牌")
            return HttpResponse(HttpStatus.UNAUTHORIZED, "需要认证")
        
        token = auth_header[7:]  # 移除 "Bearer " 前缀
        
        # 验证令牌
        user_info = self.users.get(token)
        if not user_info:
            print(f"{self.name}: 无效的认证令牌")
            return HttpResponse(HttpStatus.UNAUTHORIZED, "认证失败")
        
        # 设置用户信息
        request.user = user_info
        print(f"{self.name}: 用户认证成功 - {user_info['username']} ({user_info['role']})")
        
        # 不返回响应，继续传递
        return None
    
    def _is_public_path(self, path: str) -> bool:
        """检查是否为公开路径"""
        public_paths = ["/", "/health", "/login", "/register"]
        return path in public_paths


class AuthorizationMiddleware(Middleware):
    """授权中间件"""
    
    def __init__(self):
        super().__init__("授权中间件")
        # 路径权限配置
        self.path_permissions = {
            "/admin": ["admin"],
            "/users": ["admin", "user"],
            "/profile": ["admin", "user", "guest"]
        }
    
    def _process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """检查用户权限"""
        # 如果没有用户信息，说明是公开路径或认证失败
        if not request.user:
            return None
        
        # 检查路径权限
        required_roles = self.path_permissions.get(request.path)
        if not required_roles:
            print(f"{self.name}: 路径无权限限制")
            return None
        
        user_role = request.user.get("role")
        if user_role not in required_roles:
            print(f"{self.name}: 权限不足 - 需要 {required_roles}, 当前 {user_role}")
            return HttpResponse(HttpStatus.FORBIDDEN, "权限不足")
        
        print(f"{self.name}: 权限验证通过 - {user_role}")
        
        # 不返回响应，继续传递
        return None


class RateLimitMiddleware(Middleware):
    """限流中间件"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        super().__init__("限流中间件")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_history = {}  # IP -> [timestamp, ...]
    
    def _process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """检查请求频率"""
        # 获取客户端IP（模拟）
        client_ip = request.get_header("x-forwarded-for", "127.0.0.1")
        
        current_time = time.time()
        
        # 清理过期记录
        if client_ip in self.request_history:
            self.request_history[client_ip] = [
                timestamp for timestamp in self.request_history[client_ip]
                if current_time - timestamp < self.window_seconds
            ]
        else:
            self.request_history[client_ip] = []
        
        # 检查请求频率
        request_count = len(self.request_history[client_ip])
        if request_count >= self.max_requests:
            print(f"{self.name}: 请求频率过高 - IP: {client_ip}, 请求数: {request_count}")
            return HttpResponse(HttpStatus.BAD_REQUEST, "请求频率过高")
        
        # 记录当前请求
        self.request_history[client_ip].append(current_time)
        print(f"{self.name}: 请求通过 - IP: {client_ip}, 当前请求数: {request_count + 1}")
        
        # 不返回响应，继续传递
        return None


class BusinessLogicMiddleware(Middleware):
    """业务逻辑中间件"""
    
    def __init__(self):
        super().__init__("业务逻辑中间件")
        # 模拟数据
        self.users_data = {
            "1": {"id": "1", "name": "管理员", "email": "admin@example.com"},
            "2": {"id": "2", "name": "普通用户", "email": "user@example.com"},
            "3": {"id": "3", "name": "访客", "email": "guest@example.com"}
        }
    
    def _process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """处理业务逻辑"""
        print(f"{self.name}: 处理业务逻辑 - {request.method.value} {request.path}")
        
        # 根据路径和方法处理不同的业务逻辑
        if request.path == "/" and request.method == HttpMethod.GET:
            response = HttpResponse(HttpStatus.OK, "欢迎使用API服务")
        
        elif request.path == "/health" and request.method == HttpMethod.GET:
            health_data = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime": "99.9%"
            }
            response = HttpResponse(HttpStatus.OK)
            response.set_json(health_data)
        
        elif request.path == "/users" and request.method == HttpMethod.GET:
            response = HttpResponse(HttpStatus.OK)
            response.set_json(list(self.users_data.values()))
        
        elif request.path == "/profile" and request.method == HttpMethod.GET:
            if request.user:
                user_id = request.user["user_id"]
                user_data = self.users_data.get(user_id, {})
                response = HttpResponse(HttpStatus.OK)
                response.set_json(user_data)
            else:
                response = HttpResponse(HttpStatus.UNAUTHORIZED, "需要认证")
        
        else:
            response = HttpResponse(HttpStatus.NOT_FOUND, "未找到资源")
        
        # 添加CORS头（如果存在）
        if "cors_headers" in request.context:
            for key, value in request.context["cors_headers"].items():
                response.set_header(key, value)
        
        # 添加处理时间头
        processing_time = request.get_processing_time()
        response.set_header("X-Processing-Time", f"{processing_time:.3f}s")
        
        return response


# ==================== 请求处理器 ====================
class RequestProcessor:
    """请求处理器"""
    
    def __init__(self):
        self.middleware_chain = None
        self.processed_requests = []
    
    def setup_middleware_chain(self) -> 'RequestProcessor':
        """设置中间件链"""
        # 构建中间件链
        logging = LoggingMiddleware()
        cors = CorsMiddleware()
        rate_limit = RateLimitMiddleware(max_requests=5, window_seconds=30)
        auth = AuthenticationMiddleware()
        authz = AuthorizationMiddleware()
        business = BusinessLogicMiddleware()
        
        # 连接中间件链
        self.middleware_chain = (logging
                                .set_next(cors)
                                .set_next(rate_limit)
                                .set_next(auth)
                                .set_next(authz)
                                .set_next(business))
        
        print("中间件链设置完成:")
        current = logging
        index = 1
        while current:
            print(f"  {index}. {current.name}")
            current = current._next_middleware
            index += 1
        
        return self
    
    def process_request(self, request: HttpRequest) -> HttpResponse:
        """处理HTTP请求"""
        print(f"\n🌐 处理请求: {request.method.value} {request.path}")
        
        if not self.middleware_chain:
            return HttpResponse(HttpStatus.INTERNAL_SERVER_ERROR, "中间件链未设置")
        
        # 通过中间件链处理请求
        response = self.middleware_chain.process(request)
        
        # 记录处理结果
        self.processed_requests.append({
            "request": request,
            "response": response,
            "processing_time": request.get_processing_time(),
            "middleware_chain": request.middleware_chain
        })
        
        print(f"📤 响应: {response.status.value} - {response.body[:50]}...")
        print(f"⏱️ 处理时间: {request.get_processing_time():.3f}s")
        
        return response
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取处理统计"""
        if not self.processed_requests:
            return {"total_requests": 0}
        
        total_requests = len(self.processed_requests)
        avg_processing_time = sum(req["processing_time"] for req in self.processed_requests) / total_requests
        
        status_counts = {}
        for req in self.processed_requests:
            status = req["response"].status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_requests": total_requests,
            "average_processing_time": round(avg_processing_time, 3),
            "status_distribution": status_counts
        }


# ==================== 使用示例 ====================
def demo_request_processing():
    """请求处理演示"""
    print("=" * 60)
    print("🌐 HTTP请求处理链演示")
    print("=" * 60)
    
    # 创建请求处理器并设置中间件链
    processor = RequestProcessor().setup_middleware_chain()
    
    # 创建各种HTTP请求
    requests = [
        # 公开请求
        HttpRequest(HttpMethod.GET, "/", {"user-agent": "test-client"}),
        HttpRequest(HttpMethod.GET, "/health"),
        
        # 需要认证的请求
        HttpRequest(HttpMethod.GET, "/profile", {"authorization": "Bearer token123"}),
        HttpRequest(HttpMethod.GET, "/users", {"authorization": "Bearer token123"}),
        
        # 权限不足的请求
        HttpRequest(HttpMethod.GET, "/admin", {"authorization": "Bearer token456"}),
        
        # 无效认证的请求
        HttpRequest(HttpMethod.GET, "/profile", {"authorization": "Bearer invalid"}),
        
        # 未认证的请求
        HttpRequest(HttpMethod.GET, "/profile"),
        
        # CORS预检请求
        HttpRequest(HttpMethod.GET, "/users", {
            "origin": "https://example.com",
            "access-control-request-method": "GET"
        })
    ]
    
    # 处理所有请求
    print(f"\n🚀 开始处理 {len(requests)} 个请求:")
    for i, request in enumerate(requests, 1):
        print(f"\n{'='*20} 请求 {i} {'='*20}")
        response = processor.process_request(request)
    
    # 显示统计信息
    print(f"\n📊 处理统计:")
    stats = processor.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def demo_rate_limiting():
    """限流演示"""
    print("\n" + "=" * 60)
    print("🚦 限流中间件演示")
    print("=" * 60)
    
    # 创建只有限流和业务逻辑的简单链
    rate_limit = RateLimitMiddleware(max_requests=3, window_seconds=10)
    business = BusinessLogicMiddleware()
    rate_limit.set_next(business)
    
    processor = RequestProcessor()
    processor.middleware_chain = rate_limit
    
    # 快速发送多个请求测试限流
    print("\n🔄 快速发送5个请求测试限流:")
    for i in range(5):
        request = HttpRequest(HttpMethod.GET, "/health", {"x-forwarded-for": "192.168.1.100"})
        print(f"\n--- 请求 {i+1} ---")
        response = processor.process_request(request)
        time.sleep(0.1)  # 短暂延迟
    
    # 显示统计
    stats = processor.get_statistics()
    print(f"\n📊 限流测试统计: {stats}")


def main():
    """主演示函数"""
    demo_request_processing()
    demo_rate_limiting()
    
    print("\n" + "=" * 60)
    print("🎉 请求处理链演示完成！")
    print("💡 关键要点:")
    print("   • 中间件链实现了请求的分层处理")
    print("   • 每个中间件专注于特定的功能")
    print("   • 可以灵活组合和调整中间件顺序")
    print("   • 支持早期返回和链式传递")
    print("   • 广泛应用于Web框架和API网关")
    print("=" * 60)


if __name__ == "__main__":
    main()
