"""
05_real_world_examples.py - 外观模式的实际应用示例

这个文件展示了外观模式在实际开发中的常见应用场景，
包括API网关、日志系统、配置管理等实际场景。
"""

import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


# ==================== 示例1：API网关外观 ====================
class AuthenticationService:
    """认证服务"""
    
    def __init__(self):
        self.valid_tokens = {"token123": "user1", "token456": "user2"}
    
    def validate_token(self, token: str) -> Optional[str]:
        """验证令牌"""
        user_id = self.valid_tokens.get(token)
        if user_id:
            return f"认证服务: 令牌有效，用户ID: {user_id}"
        return "认证服务: 令牌无效"
    
    def get_user_permissions(self, user_id: str) -> List[str]:
        """获取用户权限"""
        permissions = {
            "user1": ["read", "write"],
            "user2": ["read"]
        }
        return permissions.get(user_id, [])


class RateLimitingService:
    """限流服务"""
    
    def __init__(self):
        self.request_counts = {}
        self.limit = 100  # 每分钟100次请求
    
    def check_rate_limit(self, user_id: str) -> bool:
        """检查限流"""
        current_minute = int(time.time() // 60)
        key = f"{user_id}:{current_minute}"
        
        count = self.request_counts.get(key, 0)
        if count >= self.limit:
            return False
        
        self.request_counts[key] = count + 1
        return True


class LoggingService:
    """日志服务"""
    
    def log_request(self, user_id: str, endpoint: str, method: str):
        """记录请求日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"日志服务: [{timestamp}] 用户{user_id} {method} {endpoint}"


class BackendService:
    """后端服务"""
    
    def __init__(self, name: str):
        self.name = name
    
    def process_request(self, data: Dict) -> Dict:
        """处理请求"""
        return {
            "service": self.name,
            "result": f"处理完成: {data}",
            "timestamp": datetime.now().isoformat()
        }


class APIGatewayFacade:
    """API网关外观"""
    
    def __init__(self):
        self.auth_service = AuthenticationService()
        self.rate_limiting = RateLimitingService()
        self.logging = LoggingService()
        self.services = {
            "user": BackendService("用户服务"),
            "order": BackendService("订单服务"),
            "product": BackendService("商品服务")
        }
    
    def handle_request(self, token: str, service_name: str, endpoint: str, 
                      method: str = "GET", data: Dict = None):
        """处理API请求"""
        print(f"🌐 API网关处理请求: {method} /{service_name}{endpoint}")
        
        # 1. 认证
        auth_result = self.auth_service.validate_token(token)
        print(f"  ✓ {auth_result}")
        
        if "无效" in auth_result:
            return {"error": "认证失败", "code": 401}
        
        user_id = auth_result.split("用户ID: ")[1]
        
        # 2. 限流检查
        if not self.rate_limiting.check_rate_limit(user_id):
            print("  ❌ 限流服务: 请求频率过高")
            return {"error": "请求频率过高", "code": 429}
        
        print("  ✓ 限流服务: 请求通过")
        
        # 3. 记录日志
        log_msg = self.logging.log_request(user_id, endpoint, method)
        print(f"  ✓ {log_msg}")
        
        # 4. 路由到后端服务
        if service_name in self.services:
            service = self.services[service_name]
            result = service.process_request(data or {})
            print(f"  ✓ 后端服务: {service.name}处理完成")
            return result
        else:
            return {"error": "服务不存在", "code": 404}


# ==================== 示例2：日志系统外观 ====================
class FileLogger:
    """文件日志器"""
    
    def write(self, level: str, message: str):
        return f"文件日志器: [{level}] {message} -> 写入文件"


class DatabaseLogger:
    """数据库日志器"""
    
    def write(self, level: str, message: str):
        return f"数据库日志器: [{level}] {message} -> 写入数据库"


class EmailNotifier:
    """邮件通知器"""
    
    def send_alert(self, level: str, message: str):
        if level in ["ERROR", "CRITICAL"]:
            return f"邮件通知器: 发送告警邮件 - {message}"
        return None


class LogFormatter:
    """日志格式化器"""
    
    def format(self, level: str, message: str, context: Dict = None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] [{level}] {message}"
        if context:
            formatted += f" | 上下文: {json.dumps(context, ensure_ascii=False)}"
        return formatted


class LoggingFacade:
    """日志系统外观"""
    
    def __init__(self):
        self.file_logger = FileLogger()
        self.db_logger = DatabaseLogger()
        self.email_notifier = EmailNotifier()
        self.formatter = LogFormatter()
    
    def log(self, level: str, message: str, context: Dict = None):
        """统一日志接口"""
        print(f"📝 日志系统记录: {level} - {message}")
        
        # 格式化日志
        formatted_msg = self.formatter.format(level, message, context)
        print(f"  ✓ 日志格式化器: 格式化完成")
        
        # 写入文件
        file_result = self.file_logger.write(level, formatted_msg)
        print(f"  ✓ {file_result}")
        
        # 写入数据库（仅ERROR及以上级别）
        if level in ["ERROR", "CRITICAL"]:
            db_result = self.db_logger.write(level, formatted_msg)
            print(f"  ✓ {db_result}")
        
        # 发送邮件告警
        email_result = self.email_notifier.send_alert(level, message)
        if email_result:
            print(f"  ✓ {email_result}")
    
    def info(self, message: str, context: Dict = None):
        """信息日志"""
        self.log("INFO", message, context)
    
    def warning(self, message: str, context: Dict = None):
        """警告日志"""
        self.log("WARNING", message, context)
    
    def error(self, message: str, context: Dict = None):
        """错误日志"""
        self.log("ERROR", message, context)


# ==================== 示例3：配置管理外观 ====================
class EnvironmentConfigLoader:
    """环境变量配置加载器"""
    
    def load(self) -> Dict:
        # 模拟从环境变量加载配置
        return {
            "database_url": "sqlite:///app.db",
            "debug": "true",
            "log_level": "INFO"
        }


class FileConfigLoader:
    """文件配置加载器"""
    
    def load(self, file_path: str) -> Dict:
        # 模拟从文件加载配置
        return {
            "app_name": "我的应用",
            "version": "1.0.0",
            "features": {
                "feature_a": True,
                "feature_b": False
            }
        }


class RemoteConfigLoader:
    """远程配置加载器"""
    
    def load(self, url: str) -> Dict:
        # 模拟从远程服务加载配置
        return {
            "api_endpoints": {
                "user_service": "http://user-service:8080",
                "order_service": "http://order-service:8080"
            },
            "cache_ttl": 3600
        }


class ConfigValidator:
    """配置验证器"""
    
    def validate(self, config: Dict) -> bool:
        """验证配置"""
        required_keys = ["database_url", "app_name"]
        for key in required_keys:
            if key not in config:
                print(f"配置验证器: 缺少必需配置项 '{key}'")
                return False
        
        print("配置验证器: 配置验证通过")
        return True


class ConfigurationFacade:
    """配置管理外观"""
    
    def __init__(self):
        self.env_loader = EnvironmentConfigLoader()
        self.file_loader = FileConfigLoader()
        self.remote_loader = RemoteConfigLoader()
        self.validator = ConfigValidator()
        self.config = {}
    
    def load_configuration(self, config_file: str = "config.json", 
                          remote_url: str = "http://config-service/config"):
        """加载配置"""
        print("⚙️ 开始加载应用配置...")
        
        # 1. 加载环境变量配置
        env_config = self.env_loader.load()
        print("  ✓ 环境变量配置加载器: 配置已加载")
        
        # 2. 加载文件配置
        file_config = self.file_loader.load(config_file)
        print("  ✓ 文件配置加载器: 配置已加载")
        
        # 3. 加载远程配置
        remote_config = self.remote_loader.load(remote_url)
        print("  ✓ 远程配置加载器: 配置已加载")
        
        # 4. 合并配置（优先级：远程 > 文件 > 环境变量）
        self.config = {**env_config, **file_config, **remote_config}
        print("  ✓ 配置合并完成")
        
        # 5. 验证配置
        if self.validator.validate(self.config):
            print("🎉 配置加载完成！")
            return self.config
        else:
            print("❌ 配置验证失败！")
            return None
    
    def get(self, key: str, default=None):
        """获取配置值"""
        return self.config.get(key, default)
    
    def get_nested(self, path: str, default=None):
        """获取嵌套配置值（如 'features.feature_a'）"""
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value


# ==================== 使用示例 ====================
def demo_api_gateway():
    """API网关外观演示"""
    print("=" * 60)
    print("🌐 API网关系统演示")
    print("=" * 60)
    
    gateway = APIGatewayFacade()
    
    # 有效请求
    print("\n--- 有效请求 ---")
    result1 = gateway.handle_request(
        token="token123",
        service_name="user",
        endpoint="/profile",
        method="GET"
    )
    print(f"响应: {result1}")
    
    # 无效令牌
    print("\n--- 无效令牌 ---")
    result2 = gateway.handle_request(
        token="invalid_token",
        service_name="user",
        endpoint="/profile",
        method="GET"
    )
    print(f"响应: {result2}")


def demo_logging_system():
    """日志系统外观演示"""
    print("\n" + "=" * 60)
    print("📝 日志系统演示")
    print("=" * 60)
    
    logger = LoggingFacade()
    
    # 不同级别的日志
    logger.info("用户登录成功", {"user_id": "123", "ip": "192.168.1.1"})
    print()
    
    logger.warning("磁盘空间不足", {"disk_usage": "85%"})
    print()
    
    logger.error("数据库连接失败", {"error": "Connection timeout"})


def demo_configuration_system():
    """配置管理系统演示"""
    print("\n" + "=" * 60)
    print("⚙️ 配置管理系统演示")
    print("=" * 60)
    
    config_manager = ConfigurationFacade()
    
    # 加载配置
    config = config_manager.load_configuration()
    
    if config:
        print(f"\n📋 配置内容:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        
        print(f"\n🔍 获取特定配置:")
        print(f"  应用名称: {config_manager.get('app_name')}")
        print(f"  数据库URL: {config_manager.get('database_url')}")
        print(f"  功能A状态: {config_manager.get_nested('features.feature_a')}")


def main():
    """主演示函数"""
    print("🎯 外观模式实际应用示例演示")
    
    demo_api_gateway()
    demo_logging_system()
    demo_configuration_system()
    
    print("\n" + "=" * 60)
    print("🎉 所有演示完成！外观模式在实际项目中非常有用！")
    print("=" * 60)


if __name__ == "__main__":
    main()
