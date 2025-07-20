#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理系统

本模块演示了备忘录模式在配置管理系统中的应用，包括：
1. 配置状态的版本管理
2. 配置回滚和恢复
3. 配置变更历史
4. 配置验证和安全管理

作者: Assistant
日期: 2024-01-20
"""

from typing import Dict, List, Any, Optional, Set, Callable
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import json
import copy
import re
import os


class ConfigLevel(Enum):
    """配置级别"""
    SYSTEM = "系统级"
    APPLICATION = "应用级"
    USER = "用户级"
    ENVIRONMENT = "环境级"


class ChangeType(Enum):
    """变更类型"""
    CREATE = "创建"
    UPDATE = "更新"
    DELETE = "删除"
    IMPORT = "导入"
    RESET = "重置"


@dataclass
class ConfigItem:
    """配置项"""
    key: str
    value: Any
    data_type: str
    description: str = ""
    level: ConfigLevel = ConfigLevel.APPLICATION
    readonly: bool = False
    sensitive: bool = False
    validator: Optional[Callable[[Any], bool]] = None
    
    def validate(self) -> bool:
        """验证配置值"""
        if self.validator:
            return self.validator(self.value)
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'key': self.key,
            'value': self.value if not self.sensitive else "***",
            'data_type': self.data_type,
            'description': self.description,
            'level': self.level.value,
            'readonly': self.readonly,
            'sensitive': self.sensitive
        }
    
    def copy(self) -> 'ConfigItem':
        """创建副本"""
        return ConfigItem(
            key=self.key,
            value=copy.deepcopy(self.value),
            data_type=self.data_type,
            description=self.description,
            level=self.level,
            readonly=self.readonly,
            sensitive=self.sensitive,
            validator=self.validator
        )


@dataclass
class ConfigChange:
    """配置变更记录"""
    change_type: ChangeType
    key: str
    old_value: Any = None
    new_value: Any = None
    user: str = "system"
    timestamp: datetime = field(default_factory=datetime.now)
    reason: str = ""
    
    def __str__(self) -> str:
        return f"{self.change_type.value} {self.key} by {self.user}"


class ConfigMemento:
    """配置备忘录"""
    
    def __init__(self, config_state: Dict[str, ConfigItem], version: str, description: str):
        self._config_state = {key: item.copy() for key, item in config_state.items()}
        self._version = version
        self._description = description
        self._timestamp = datetime.now()
        self._checksum = self._calculate_checksum()
    
    def get_config_state(self) -> Dict[str, ConfigItem]:
        """获取配置状态"""
        return {key: item.copy() for key, item in self._config_state.items()}
    
    def get_version(self) -> str:
        """获取版本"""
        return self._version
    
    def get_description(self) -> str:
        """获取描述"""
        return self._description
    
    def get_timestamp(self) -> datetime:
        """获取时间戳"""
        return self._timestamp
    
    def get_checksum(self) -> str:
        """获取校验和"""
        return self._checksum
    
    def _calculate_checksum(self) -> str:
        """计算校验和"""
        # 创建配置的字符串表示用于校验
        config_str = ""
        for key in sorted(self._config_state.keys()):
            item = self._config_state[key]
            if not item.sensitive:  # 敏感信息不参与校验和计算
                config_str += f"{key}:{item.value}:{item.data_type};"
        return str(hash(config_str))
    
    def verify_integrity(self) -> bool:
        """验证完整性"""
        return self._checksum == self._calculate_checksum()
    
    def __str__(self) -> str:
        return f"配置版本 {self._version}: {self._description} [{self._timestamp.strftime('%Y-%m-%d %H:%M:%S')}]"


class ConfigurationManager:
    """配置管理器 - 发起人"""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.config_items: Dict[str, ConfigItem] = {}
        self.change_history: List[ConfigChange] = []
        self.current_version = "1.0.0"
        self.created_at = datetime.now()
        self.last_modified = datetime.now()
        
        # 初始化默认配置
        self._initialize_default_config()
    
    def _initialize_default_config(self) -> None:
        """初始化默认配置"""
        default_configs = [
            ConfigItem("app.name", self.app_name, "string", "应用程序名称", ConfigLevel.APPLICATION, True),
            ConfigItem("app.version", "1.0.0", "string", "应用程序版本", ConfigLevel.APPLICATION, True),
            ConfigItem("app.debug", False, "boolean", "调试模式", ConfigLevel.APPLICATION),
            ConfigItem("server.host", "localhost", "string", "服务器主机", ConfigLevel.SYSTEM),
            ConfigItem("server.port", 8080, "integer", "服务器端口", ConfigLevel.SYSTEM),
            ConfigItem("database.url", "sqlite:///app.db", "string", "数据库连接", ConfigLevel.SYSTEM, False, True),
            ConfigItem("logging.level", "INFO", "string", "日志级别", ConfigLevel.APPLICATION),
            ConfigItem("cache.enabled", True, "boolean", "缓存启用", ConfigLevel.APPLICATION),
            ConfigItem("cache.ttl", 3600, "integer", "缓存过期时间", ConfigLevel.APPLICATION),
        ]
        
        for config in default_configs:
            self.config_items[config.key] = config
    
    def set_config(self, key: str, value: Any, user: str = "system", reason: str = "") -> bool:
        """设置配置项"""
        if key in self.config_items:
            item = self.config_items[key]
            
            # 检查只读权限
            if item.readonly:
                print(f"❌ 配置项 {key} 为只读，无法修改")
                return False
            
            # 验证新值
            old_value = item.value
            item.value = value
            
            if not item.validate():
                item.value = old_value  # 恢复原值
                print(f"❌ 配置项 {key} 验证失败")
                return False
            
            # 记录变更
            change = ConfigChange(ChangeType.UPDATE, key, old_value, value, user, reason=reason)
            self.change_history.append(change)
            self.last_modified = datetime.now()
            
            print(f"✅ 更新配置: {key} = {value if not item.sensitive else '***'}")
            return True
        else:
            print(f"❌ 配置项 {key} 不存在")
            return False
    
    def get_config(self, key: str) -> Any:
        """获取配置项值"""
        if key in self.config_items:
            return self.config_items[key].value
        return None
    
    def add_config(self, config_item: ConfigItem, user: str = "system", reason: str = "") -> bool:
        """添加新配置项"""
        if config_item.key in self.config_items:
            print(f"❌ 配置项 {config_item.key} 已存在")
            return False
        
        if not config_item.validate():
            print(f"❌ 配置项 {config_item.key} 验证失败")
            return False
        
        self.config_items[config_item.key] = config_item
        
        # 记录变更
        change = ConfigChange(ChangeType.CREATE, config_item.key, None, config_item.value, user, reason=reason)
        self.change_history.append(change)
        self.last_modified = datetime.now()
        
        print(f"➕ 添加配置: {config_item.key}")
        return True
    
    def remove_config(self, key: str, user: str = "system", reason: str = "") -> bool:
        """删除配置项"""
        if key not in self.config_items:
            print(f"❌ 配置项 {key} 不存在")
            return False
        
        item = self.config_items[key]
        if item.readonly:
            print(f"❌ 配置项 {key} 为只读，无法删除")
            return False
        
        old_value = item.value
        del self.config_items[key]
        
        # 记录变更
        change = ConfigChange(ChangeType.DELETE, key, old_value, None, user, reason=reason)
        self.change_history.append(change)
        self.last_modified = datetime.now()
        
        print(f"🗑️ 删除配置: {key}")
        return True
    
    def create_memento(self, version: str, description: str) -> ConfigMemento:
        """创建配置备忘录"""
        memento = ConfigMemento(self.config_items, version, description)
        print(f"💾 创建配置快照: {version} - {description}")
        return memento
    
    def restore_from_memento(self, memento: ConfigMemento, user: str = "system") -> bool:
        """从备忘录恢复配置"""
        if not memento.verify_integrity():
            print("❌ 配置备忘录数据损坏")
            return False
        
        try:
            old_config = self.config_items.copy()
            self.config_items = memento.get_config_state()
            self.current_version = memento.get_version()
            self.last_modified = datetime.now()
            
            # 记录恢复操作
            change = ConfigChange(
                ChangeType.RESET, 
                "全部配置", 
                f"版本 {self.current_version}", 
                f"版本 {memento.get_version()}", 
                user,
                reason=f"恢复到版本 {memento.get_version()}"
            )
            self.change_history.append(change)
            
            print(f"🔄 恢复配置到版本: {memento.get_version()}")
            return True
            
        except Exception as e:
            print(f"❌ 恢复配置失败: {e}")
            return False
    
    def export_config(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """导出配置"""
        exported = {
            'app_name': self.app_name,
            'version': self.current_version,
            'created_at': self.created_at.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'config_items': {}
        }
        
        for key, item in self.config_items.items():
            if item.sensitive and not include_sensitive:
                continue
            exported['config_items'][key] = item.to_dict()
        
        return exported
    
    def import_config(self, config_data: Dict[str, Any], user: str = "system") -> bool:
        """导入配置"""
        try:
            if 'config_items' not in config_data:
                print("❌ 无效的配置数据格式")
                return False
            
            imported_count = 0
            for key, item_data in config_data['config_items'].items():
                if key not in self.config_items:
                    # 创建新配置项
                    config_item = ConfigItem(
                        key=item_data['key'],
                        value=item_data['value'],
                        data_type=item_data['data_type'],
                        description=item_data.get('description', ''),
                        level=ConfigLevel(item_data.get('level', ConfigLevel.APPLICATION.value)),
                        readonly=item_data.get('readonly', False),
                        sensitive=item_data.get('sensitive', False)
                    )
                    
                    if self.add_config(config_item, user, "配置导入"):
                        imported_count += 1
                else:
                    # 更新现有配置项
                    if self.set_config(key, item_data['value'], user, "配置导入"):
                        imported_count += 1
            
            print(f"📥 导入配置完成: {imported_count} 项")
            return True
            
        except Exception as e:
            print(f"❌ 导入配置失败: {e}")
            return False
    
    def validate_all_configs(self) -> Dict[str, List[str]]:
        """验证所有配置"""
        validation_results = {'valid': [], 'invalid': []}
        
        for key, item in self.config_items.items():
            if item.validate():
                validation_results['valid'].append(key)
            else:
                validation_results['invalid'].append(key)
        
        return validation_results
    
    def get_config_summary(self) -> Dict[str, Any]:
        """获取配置摘要"""
        level_counts = {}
        for item in self.config_items.values():
            level = item.level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            'app_name': self.app_name,
            'version': self.current_version,
            'total_configs': len(self.config_items),
            'level_distribution': level_counts,
            'readonly_count': sum(1 for item in self.config_items.values() if item.readonly),
            'sensitive_count': sum(1 for item in self.config_items.values() if item.sensitive),
            'last_modified': self.last_modified,
            'change_count': len(self.change_history)
        }


class ConfigVersionManager:
    """配置版本管理器 - 管理者"""
    
    def __init__(self, config_manager: ConfigurationManager, max_versions: int = 10):
        self.config_manager = config_manager
        self.max_versions = max_versions
        self.versions: Dict[str, ConfigMemento] = {}
        self.version_order: List[str] = []
        
        # 创建初始版本
        self._create_initial_version()
    
    def _create_initial_version(self) -> None:
        """创建初始版本"""
        initial_memento = self.config_manager.create_memento("1.0.0", "初始配置")
        self.save_version(initial_memento)
    
    def save_version(self, memento: ConfigMemento) -> None:
        """保存版本"""
        version = memento.get_version()
        
        # 如果版本已存在，覆盖
        if version in self.versions:
            print(f"⚠️ 版本 {version} 已存在，将被覆盖")
        else:
            self.version_order.append(version)
        
        self.versions[version] = memento
        
        # 管理版本数量
        while len(self.version_order) > self.max_versions:
            oldest_version = self.version_order.pop(0)
            del self.versions[oldest_version]
            print(f"🗑️ 删除旧版本: {oldest_version}")
        
        print(f"💾 保存配置版本: {version}")
    
    def restore_version(self, version: str, user: str = "system") -> bool:
        """恢复到指定版本"""
        if version not in self.versions:
            print(f"❌ 版本 {version} 不存在")
            return False
        
        memento = self.versions[version]
        return self.config_manager.restore_from_memento(memento, user)
    
    def get_version_list(self) -> List[Dict[str, Any]]:
        """获取版本列表"""
        version_list = []
        for version in self.version_order:
            memento = self.versions[version]
            version_info = {
                'version': version,
                'description': memento.get_description(),
                'timestamp': memento.get_timestamp(),
                'is_current': version == self.config_manager.current_version
            }
            version_list.append(version_info)
        
        return sorted(version_list, key=lambda x: x['timestamp'], reverse=True)
    
    def create_new_version(self, version: str, description: str) -> bool:
        """创建新版本"""
        if version in self.versions:
            print(f"❌ 版本 {version} 已存在")
            return False
        
        memento = self.config_manager.create_memento(version, description)
        self.save_version(memento)
        self.config_manager.current_version = version
        return True
    
    def compare_versions(self, version1: str, version2: str) -> Dict[str, Any]:
        """比较两个版本"""
        if version1 not in self.versions or version2 not in self.versions:
            return {'error': '版本不存在'}
        
        config1 = self.versions[version1].get_config_state()
        config2 = self.versions[version2].get_config_state()
        
        differences = {
            'added': [],      # 在version2中新增的
            'removed': [],    # 在version2中删除的
            'modified': []    # 在version2中修改的
        }
        
        # 检查新增和修改
        for key, item2 in config2.items():
            if key not in config1:
                differences['added'].append({
                    'key': key,
                    'value': item2.value if not item2.sensitive else '***'
                })
            elif config1[key].value != item2.value:
                differences['modified'].append({
                    'key': key,
                    'old_value': config1[key].value if not config1[key].sensitive else '***',
                    'new_value': item2.value if not item2.sensitive else '***'
                })
        
        # 检查删除
        for key in config1:
            if key not in config2:
                differences['removed'].append({
                    'key': key,
                    'value': config1[key].value if not config1[key].sensitive else '***'
                })
        
        return differences


def demo_configuration_manager():
    """演示配置管理系统"""
    print("=" * 50)
    print("⚙️ 配置管理系统演示")
    print("=" * 50)
    
    # 创建配置管理器和版本管理器
    config_mgr = ConfigurationManager("MyApp")
    version_mgr = ConfigVersionManager(config_mgr, max_versions=5)
    
    print(f"\n📊 初始配置摘要: {config_mgr.get_config_summary()}")
    
    # 修改一些配置
    print("\n🔧 修改配置:")
    config_mgr.set_config("app.debug", True, "admin", "启用调试模式")
    config_mgr.set_config("server.port", 9000, "admin", "更改服务端口")
    config_mgr.set_config("logging.level", "DEBUG", "admin", "提高日志级别")
    
    # 创建新版本
    print("\n📦 创建新版本:")
    version_mgr.create_new_version("1.1.0", "调试配置版本")
    
    # 添加新配置项
    print("\n➕ 添加新配置:")
    new_config = ConfigItem("feature.new_ui", True, "boolean", "新UI功能", ConfigLevel.USER)
    config_mgr.add_config(new_config, "developer", "添加新功能开关")
    
    # 创建另一个版本
    version_mgr.create_new_version("1.2.0", "添加新功能")
    
    # 显示版本列表
    print("\n📋 版本历史:")
    for version_info in version_mgr.get_version_list():
        current_marker = " (当前)" if version_info['is_current'] else ""
        timestamp = version_info['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {version_info['version']}: {version_info['description']} [{timestamp}]{current_marker}")
    
    # 比较版本
    print("\n🔍 版本比较 (1.0.0 vs 1.2.0):")
    diff = version_mgr.compare_versions("1.0.0", "1.2.0")
    for change_type, changes in diff.items():
        if changes:
            print(f"  {change_type}:")
            for change in changes:
                print(f"    {change}")
    
    # 回滚到之前版本
    print("\n↶ 回滚到版本 1.1.0:")
    version_mgr.restore_version("1.1.0", "admin")
    
    print(f"📊 回滚后配置摘要: {config_mgr.get_config_summary()}")
    
    # 导出配置
    print("\n📤 导出配置:")
    exported_config = config_mgr.export_config(include_sensitive=False)
    print(f"导出了 {len(exported_config['config_items'])} 个配置项")


if __name__ == "__main__":
    print("🎯 配置管理系统备忘录模式演示")
    
    demo_configuration_manager()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 配置管理系统展示了备忘录模式在版本控制中的应用")
    print("=" * 50)
