"""
04_config_factory.py - 配置管理器工厂简单工厂模式

配置管理器工厂示例
这个示例展示了简单工厂模式在配置管理系统中的应用。
我们有不同格式的配置文件（JSON、YAML、INI、XML等），通过一个配置工厂来创建对应的解析器。
体现了简单工厂模式在文件处理和配置管理中的实际价值。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
import json
import os
import re
from datetime import datetime


# ==================== 抽象产品 ====================
class ConfigParser(ABC):
    """配置解析器抽象基类"""
    
    def __init__(self, name: str, file_extensions: List[str]):
        self.name = name
        self.file_extensions = file_extensions
        self.last_loaded_file = None
        self.last_loaded_time = None
    
    @abstractmethod
    def parse(self, content: str) -> Dict[str, Any]:
        """解析配置内容"""
        pass
    
    @abstractmethod
    def serialize(self, config: Dict[str, Any]) -> str:
        """序列化配置为字符串"""
        pass
    
    @abstractmethod
    def validate_format(self, content: str) -> bool:
        """验证配置格式"""
        pass
    
    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        """从文件加载配置"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"配置文件不存在: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not self.validate_format(content):
                raise ValueError(f"配置文件格式不正确: {file_path}")
            
            config = self.parse(content)
            self.last_loaded_file = file_path
            self.last_loaded_time = datetime.now()
            
            print(f"📁 成功加载配置文件: {file_path}")
            return config
            
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            raise
    
    def save_to_file(self, config: Dict[str, Any], file_path: str):
        """保存配置到文件"""
        try:
            content = self.serialize(config)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"💾 成功保存配置文件: {file_path}")
            
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
            raise
    
    def get_info(self) -> Dict[str, Any]:
        """获取解析器信息"""
        return {
            "name": self.name,
            "extensions": self.file_extensions,
            "last_loaded_file": self.last_loaded_file,
            "last_loaded_time": self.last_loaded_time.isoformat() if self.last_loaded_time else None
        }


# ==================== 具体产品 ====================
class JSONConfigParser(ConfigParser):
    """JSON配置解析器"""
    
    def __init__(self):
        super().__init__("JSON配置解析器", [".json"])
    
    def parse(self, content: str) -> Dict[str, Any]:
        """解析JSON配置"""
        try:
            config = json.loads(content)
            print(f"📊 JSON配置解析成功，包含 {len(config)} 个顶级配置项")
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON格式错误: {e}")
    
    def serialize(self, config: Dict[str, Any]) -> str:
        """序列化为JSON格式"""
        return json.dumps(config, indent=2, ensure_ascii=False)
    
    def validate_format(self, content: str) -> bool:
        """验证JSON格式"""
        try:
            json.loads(content)
            return True
        except json.JSONDecodeError:
            return False


class YAMLConfigParser(ConfigParser):
    """YAML配置解析器（简化实现）"""
    
    def __init__(self):
        super().__init__("YAML配置解析器", [".yaml", ".yml"])
    
    def parse(self, content: str) -> Dict[str, Any]:
        """解析YAML配置（简化实现）"""
        config = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # 简单的类型转换
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                
                config[key] = value
        
        print(f"📊 YAML配置解析成功，包含 {len(config)} 个配置项")
        return config
    
    def serialize(self, config: Dict[str, Any]) -> str:
        """序列化为YAML格式"""
        lines = []
        for key, value in config.items():
            if isinstance(value, str):
                lines.append(f"{key}: \"{value}\"")
            else:
                lines.append(f"{key}: {value}")
        return '\n'.join(lines)
    
    def validate_format(self, content: str) -> bool:
        """验证YAML格式（简化）"""
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if ':' not in line:
                    return False
        return True


class INIConfigParser(ConfigParser):
    """INI配置解析器"""
    
    def __init__(self):
        super().__init__("INI配置解析器", [".ini", ".cfg"])
    
    def parse(self, content: str) -> Dict[str, Any]:
        """解析INI配置"""
        config = {}
        current_section = "default"
        config[current_section] = {}
        
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            
            # 跳过注释和空行
            if not line or line.startswith(('#', ';')):
                continue
            
            # 处理节（section）
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
                continue
            
            # 处理键值对
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # 简单的类型转换
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
                
                config[current_section][key] = value
        
        print(f"📊 INI配置解析成功，包含 {len(config)} 个节")
        return config
    
    def serialize(self, config: Dict[str, Any]) -> str:
        """序列化为INI格式"""
        lines = []
        for section, items in config.items():
            lines.append(f"[{section}]")
            for key, value in items.items():
                lines.append(f"{key} = {value}")
            lines.append("")  # 空行分隔节
        return '\n'.join(lines)
    
    def validate_format(self, content: str) -> bool:
        """验证INI格式"""
        lines = content.strip().split('\n')
        has_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith(('#', ';')):
                continue
            
            if line.startswith('[') and line.endswith(']'):
                has_section = True
            elif '=' in line:
                continue
            else:
                return False
        
        return has_section


