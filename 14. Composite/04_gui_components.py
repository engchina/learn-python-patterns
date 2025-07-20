"""
组合模式GUI应用 - 图形用户界面组件系统

这个示例展示了组合模式在GUI系统中的应用，演示如何构建
复杂的用户界面组件层次结构。

作者: Composite Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Tuple
from enum import Enum


class EventType(Enum):
    """事件类型枚举"""
    CLICK = "click"
    HOVER = "hover"
    FOCUS = "focus"
    BLUR = "blur"
    RESIZE = "resize"


class UIComponent(ABC):
    """UI组件抽象基类"""
    
    def __init__(self, name: str, x: int = 0, y: int = 0, width: int = 100, height: int = 30):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
        self.parent: Optional['Container'] = None
        self.event_handlers: Dict[EventType, List[callable]] = {}
    
    @abstractmethod
    def render(self, indent: int = 0) -> str:
        """渲染组件"""
        pass
    
    @abstractmethod
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """获取组件边界 (x, y, width, height)"""
        pass
    
    def add_event_handler(self, event_type: EventType, handler: callable) -> None:
        """添加事件处理器"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def trigger_event(self, event_type: EventType, event_data: Dict = None) -> None:
        """触发事件"""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                handler(self, event_data or {})
    
    def set_position(self, x: int, y: int) -> None:
        """设置位置"""
        self.x = x
        self.y = y
    
    def set_size(self, width: int, height: int) -> None:
        """设置大小"""
        self.width = width
        self.height = height
    
    def set_visible(self, visible: bool) -> None:
        """设置可见性"""
        self.visible = visible
    
    def set_enabled(self, enabled: bool) -> None:
        """设置启用状态"""
        self.enabled = enabled
    
    def get_absolute_position(self) -> Tuple[int, int]:
        """获取绝对位置"""
        if self.parent:
            parent_x, parent_y = self.parent.get_absolute_position()
            return (parent_x + self.x, parent_y + self.y)
        return (self.x, self.y)


class Button(UIComponent):
    """按钮组件 - 叶子组件"""
    
    def __init__(self, name: str, text: str, x: int = 0, y: int = 0, 
                 width: int = 100, height: int = 30):
        super().__init__(name, x, y, width, height)
        self.text = text
        self.clicked = False
    
    def render(self, indent: int = 0) -> str:
        """渲染按钮"""
        prefix = "  " * indent
        status = "✓" if self.clicked else " "
        state = "" if self.enabled else " (禁用)"
        visibility = "" if self.visible else " (隐藏)"
        return f"{prefix}🔘 按钮 '{self.name}': '{self.text}' [{status}]{state}{visibility}"
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """获取按钮边界"""
        return (self.x, self.y, self.width, self.height)
    
    def click(self) -> None:
        """点击按钮"""
        if self.enabled and self.visible:
            self.clicked = True
            self.trigger_event(EventType.CLICK, {"button": self.text})
            print(f"🖱️  按钮 '{self.text}' 被点击")


class Label(UIComponent):
    """标签组件 - 叶子组件"""
    
    def __init__(self, name: str, text: str, x: int = 0, y: int = 0, 
                 width: int = 100, height: int = 20):
        super().__init__(name, x, y, width, height)
        self.text = text
        self.font_size = 12
    
    def render(self, indent: int = 0) -> str:
        """渲染标签"""
        prefix = "  " * indent
        visibility = "" if self.visible else " (隐藏)"
        return f"{prefix}🏷️  标签 '{self.name}': '{self.text}'{visibility}"
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """获取标签边界"""
        return (self.x, self.y, self.width, self.height)
    
    def set_text(self, text: str) -> None:
        """设置文本"""
        self.text = text
        print(f"📝 标签 '{self.name}' 文本已更新为: '{text}'")


