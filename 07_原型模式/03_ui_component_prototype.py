"""
03_ui_component_prototype.py - UI组件原型模式

用户界面组件系统示例
这个示例展示了如何使用原型模式来创建UI组件。
在GUI开发中，经常需要创建相似的UI组件，
原型模式可以提供预配置的组件模板，快速构建界面。
"""

import copy
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any


# ==================== UI组件原型接口 ====================
class UIComponentPrototype(ABC):
    """UI组件原型抽象基类"""
    
    @abstractmethod
    def clone(self):
        """克隆组件"""
        pass
    
    @abstractmethod
    def render(self) -> str:
        """渲染组件"""
        pass
    
    @abstractmethod
    def set_position(self, x: int, y: int):
        """设置位置"""
        pass
    
    @abstractmethod
    def set_size(self, width: int, height: int):
        """设置大小"""
        pass


# ==================== 具体UI组件类 ====================
class Button(UIComponentPrototype):
    """按钮组件"""
    
    def __init__(self, text: str = "按钮"):
        self.text = text
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 30
        self.background_color = "#f0f0f0"
        self.text_color = "#000000"
        self.font_size = 12
        self.border_width = 1
        self.border_color = "#cccccc"
        self.is_enabled = True
        self.is_visible = True
        self.click_handler = None
        self.styles = {}
    
    def clone(self):
        """克隆按钮"""
        new_button = copy.copy(self)
        new_button.styles = self.styles.copy()
        return new_button
    
    def set_position(self, x: int, y: int):
        """设置位置"""
        self.x = x
        self.y = y
    
    def set_size(self, width: int, height: int):
        """设置大小"""
        self.width = width
        self.height = height
    
    def set_text(self, text: str):
        """设置按钮文本"""
        self.text = text
    
    def set_colors(self, bg_color: str, text_color: str):
        """设置颜色"""
        self.background_color = bg_color
        self.text_color = text_color
    
    def set_click_handler(self, handler):
        """设置点击事件处理器"""
        self.click_handler = handler
    
    def render(self) -> str:
        """渲染按钮"""
        return (f"按钮组件:\n"
                f"  文本: {self.text}\n"
                f"  位置: ({self.x}, {self.y})\n"
                f"  大小: {self.width}x{self.height}\n"
                f"  背景色: {self.background_color}\n"
                f"  文字色: {self.text_color}\n"
                f"  字体大小: {self.font_size}px\n"
                f"  启用状态: {self.is_enabled}")


class TextBox(UIComponentPrototype):
    """文本框组件"""
    
    def __init__(self, placeholder: str = "请输入文本"):
        self.placeholder = placeholder
        self.value = ""
        self.x = 0
        self.y = 0
        self.width = 200
        self.height = 25
        self.background_color = "#ffffff"
        self.text_color = "#000000"
        self.border_color = "#cccccc"
        self.font_size = 12
        self.is_readonly = False
        self.is_enabled = True
        self.is_visible = True
        self.max_length = 255
        self.validation_rules = []
    
    def clone(self):
        """克隆文本框"""
        new_textbox = copy.copy(self)
        new_textbox.validation_rules = self.validation_rules.copy()
        return new_textbox
    
    def set_position(self, x: int, y: int):
        """设置位置"""
        self.x = x
        self.y = y
    
    def set_size(self, width: int, height: int):
        """设置大小"""
        self.width = width
        self.height = height
    
    def set_value(self, value: str):
        """设置文本值"""
        if len(value) <= self.max_length:
            self.value = value
        else:
            raise ValueError(f"文本长度超过最大限制 {self.max_length}")
    
    def add_validation_rule(self, rule: str):
        """添加验证规则"""
        self.validation_rules.append(rule)
    
    def render(self) -> str:
        """渲染文本框"""
        return (f"文本框组件:\n"
                f"  占位符: {self.placeholder}\n"
                f"  当前值: {self.value}\n"
                f"  位置: ({self.x}, {self.y})\n"
                f"  大小: {self.width}x{self.height}\n"
                f"  只读: {self.is_readonly}\n"
                f"  最大长度: {self.max_length}\n"
                f"  验证规则: {self.validation_rules}")