class XMLConfigParser(ConfigParser):
    """XML配置解析器（简化实现）"""
    
    def __init__(self):
        super().__init__("XML配置解析器", [".xml"])
    
    def parse(self, content: str) -> Dict[str, Any]:
        """解析XML配置（简化实现）"""
        config = {}
        
        # 简单的XML解析（实际项目中应使用xml.etree.ElementTree）
        import re
        
        # 提取所有标签和内容
        pattern = r'<(\w+)>(.*?)</\1>'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for tag, value in matches:
            value = value.strip()
            
            # 简单的类型转换
            if value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '').isdigit():
                value = float(value)
            
            config[tag] = value
        
        print(f"📊 XML配置解析成功，包含 {len(config)} 个配置项")
        return config
    
    def serialize(self, config: Dict[str, Any]) -> str:
        """序列化为XML格式"""
        lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<config>']
        
        for key, value in config.items():
            lines.append(f"  <{key}>{value}</{key}>")
        
        lines.append('</config>')
        return '\n'.join(lines)
    
    def validate_format(self, content: str) -> bool:
        """验证XML格式"""
        import re
        # 简单验证：包含XML标签
        return bool(re.search(r'<\w+.*?>', content))


class PropertiesConfigParser(ConfigParser):
    """Properties配置解析器"""
    
    def __init__(self):
        super().__init__("Properties配置解析器", [".properties"])
    
    def parse(self, content: str) -> Dict[str, Any]:
        """解析Properties配置"""
        config = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 跳过注释和空行
            if not line or line.startswith('#'):
                continue
            
            # 处理键值对
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Properties文件通常都是字符串，但可以做简单转换
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
                
                config[key] = value
        
        print(f"📊 Properties配置解析成功，包含 {len(config)} 个配置项")
        return config
    
    def serialize(self, config: Dict[str, Any]) -> str:
        """序列化为Properties格式"""
        lines = []
        for key, value in config.items():
            lines.append(f"{key} = {value}")
        return '\n'.join(lines)
    
    def validate_format(self, content: str) -> bool:
        """验证Properties格式"""
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' not in line:
                    return False
        return True


# ==================== 简单工厂 ====================
class ConfigParserFactory:
    """配置解析器工厂类"""
    
    # 支持的解析器类型
    SUPPORTED_PARSERS = {
        "json": ("JSON", JSONConfigParser),
        "yaml": ("YAML", YAMLConfigParser),
        "yml": ("YAML", YAMLConfigParser),
        "ini": ("INI", INIConfigParser),
        "cfg": ("INI", INIConfigParser),
        "xml": ("XML", XMLConfigParser),
        "properties": ("Properties", PropertiesConfigParser),
    }
    
    @staticmethod
    def create_parser(config_type: str) -> ConfigParser:
        """
        创建配置解析器对象
        
        Args:
            config_type: 配置类型或文件扩展名
        
        Returns:
            ConfigParser: 创建的解析器对象
        
        Raises:
            ValueError: 不支持的配置类型
        """
        config_type = config_type.lower().strip().lstrip('.')
        
        if config_type in ConfigParserFactory.SUPPORTED_PARSERS:
            parser_name, parser_class = ConfigParserFactory.SUPPORTED_PARSERS[config_type]
            print(f"🏭 配置解析器工厂正在创建 {parser_name} 解析器...")
            parser = parser_class()
            print(f"✅ {parser.name} 创建成功")
            return parser
        else:
            supported = list(set([name for name, _ in ConfigParserFactory.SUPPORTED_PARSERS.values()]))
            raise ValueError(f"不支持的配置类型: {config_type}。支持的类型: {supported}")
    
    @staticmethod
    def create_parser_from_file(file_path: str) -> ConfigParser:
        """根据文件扩展名创建解析器"""
        _, ext = os.path.splitext(file_path)
        if not ext:
            raise ValueError(f"无法从文件路径确定配置类型: {file_path}")
        
        return ConfigParserFactory.create_parser(ext)
    
    @staticmethod
    def auto_detect_type(content: str) -> str:
        """自动检测配置类型"""
        content_stripped = content.strip()
        
        # JSON检测
        if content_stripped.startswith(('{', '[')):
            try:
                json.loads(content)
                return "json"
            except:
                pass
        
        # XML检测
        if content_stripped.startswith('<?xml') or content_stripped.startswith('<'):
            return "xml"
        
        # INI检测（包含节）
        if '[' in content and ']' in content:
            return "ini"
        
        # YAML检测（包含冒号但不是每行都有等号）
        lines = content.split('\n')
        has_colon = any(':' in line for line in lines if line.strip() and not line.strip().startswith('#'))
        has_equals = any('=' in line for line in lines if line.strip() and not line.strip().startswith('#'))
        
        if has_colon and not has_equals:
            return "yaml"
        
        # Properties检测
        if has_equals:
            return "properties"
        
        # 默认为JSON
        return "json"