class TextBox(UIComponent):
    """文本框组件 - 叶子组件"""
    
    def __init__(self, name: str, placeholder: str = "", x: int = 0, y: int = 0, 
                 width: int = 150, height: int = 25):
        super().__init__(name, x, y, width, height)
        self.placeholder = placeholder
        self.value = ""
        self.focused = False
    
    def render(self, indent: int = 0) -> str:
        """渲染文本框"""
        prefix = "  " * indent
        content = self.value if self.value else f"[{self.placeholder}]"
        focus_indicator = "🔍" if self.focused else "📝"
        state = "" if self.enabled else " (禁用)"
        visibility = "" if self.visible else " (隐藏)"
        return f"{prefix}{focus_indicator} 文本框 '{self.name}': {content}{state}{visibility}"
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """获取文本框边界"""
        return (self.x, self.y, self.width, self.height)
    
    def set_value(self, value: str) -> None:
        """设置值"""
        self.value = value
        print(f"✏️  文本框 '{self.name}' 值已设置为: '{value}'")
    
    def focus(self) -> None:
        """获得焦点"""
        self.focused = True
        self.trigger_event(EventType.FOCUS)
        print(f"🎯 文本框 '{self.name}' 获得焦点")
    
    def blur(self) -> None:
        """失去焦点"""
        self.focused = False
        self.trigger_event(EventType.BLUR)
        print(f"😶 文本框 '{self.name}' 失去焦点")


class Container(UIComponent):
    """容器组件 - 组合组件"""
    
    def __init__(self, name: str, x: int = 0, y: int = 0, width: int = 300, height: int = 200):
        super().__init__(name, x, y, width, height)
        self._children: List[UIComponent] = []
        self.background_color = "white"
        self.border = True
    
    def render(self, indent: int = 0) -> str:
        """渲染容器"""
        prefix = "  " * indent
        visibility = "" if self.visible else " (隐藏)"
        result = [f"{prefix}📦 容器 '{self.name}' ({len(self._children)} 个子组件){visibility}"]
        
        if self.visible:
            for child in self._children:
                result.append(child.render(indent + 1))
        
        return "\n".join(result)
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """获取容器边界"""
        return (self.x, self.y, self.width, self.height)
    
    def add_component(self, component: UIComponent) -> None:
        """添加子组件"""
        if component not in self._children:
            component.parent = self
            self._children.append(component)
            print(f"➕ 组件 '{component.name}' 已添加到容器 '{self.name}'")
        else:
            print(f"⚠️  组件 '{component.name}' 已存在于容器 '{self.name}' 中")
    
    def remove_component(self, component: UIComponent) -> None:
        """移除子组件"""
        if component in self._children:
            component.parent = None
            self._children.remove(component)
            print(f"➖ 组件 '{component.name}' 已从容器 '{self.name}' 中移除")
        else:
            print(f"⚠️  组件 '{component.name}' 不存在于容器 '{self.name}' 中")
    
    def find_component(self, name: str) -> Optional[UIComponent]:
        """查找组件"""
        for child in self._children:
            if child.name == name:
                return child
            if isinstance(child, Container):
                found = child.find_component(name)
                if found:
                    return found
        return None
    
    def get_all_components(self) -> List[UIComponent]:
        """获取所有子组件（递归）"""
        components = []
        for child in self._children:
            components.append(child)
            if isinstance(child, Container):
                components.extend(child.get_all_components())
        return components
    
    def layout_vertical(self, spacing: int = 5) -> None:
        """垂直布局"""
        current_y = spacing
        for child in self._children:
            child.set_position(spacing, current_y)
            current_y += child.height + spacing
        print(f"📐 容器 '{self.name}' 已应用垂直布局")
    
    def layout_horizontal(self, spacing: int = 5) -> None:
        """水平布局"""
        current_x = spacing
        for child in self._children:
            child.set_position(current_x, spacing)
            current_x += child.width + spacing
        print(f"📐 容器 '{self.name}' 已应用水平布局")


