"""
01_basic_abstract_factory.py - 抽象工厂模式基础实现

UI主题系统示例
这个示例展示了如何使用抽象工厂模式来创建不同主题的UI组件。
在GUI应用程序中，通常需要支持多种主题（如深色主题、浅色主题），
抽象工厂模式可以确保同一主题的所有组件风格一致。
"""

from abc import ABC, abstractmethod


# ==================== 抽象产品类 ====================
class Button(ABC):
    """按钮抽象基类"""
    
    @abstractmethod
    def render(self) -> str:
        """渲染按钮"""
        pass
    
    @abstractmethod
    def click(self) -> str:
        """点击按钮"""
        pass


class TextField(ABC):
    """文本框抽象基类"""
    
    @abstractmethod
    def render(self) -> str:
        """渲染文本框"""
        pass
    
    @abstractmethod
    def input_text(self, text: str) -> str:
        """输入文本"""
        pass


class Window(ABC):
    """窗口抽象基类"""
    
    @abstractmethod
    def render(self) -> str:
        """渲染窗口"""
        pass
    
    @abstractmethod
    def close(self) -> str:
        """关闭窗口"""
        pass


# ==================== 深色主题产品族 ====================
class DarkButton(Button):
    """深色主题按钮"""
    
    def __init__(self, text: str = "按钮"):
        self.text = text
        self.background_color = "#2D2D2D"
        self.text_color = "#FFFFFF"
        self.border_color = "#404040"
    
    def render(self) -> str:
        """渲染深色按钮"""
        return (f"深色按钮: [{self.text}] "
                f"背景:{self.background_color} "
                f"文字:{self.text_color} "
                f"边框:{self.border_color}")
    
    def click(self) -> str:
        """点击深色按钮"""
        return f"深色按钮 '{self.text}' 被点击了"


class DarkTextField(TextField):
    """深色主题文本框"""
    
    def __init__(self, placeholder: str = "请输入..."):
        self.placeholder = placeholder
        self.background_color = "#1E1E1E"
        self.text_color = "#FFFFFF"
        self.border_color = "#404040"
        self.content = ""
    
    def render(self) -> str:
        """渲染深色文本框"""
        display_text = self.content if self.content else self.placeholder
        return (f"深色文本框: [{display_text}] "
                f"背景:{self.background_color} "
                f"文字:{self.text_color} "
                f"边框:{self.border_color}")
    
    def input_text(self, text: str) -> str:
        """输入文本到深色文本框"""
        self.content = text
        return f"深色文本框输入: '{text}'"


class DarkWindow(Window):
    """深色主题窗口"""
    
    def __init__(self, title: str = "窗口"):
        self.title = title
        self.background_color = "#1A1A1A"
        self.title_bar_color = "#2D2D2D"
        self.text_color = "#FFFFFF"
        self.is_open = True
    
    def render(self) -> str:
        """渲染深色窗口"""
        return (f"深色窗口: '{self.title}' "
                f"背景:{self.background_color} "
                f"标题栏:{self.title_bar_color} "
                f"文字:{self.text_color}")
    
    def close(self) -> str:
        """关闭深色窗口"""
        self.is_open = False
        return f"深色窗口 '{self.title}' 已关闭"


# ==================== 浅色主题产品族 ====================
class LightButton(Button):
    """浅色主题按钮"""
    
    def __init__(self, text: str = "按钮"):
        self.text = text
        self.background_color = "#F0F0F0"
        self.text_color = "#333333"
        self.border_color = "#CCCCCC"
    
    def render(self) -> str:
        """渲染浅色按钮"""
        return (f"浅色按钮: [{self.text}] "
                f"背景:{self.background_color} "
                f"文字:{self.text_color} "
                f"边框:{self.border_color}")
    
    def click(self) -> str:
        """点击浅色按钮"""
        return f"浅色按钮 '{self.text}' 被点击了"


class LightTextField(TextField):
    """浅色主题文本框"""
    
    def __init__(self, placeholder: str = "请输入..."):
        self.placeholder = placeholder
        self.background_color = "#FFFFFF"
        self.text_color = "#333333"
        self.border_color = "#CCCCCC"
        self.content = ""
    
    def render(self) -> str:
        """渲染浅色文本框"""
        display_text = self.content if self.content else self.placeholder
        return (f"浅色文本框: [{display_text}] "
                f"背景:{self.background_color} "
                f"文字:{self.text_color} "
                f"边框:{self.border_color}")
    
    def input_text(self, text: str) -> str:
        """输入文本到浅色文本框"""
        self.content = text
        return f"浅色文本框输入: '{text}'"


