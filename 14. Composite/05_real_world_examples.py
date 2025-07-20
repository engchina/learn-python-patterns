"""
组合模式实际应用案例集合

这个文件包含了多个实际项目中组合模式的应用案例，展示了
不同场景下组合模式的变体和最佳实践。

作者: Composite Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import json
from enum import Enum


# ==================== 案例1: 菜单系统 ====================

class MenuComponent(ABC):
    """菜单组件抽象基类"""
    
    def __init__(self, name: str, icon: str = ""):
        self.name = name
        self.icon = icon
        self.enabled = True
        self.visible = True
    
    @abstractmethod
    def execute(self) -> None:
        """执行菜单项"""
        pass
    
    @abstractmethod
    def render(self, indent: int = 0) -> str:
        """渲染菜单"""
        pass


class MenuItem(MenuComponent):
    """菜单项 - 叶子组件"""
    
    def __init__(self, name: str, action: callable = None, icon: str = "📄", 
                 shortcut: str = ""):
        super().__init__(name, icon)
        self.action = action
        self.shortcut = shortcut
    
    def execute(self) -> None:
        """执行菜单项动作"""
        if self.action and self.enabled:
            print(f"🎯 执行菜单项: {self.name}")
            self.action()
        elif not self.enabled:
            print(f"⚠️  菜单项 '{self.name}' 已禁用")
    
    def render(self, indent: int = 0) -> str:
        """渲染菜单项"""
        prefix = "  " * indent
        shortcut_text = f" ({self.shortcut})" if self.shortcut else ""
        state = "" if self.enabled else " [禁用]"
        return f"{prefix}{self.icon} {self.name}{shortcut_text}{state}"


class Menu(MenuComponent):
    """菜单 - 组合组件"""
    
    def __init__(self, name: str, icon: str = "📁"):
        super().__init__(name, icon)
        self._items: List[MenuComponent] = []
    
    def execute(self) -> None:
        """显示菜单"""
        print(f"📋 显示菜单: {self.name}")
        print(self.render())
    
    def render(self, indent: int = 0) -> str:
        """渲染菜单"""
        prefix = "  " * indent
        result = [f"{prefix}{self.icon} {self.name}"]
        
        for item in self._items:
            if item.visible:
                result.append(item.render(indent + 1))
        
        return "\n".join(result)
    
    def add_item(self, item: MenuComponent) -> None:
        """添加菜单项"""
        self._items.append(item)
    
    def remove_item(self, item: MenuComponent) -> None:
        """移除菜单项"""
        if item in self._items:
            self._items.remove(item)
    
    def find_item(self, name: str) -> Optional[MenuComponent]:
        """查找菜单项"""
        for item in self._items:
            if item.name == name:
                return item
            if isinstance(item, Menu):
                found = item.find_item(name)
                if found:
                    return found
        return None


class MenuSeparator(MenuComponent):
    """菜单分隔符 - 特殊的叶子组件"""
    
    def __init__(self):
        super().__init__("---", "")
    
    def execute(self) -> None:
        """分隔符不执行任何操作"""
        pass
    
    def render(self, indent: int = 0) -> str:
        """渲染分隔符"""
        prefix = "  " * indent
        return f"{prefix}{'─' * 20}"


# ==================== 案例2: 表达式解析器 ====================

class Expression(ABC):
    """表达式抽象基类"""
    
    @abstractmethod
    def evaluate(self, context: Dict[str, float] = None) -> float:
        """计算表达式值"""
        pass
    
    @abstractmethod
    def to_string(self) -> str:
        """转换为字符串表示"""
        pass


class NumberExpression(Expression):
    """数字表达式 - 叶子组件"""
    
    def __init__(self, value: float):
        self.value = value
    
    def evaluate(self, context: Dict[str, float] = None) -> float:
        """返回数字值"""
        return self.value
    
    def to_string(self) -> str:
        """返回数字字符串"""
        return str(self.value)


class VariableExpression(Expression):
    """变量表达式 - 叶子组件"""
    
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, context: Dict[str, float] = None) -> float:
        """从上下文中获取变量值"""
        if context and self.name in context:
            return context[self.name]
        raise ValueError(f"未定义的变量: {self.name}")
    
    def to_string(self) -> str:
        """返回变量名"""
        return self.name


class BinaryExpression(Expression):
    """二元表达式 - 组合组件"""
    
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right
    
    def evaluate(self, context: Dict[str, float] = None) -> float:
        """计算二元表达式"""
        left_val = self.left.evaluate(context)
        right_val = self.right.evaluate(context)
        
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            if right_val == 0:
                raise ValueError("除零错误")
            return left_val / right_val
        else:
            raise ValueError(f"不支持的操作符: {self.operator}")
    
    def to_string(self) -> str:
        """返回表达式字符串"""
        return f"({self.left.to_string()} {self.operator} {self.right.to_string()})"


class UnaryExpression(Expression):
    """一元表达式 - 组合组件"""
    
    def __init__(self, operator: str, operand: Expression):
        self.operator = operator
        self.operand = operand
    
    def evaluate(self, context: Dict[str, float] = None) -> float:
        """计算一元表达式"""
        operand_val = self.operand.evaluate(context)
        
        if self.operator == '-':
            return -operand_val
        elif self.operator == '+':
            return operand_val
        else:
            raise ValueError(f"不支持的一元操作符: {self.operator}")
    
    def to_string(self) -> str:
        """返回表达式字符串"""
        return f"{self.operator}{self.operand.to_string()}"


# ==================== 案例3: 配置管理系统 ====================

class ConfigNode(ABC):
    """配置节点抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def get_value(self) -> Any:
        """获取配置值"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """转换为字典"""
        pass


class ConfigValue(ConfigNode):
    """配置值 - 叶子组件"""
    
    def __init__(self, name: str, value: Any):
        super().__init__(name)
        self.value = value
    
    def get_value(self) -> Any:
        """获取值"""
        return self.value
    
    def set_value(self, value: Any) -> None:
        """设置值"""
        self.value = value
    
    def to_dict(self) -> Any:
        """返回值本身"""
        return self.value


class ConfigSection(ConfigNode):
    """配置节 - 组合组件"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self._children: Dict[str, ConfigNode] = {}
    
    def get_value(self) -> Dict:
        """获取所有子配置"""
        return {name: child.get_value() for name, child in self._children.items()}
    
    def add_config(self, config: ConfigNode) -> None:
        """添加配置项"""
        self._children[config.name] = config
    
    def get_config(self, path: str) -> Optional[ConfigNode]:
        """根据路径获取配置"""
        parts = path.split('.')
        current = self
        
        for part in parts:
            if isinstance(current, ConfigSection) and part in current._children:
                current = current._children[part]
            else:
                return None
        
        return current
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {name: child.to_dict() for name, child in self._children.items()}


