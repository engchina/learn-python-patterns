"""
04_configuration_prototype.py - 配置原型模式

系统配置管理示例
这个示例展示了如何使用原型模式来管理系统配置。
在企业应用中，经常需要为不同环境（开发、测试、生产）
创建相似但略有差异的配置，原型模式可以提供配置模板。
"""

import copy
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime


# ==================== 配置原型接口 ====================
class ConfigurationPrototype(ABC):
    """配置原型抽象基类"""
    
    @abstractmethod
    def clone(self):
        """克隆配置"""
        pass
    
    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """获取配置字典"""
        pass
    
    @abstractmethod
    def set_property(self, key: str, value: Any):
        """设置配置属性"""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """验证配置有效性"""
        pass


# ==================== 具体配置类 ====================
class DatabaseConfiguration(ConfigurationPrototype):
    """数据库配置类"""
    
    def __init__(self, name: str = "默认数据库配置"):
        self.name = name
        self.host = "localhost"
        self.port = 3306
        self.database = "myapp"
        self.username = "root"
        self.password = ""
        self.charset = "utf8mb4"
        self.pool_size = 10
        self.max_connections = 100
        self.timeout = 30
        self.ssl_enabled = False
        self.ssl_cert_path = ""
        self.backup_hosts = []
        self.connection_params = {}
        self.created_at = datetime.now()
        self.environment = "development"
    
    def clone(self):
        """克隆数据库配置"""
        new_config = copy.copy(self)
        # 深拷贝复杂对象
        new_config.backup_hosts = self.backup_hosts.copy()
        new_config.connection_params = self.connection_params.copy()
        new_config.created_at = datetime.now()
        return new_config
    
    def set_property(self, key: str, value: Any):
        """设置配置属性"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.connection_params[key] = value
    
    def add_backup_host(self, host: str, port: int = None):
        """添加备份主机"""
        backup = {"host": host, "port": port or self.port}
        self.backup_hosts.append(backup)
    
    def enable_ssl(self, cert_path: str):
        """启用SSL"""
        self.ssl_enabled = True
        self.ssl_cert_path = cert_path
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置字典"""
        return {
            "name": self.name,
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
            "ssl_cert_path": self.ssl_cert_path,
            "backup_hosts": self.backup_hosts,
            "connection_params": self.connection_params,
            "environment": self.environment
        }
    
    def validate(self) -> bool:
        """验证配置有效性"""
        if not self.host or not self.database or not self.username:
            return False
        if self.port <= 0 or self.port > 65535:
            return False
        if self.pool_size <= 0 or self.max_connections <= 0:
            return False
        return True
    
    def get_connection_string(self) -> str:
        """获取连接字符串"""
        return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class WebServerConfiguration(ConfigurationPrototype):
    """Web服务器配置类"""
    
    def __init__(self, name: str = "默认Web服务器配置"):
        self.name = name
        self.host = "0.0.0.0"
        self.port = 8080
        self.debug = True
        self.log_level = "INFO"
        self.log_file = "app.log"
        self.static_folder = "static"
        self.template_folder = "templates"
        self.secret_key = "dev-secret-key"
        self.session_timeout = 3600
        self.max_request_size = 16 * 1024 * 1024  # 16MB
        self.cors_enabled = False
        self.cors_origins = []
        self.middleware = []
        self.security_headers = {}
        self.created_at = datetime.now()
        self.environment = "development"
    
    def clone(self):
        """克隆Web服务器配置"""
        new_config = copy.copy(self)
        new_config.cors_origins = self.cors_origins.copy()
        new_config.middleware = self.middleware.copy()
        new_config.security_headers = self.security_headers.copy()
        new_config.created_at = datetime.now()
        return new_config
    
    def set_property(self, key: str, value: Any):
        """设置配置属性"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise ValueError(f"未知的配置属性: {key}")
    
    def enable_cors(self, origins: List[str] = None):
        """启用CORS"""
        self.cors_enabled = True
        if origins:
            self.cors_origins = origins
        else:
            self.cors_origins = ["*"]
    
    def add_middleware(self, middleware_name: str, config: Dict[str, Any] = None):
        """添加中间件"""
        middleware_config = {
            "name": middleware_name,
            "config": config or {}
        }
        self.middleware.append(middleware_config)
    
    def set_security_header(self, header: str, value: str):
        """设置安全头"""
        self.security_headers[header] = value
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置字典"""
        return {
            "name": self.name,
            "host": self.host,
            "port": self.port,
            "debug": self.debug,
            "log_level": self.log_level,
            "log_file": self.log_file,
            "static_folder": self.static_folder,
            "template_folder": self.template_folder,
            "secret_key": self.secret_key,
            "session_timeout": self.session_timeout,
            "max_request_size": self.max_request_size,
            "cors_enabled": self.cors_enabled,
            "cors_origins": self.cors_origins,
            "middleware": self.middleware,
            "security_headers": self.security_headers,
            "environment": self.environment
        }
    
    def validate(self) -> bool:
        """验证配置有效性"""
        if not self.host or self.port <= 0 or self.port > 65535:
            return False
        if not self.secret_key or len(self.secret_key) < 8:
            return False
        if self.session_timeout <= 0:
            return False
        return True


