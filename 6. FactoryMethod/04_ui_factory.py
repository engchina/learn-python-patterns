"""
04_ui_factory.py - UI组件工厂方法模式

UI组件主题系统示例
这个示例展示了工厂方法模式在GUI开发中的应用。
我们有不同主题的UI组件（现代主题、经典主题、暗黑主题），每种主题都有对应的组件工厂。
通过工厂方法模式，可以轻松实现主题切换和组件的统一创建。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import time


# ==================== 抽象产品：UI组件 ====================
class UIComponent(ABC):
    """UI组件抽象基类"""

    def __init__(self, text: str, width: int = 100, height: int = 30):
        self.text = text
        self.width = width
        self.height = height
        self.theme_name = ""

    @abstractmethod
    def render(self) -> str:
        """渲染组件"""
        pass

    @abstractmethod
    def get_style_info(self) -> Dict[str, Any]:
        """获取样式信息"""
        pass

    def get_component_info(self) -> str:
        """获取组件基本信息"""
        return f"{self.__class__.__name__}('{self.text}', {self.width}x{self.height})"


class Button(UIComponent):
    """按钮组件抽象基类"""

    def __init__(self, text: str, width: int = 100, height: int = 30):
        super().__init__(text, width, height)
        self.clickable = True


class TextField(UIComponent):
    """文本输入框组件抽象基类"""

    def __init__(self, placeholder: str = "", width: int = 200, height: int = 25):
        super().__init__(placeholder, width, height)
        self.placeholder = placeholder
        self.editable = True


class Label(UIComponent):
    """标签组件抽象基类"""

    def __init__(self, text: str, width: int = 150, height: int = 20):
        super().__init__(text, width, height)
        self.selectable = False


# ==================== 具体产品：现代主题组件 ====================
class ModernButton(Button):
    """现代主题按钮"""

    def __init__(self, text: str, width: int = 100, height: int = 30):
        super().__init__(text, width, height)
        self.theme_name = "现代主题"

    def render(self) -> str:
        return f"""
┌─────────────────────────────────┐
│  🔘 {self.text:<25} │  现代按钮
│     渐变背景 + 圆角边框         │
└─────────────────────────────────┘"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "border": "none",
            "border_radius": "8px",
            "color": "#ffffff",
            "font_weight": "500",
            "box_shadow": "0 4px 15px rgba(0,0,0,0.2)"
        }


class ModernTextField(TextField):
    """现代主题文本输入框"""

    def __init__(self, placeholder: str = "", width: int = 200, height: int = 25):
        super().__init__(placeholder, width, height)
        self.theme_name = "现代主题"

    def render(self) -> str:
        return f"""
┌─────────────────────────────────────────┐
│  📝 {self.placeholder:<30} │  现代输入框
│     浮动标签 + 下划线动画               │
└─────────────────────────────────────────┘"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "border": "none",
            "border_bottom": "2px solid #e0e0e0",
            "background": "transparent",
            "padding": "8px 0",
            "font_size": "16px",
            "transition": "border-color 0.3s ease"
        }


class ModernLabel(Label):
    """现代主题标签"""

    def __init__(self, text: str, width: int = 150, height: int = 20):
        super().__init__(text, width, height)
        self.theme_name = "现代主题"

    def render(self) -> str:
        return f"""
┌─────────────────────────────────┐
│  🏷️  {self.text:<25} │  现代标签
│     简洁字体 + 柔和颜色         │
└─────────────────────────────────┘"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "color": "#333333",
            "font_family": "SF Pro Display, Arial, sans-serif",
            "font_weight": "400",
            "letter_spacing": "0.5px"
        }


# ==================== 具体产品：经典主题组件 ====================
class ClassicButton(Button):
    """经典主题按钮"""

    def __init__(self, text: str, width: int = 100, height: int = 30):
        super().__init__(text, width, height)
        self.theme_name = "经典主题"

    def render(self) -> str:
        return f"""
╔═══════════════════════════════════╗
║  ⬜ {self.text:<25} ║  经典按钮
║     3D效果 + 边框阴影             ║
╚═══════════════════════════════════╝"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "background": "#f0f0f0",
            "border": "2px outset #cccccc",
            "color": "#000000",
            "font_family": "Arial, sans-serif",
            "font_weight": "normal"
        }


class ClassicTextField(TextField):
    """经典主题文本输入框"""

    def __init__(self, placeholder: str = "", width: int = 200, height: int = 25):
        super().__init__(placeholder, width, height)
        self.theme_name = "经典主题"

    def render(self) -> str:
        return f"""