def demo_menu_system():
    """菜单系统演示"""
    print("=" * 50)
    print("📋 菜单系统演示")
    print("=" * 50)
    
    # 创建菜单动作
    def new_file():
        print("📄 创建新文件")
    
    def open_file():
        print("📂 打开文件")
    
    def save_file():
        print("💾 保存文件")
    
    def exit_app():
        print("🚪 退出应用")
    
    # 创建菜单结构
    main_menu = Menu("主菜单", "🏠")
    
    file_menu = Menu("文件", "📁")
    file_menu.add_item(MenuItem("新建", new_file, "📄", "Ctrl+N"))
    file_menu.add_item(MenuItem("打开", open_file, "📂", "Ctrl+O"))
    file_menu.add_item(MenuSeparator())
    file_menu.add_item(MenuItem("保存", save_file, "💾", "Ctrl+S"))
    file_menu.add_item(MenuSeparator())
    file_menu.add_item(MenuItem("退出", exit_app, "🚪", "Alt+F4"))
    
    edit_menu = Menu("编辑", "✏️")
    edit_menu.add_item(MenuItem("复制", lambda: print("📋 复制"), "📋", "Ctrl+C"))
    edit_menu.add_item(MenuItem("粘贴", lambda: print("📄 粘贴"), "📄", "Ctrl+V"))
    
    main_menu.add_item(file_menu)
    main_menu.add_item(edit_menu)
    
    # 显示菜单
    print("🖼️  菜单结构:")
    main_menu.execute()
    
    # 执行菜单项
    print(f"\n🎯 执行菜单项:")
    new_item = main_menu.find_item("新建")
    if new_item:
        new_item.execute()


def demo_expression_parser():
    """表达式解析器演示"""
    print("\n" + "=" * 50)
    print("🧮 表达式解析器演示")
    print("=" * 50)
    
    # 构建表达式: (x + 5) * (y - 2)
    x = VariableExpression("x")
    five = NumberExpression(5)
    y = VariableExpression("y")
    two = NumberExpression(2)
    
    left_expr = BinaryExpression(x, "+", five)
    right_expr = BinaryExpression(y, "-", two)
    main_expr = BinaryExpression(left_expr, "*", right_expr)
    
    print(f"📝 表达式: {main_expr.to_string()}")
    
    # 计算表达式
    context = {"x": 3, "y": 7}
    result = main_expr.evaluate(context)
    print(f"🧮 当 x={context['x']}, y={context['y']} 时，结果 = {result}")
    
    # 构建更复杂的表达式: -(x + y) / 2
    sum_expr = BinaryExpression(x, "+", y)
    neg_expr = UnaryExpression("-", sum_expr)
    complex_expr = BinaryExpression(neg_expr, "/", NumberExpression(2))
    
    print(f"\n📝 复杂表达式: {complex_expr.to_string()}")
    result2 = complex_expr.evaluate(context)
    print(f"🧮 结果 = {result2}")


def demo_config_system():
    """配置管理系统演示"""
    print("\n" + "=" * 50)
    print("⚙️  配置管理系统演示")
    print("=" * 50)
    
    # 创建配置结构
    root_config = ConfigSection("app")
    
    # 数据库配置
    db_config = ConfigSection("database")
    db_config.add_config(ConfigValue("host", "localhost"))
    db_config.add_config(ConfigValue("port", 5432))
    db_config.add_config(ConfigValue("name", "myapp"))
    
    # 服务器配置
    server_config = ConfigSection("server")
    server_config.add_config(ConfigValue("host", "0.0.0.0"))
    server_config.add_config(ConfigValue("port", 8080))
    server_config.add_config(ConfigValue("debug", True))
    
    # 日志配置
    log_config = ConfigSection("logging")
    log_config.add_config(ConfigValue("level", "INFO"))
    log_config.add_config(ConfigValue("file", "app.log"))
    
    root_config.add_config(db_config)
    root_config.add_config(server_config)
    root_config.add_config(log_config)
    
    # 显示配置
    print("📋 配置结构:")
    config_dict = root_config.to_dict()
    print(json.dumps(config_dict, indent=2, ensure_ascii=False))
    
    # 获取特定配置
    print(f"\n🔍 获取特定配置:")
    db_host = root_config.get_config("database.host")
    if db_host:
        print(f"  数据库主机: {db_host.get_value()}")
    
    server_port = root_config.get_config("server.port")
    if server_port:
        print(f"  服务器端口: {server_port.get_value()}")


if __name__ == "__main__":
    demo_menu_system()
    demo_expression_parser()
    demo_config_system()