class Panel(UIComponentPrototype):
    """面板组件"""
    
    def __init__(self, title: str = "面板"):
        self.title = title
        self.x = 0
        self.y = 0
        self.width = 300
        self.height = 200
        self.background_color = "#f5f5f5"
        self.border_color = "#cccccc"
        self.border_width = 1
        self.padding = 10
        self.children = []
        self.layout_type = "absolute"  # absolute, flow, grid
        self.is_visible = True
        self.is_collapsible = False
        self.is_collapsed = False
    
    def clone(self):
        """克隆面板"""
        new_panel = copy.copy(self)
        # 深拷贝子组件列表
        new_panel.children = []
        for child in self.children:
            new_panel.children.append(child.clone())
        return new_panel
    
    def set_position(self, x: int, y: int):
        """设置位置"""
        self.x = x
        self.y = y
    
    def set_size(self, width: int, height: int):
        """设置大小"""
        self.width = width
        self.height = height
    
    def add_child(self, child: UIComponentPrototype):
        """添加子组件"""
        self.children.append(child)
    
    def remove_child(self, child: UIComponentPrototype):
        """移除子组件"""
        if child in self.children:
            self.children.remove(child)
    
    def set_layout(self, layout_type: str):
        """设置布局类型"""
        self.layout_type = layout_type
    
    def render(self) -> str:
        """渲染面板"""
        content = (f"面板组件:\n"
                  f"  标题: {self.title}\n"
                  f"  位置: ({self.x}, {self.y})\n"
                  f"  大小: {self.width}x{self.height}\n"
                  f"  布局: {self.layout_type}\n"
                  f"  子组件数量: {len(self.children)}\n")
        
        if self.children:
            content += "  子组件:\n"
            for i, child in enumerate(self.children):
                child_info = child.render().replace('\n', '\n    ')
                content += f"    [{i+1}] {child_info}\n"
        
        return content


class Menu(UIComponentPrototype):
    """菜单组件"""
    
    def __init__(self, title: str = "菜单"):
        self.title = title
        self.x = 0
        self.y = 0
        self.width = 150
        self.height = 25
        self.background_color = "#ffffff"
        self.text_color = "#000000"
        self.hover_color = "#e0e0e0"
        self.items = []
        self.is_horizontal = True
        self.is_visible = True
        self.separator_color = "#cccccc"
    
    def clone(self):
        """克隆菜单"""
        new_menu = copy.copy(self)
        new_menu.items = copy.deepcopy(self.items)
        return new_menu
    
    def set_position(self, x: int, y: int):
        """设置位置"""
        self.x = x
        self.y = y
    
    def set_size(self, width: int, height: int):
        """设置大小"""
        self.width = width
        self.height = height
    
    def add_item(self, text: str, action=None, submenu=None):
        """添加菜单项"""
        item = {
            "text": text,
            "action": action,
            "submenu": submenu,
            "enabled": True,
            "separator": False
        }
        self.items.append(item)
    
    def add_separator(self):
        """添加分隔符"""
        separator = {
            "text": "",
            "action": None,
            "submenu": None,
            "enabled": False,
            "separator": True
        }
        self.items.append(separator)
    
    def render(self) -> str:
        """渲染菜单"""
        content = (f"菜单组件:\n"
                  f"  标题: {self.title}\n"
                  f"  位置: ({self.x}, {self.y})\n"
                  f"  大小: {self.width}x{self.height}\n"
                  f"  方向: {'水平' if self.is_horizontal else '垂直'}\n"
                  f"  菜单项:\n")
        
        for item in self.items:
            if item["separator"]:
                content += "    --------\n"
            else:
                content += f"    {item['text']}\n"
        
        return content