╔═══════════════════════════════════════════╗
║  📄 {self.placeholder:<30} ║  经典输入框
║     内嵌边框 + 白色背景                   ║
╚═══════════════════════════════════════════╝"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "border": "2px inset #cccccc",
            "background": "#ffffff",
            "padding": "4px",
            "font_family": "Arial, sans-serif",
            "font_size": "14px"
        }


class ClassicLabel(Label):
    """经典主题标签"""

    def __init__(self, text: str, width: int = 150, height: int = 20):
        super().__init__(text, width, height)
        self.theme_name = "经典主题"

    def render(self) -> str:
        return f"""
╔═══════════════════════════════════╗
║  📋 {self.text:<25} ║  经典标签
║     传统字体 + 标准颜色           ║
╚═══════════════════════════════════╝"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "color": "#000000",
            "font_family": "Arial, sans-serif",
            "font_weight": "normal",
            "background": "transparent"
        }


# ==================== 具体产品：暗黑主题组件 ====================
class DarkButton(Button):
    """暗黑主题按钮"""

    def __init__(self, text: str, width: int = 100, height: int = 30):
        super().__init__(text, width, height)
        self.theme_name = "暗黑主题"

    def render(self) -> str:
        return f"""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓  ⚫ {self.text:<25} ▓  暗黑按钮
▓     霓虹边框 + 发光效果           ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "background": "#1a1a1a",
            "border": "1px solid #00ff88",
            "color": "#00ff88",
            "font_weight": "bold",
            "box_shadow": "0 0 10px rgba(0,255,136,0.3)"
        }


class DarkTextField(TextField):
    """暗黑主题文本输入框"""

    def __init__(self, placeholder: str = "", width: int = 200, height: int = 25):
        super().__init__(placeholder, width, height)
        self.theme_name = "暗黑主题"

    def render(self) -> str:
        return f"""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓  ⚫ {self.placeholder:<30} ▓  暗黑输入框
▓     深色背景 + 霓虹光标                 ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "background": "#2a2a2a",
            "border": "1px solid #444444",
            "color": "#ffffff",
            "caret_color": "#00ff88",
            "padding": "8px"
        }


class DarkLabel(Label):
    """暗黑主题标签"""

    def __init__(self, text: str, width: int = 150, height: int = 20):
        super().__init__(text, width, height)
        self.theme_name = "暗黑主题"

    def render(self) -> str:
        return f"""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓  ⚫ {self.text:<25} ▓  暗黑标签