class CacheConfiguration(ConfigurationPrototype):
    """缓存配置类"""
    
    def __init__(self, name: str = "默认缓存配置"):
        self.name = name
        self.cache_type = "redis"  # redis, memcached, memory
        self.host = "localhost"
        self.port = 6379
        self.password = ""
        self.database = 0
        self.max_connections = 50
        self.timeout = 5
        self.default_ttl = 3600  # 默认过期时间（秒）
        self.key_prefix = "myapp:"
        self.serializer = "json"  # json, pickle
        self.compression = False
        self.cluster_nodes = []
        self.sentinel_hosts = []
        self.created_at = datetime.now()
        self.environment = "development"
    
    def clone(self):
        """克隆缓存配置"""
        new_config = copy.copy(self)
        new_config.cluster_nodes = self.cluster_nodes.copy()
        new_config.sentinel_hosts = self.sentinel_hosts.copy()
        new_config.created_at = datetime.now()
        return new_config
    
    def set_property(self, key: str, value: Any):
        """设置配置属性"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise ValueError(f"未知的配置属性: {key}")
    
    def add_cluster_node(self, host: str, port: int):
        """添加集群节点"""
        node = {"host": host, "port": port}
        self.cluster_nodes.append(node)
    
    def add_sentinel_host(self, host: str, port: int = 26379):
        """添加哨兵主机"""
        sentinel = {"host": host, "port": port}
        self.sentinel_hosts.append(sentinel)
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置字典"""
        return {
            "name": self.name,
            "cache_type": self.cache_type,
            "host": self.host,
            "port": self.port,
            "password": self.password,
            "database": self.database,
            "max_connections": self.max_connections,
            "timeout": self.timeout,
            "default_ttl": self.default_ttl,
            "key_prefix": self.key_prefix,
            "serializer": self.serializer,
            "compression": self.compression,
            "cluster_nodes": self.cluster_nodes,
            "sentinel_hosts": self.sentinel_hosts,
            "environment": self.environment
        }
    
    def validate(self) -> bool:
        """验证配置有效性"""
        if not self.host or self.port <= 0 or self.port > 65535:
            return False
        if self.cache_type not in ["redis", "memcached", "memory"]:
            return False
        if self.default_ttl <= 0:
            return False
        return True


