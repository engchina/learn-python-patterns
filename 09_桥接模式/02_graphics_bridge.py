"""
桥接模式图形应用 - 跨平台图形绘制系统

这个示例展示了桥接模式在图形系统中的应用，演示如何将
图形对象（抽象）与渲染引擎（实现）分离，实现跨平台绘制。

作者: Bridge Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import Tuple, List
import math


# ==================== 实现层接口 ====================

class RenderEngine(ABC):
    """渲染引擎接口 - 实现层"""
    
    @abstractmethod
    def draw_line(self, x1: float, y1: float, x2: float, y2: float, color: str = "black") -> None:
        """绘制直线"""
        pass
    
    @abstractmethod
    def draw_circle(self, x: float, y: float, radius: float, color: str = "black") -> None:
        """绘制圆形"""
        pass
    
    @abstractmethod
    def draw_rectangle(self, x: float, y: float, width: float, height: float, color: str = "black") -> None:
        """绘制矩形"""
        pass
    
    @abstractmethod
    def fill_circle(self, x: float, y: float, radius: float, color: str = "black") -> None:
        """填充圆形"""
        pass
    
    @abstractmethod
    def fill_rectangle(self, x: float, y: float, width: float, height: float, color: str = "black") -> None:
        """填充矩形"""
        pass
    
    @abstractmethod
    def get_engine_info(self) -> str:
        """获取引擎信息"""
        pass


# ==================== 具体实现 ====================

class ConsoleRenderEngine(RenderEngine):
    """控制台渲染引擎 - 具体实现A"""
    
    def __init__(self):
        self.draw_count = 0
    
    def draw_line(self, x1: float, y1: float, x2: float, y2: float, color: str = "black") -> None:
        print(f"  🖊️  控制台绘制直线: ({x1:.1f}, {y1:.1f}) -> ({x2:.1f}, {y2:.1f}) [{color}]")
        self.draw_count += 1
    
    def draw_circle(self, x: float, y: float, radius: float, color: str = "black") -> None:
        print(f"  ⭕ 控制台绘制圆形: 中心({x:.1f}, {y:.1f}), 半径{radius:.1f} [{color}]")
        self.draw_count += 1
    
    def draw_rectangle(self, x: float, y: float, width: float, height: float, color: str = "black") -> None:
        print(f"  ⬜ 控制台绘制矩形: ({x:.1f}, {y:.1f}), 大小{width:.1f}x{height:.1f} [{color}]")
        self.draw_count += 1
    
    def fill_circle(self, x: float, y: float, radius: float, color: str = "black") -> None:
        print(f"  🔵 控制台填充圆形: 中心({x:.1f}, {y:.1f}), 半径{radius:.1f} [{color}]")
        self.draw_count += 1
    
    def fill_rectangle(self, x: float, y: float, width: float, height: float, color: str = "black") -> None:
        print(f"  🟦 控制台填充矩形: ({x:.1f}, {y:.1f}), 大小{width:.1f}x{height:.1f} [{color}]")
        self.draw_count += 1
    
    def get_engine_info(self) -> str:
        return f"控制台渲染引擎 (已绘制: {self.draw_count} 个图元)"


class OpenGLRenderEngine(RenderEngine):
    """OpenGL渲染引擎 - 具体实现B"""
    
    def __init__(self):
        self.draw_count = 0
        self.gpu_memory_used = 0
    
    def draw_line(self, x1: float, y1: float, x2: float, y2: float, color: str = "black") -> None:
        print(f"  🎮 OpenGL绘制直线: glVertex({x1:.1f}, {y1:.1f}) -> glVertex({x2:.1f}, {y2:.1f}) [{color}]")
        self.draw_count += 1
        self.gpu_memory_used += 8  # 模拟GPU内存使用
    
    def draw_circle(self, x: float, y: float, radius: float, color: str = "black") -> None:
        print(f"  🎮 OpenGL绘制圆形: glCircle({x:.1f}, {y:.1f}, {radius:.1f}) [{color}]")
        self.draw_count += 1
        self.gpu_memory_used += 16
    
    def draw_rectangle(self, x: float, y: float, width: float, height: float, color: str = "black") -> None:
        print(f"  🎮 OpenGL绘制矩形: glRect({x:.1f}, {y:.1f}, {width:.1f}, {height:.1f}) [{color}]")
        self.draw_count += 1
        self.gpu_memory_used += 12
    
    def fill_circle(self, x: float, y: float, radius: float, color: str = "black") -> None:
        print(f"  🎮 OpenGL填充圆形: glFillCircle({x:.1f}, {y:.1f}, {radius:.1f}) [{color}]")
        self.draw_count += 1
        self.gpu_memory_used += 24
    
    def fill_rectangle(self, x: float, y: float, width: float, height: float, color: str = "black") -> None:
        print(f"  🎮 OpenGL填充矩形: glFillRect({x:.1f}, {y:.1f}, {width:.1f}, {height:.1f}) [{color}]")
        self.draw_count += 1
        self.gpu_memory_used += 20
    
    def get_engine_info(self) -> str:
        return f"OpenGL渲染引擎 (已绘制: {self.draw_count} 个图元, GPU内存: {self.gpu_memory_used}KB)"


class SVGRenderEngine(RenderEngine):
    """SVG渲染引擎 - 具体实现C"""
    
    def __init__(self):
        self.svg_elements = []
        self.draw_count = 0
    
    def draw_line(self, x1: float, y1: float, x2: float, y2: float, color: str = "black") -> None:
        svg_line = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}"/>'
        self.svg_elements.append(svg_line)
        print(f"  📄 SVG生成直线: {svg_line}")
        self.draw_count += 1
    
    def draw_circle(self, x: float, y: float, radius: float, color: str = "black") -> None:
        svg_circle = f'<circle cx="{x}" cy="{y}" r="{radius}" stroke="{color}" fill="none"/>'
        self.svg_elements.append(svg_circle)
        print(f"  📄 SVG生成圆形: {svg_circle}")
        self.draw_count += 1
    
    def draw_rectangle(self, x: float, y: float, width: float, height: float, color: str = "black") -> None:
        svg_rect = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" stroke="{color}" fill="none"/>'
        self.svg_elements.append(svg_rect)
        print(f"  📄 SVG生成矩形: {svg_rect}")
        self.draw_count += 1
    
    def fill_circle(self, x: float, y: float, radius: float, color: str = "black") -> None:
        svg_circle = f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}"/>'
        self.svg_elements.append(svg_circle)
        print(f"  📄 SVG生成填充圆形: {svg_circle}")
        self.draw_count += 1
    
    def fill_rectangle(self, x: float, y: float, width: float, height: float, color: str = "black") -> None:
        svg_rect = f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}"/>'
        self.svg_elements.append(svg_rect)
        print(f"  📄 SVG生成填充矩形: {svg_rect}")
        self.draw_count += 1
    
    def get_engine_info(self) -> str:
        return f"SVG渲染引擎 (已生成: {self.draw_count} 个元素, SVG大小: {len(self.svg_elements)} 行)"
    
    def export_svg(self) -> str:
        """导出完整的SVG文档"""
        svg_content = ['<svg xmlns="http://www.w3.org/2000/svg">']
        svg_content.extend(self.svg_elements)
        svg_content.append('</svg>')
        return '\n'.join(svg_content)


# ==================== 抽象层 ====================

class Shape:
    """图形抽象类 - 抽象层"""
    
    def __init__(self, renderer: RenderEngine, color: str = "black"):
        self.renderer = renderer
        self.color = color
        self.visible = True
    
    @abstractmethod
    def draw(self) -> None:
        """绘制图形"""
        pass
    
    def set_renderer(self, renderer: RenderEngine) -> None:
        """设置渲染引擎"""
        self.renderer = renderer
        print(f"🔄 图形渲染引擎已切换为: {renderer.get_engine_info()}")
    
    def set_color(self, color: str) -> None:
        """设置颜色"""
        self.color = color
    
    def set_visible(self, visible: bool) -> None:
        """设置可见性"""
        self.visible = visible


# ==================== 扩展抽象层 ====================

class Circle(Shape):
    """圆形 - 扩展抽象层"""
    
    def __init__(self, x: float, y: float, radius: float, renderer: RenderEngine, color: str = "black"):
        super().__init__(renderer, color)
        self.x = x
        self.y = y
        self.radius = radius
        self.filled = False
    
    def draw(self) -> None:
        """绘制圆形"""
        if not self.visible:
            return
        
        if self.filled:
            self.renderer.fill_circle(self.x, self.y, self.radius, self.color)
        else:
            self.renderer.draw_circle(self.x, self.y, self.radius, self.color)
    
    def set_filled(self, filled: bool) -> None:
        """设置是否填充"""
        self.filled = filled
    
    def get_area(self) -> float:
        """计算面积"""
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    """矩形 - 扩展抽象层"""
    
    def __init__(self, x: float, y: float, width: float, height: float, 
                 renderer: RenderEngine, color: str = "black"):
        super().__init__(renderer, color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.filled = False
    
    def draw(self) -> None:
        """绘制矩形"""
        if not self.visible:
            return
        
        if self.filled:
            self.renderer.fill_rectangle(self.x, self.y, self.width, self.height, self.color)
        else:
            self.renderer.draw_rectangle(self.x, self.y, self.width, self.height, self.color)
    
    def set_filled(self, filled: bool) -> None:
        """设置是否填充"""
        self.filled = filled
    
    def get_area(self) -> float:
        """计算面积"""
        return self.width * self.height


class Line(Shape):
    """直线 - 扩展抽象层"""
    
    def __init__(self, x1: float, y1: float, x2: float, y2: float, 
                 renderer: RenderEngine, color: str = "black"):
        super().__init__(renderer, color)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def draw(self) -> None:
        """绘制直线"""
        if not self.visible:
            return
        
        self.renderer.draw_line(self.x1, self.y1, self.x2, self.y2, self.color)
    
    def get_length(self) -> float:
        """计算长度"""
        return math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)


class ComplexShape(Shape):
    """复杂图形 - 扩展抽象层"""
    
    def __init__(self, renderer: RenderEngine, color: str = "black"):
        super().__init__(renderer, color)
        self.shapes: List[Shape] = []
    
    def add_shape(self, shape: Shape) -> None:
        """添加子图形"""
        shape.set_renderer(self.renderer)
        shape.set_color(self.color)
        self.shapes.append(shape)
    
    def draw(self) -> None:
        """绘制复杂图形"""
        if not self.visible:
            return
        
        print(f"  🎨 绘制复杂图形 (包含 {len(self.shapes)} 个子图形)")
        for shape in self.shapes:
            shape.draw()


def demo_graphics_bridge():
    """图形桥接模式演示"""
    print("=" * 60)
    print("🎨 跨平台图形绘制系统 - 桥接模式演示")
    print("=" * 60)
    
    # 创建不同的渲染引擎
    console_engine = ConsoleRenderEngine()
    opengl_engine = OpenGLRenderEngine()
    svg_engine = SVGRenderEngine()
    
    # 创建图形对象
    circle = Circle(50, 50, 25, console_engine, "red")
    rectangle = Rectangle(10, 10, 80, 40, console_engine, "blue")
    line = Line(0, 0, 100, 100, console_engine, "green")
    
    print("\n🖼️  使用控制台渲染引擎:")
    circle.draw()
    rectangle.draw()
    line.draw()
    
    print(f"\n🔄 切换到OpenGL渲染引擎:")
    circle.set_renderer(opengl_engine)
    rectangle.set_renderer(opengl_engine)
    line.set_renderer(opengl_engine)
    
    circle.draw()
    rectangle.draw()
    line.draw()
    
    print(f"\n📄 切换到SVG渲染引擎:")
    circle.set_renderer(svg_engine)
    rectangle.set_renderer(svg_engine)
    line.set_renderer(svg_engine)
    
    circle.set_filled(True)
    rectangle.set_filled(True)
    
    circle.draw()
    rectangle.draw()
    line.draw()


def demo_complex_graphics():
    """复杂图形演示"""
    print("\n" + "=" * 60)
    print("🎭 复杂图形演示")
    print("=" * 60)
    
    # 创建渲染引擎
    engine = ConsoleRenderEngine()
    
    # 创建复杂图形 - 房子
    house = ComplexShape(engine, "brown")
    
    # 房子的各个部分
    base = Rectangle(20, 60, 60, 40, engine, "brown")  # 房子主体
    roof = Line(20, 60, 50, 30, engine, "red")         # 屋顶左边
    roof2 = Line(50, 30, 80, 60, engine, "red")        # 屋顶右边
    door = Rectangle(40, 80, 10, 20, engine, "black")  # 门
    window = Circle(30, 70, 5, engine, "blue")         # 窗户
    
    house.add_shape(base)
    house.add_shape(roof)
    house.add_shape(roof2)
    house.add_shape(door)
    house.add_shape(window)
    
    print("\n🏠 绘制房子:")
    house.draw()
    
    # 切换渲染引擎
    print(f"\n🔄 切换到SVG引擎重新绘制:")
    svg_engine = SVGRenderEngine()
    house.set_renderer(svg_engine)
    house.draw()


if __name__ == "__main__":
    demo_graphics_bridge()
    demo_complex_graphics()
