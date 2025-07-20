"""
GUI装饰器模式实用示例
展示如何在图形界面中应用装饰器模式
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

# 抽象UI组件
class UIComponent(ABC):
    """UI组件抽象基类"""
    
    @abstractmethod
    def render(self, parent) -> tk.Widget:
        """渲染组件"""
        pass

# 基础UI组件
class Button(UIComponent):
    """基础按钮组件"""
    
    def __init__(self, text: str, command=None):
        self.text = text
        self.command = command
    
    def render(self, parent) -> tk.Widget:
        """渲染按钮"""
        return tk.Button(parent, text=self.text, command=self.command)

class Label(UIComponent):
    """基础标签组件"""
    
    def __init__(self, text: str):
        self.text = text
    
    def render(self, parent) -> tk.Widget:
        """渲染标签"""
        return tk.Label(parent, text=self.text)

# UI装饰器基类
class UIDecorator(UIComponent):
    """UI装饰器基类"""
    
    def __init__(self, component: UIComponent):
        self._component = component
    
    def render(self, parent) -> tk.Widget:
        """默认渲染行为"""
        return self._component.render(parent)

# 具体装饰器
class BorderDecorator(UIDecorator):
    """边框装饰器"""
    
    def __init__(self, component: UIComponent, border_width: int = 2, border_color: str = "black"):
        super().__init__(component)
        self.border_width = border_width
        self.border_color = border_color
    
    def render(self, parent) -> tk.Widget:
        """添加边框效果"""
        widget = self._component.render(parent)
        widget.config(
            relief=tk.SOLID,
            borderwidth=self.border_width,
            highlightbackground=self.border_color
        )
        return widget

class ColorDecorator(UIDecorator):
    """颜色装饰器"""
    
    def __init__(self, component: UIComponent, bg_color: str = "lightblue", fg_color: str = "black"):
        super().__init__(component)
        self.bg_color = bg_color
        self.fg_color = fg_color
    
    def render(self, parent) -> tk.Widget:
        """添加颜色效果"""
        widget = self._component.render(parent)
        widget.config(bg=self.bg_color, fg=self.fg_color)
        return widget

class HoverDecorator(UIDecorator):
    """悬停效果装饰器"""
    
    def __init__(self, component: UIComponent, hover_color: str = "yellow"):
        super().__init__(component)
        self.hover_color = hover_color
        self.original_color = None
    
    def render(self, parent) -> tk.Widget:
        """添加悬停效果"""
        widget = self._component.render(parent)
        self.original_color = widget.cget("bg")
        
        def on_enter(event):
            widget.config(bg=self.hover_color)
        
        def on_leave(event):
            widget.config(bg=self.original_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        return widget

class SizeDecorator(UIDecorator):
    """尺寸装饰器"""
    
    def __init__(self, component: UIComponent, width: int = None, height: int = None):
        super().__init__(component)
        self.width = width
        self.height = height
    
    def render(self, parent) -> tk.Widget:
        """设置组件尺寸"""
        widget = self._component.render(parent)
        if self.width:
            widget.config(width=self.width)
        if self.height:
            widget.config(height=self.height)
        return widget

class AnimationDecorator(UIDecorator):
    """动画装饰器"""
    
    def __init__(self, component: UIComponent):
        super().__init__(component)
    
    def render(self, parent) -> tk.Widget:
        """添加点击动画效果"""
        widget = self._component.render(parent)
        original_command = widget.cget("command")
        
        def animated_command():
            # 动画效果：按钮按下效果
            widget.config(relief=tk.SUNKEN)
            parent.after(100, lambda: widget.config(relief=tk.RAISED))
            
            # 执行原始命令
            if original_command:
                original_command()
        
        if hasattr(widget, 'config') and 'command' in widget.keys():
            widget.config(command=animated_command)
        
        return widget

# 演示应用程序
class DecoratorDemo:
    """装饰器演示应用"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI装饰器模式演示")
        self.root.geometry("600x500")
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 标题
        title_label = Label("GUI装饰器模式演示")
        title_widget = ColorDecorator(
            SizeDecorator(title_label, height=2),
            bg_color="navy",
            fg_color="white"
        ).render(self.root)
        title_widget.pack(pady=10)
        
        # 创建不同装饰效果的按钮
        self.create_demo_buttons()
        
        # 状态显示
        self.status_var = tk.StringVar(value="准备就绪")
        status_label = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_demo_buttons(self):
        """创建演示按钮"""
        # 按钮容器
        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # 1. 基础按钮
        basic_button = Button("基础按钮", lambda: self.update_status("点击了基础按钮"))
        basic_widget = basic_button.render(button_frame)
        basic_widget.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # 2. 带边框的按钮
        border_button = Button("边框按钮", lambda: self.update_status("点击了边框按钮"))
        border_widget = BorderDecorator(border_button, border_width=3, border_color="red").render(button_frame)
        border_widget.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # 3. 彩色按钮
        color_button = Button("彩色按钮", lambda: self.update_status("点击了彩色按钮"))
        color_widget = ColorDecorator(color_button, bg_color="lightgreen", fg_color="darkgreen").render(button_frame)
        color_widget.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # 4. 悬停效果按钮
        hover_button = Button("悬停按钮", lambda: self.update_status("点击了悬停按钮"))
        hover_widget = HoverDecorator(
            ColorDecorator(hover_button, bg_color="lightblue"),
            hover_color="orange"
        ).render(button_frame)
        hover_widget.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # 5. 大尺寸按钮
        size_button = Button("大按钮", lambda: self.update_status("点击了大按钮"))
        size_widget = SizeDecorator(
            ColorDecorator(size_button, bg_color="purple", fg_color="white"),
            width=15, height=3
        ).render(button_frame)
        size_widget.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        # 6. 多重装饰按钮
        multi_button = Button("多重装饰按钮", lambda: self.update_status("点击了多重装饰按钮"))
        multi_widget = AnimationDecorator(
            HoverDecorator(
                BorderDecorator(
                    ColorDecorator(
                        SizeDecorator(multi_button, width=20, height=2),
                        bg_color="gold", fg_color="black"
                    ),
                    border_width=2, border_color="darkgoldenrod"
                ),
                hover_color="yellow"
            )
        ).render(button_frame)
        multi_widget.grid(row=3, column=0, columnspan=2, padx=10, pady=20)
        
        # 配置网格权重
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # 说明标签
        info_text = """
装饰器模式演示说明：
• 基础按钮：无装饰效果
• 边框按钮：添加了红色边框
• 彩色按钮：添加了背景和前景色
• 悬停按钮：鼠标悬停时变色
• 大按钮：设置了特定尺寸
• 多重装饰按钮：组合了多种装饰效果
        """
        
        info_label = tk.Label(button_frame, text=info_text, justify=tk.LEFT, 
                             bg="lightyellow", relief=tk.GROOVE, padx=10, pady=10)
        info_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    
    def update_status(self, message: str):
        """更新状态信息"""
        self.status_var.set(message)
        print(f"📱 {message}")
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

def main():
    """主函数"""
    print("=== GUI装饰器模式演示 ===")
    print("启动图形界面...")
    
    app = DecoratorDemo()
    app.run()

if __name__ == "__main__":
    main()