class Window(Container):
    """窗口组件 - 特殊的容器"""
    
    def __init__(self, name: str, title: str, width: int = 400, height: int = 300):
        super().__init__(name, 0, 0, width, height)
        self.title = title
        self.resizable = True
        self.minimized = False
        self.maximized = False
    
    def render(self, indent: int = 0) -> str:
        """渲染窗口"""
        prefix = "  " * indent
        state = ""
        if self.minimized:
            state = " (最小化)"
        elif self.maximized:
            state = " (最大化)"
        
        visibility = "" if self.visible else " (隐藏)"
        result = [f"{prefix}🪟 窗口 '{self.title}' ({len(self._children)} 个组件){state}{visibility}"]
        
        if self.visible and not self.minimized:
            for child in self._children:
                result.append(child.render(indent + 1))
        
        return "\n".join(result)
    
    def minimize(self) -> None:
        """最小化窗口"""
        self.minimized = True
        self.maximized = False
        print(f"🔽 窗口 '{self.title}' 已最小化")
    
    def maximize(self) -> None:
        """最大化窗口"""
        self.maximized = True
        self.minimized = False
        print(f"🔼 窗口 '{self.title}' 已最大化")
    
    def restore(self) -> None:
        """还原窗口"""
        self.minimized = False
        self.maximized = False
        print(f"↩️  窗口 '{self.title}' 已还原")


def demo_gui_components():
    """GUI组件系统演示"""
    print("=" * 60)
    print("🖥️  GUI组件系统 - 组合模式演示")
    print("=" * 60)
    
    # 创建主窗口
    main_window = Window("main_window", "用户管理系统", 600, 400)
    
    # 创建头部面板
    header_panel = Container("header", 0, 0, 580, 60)
    title_label = Label("title", "用户管理系统", 10, 20, 200, 25)
    
    # 创建表单面板
    form_panel = Container("form", 0, 70, 580, 150)
    name_label = Label("name_label", "姓名:", 20, 20, 60, 20)
    name_input = TextBox("name_input", "请输入姓名", 90, 20, 150, 25)
    email_label = Label("email_label", "邮箱:", 20, 60, 60, 20)
    email_input = TextBox("email_input", "请输入邮箱", 90, 60, 150, 25)
    
    # 创建按钮面板
    button_panel = Container("buttons", 0, 230, 580, 50)
    save_button = Button("save_btn", "保存", 20, 10, 80, 30)
    cancel_button = Button("cancel_btn", "取消", 110, 10, 80, 30)
    delete_button = Button("delete_btn", "删除", 200, 10, 80, 30)
    
    # 构建UI层次结构
    print("\n🏗️  构建UI结构:")
    
    # 添加到头部面板
    header_panel.add_component(title_label)
    
    # 添加到表单面板
    form_panel.add_component(name_label)
    form_panel.add_component(name_input)
    form_panel.add_component(email_label)
    form_panel.add_component(email_input)
    
    # 添加到按钮面板
    button_panel.add_component(save_button)
    button_panel.add_component(cancel_button)
    button_panel.add_component(delete_button)
    
    # 添加到主窗口
    main_window.add_component(header_panel)
    main_window.add_component(form_panel)
    main_window.add_component(button_panel)
    
    # 添加事件处理器
    def on_save_click(component, event_data):
        print(f"💾 保存用户信息: 姓名={name_input.value}, 邮箱={email_input.value}")
    
    def on_cancel_click(component, event_data):
        name_input.set_value("")
        email_input.set_value("")
        print("🚫 已取消操作，清空表单")
    
    save_button.add_event_handler(EventType.CLICK, on_save_click)
    cancel_button.add_event_handler(EventType.CLICK, on_cancel_click)
    
    # 显示UI结构
    print(f"\n🖼️  UI结构:")
    print(main_window.render())
    
    # 模拟用户交互
    print(f"\n🖱️  模拟用户交互:")
    name_input.focus()
    name_input.set_value("张三")
    name_input.blur()
    
    email_input.focus()
    email_input.set_value("zhangsan@example.com")
    email_input.blur()
    
    save_button.click()
    
    print(f"\n🖼️  交互后的UI状态:")
    print(main_window.render())


if __name__ == "__main__":
    demo_gui_components()
