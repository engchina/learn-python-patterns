"""
04_configuration_builder.py - 配置建造者模式

系统配置构建器示例
这个示例展示了如何使用建造者模式来构建复杂的系统配置。
在企业应用中，系统配置往往包含多个层面的设置，
建造者模式可以帮助我们分步骤构建不同环境的配置。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum
import json


# ==================== 枚举类型 ====================
class Environment(Enum):
    """环境类型"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseType(Enum):
    """数据库类型"""
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    REDIS = "redis"


# ==================== 配置组件类 ====================
class DatabaseConfig:
    """数据库配置"""

    def __init__(self):
        self.type = DatabaseType.MYSQL
        self.host = "localhost"
        self.port = 3306
        self.database = ""
        self.username = ""
        self.password = ""
        self.charset = "utf8mb4"
        self.pool_size = 10
        self.max_connections = 100
        self.timeout = 30
        self.ssl_enabled = False
        self.backup_hosts = []
        self.connection_params = {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type.value,
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "username": self.username,
            "password": self.password,
            "charset": self.charset,
            "pool_size": self.pool_size,
            "max_connections": self.max_connections,
            "timeout": self.timeout,
            "ssl_enabled": self.ssl_enabled,
            "backup_hosts": self.backup_hosts,
            "connection_params": self.connection_params
        }


class CacheConfig:
    """缓存配置"""

    def __init__(self):
        self.type = "redis"
        self.host = "localhost"
        self.port = 6379
        self.password = ""
        self.database = 0
        self.max_connections = 50
        self.timeout = 5
        self.default_ttl = 3600
        self.key_prefix = ""
        self.cluster_nodes = []

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type,
            "host": self.host,
            "port": self.port,
            "password": self.password,
            "database": self.database,
            "max_connections": self.max_connections,
            "timeout": self.timeout,
            "default_ttl": self.default_ttl,
            "key_prefix": self.key_prefix,
            "cluster_nodes": self.cluster_nodes
        }


class LoggingConfig:
    """日志配置"""

    def __init__(self):
        self.level = LogLevel.INFO
        self.format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.file_path = "app.log"
        self.max_file_size = "10MB"
        self.backup_count = 5
        self.console_output = True
        self.loggers = {}
        self.handlers = {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "level": self.level.value,
            "format": self.format,
            "file_path": self.file_path,
            "max_file_size": self.max_file_size,
            "backup_count": self.backup_count,
            "console_output": self.console_output,
            "loggers": self.loggers,
            "handlers": self.handlers
        }


class SecurityConfig:
    """安全配置"""

    def __init__(self):
        self.secret_key = ""
        self.jwt_secret = ""
        self.jwt_expiration = 3600
        self.password_min_length = 8
        self.password_require_special = True
        self.session_timeout = 1800
        self.max_login_attempts = 5
        self.lockout_duration = 300
        self.cors_origins = []
        self.security_headers = {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "secret_key": self.secret_key,
            "jwt_secret": self.jwt_secret,
            "jwt_expiration": self.jwt_expiration,
            "password_min_length": self.password_min_length,
            "password_require_special": self.password_require_special,
            "session_timeout": self.session_timeout,
            "max_login_attempts": self.max_login_attempts,
            "lockout_duration": self.lockout_duration,
            "cors_origins": self.cors_origins,
            "security_headers": self.security_headers
        }