# ==================== 配置管理器 ====================
class ConfigManager:
    """配置管理器 - 演示工厂的使用"""
    
    def __init__(self):
        self.configs = {}  # 存储加载的配置
        self.parsers = {}  # 缓存解析器实例
    
    def load_config(self, file_path: str, config_name: Optional[str] = None) -> Dict[str, Any]:
        """加载配置文件"""
        if config_name is None:
            config_name = os.path.basename(file_path)
        
        try:
            # 根据文件扩展名创建解析器
            parser = ConfigParserFactory.create_parser_from_file(file_path)
            config = parser.load_from_file(file_path)
            
            # 存储配置
            self.configs[config_name] = {
                "config": config,
                "file_path": file_path,
                "parser": parser,
                "loaded_time": datetime.now()
            }
            
            return config
            
        except Exception as e:
            print(f"❌ 加载配置失败: {e}")
            raise
    
    def save_config(self, config_name: str, file_path: Optional[str] = None):
        """保存配置到文件"""
        if config_name not in self.configs:
            raise ValueError(f"配置不存在: {config_name}")
        
        config_info = self.configs[config_name]
        target_path = file_path or config_info["file_path"]
        
        parser = config_info["parser"]
        config = config_info["config"]
        
        parser.save_to_file(config, target_path)
    
    def get_config(self, config_name: str) -> Dict[str, Any]:
        """获取配置"""
        if config_name not in self.configs:
            raise ValueError(f"配置不存在: {config_name}")
        
        return self.configs[config_name]["config"]
    
    def set_config_value(self, config_name: str, key: str, value: Any):
        """设置配置值"""
        if config_name not in self.configs:
            raise ValueError(f"配置不存在: {config_name}")
        
        self.configs[config_name]["config"][key] = value
        print(f"✅ 配置 {config_name} 的 {key} 已更新为: {value}")
    
    def list_configs(self):
        """列出所有配置"""
        if not self.configs:
            print("📭 没有加载的配置")
            return
        
        print(f"📋 已加载的配置 - 共 {len(self.configs)} 个")
        print("=" * 60)
        
        for name, info in self.configs.items():
            config = info["config"]
            parser = info["parser"]
            loaded_time = info["loaded_time"]
            
            print(f"配置名: {name}")
            print(f"  文件路径: {info['file_path']}")
            print(f"  解析器: {parser.name}")
            print(f"  配置项数: {len(config)}")
            print(f"  加载时间: {loaded_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()


# ==================== 演示函数 ====================
def demo_config_parsing():
    """演示配置解析功能"""
    print("=== 配置解析器工厂演示 ===\n")
    
    # 创建示例配置内容
    configs = {
        "app.json": {
            "type": "json",
            "content": '{"app_name": "MyApp", "version": "1.0.0", "debug": true, "port": 8080}'
        },
        "database.ini": {
            "type": "ini",
            "content": """[database]
host = localhost
port = 5432
username = admin
password = secret123

[cache]
enabled = true
ttl = 3600"""
        },
        "server.yaml": {
            "type": "yaml",
            "content": """host: "0.0.0.0"
port: 8000
workers: 4
debug: false
timeout: 30"""
        },
        "app.properties": {
            "type": "properties",
            "content": """app.name = MyApplication
app.version = 2.1.0
server.port = 9090
logging.level = INFO"""
        }
    }
    
    manager = ConfigManager()
    
    # 创建临时配置文件并加载
    for filename, config_info in configs.items():
        print(f"\n--- 处理配置文件: {filename} ---")
        
        try:
            # 创建解析器并解析内容
            parser = ConfigParserFactory.create_parser(config_info["type"])
            parsed_config = parser.parse(config_info["content"])
            
            print(f"解析结果: {parsed_config}")
            
            # 测试序列化
            serialized = parser.serialize(parsed_config)
            print(f"序列化结果:\n{serialized}")
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
    
    # 显示所有配置
    manager.list_configs()


def demo_auto_detection():
    """演示自动类型检测"""
    print("\n" + "=" * 60)
    print("自动类型检测演示")
    print("=" * 60)
    
    test_contents = [
        ('{"name": "test", "value": 123}', "JSON格式"),
        ('[section]\nkey = value', "INI格式"),
        ('name: test\nvalue: 123', "YAML格式"),
        ('<?xml version="1.0"?><config><name>test</name></config>', "XML格式"),
        ('app.name = TestApp\napp.version = 1.0', "Properties格式")
    ]
    
    for content, description in test_contents:
        print(f"\n测试内容 ({description}):")
        print(f"内容: {content}")
        
        detected_type = ConfigParserFactory.auto_detect_type(content)
        print(f"检测结果: {detected_type}")
        
        try:
            parser = ConfigParserFactory.create_parser(detected_type)
            result = parser.parse(content)
            print(f"解析成功: {result}")
        except Exception as e:
            print(f"解析失败: {e}")


def main():
    """主函数"""
    demo_config_parsing()
    demo_auto_detection()
    
    print("\n" + "=" * 60)
    print("简单工厂模式在配置管理中的优势:")
    print("1. 格式无关性：统一的接口处理不同格式的配置文件")
    print("2. 自动检测：可以自动识别配置文件格式")
    print("3. 类型安全：每个解析器都有相应的验证逻辑")
    print("4. 易于扩展：添加新的配置格式很简单")
    print("5. 序列化支持：支持配置的读取和写入")
    print("=" * 60)


if __name__ == "__main__":
    main()