# ==================== 配置管理器 ====================
class ConfigurationManager:
    """配置管理器"""
    
    def __init__(self):
        self._templates: Dict[str, ConfigurationPrototype] = {}
        self._environments = ["development", "testing", "staging", "production"]
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """初始化默认配置模板"""
        # 开发环境数据库配置
        dev_db = DatabaseConfiguration("开发数据库")
        dev_db.host = "localhost"
        dev_db.database = "myapp_dev"
        dev_db.username = "dev_user"
        dev_db.password = "dev_pass"
        dev_db.environment = "development"
        
        # 生产环境数据库配置
        prod_db = DatabaseConfiguration("生产数据库")
        prod_db.host = "prod-db.example.com"
        prod_db.database = "myapp_prod"
        prod_db.username = "prod_user"
        prod_db.password = "secure_prod_pass"
        prod_db.pool_size = 50
        prod_db.max_connections = 500
        prod_db.ssl_enabled = True
        prod_db.environment = "production"
        
        # Web服务器配置
        dev_web = WebServerConfiguration("开发Web服务器")
        dev_web.debug = True
        dev_web.log_level = "DEBUG"
        dev_web.environment = "development"
        
        prod_web = WebServerConfiguration("生产Web服务器")
        prod_web.host = "0.0.0.0"
        prod_web.port = 80
        prod_web.debug = False
        prod_web.log_level = "ERROR"
        prod_web.secret_key = "super-secure-production-key"
        prod_web.environment = "production"
        prod_web.set_security_header("X-Frame-Options", "DENY")
        prod_web.set_security_header("X-Content-Type-Options", "nosniff")
        
        # 缓存配置
        dev_cache = CacheConfiguration("开发缓存")
        dev_cache.environment = "development"
        
        prod_cache = CacheConfiguration("生产缓存")
        prod_cache.host = "prod-cache.example.com"
        prod_cache.password = "cache_password"
        prod_cache.max_connections = 200
        prod_cache.environment = "production"
        
        # 注册模板
        self.register_template("dev_database", dev_db)
        self.register_template("prod_database", prod_db)
        self.register_template("dev_webserver", dev_web)
        self.register_template("prod_webserver", prod_web)
        self.register_template("dev_cache", dev_cache)
        self.register_template("prod_cache", prod_cache)
    
    def register_template(self, name: str, template: ConfigurationPrototype):
        """注册配置模板"""
        self._templates[name] = template
        print(f"配置管理器: 已注册模板 '{name}'")
    
    def create_configuration(self, template_name: str, custom_name: str = None) -> ConfigurationPrototype:
        """基于模板创建配置"""
        if template_name not in self._templates:
            raise ValueError(f"未找到模板 '{template_name}'")
        
        config = self._templates[template_name].clone()
        if custom_name:
            config.name = custom_name
        
        print(f"配置管理器: 基于 '{template_name}' 创建了配置")
        return config
    
    def create_environment_config(self, base_template: str, environment: str) -> ConfigurationPrototype:
        """为特定环境创建配置"""
        if environment not in self._environments:
            raise ValueError(f"不支持的环境: {environment}")
        
        config = self.create_configuration(base_template)
        config.environment = environment
        
        # 根据环境调整配置
        if environment == "production":
            if hasattr(config, 'debug'):
                config.debug = False
            if hasattr(config, 'log_level'):
                config.log_level = "ERROR"
        elif environment == "development":
            if hasattr(config, 'debug'):
                config.debug = True
            if hasattr(config, 'log_level'):
                config.log_level = "DEBUG"
        
        return config
    
    def list_templates(self) -> List[str]:
        """列出所有模板"""
        return list(self._templates.keys())
    
    def export_config(self, config: ConfigurationPrototype, format: str = "json") -> str:
        """导出配置"""
        config_dict = config.get_config()
        if format == "json":
            return json.dumps(config_dict, indent=2, default=str)
        else:
            raise ValueError(f"不支持的格式: {format}")


# ==================== 演示函数 ====================
def demonstrate_configuration_cloning():
    """演示配置克隆"""
    print("=" * 50)
    print("配置克隆演示")
    print("=" * 50)
    
    # 创建基础配置
    base_config = DatabaseConfiguration("基础数据库配置")
    base_config.host = "db.example.com"
    base_config.database = "myapp"
    base_config.add_backup_host("backup1.example.com")
    base_config.add_backup_host("backup2.example.com")
    
    print("基础配置:")
    print(json.dumps(base_config.get_config(), indent=2, default=str))
    print()
    
    # 克隆并修改配置
    test_config = base_config.clone()
    test_config.name = "测试数据库配置"
    test_config.database = "myapp_test"
    test_config.environment = "testing"
    
    print("克隆的测试配置:")
    print(json.dumps(test_config.get_config(), indent=2, default=str))


def demonstrate_configuration_manager():
    """演示配置管理器"""
    print("\n" + "=" * 50)
    print("配置管理器演示")
    print("=" * 50)
    
    manager = ConfigurationManager()
    
    print("可用的配置模板:")
    for template in manager.list_templates():
        print(f"- {template}")
    print()
    
    # 创建不同环境的配置
    print("创建不同环境的配置:")
    
    # 开发环境
    dev_db = manager.create_configuration("dev_database", "我的开发数据库")
    dev_web = manager.create_configuration("dev_webserver", "我的开发服务器")
    
    # 生产环境
    prod_db = manager.create_configuration("prod_database", "我的生产数据库")
    prod_web = manager.create_configuration("prod_webserver", "我的生产服务器")
    
    configs = [
        ("开发数据库", dev_db),
        ("开发Web服务器", dev_web),
        ("生产数据库", prod_db),
        ("生产Web服务器", prod_web)
    ]
    
    for name, config in configs:
        print(f"\n{name}配置:")
        print(f"  环境: {config.environment}")
        print(f"  验证结果: {'通过' if config.validate() else '失败'}")
        if hasattr(config, 'host'):
            print(f"  主机: {config.host}")
        if hasattr(config, 'port'):
            print(f"  端口: {config.port}")


def main():
    """主函数"""
    print("配置原型模式演示")
    
    demonstrate_configuration_cloning()
    demonstrate_configuration_manager()
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