# ==================== 应用配置产品类 ====================
class ApplicationConfig:
    """应用配置产品类"""

    def __init__(self):
        self.app_name = ""
        self.version = "1.0.0"
        self.environment = Environment.DEVELOPMENT
        self.debug = True
        self.host = "0.0.0.0"
        self.port = 8000

        # 各个配置组件
        self.database = DatabaseConfig()
        self.cache = CacheConfig()
        self.logging = LoggingConfig()
        self.security = SecurityConfig()

        # 其他配置
        self.features = {}
        self.external_services = {}
        self.monitoring = {}
        self.custom_settings = {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为完整配置字典"""
        return {
            "app_name": self.app_name,
            "version": self.version,
            "environment": self.environment.value,
            "debug": self.debug,
            "host": self.host,
            "port": self.port,
            "database": self.database.to_dict(),
            "cache": self.cache.to_dict(),
            "logging": self.logging.to_dict(),
            "security": self.security.to_dict(),
            "features": self.features,
            "external_services": self.external_services,
            "monitoring": self.monitoring,
            "custom_settings": self.custom_settings
        }

    def to_json(self, indent: int = 2) -> str:
        """转换为JSON格式"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_yaml(self) -> str:
        """转换为YAML格式（简化实现）"""
        def dict_to_yaml(data, indent=0):
            """简单的字典转YAML实现"""
            yaml_lines = []
            prefix = "  " * indent

            for key, value in data.items():
                if isinstance(value, dict):
                    yaml_lines.append(f"{prefix}{key}:")
                    yaml_lines.append(dict_to_yaml(value, indent + 1))
                elif isinstance(value, list):
                    yaml_lines.append(f"{prefix}{key}:")
                    for item in value:
                        if isinstance(item, dict):
                            yaml_lines.append(f"{prefix}  -")
                            yaml_lines.append(dict_to_yaml(item, indent + 2))
                        else:
                            yaml_lines.append(f"{prefix}  - {item}")
                else:
                    yaml_lines.append(f"{prefix}{key}: {value}")

            return "\n".join(yaml_lines)

        return dict_to_yaml(self.to_dict())

    def validate(self) -> List[str]:
        """验证配置有效性"""
        errors = []

        if not self.app_name:
            errors.append("应用名称不能为空")

        if not self.database.database:
            errors.append("数据库名称不能为空")

        if not self.security.secret_key:
            errors.append("安全密钥不能为空")

        if self.port <= 0 or self.port > 65535:
            errors.append("端口号必须在1-65535之间")

        return errors


# ==================== 抽象建造者 ====================
class ConfigurationBuilder(ABC):
    """配置建造者抽象基类"""

    def __init__(self):
        self.config = ApplicationConfig()

    @abstractmethod
    def set_basic_info(self, app_name: str, version: str, environment: Environment):
        """设置基本信息"""
        pass

    @abstractmethod
    def configure_database(self):
        """配置数据库"""
        pass

    @abstractmethod
    def configure_cache(self):
        """配置缓存"""
        pass

    @abstractmethod
    def configure_logging(self):
        """配置日志"""
        pass

    @abstractmethod
    def configure_security(self):
        """配置安全"""
        pass

    def configure_features(self):
        """配置功能特性（可选）"""
        pass

    def configure_monitoring(self):
        """配置监控（可选）"""
        pass

    def configure_external_services(self):
        """配置外部服务（可选）"""
        pass

    def get_config(self) -> ApplicationConfig:
        """获取构建的配置"""
        return self.config


# ==================== 具体建造者类 ====================
class DevelopmentConfigBuilder(ConfigurationBuilder):
    """开发环境配置建造者"""

    def set_basic_info(self, app_name: str, version: str, environment: Environment = Environment.DEVELOPMENT):
        """设置基本信息"""
        self.config.app_name = app_name
        self.config.version = version
        self.config.environment = environment
        self.config.debug = True
        self.config.host = "127.0.0.1"
        self.config.port = 8000

    def configure_database(self):
        """配置开发数据库"""
        self.config.database.type = DatabaseType.MYSQL
        self.config.database.host = "localhost"
        self.config.database.port = 3306
        self.config.database.database = f"{self.config.app_name}_dev"
        self.config.database.username = "dev_user"
        self.config.database.password = "dev_password"
        self.config.database.pool_size = 5
        self.config.database.max_connections = 20

    def configure_cache(self):
        """配置开发缓存"""
        self.config.cache.host = "localhost"
        self.config.cache.port = 6379
        self.config.cache.database = 0
        self.config.cache.key_prefix = f"{self.config.app_name}:dev:"
        self.config.cache.default_ttl = 300  # 5分钟

    def configure_logging(self):
        """配置开发日志"""
        self.config.logging.level = LogLevel.DEBUG
        self.config.logging.console_output = True
        self.config.logging.file_path = f"logs/{self.config.app_name}_dev.log"
        self.config.logging.loggers = {
            "sqlalchemy": {"level": "INFO"},
            "requests": {"level": "WARNING"}
        }

    def configure_security(self):
        """配置开发安全"""
        self.config.security.secret_key = "dev-secret-key-not-for-production"
        self.config.security.jwt_secret = "dev-jwt-secret"
        self.config.security.jwt_expiration = 7200  # 2小时
        self.config.security.password_min_length = 6
        self.config.security.max_login_attempts = 10
        self.config.security.cors_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

    def configure_features(self):
        """配置开发功能"""
        self.config.features = {
            "debug_toolbar": True,
            "auto_reload": True,
            "mock_external_apis": True,
            "detailed_errors": True
        }


class ProductionConfigBuilder(ConfigurationBuilder):
    """生产环境配置建造者"""

    def set_basic_info(self, app_name: str, version: str, environment: Environment = Environment.PRODUCTION):
        """设置基本信息"""
        self.config.app_name = app_name
        self.config.version = version
        self.config.environment = environment
        self.config.debug = False
        self.config.host = "0.0.0.0"
        self.config.port = 80

    def configure_database(self):
        """配置生产数据库"""
        self.config.database.type = DatabaseType.MYSQL
        self.config.database.host = "prod-db.example.com"
        self.config.database.port = 3306
        self.config.database.database = f"{self.config.app_name}_prod"
        self.config.database.username = "prod_user"
        self.config.database.password = "secure_prod_password"
        self.config.database.pool_size = 20
        self.config.database.max_connections = 100
        self.config.database.ssl_enabled = True
        self.config.database.backup_hosts = [
            "prod-db-backup1.example.com",
            "prod-db-backup2.example.com"
        ]

    def configure_cache(self):
        """配置生产缓存"""
        self.config.cache.host = "prod-cache.example.com"
        self.config.cache.port = 6379
        self.config.cache.password = "cache_password"
        self.config.cache.database = 0
        self.config.cache.key_prefix = f"{self.config.app_name}:prod:"
        self.config.cache.default_ttl = 3600  # 1小时
        self.config.cache.max_connections = 100

    def configure_logging(self):
        """配置生产日志"""
        self.config.logging.level = LogLevel.WARNING
        self.config.logging.console_output = False
        self.config.logging.file_path = f"/var/log/{self.config.app_name}/app.log"
        self.config.logging.max_file_size = "100MB"
        self.config.logging.backup_count = 10
        self.config.logging.handlers = {
            "syslog": {
                "address": "/dev/log",
                "facility": "local0"
            }
        }

    def configure_security(self):
        """配置生产安全"""
        self.config.security.secret_key = "super-secure-production-key"
        self.config.security.jwt_secret = "super-secure-jwt-secret"
        self.config.security.jwt_expiration = 1800  # 30分钟
        self.config.security.password_min_length = 12
        self.config.security.password_require_special = True
        self.config.security.max_login_attempts = 3
        self.config.security.lockout_duration = 900  # 15分钟
        self.config.security.cors_origins = ["https://app.example.com"]
        self.config.security.security_headers = {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
        }

    def configure_monitoring(self):
        """配置生产监控"""
        self.config.monitoring = {
            "metrics_enabled": True,
            "health_check_endpoint": "/health",
            "prometheus_endpoint": "/metrics",
            "alerting": {
                "email": "alerts@example.com",
                "slack_webhook": "https://hooks.slack.com/..."
            }
        }

    def configure_external_services(self):
        """配置外部服务"""
        self.config.external_services = {
            "email_service": {
                "provider": "sendgrid",
                "api_key": "sg.xxx",
                "from_email": "noreply@example.com"
            },
            "payment_gateway": {
                "provider": "stripe",
                "public_key": "pk_live_xxx",
                "secret_key": "sk_live_xxx"
            }
        }


# ==================== 指挥者类 ====================
class ConfigurationDirector:
    """配置构建指挥者"""

    def __init__(self, builder: ConfigurationBuilder):
        self.builder = builder

    def build_complete_config(self, app_name: str, version: str) -> ApplicationConfig:
        """构建完整配置"""
        print(f"开始构建 {app_name} v{version} 的配置...")

        # 设置基本信息
        self.builder.set_basic_info(app_name, version)

        # 构建各个配置组件
        self.builder.configure_database()
        self.builder.configure_cache()
        self.builder.configure_logging()
        self.builder.configure_security()
        self.builder.configure_features()
        self.builder.configure_monitoring()
        self.builder.configure_external_services()

        config = self.builder.get_config()

        # 验证配置
        errors = config.validate()
        if errors:
            print("配置验证失败:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("配置构建完成并验证通过！")

        return config

    def build_basic_config(self, app_name: str, version: str) -> ApplicationConfig:
        """构建基础配置"""
        print(f"开始构建 {app_name} v{version} 的基础配置...")

        self.builder.set_basic_info(app_name, version)
        self.builder.configure_database()
        self.builder.configure_cache()
        self.builder.configure_logging()
        self.builder.configure_security()

        config = self.builder.get_config()
        print("基础配置构建完成！")
        return config


# ==================== 演示函数 ====================
def demonstrate_development_config():
    """演示开发环境配置构建"""
    print("=" * 60)
    print("开发环境配置构建演示")
    print("=" * 60)

    # 构建开发配置
    dev_builder = DevelopmentConfigBuilder()
    director = ConfigurationDirector(dev_builder)
    dev_config = director.build_complete_config("MyApp", "1.0.0")

    print("\n开发环境配置 (JSON格式):")
    print(dev_config.to_json())


def demonstrate_production_config():
    """演示生产环境配置构建"""
    print("\n" + "=" * 60)
    print("生产环境配置构建演示")
    print("=" * 60)

    # 构建生产配置
    prod_builder = ProductionConfigBuilder()
    director = ConfigurationDirector(prod_builder)
    prod_config = director.build_complete_config("MyApp", "1.0.0")

    print("\n生产环境配置 (YAML格式):")
    print(prod_config.to_yaml())


def main():
    """主函数"""
    print("配置建造者模式演示")

    demonstrate_development_config()
    demonstrate_production_config()

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
