"""
04_remote_proxy.py - 远程代理示例

这个示例展示了远程代理在分布式系统中的应用。
包括网络服务代理、API调用封装和错误处理重试机制。
"""

import json
import time
import random
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime
import urllib.parse


class ServiceStatus(Enum):
    """服务状态枚举"""
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    OVERLOADED = "overloaded"


class RequestMethod(Enum):
    """请求方法枚举"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


# ==================== 远程服务接口 ====================
class RemoteService(ABC):
    """远程服务抽象接口"""
    
    @abstractmethod
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """获取用户档案"""
        pass
    
    @abstractmethod
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """更新用户档案"""
        pass
    
    @abstractmethod
    def get_order_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取订单历史"""
        pass
    
    @abstractmethod
    def create_order(self, user_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建订单"""
        pass
    
    @abstractmethod
    def get_service_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        pass


# ==================== 真实远程服务 ====================
class ActualRemoteService(RemoteService):
    """实际的远程服务（模拟）"""
    
    def __init__(self, service_name: str, base_url: str):
        self.service_name = service_name
        self.base_url = base_url
        self.status = ServiceStatus.ONLINE
        self.request_count = 0
        self.error_rate = 0.1  # 10% 错误率
        print(f"远程服务 '{service_name}' 初始化完成: {base_url}")
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """获取用户档案"""
        self._simulate_network_request("GET", f"/users/{user_id}")
        
        return {
            "user_id": user_id,
            "name": f"用户{user_id}",
            "email": f"user{user_id}@example.com",
            "phone": f"138{user_id}0000",
            "address": f"地址{user_id}",
            "created_at": "2023-01-01T00:00:00Z",
            "last_updated": datetime.now().isoformat()
        }
    
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """更新用户档案"""
        self._simulate_network_request("PUT", f"/users/{user_id}", profile_data)
        return True
    
    def get_order_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取订单历史"""
        self._simulate_network_request("GET", f"/users/{user_id}/orders?limit={limit}")
        
        orders = []
        for i in range(min(limit, 5)):  # 最多返回5个订单
            orders.append({
                "order_id": f"ORD{user_id}{i+1:03d}",
                "user_id": user_id,
                "total_amount": 99.99 + i * 50,
                "status": "completed",
                "created_at": f"2023-{i+1:02d}-01T00:00:00Z",
                "items_count": i + 1
            })
        
        return orders
    
    def create_order(self, user_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建订单"""
        order_data = {
            "user_id": user_id,
            "items": items,
            "total_amount": sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
        }
        
        self._simulate_network_request("POST", "/orders", order_data)
        
        order_id = f"ORD{user_id}{int(time.time()) % 10000:04d}"
        return {
            "order_id": order_id,
            "user_id": user_id,
            "items": items,
            "total_amount": order_data["total_amount"],
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
    
    def get_service_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        self._simulate_network_request("GET", "/health")
        
        return {
            "service_name": self.service_name,
            "status": self.status.value,
            "uptime": "99.9%",
            "request_count": self.request_count,
            "last_check": datetime.now().isoformat()
        }
    
    def _simulate_network_request(self, method: str, endpoint: str, data: Any = None):
        """模拟网络请求"""
        self.request_count += 1
        
        # 模拟网络延迟
        network_delay = random.uniform(0.1, 0.5)
        time.sleep(network_delay)
        
        # 模拟网络错误
        if random.random() < self.error_rate:
            error_types = ["timeout", "connection_error", "server_error"]
            error_type = random.choice(error_types)
            raise NetworkError(f"网络错误: {error_type} - {method} {endpoint}")
        
        # 模拟服务状态变化
        if self.request_count % 20 == 0:
            self.status = random.choice(list(ServiceStatus))
            if self.status != ServiceStatus.ONLINE:
                raise ServiceUnavailableError(f"服务不可用: {self.status.value}")
        
        print(f"网络请求: {method} {self.base_url}{endpoint} - 耗时 {network_delay:.2f}s")


# ==================== 自定义异常 ====================
class NetworkError(Exception):
    """网络错误"""
    pass


class ServiceUnavailableError(Exception):
    """服务不可用错误"""
    pass


class RetryExhaustedError(Exception):
    """重试次数耗尽错误"""
    pass


# ==================== 远程代理 ====================
class RemoteServiceProxy(RemoteService):
    """远程服务代理"""
    
    def __init__(self, remote_service: ActualRemoteService, max_retries: int = 3, 
                 retry_delay: float = 1.0, timeout: float = 10.0):
        self.remote_service = remote_service
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.retry_count = 0
        print(f"远程代理已创建: 最大重试={max_retries}, 重试延迟={retry_delay}s, 超时={timeout}s")
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """获取用户档案 - 带重试机制"""
        return self._execute_with_retry(
            lambda: self.remote_service.get_user_profile(user_id),
            f"获取用户档案: {user_id}"
        )
    
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """更新用户档案 - 带重试机制"""
        return self._execute_with_retry(
            lambda: self.remote_service.update_user_profile(user_id, profile_data),
            f"更新用户档案: {user_id}"
        )
    
    def get_order_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取订单历史 - 带重试机制"""
        return self._execute_with_retry(
            lambda: self.remote_service.get_order_history(user_id, limit),
            f"获取订单历史: {user_id}"
        )
    
    def create_order(self, user_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建订单 - 带重试机制"""
        return self._execute_with_retry(
            lambda: self.remote_service.create_order(user_id, items),
            f"创建订单: {user_id}"
        )
    
    def get_service_status(self) -> Dict[str, Any]:
        """获取服务状态 - 带重试机制"""
        return self._execute_with_retry(
            lambda: self.remote_service.get_service_status(),
            "获取服务状态"
        )
    
    def _execute_with_retry(self, operation, operation_name: str):
        """执行操作并处理重试"""
        self.request_count += 1
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                print(f"远程代理: {operation_name} - 尝试 {attempt + 1}/{self.max_retries + 1}")
                
                # 执行操作
                result = operation()
                
                if attempt > 0:
                    print(f"远程代理: {operation_name} - 重试成功")
                
                self.success_count += 1
                return result
                
            except (NetworkError, ServiceUnavailableError) as e:
                last_error = e
                self.error_count += 1
                
                if attempt < self.max_retries:
                    self.retry_count += 1
                    retry_delay = self.retry_delay * (2 ** attempt)  # 指数退避
                    print(f"远程代理: {operation_name} - 失败，{retry_delay:.1f}秒后重试: {e}")
                    time.sleep(retry_delay)
                else:
                    print(f"远程代理: {operation_name} - 重试次数耗尽")
                    break
            
            except Exception as e:
                # 其他类型的错误不重试
                print(f"远程代理: {operation_name} - 不可重试的错误: {e}")
                self.error_count += 1
                raise
        
        # 重试次数耗尽
        raise RetryExhaustedError(f"操作失败，重试次数耗尽: {last_error}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取代理统计信息"""
        success_rate = (self.success_count / self.request_count * 100) if self.request_count > 0 else 0
        
        return {
            "total_requests": self.request_count,
            "successful_requests": self.success_count,
            "failed_requests": self.error_count,
            "retry_attempts": self.retry_count,
            "success_rate": round(success_rate, 1),
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay
        }


# ==================== 负载均衡代理 ====================
class LoadBalancingProxy(RemoteService):
    """负载均衡代理"""
    
    def __init__(self, services: List[RemoteServiceProxy]):
        self.services = services
        self.current_index = 0
        self.request_count = 0
        print(f"负载均衡代理已创建: {len(services)} 个服务实例")
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """获取用户档案 - 负载均衡"""
        return self._execute_with_load_balancing(
            lambda service: service.get_user_profile(user_id)
        )
    
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """更新用户档案 - 负载均衡"""
        return self._execute_with_load_balancing(
            lambda service: service.update_user_profile(user_id, profile_data)
        )
    
    def get_order_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取订单历史 - 负载均衡"""
        return self._execute_with_load_balancing(
            lambda service: service.get_order_history(user_id, limit)
        )
    
    def create_order(self, user_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建订单 - 负载均衡"""
        return self._execute_with_load_balancing(
            lambda service: service.create_order(user_id, items)
        )
    
    def get_service_status(self) -> Dict[str, Any]:
        """获取服务状态 - 负载均衡"""
        return self._execute_with_load_balancing(
            lambda service: service.get_service_status()
        )
    
    def _execute_with_load_balancing(self, operation):
        """执行负载均衡操作"""
        self.request_count += 1
        
        # 轮询选择服务
        service = self._get_next_service()
        service_index = self.services.index(service)
        
        try:
            print(f"负载均衡: 使用服务实例 {service_index + 1}")
            return operation(service)
        except Exception as e:
            print(f"负载均衡: 服务实例 {service_index + 1} 失败，尝试其他实例")
            
            # 尝试其他服务实例
            for i, backup_service in enumerate(self.services):
                if backup_service != service:
                    try:
                        print(f"负载均衡: 尝试备用服务实例 {i + 1}")
                        return operation(backup_service)
                    except Exception:
                        continue
            
            # 所有服务都失败
            raise e
    
    def _get_next_service(self) -> RemoteServiceProxy:
        """获取下一个服务（轮询）"""
        service = self.services[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.services)
        return service
    
    def get_all_statistics(self) -> Dict[str, Any]:
        """获取所有服务的统计信息"""
        stats = {
            "load_balancer": {
                "total_requests": self.request_count,
                "service_count": len(self.services)
            },
            "services": []
        }
        
        for i, service in enumerate(self.services):
            service_stats = service.get_statistics()
            service_stats["service_index"] = i + 1
            stats["services"].append(service_stats)
        
        return stats


# ==================== 使用示例 ====================
def demo_remote_proxy():
    """远程代理演示"""
    print("=" * 60)
    print("🌐 远程代理演示 - 网络服务访问")
    print("=" * 60)
    
    # 创建远程服务和代理
    remote_service = ActualRemoteService("用户服务", "https://api.example.com")
    proxy = RemoteServiceProxy(remote_service, max_retries=3, retry_delay=0.5)
    
    user_id = "12345"
    
    print(f"\n👤 测试用户操作: {user_id}")
    
    try:
        # 获取用户档案
        print("\n--- 获取用户档案 ---")
        profile = proxy.get_user_profile(user_id)
        print(f"用户档案: {profile['name']}, {profile['email']}")
        
        # 更新用户档案
        print("\n--- 更新用户档案 ---")
        update_data = {"phone": "13900000000", "address": "新地址"}
        success = proxy.update_user_profile(user_id, update_data)
        print(f"更新结果: {'成功' if success else '失败'}")
        
        # 获取订单历史
        print("\n--- 获取订单历史 ---")
        orders = proxy.get_order_history(user_id, limit=3)
        print(f"订单历史: 找到 {len(orders)} 个订单")
        for order in orders:
            print(f"  订单 {order['order_id']}: ¥{order['total_amount']}")
        
        # 创建新订单
        print("\n--- 创建新订单 ---")
        items = [
            {"product_id": "P001", "name": "商品1", "price": 99.99, "quantity": 2},
            {"product_id": "P002", "name": "商品2", "price": 149.99, "quantity": 1}
        ]
        new_order = proxy.create_order(user_id, items)
        print(f"新订单: {new_order['order_id']}, 总金额: ¥{new_order['total_amount']}")
        
    except RetryExhaustedError as e:
        print(f"操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")
    
    # 显示统计信息
    print(f"\n📊 代理统计信息:")
    stats = proxy.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def demo_load_balancing():
    """负载均衡演示"""
    print("\n" + "=" * 60)
    print("⚖️ 负载均衡代理演示")
    print("=" * 60)
    
    # 创建多个服务实例
    services = []
    for i in range(3):
        remote_service = ActualRemoteService(f"服务实例{i+1}", f"https://api{i+1}.example.com")
        proxy = RemoteServiceProxy(remote_service, max_retries=2, retry_delay=0.3)
        services.append(proxy)
    
    # 创建负载均衡代理
    load_balancer = LoadBalancingProxy(services)
    
    print(f"\n🔄 执行多个请求测试负载均衡:")
    
    # 执行多个请求
    for i in range(6):
        try:
            print(f"\n--- 请求 {i+1} ---")
            status = load_balancer.get_service_status()
            print(f"服务状态: {status['service_name']} - {status['status']}")
            
        except Exception as e:
            print(f"请求失败: {e}")
    
    # 显示所有统计信息
    print(f"\n📊 负载均衡统计:")
    all_stats = load_balancer.get_all_statistics()
    
    print(f"负载均衡器: {all_stats['load_balancer']}")
    
    for service_stats in all_stats['services']:
        print(f"服务 {service_stats['service_index']}: "
              f"成功率 {service_stats['success_rate']}%, "
              f"请求数 {service_stats['total_requests']}, "
              f"重试数 {service_stats['retry_attempts']}")


def demo_error_handling():
    """错误处理演示"""
    print("\n" + "=" * 60)
    print("🚨 错误处理和重试演示")
    print("=" * 60)
    
    # 创建高错误率的服务
    remote_service = ActualRemoteService("不稳定服务", "https://unstable.example.com")
    remote_service.error_rate = 0.7  # 70% 错误率
    
    proxy = RemoteServiceProxy(remote_service, max_retries=5, retry_delay=0.2)
    
    print(f"\n🎯 测试高错误率服务 (错误率: {remote_service.error_rate * 100}%):")
    
    # 尝试多次操作
    for i in range(3):
        try:
            print(f"\n--- 尝试 {i+1} ---")
            status = proxy.get_service_status()
            print(f"成功获取状态: {status['service_name']}")
            
        except RetryExhaustedError as e:
            print(f"重试耗尽: {e}")
        except Exception as e:
            print(f"其他错误: {e}")
    
    # 显示最终统计
    print(f"\n📊 错误处理统计:")
    stats = proxy.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def main():
    """主演示函数"""
    demo_remote_proxy()
    demo_load_balancing()
    demo_error_handling()
    
    print("\n" + "=" * 60)
    print("🎉 远程代理演示完成！")
    print("💡 关键要点:")
    print("   • 远程代理封装网络通信的复杂性")
    print("   • 提供重试机制处理网络不稳定")
    print("   • 负载均衡提高系统可用性")
    print("   • 透明地处理分布式系统的挑战")
    print("   • 在微服务架构中非常有用")
    print("=" * 60)


if __name__ == "__main__":
    main()