# ==================== UI组件工厂 ====================
class UIComponentFactory:
    """UI组件工厂"""
    
    def __init__(self):
        self._prototypes: Dict[str, UIComponentPrototype] = {}
        self._initialize_default_prototypes()
    
    def _initialize_default_prototypes(self):
        """初始化默认原型"""
        # 按钮原型
        primary_button = Button("主要按钮")
        primary_button.set_colors("#007bff", "#ffffff")
        primary_button.font_size = 14
        
        secondary_button = Button("次要按钮")
        secondary_button.set_colors("#6c757d", "#ffffff")
        
        danger_button = Button("危险按钮")
        danger_button.set_colors("#dc3545", "#ffffff")
        
        # 文本框原型
        email_textbox = TextBox("请输入邮箱地址")
        email_textbox.add_validation_rule("email")
        email_textbox.max_length = 100
        
        password_textbox = TextBox("请输入密码")
        password_textbox.add_validation_rule("password")
        password_textbox.max_length = 50
        
        # 面板原型
        form_panel = Panel("表单面板")
        form_panel.set_size(400, 300)
        form_panel.layout_type = "flow"
        
        # 菜单原型
        main_menu = Menu("主菜单")
        main_menu.add_item("文件")
        main_menu.add_item("编辑")
        main_menu.add_item("视图")
        main_menu.add_separator()
        main_menu.add_item("帮助")
        
        # 注册原型
        self.register_prototype("primary_button", primary_button)
        self.register_prototype("secondary_button", secondary_button)
        self.register_prototype("danger_button", danger_button)
        self.register_prototype("email_textbox", email_textbox)
        self.register_prototype("password_textbox", password_textbox)
        self.register_prototype("form_panel", form_panel)
        self.register_prototype("main_menu", main_menu)
    
    def register_prototype(self, name: str, prototype: UIComponentPrototype):
        """注册原型"""
        self._prototypes[name] = prototype
        print(f"UI工厂: 已注册原型 '{name}'")
    
    def create_component(self, prototype_name: str) -> UIComponentPrototype:
        """创建组件"""
        if prototype_name not in self._prototypes:
            raise ValueError(f"未找到原型 '{prototype_name}'")
        
        component = self._prototypes[prototype_name].clone()
        print(f"UI工厂: 基于 '{prototype_name}' 创建了组件")
        return component
    
    def list_prototypes(self) -> List[str]:
        """列出所有原型"""
        return list(self._prototypes.keys())


# ==================== 演示函数 ====================
def demonstrate_ui_cloning():
    """演示UI组件克隆"""
    print("=" * 50)
    print("UI组件克隆演示")
    print("=" * 50)
    
    # 创建原始按钮
    original_button = Button("保存")
    original_button.set_position(10, 10)
    original_button.set_colors("#28a745", "#ffffff")
    
    print("原始按钮:")
    print(original_button.render())
    print()
    
    # 克隆按钮
    cloned_button = original_button.clone()
    cloned_button.set_text("取消")
    cloned_button.set_position(120, 10)
    cloned_button.set_colors("#dc3545", "#ffffff")
    
    print("克隆按钮:")
    print(cloned_button.render())


def demonstrate_ui_factory():
    """演示UI组件工厂"""
    print("\n" + "=" * 50)
    print("UI组件工厂演示")
    print("=" * 50)
    
    factory = UIComponentFactory()
    
    print("可用的组件原型:")
    for prototype in factory.list_prototypes():
        print(f"- {prototype}")
    print()
    
    # 创建登录表单
    print("创建登录表单:")
    login_panel = factory.create_component("form_panel")
    login_panel.title = "用户登录"
    
    username_field = factory.create_component("email_textbox")
    username_field.placeholder = "用户名"
    username_field.set_position(20, 50)
    
    password_field = factory.create_component("password_textbox")
    password_field.set_position(20, 90)
    
    login_button = factory.create_component("primary_button")
    login_button.set_text("登录")
    login_button.set_position(20, 130)
    
    cancel_button = factory.create_component("secondary_button")
    cancel_button.set_text("取消")
    cancel_button.set_position(130, 130)
    
    # 组装表单
    login_panel.add_child(username_field)
    login_panel.add_child(password_field)
    login_panel.add_child(login_button)
    login_panel.add_child(cancel_button)
    
    print(login_panel.render())


def main():
    """主函数"""
    print("UI组件原型模式演示")
    
    demonstrate_ui_cloning()
    demonstrate_ui_factory()
    
    print("\n" + "=" * 50)
    print("演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