class LightWindow(Window):
    """浅色主题窗口"""
    
    def __init__(self, title: str = "窗口"):
        self.title = title
        self.background_color = "#FFFFFF"
        self.title_bar_color = "#F0F0F0"
        self.text_color = "#333333"
        self.is_open = True
    
    def render(self) -> str:
        """渲染浅色窗口"""
        return (f"浅色窗口: '{self.title}' "
                f"背景:{self.background_color} "
                f"标题栏:{self.title_bar_color} "
                f"文字:{self.text_color}")
    
    def close(self) -> str:
        """关闭浅色窗口"""
        self.is_open = False
        return f"浅色窗口 '{self.title}' 已关闭"


# ==================== 抽象工厂类 ====================
class UIFactory(ABC):
    """UI组件抽象工厂"""
    
    @abstractmethod
    def create_button(self, text: str = "按钮") -> Button:
        """创建按钮"""
        pass
    
    @abstractmethod
    def create_text_field(self, placeholder: str = "请输入...") -> TextField:
        """创建文本框"""
        pass
    
    @abstractmethod
    def create_window(self, title: str = "窗口") -> Window:
        """创建窗口"""
        pass


# ==================== 具体工厂类 ====================
class DarkThemeFactory(UIFactory):
    """深色主题工厂"""
    
    def create_button(self, text: str = "按钮") -> Button:
        """创建深色主题按钮"""
        return DarkButton(text)
    
    def create_text_field(self, placeholder: str = "请输入...") -> TextField:
        """创建深色主题文本框"""
        return DarkTextField(placeholder)
    
    def create_window(self, title: str = "窗口") -> Window:
        """创建深色主题窗口"""
        return DarkWindow(title)


class LightThemeFactory(UIFactory):
    """浅色主题工厂"""
    
    def create_button(self, text: str = "按钮") -> Button:
        """创建浅色主题按钮"""
        return LightButton(text)
    
    def create_text_field(self, placeholder: str = "请输入...") -> TextField:
        """创建浅色主题文本框"""
        return LightTextField(placeholder)
    
    def create_window(self, title: str = "窗口") -> Window:
        """创建浅色主题窗口"""
        return LightWindow(title)


# ==================== 客户端代码 ====================
class Application:
    """应用程序类"""
    
    def __init__(self, factory: UIFactory):
        self.factory = factory
        self.components = []
    
    def create_login_form(self):
        """创建登录表单"""
        print("创建登录表单...")
        
        # 创建窗口
        window = self.factory.create_window("用户登录")
        print(window.render())
        self.components.append(window)
        
        # 创建用户名输入框
        username_field = self.factory.create_text_field("请输入用户名")
        print(username_field.render())
        self.components.append(username_field)
        
        # 创建密码输入框
        password_field = self.factory.create_text_field("请输入密码")
        print(password_field.render())
        self.components.append(password_field)
        
        # 创建登录按钮
        login_button = self.factory.create_button("登录")
        print(login_button.render())
        self.components.append(login_button)
        
        # 创建取消按钮
        cancel_button = self.factory.create_button("取消")
        print(cancel_button.render())
        self.components.append(cancel_button)
        
        return {
            "window": window,
            "username_field": username_field,
            "password_field": password_field,
            "login_button": login_button,
            "cancel_button": cancel_button
        }
    
    def simulate_user_interaction(self, form_components):
        """模拟用户交互"""
        print("\n模拟用户交互:")
        
        # 用户输入用户名
        username_result = form_components["username_field"].input_text("admin")
        print(username_result)
        
        # 用户输入密码
        password_result = form_components["password_field"].input_text("password123")
        print(password_result)
        
        # 用户点击登录按钮
        login_result = form_components["login_button"].click()
        print(login_result)
        
        # 关闭窗口
        close_result = form_components["window"].close()
        print(close_result)


# ==================== 演示函数 ====================
def demonstrate_dark_theme():
    """演示深色主题"""
    print("=" * 60)
    print("深色主题演示")
    print("=" * 60)
    
    # 获取深色主题工厂
    dark_factory = DarkThemeFactory()
    
    # 创建应用程序
    app = Application(dark_factory)
    
    # 创建登录表单
    form = app.create_login_form()
    
    # 模拟用户交互
    app.simulate_user_interaction(form)


def demonstrate_light_theme():
    """演示浅色主题"""
    print("\n" + "=" * 60)
    print("浅色主题演示")
    print("=" * 60)
    
    # 获取浅色主题工厂
    light_factory = LightThemeFactory()
    
    # 创建应用程序
    app = Application(light_factory)
    
    # 创建登录表单
    form = app.create_login_form()
    
    # 模拟用户交互
    app.simulate_user_interaction(form)


# ==================== 主函数 ====================
def main():
    """主函数 - 演示抽象工厂模式的各种用法"""
    print("抽象工厂模式演示 - UI主题系统")
    
    # 演示深色主题
    demonstrate_dark_theme()
    
    # 演示浅色主题
    demonstrate_light_theme()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