▓     高对比度 + 发光文字           ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓"""

    def get_style_info(self) -> Dict[str, Any]:
        return {
            "color": "#ffffff",
            "font_weight": "bold",
            "text_shadow": "0 0 5px rgba(255,255,255,0.5)",
            "background": "transparent"
        }


# ==================== 抽象创建者 ====================
class UIThemeFactory(ABC):
    """UI主题工厂抽象基类"""

    @abstractmethod
    def create_button(self, text: str) -> Button:
        """创建按钮"""
        pass

    @abstractmethod
    def create_text_field(self, placeholder: str = "") -> TextField:
        """创建文本输入框"""
        pass

    @abstractmethod
    def create_label(self, text: str) -> Label:
        """创建标签"""
        pass

    def create_form(self, title: str, fields: List[Dict[str, str]]) -> List[UIComponent]:
        """创建表单（业务逻辑）"""
        print(f"🎨 使用 {self.__class__.__name__} 创建表单: {title}")

        components = []

        # 添加标题标签
        title_label = self.create_label(title)
        components.append(title_label)

        # 添加表单字段
        for field in fields:
            # 字段标签
            label = self.create_label(field["label"])
            components.append(label)

            # 输入框
            text_field = self.create_text_field(field.get("placeholder", ""))
            components.append(text_field)

        # 添加提交按钮
        submit_button = self.create_button("提交")
        components.append(submit_button)

        return components


# ==================== 具体创建者 ====================
class ModernThemeFactory(UIThemeFactory):
    """现代主题工厂"""

    def create_button(self, text: str) -> Button:
        return ModernButton(text)

    def create_text_field(self, placeholder: str = "") -> TextField:
        return ModernTextField(placeholder)

    def create_label(self, text: str) -> Label:
        return ModernLabel(text)


class ClassicThemeFactory(UIThemeFactory):
    """经典主题工厂"""

    def create_button(self, text: str) -> Button:
        return ClassicButton(text)

    def create_text_field(self, placeholder: str = "") -> TextField:
        return ClassicTextField(placeholder)

    def create_label(self, text: str) -> Label:
        return ClassicLabel(text)


class DarkThemeFactory(UIThemeFactory):
    """暗黑主题工厂"""

    def create_button(self, text: str) -> Button:
        return DarkButton(text)

    def create_text_field(self, placeholder: str = "") -> TextField:
        return DarkTextField(placeholder)

    def create_label(self, text: str) -> Label:
        return DarkLabel(text)


# ==================== UI应用程序 ====================
class UIApplication:
    """UI应用程序 - 演示主题切换"""

    def __init__(self):
        self.themes = {
            "modern": ModernThemeFactory(),
            "classic": ClassicThemeFactory(),
            "dark": DarkThemeFactory()
        }
        self.current_theme = "modern"

    def set_theme(self, theme_name: str):
        """设置主题"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            print(f"🎨 主题已切换为: {theme_name}")
        else:
            print(f"❌ 不支持的主题: {theme_name}")

    def create_login_form(self) -> List[UIComponent]:
        """创建登录表单"""
        factory = self.themes[self.current_theme]

        fields = [
            {"label": "用户名", "placeholder": "请输入用户名"},
            {"label": "密码", "placeholder": "请输入密码"}
        ]

        return factory.create_form("用户登录", fields)

    def create_registration_form(self) -> List[UIComponent]:
        """创建注册表单"""
        factory = self.themes[self.current_theme]

        fields = [
            {"label": "用户名", "placeholder": "请输入用户名"},
            {"label": "邮箱", "placeholder": "请输入邮箱地址"},
            {"label": "密码", "placeholder": "请输入密码"},
            {"label": "确认密码", "placeholder": "请再次输入密码"}
        ]

        return factory.create_form("用户注册", fields)

    def render_components(self, components: List[UIComponent]):
        """渲染组件列表"""
        print(f"\n🖼️  渲染 {self.current_theme} 主题组件:")
        print("="*60)

        for i, component in enumerate(components, 1):
            print(f"\n组件 {i}: {component.get_component_info()}")
            print(component.render())

            # 显示样式信息
            style_info = component.get_style_info()
            print(f"样式信息: {style_info}")


# ==================== 演示函数 ====================
def demo_ui_themes():
    """演示UI主题系统"""
    print("=== UI组件主题工厂演示 ===\n")

    app = UIApplication()

    # 演示不同主题的登录表单
    themes = ["modern", "classic", "dark"]

    for theme in themes:
        print(f"\n{'='*70}")
        print(f"演示 {theme.upper()} 主题")
        print('='*70)

        app.set_theme(theme)
        login_form = app.create_login_form()
        app.render_components(login_form)


def demo_theme_switching():
    """演示主题切换"""
    print("\n" + "="*70)
    print("主题切换演示")
    print("="*70)

    app = UIApplication()

    # 创建一个简单的界面
    print("\n🔧 创建基础组件...")

    # 现代主题
    app.set_theme("modern")
    modern_button = app.themes["modern"].create_button("现代按钮")

    # 经典主题
    app.set_theme("classic")
    classic_button = app.themes["classic"].create_button("经典按钮")

    # 暗黑主题
    app.set_theme("dark")
    dark_button = app.themes["dark"].create_button("暗黑按钮")

    # 展示不同主题的同一组件
    buttons = [modern_button, classic_button, dark_button]

    print(f"\n🎨 同一按钮在不同主题下的表现:")
    for button in buttons:
        print(f"\n{button.theme_name}:")
        print(button.render())


def main():
    """主函数"""
    demo_ui_themes()
    demo_theme_switching()

    print("\n" + "="*70)
    print("工厂方法模式在UI开发中的优势:")
    print("1. 主题一致性：确保同一主题下所有组件风格统一")
    print("2. 易于扩展：可以轻松添加新的主题和组件类型")
    print("3. 运行时切换：支持动态切换主题")
    print("4. 代码复用：主题切换逻辑可以复用")
    print("5. 维护性：每个主题的样式集中管理")
    print("="*70)


if __name__ == "__main__":
    main()
