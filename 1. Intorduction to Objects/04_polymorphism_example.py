"""
04_polymorphism_example.py - 多态性的实际应用

这个示例通过图形绘制系统展示多态的核心概念：
- 统一接口的不同实现
- 动态方法调用
- 接口设计的重要性
- 多态在实际开发中的应用
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
import math


# ==================== 抽象图形基类 ====================
class Shape(ABC):
    """图形抽象基类 - 定义所有图形的统一接口"""
    
    def __init__(self, x: float, y: float, color: str = "黑色"):
        """
        初始化图形
        
        参数:
            x: X坐标
            y: Y坐标
            color: 颜色
        """
        self.x = x
        self.y = y
        self.color = color
        self.is_filled = False
        self.border_width = 1
        
        print(f"🎨 创建了一个{color}的{self.__class__.__name__}")
    
    @abstractmethod
    def calculate_area(self) -> float:
        """计算面积 - 抽象方法"""
        pass
    
    @abstractmethod
    def calculate_perimeter(self) -> float:
        """计算周长 - 抽象方法"""
        pass
    
    @abstractmethod
    def draw(self) -> str:
        """绘制图形 - 抽象方法"""
        pass
    
    def move(self, dx: float, dy: float):
        """移动图形"""
        old_x, old_y = self.x, self.y
        self.x += dx
        self.y += dy
        print(f"📍 {self.__class__.__name__} 从 ({old_x}, {old_y}) 移动到 ({self.x}, {self.y})")
    
    def set_color(self, color: str):
        """设置颜色"""
        old_color = self.color
        self.color = color
        print(f"🎨 {self.__class__.__name__} 颜色从 {old_color} 改为 {color}")
    
    def set_fill(self, filled: bool):
        """设置填充"""
        self.is_filled = filled
        status = "填充" if filled else "不填充"
        print(f"🖌️  {self.__class__.__name__} 设置为 {status}")
    
    def get_info(self) -> str:
        """获取图形信息"""
        fill_status = "填充" if self.is_filled else "不填充"
        return (f"📐 {self.__class__.__name__} 信息:\n"
                f"   位置: ({self.x}, {self.y})\n"
                f"   颜色: {self.color}\n"
                f"   填充: {fill_status}\n"
                f"   边框宽度: {self.border_width}\n"
                f"   面积: {self.calculate_area():.2f}\n"
                f"   周长: {self.calculate_perimeter():.2f}")
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(位置=({self.x}, {self.y}), 颜色={self.color})"


# ==================== 具体图形类 ====================
class Circle(Shape):
    """圆形类"""
    
    def __init__(self, x: float, y: float, radius: float, color: str = "红色"):
        """
        初始化圆形
        
        参数:
            x: 圆心X坐标
            y: 圆心Y坐标
            radius: 半径
            color: 颜色
        """
        super().__init__(x, y, color)
        self.radius = radius
    
    def calculate_area(self) -> float:
        """计算圆的面积"""
        return math.pi * self.radius ** 2
    
    def calculate_perimeter(self) -> float:
        """计算圆的周长"""
        return 2 * math.pi * self.radius
    
    def draw(self) -> str:
        """绘制圆形"""
        fill_char = "●" if self.is_filled else "○"
        return f"🎨 绘制圆形 {fill_char} 在 ({self.x}, {self.y})，半径={self.radius}"
    
    def get_diameter(self) -> float:
        """获取直径"""
        return 2 * self.radius
    
    def scale(self, factor: float):
        """缩放圆形"""
        old_radius = self.radius
        self.radius *= factor
        print(f"🔍 圆形半径从 {old_radius} 缩放到 {self.radius}")


class Rectangle(Shape):
    """矩形类"""
    
    def __init__(self, x: float, y: float, width: float, height: float, color: str = "蓝色"):
        """
        初始化矩形
        
        参数:
            x: 左上角X坐标
            y: 左上角Y坐标
            width: 宽度
            height: 高度
            color: 颜色
        """
        super().__init__(x, y, color)
        self.width = width
        self.height = height
    
    def calculate_area(self) -> float:
        """计算矩形面积"""
        return self.width * self.height
    
    def calculate_perimeter(self) -> float:
        """计算矩形周长"""
        return 2 * (self.width + self.height)
    
    def draw(self) -> str:
        """绘制矩形"""
        fill_char = "■" if self.is_filled else "□"
        return f"🎨 绘制矩形 {fill_char} 在 ({self.x}, {self.y})，尺寸={self.width}x{self.height}"
    
    def is_square(self) -> bool:
        """判断是否为正方形"""
        return abs(self.width - self.height) < 0.001
    
    def resize(self, new_width: float, new_height: float):
        """调整大小"""
        old_size = f"{self.width}x{self.height}"
        self.width = new_width
        self.height = new_height
        print(f"📏 矩形尺寸从 {old_size} 调整为 {self.width}x{self.height}")


class Triangle(Shape):
    """三角形类"""
    
    def __init__(self, x: float, y: float, base: float, height: float, color: str = "绿色"):
        """
        初始化三角形
        
        参数:
            x: 底边中点X坐标
            y: 底边Y坐标
            base: 底边长度
            height: 高度
            color: 颜色
        """
        super().__init__(x, y, color)
        self.base = base
        self.height = height
    
    def calculate_area(self) -> float:
        """计算三角形面积"""
        return 0.5 * self.base * self.height
    
    def calculate_perimeter(self) -> float:
        """计算三角形周长（假设为等腰三角形）"""
        # 计算两条边的长度
        side_length = math.sqrt((self.base / 2) ** 2 + self.height ** 2)
        return self.base + 2 * side_length
    
    def draw(self) -> str:
        """绘制三角形"""
        fill_char = "▲" if self.is_filled else "△"
        return f"🎨 绘制三角形 {fill_char} 在 ({self.x}, {self.y})，底={self.base}, 高={self.height}"
    
    def get_side_length(self) -> float:
        """获取边长（等腰三角形的腰长）"""
        return math.sqrt((self.base / 2) ** 2 + self.height ** 2)


class Polygon(Shape):
    """多边形类"""
    
    def __init__(self, x: float, y: float, vertices: List[Tuple[float, float]], color: str = "紫色"):
        """
        初始化多边形
        
        参数:
            x: 中心X坐标
            y: 中心Y坐标
            vertices: 顶点坐标列表（相对于中心点）
            color: 颜色
        """
        super().__init__(x, y, color)
        self.vertices = vertices
        self.sides = len(vertices)
    
    def calculate_area(self) -> float:
        """使用鞋带公式计算多边形面积"""
        if len(self.vertices) < 3:
            return 0
        
        area = 0
        n = len(self.vertices)
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i][0] * self.vertices[j][1]
            area -= self.vertices[j][0] * self.vertices[i][1]
        return abs(area) / 2
    
    def calculate_perimeter(self) -> float:
        """计算多边形周长"""
        if len(self.vertices) < 2:
            return 0
        
        perimeter = 0
        n = len(self.vertices)
        for i in range(n):
            j = (i + 1) % n
            dx = self.vertices[j][0] - self.vertices[i][0]
            dy = self.vertices[j][1] - self.vertices[i][1]
            perimeter += math.sqrt(dx ** 2 + dy ** 2)
        return perimeter
    
    def draw(self) -> str:
        """绘制多边形"""
        fill_char = "◆" if self.is_filled else "◇"
        return f"🎨 绘制{self.sides}边形 {fill_char} 在 ({self.x}, {self.y})"
    
    def add_vertex(self, vertex: Tuple[float, float]):
        """添加顶点"""
        self.vertices.append(vertex)
        self.sides = len(self.vertices)
        print(f"📍 多边形添加顶点 {vertex}，现在是{self.sides}边形")


# ==================== 图形管理器 ====================
class Canvas:
    """画布类 - 展示多态的实际应用"""
    
    def __init__(self, width: float, height: float, name: str = "画布"):
        """
        初始化画布
        
        参数:
            width: 画布宽度
            height: 画布高度
            name: 画布名称
        """
        self.width = width
        self.height = height
        self.name = name
        self.shapes: List[Shape] = []
        self.background_color = "白色"
        
        print(f"🖼️  创建了 {name}，尺寸: {width}x{height}")
    
    def add_shape(self, shape: Shape):
        """添加图形到画布"""
        # 检查图形是否在画布范围内
        if 0 <= shape.x <= self.width and 0 <= shape.y <= self.height:
            self.shapes.append(shape)
            print(f"✅ {shape} 已添加到画布")
        else:
            print(f"❌ {shape} 超出画布范围，无法添加")
    
    def remove_shape(self, shape: Shape):
        """从画布移除图形"""
        if shape in self.shapes:
            self.shapes.remove(shape)
            print(f"🗑️  {shape} 已从画布移除")
        else:
            print(f"❌ 画布中没有找到 {shape}")
    
    def draw_all(self):
        """绘制所有图形 - 多态的核心应用"""
        print(f"\n🎨 开始绘制 {self.name} 上的所有图形:")
        print(f"   画布背景: {self.background_color}")
        print("-" * 50)
        
        if not self.shapes:
            print("   画布为空")
            return
        
        for i, shape in enumerate(self.shapes, 1):
            # 这里体现了多态：不同类型的图形调用各自的draw方法
            print(f"   {i}. {shape.draw()}")
        
        print("-" * 50)
    
    def calculate_total_area(self) -> float:
        """计算所有图形的总面积 - 多态应用"""
        total_area = 0
        for shape in self.shapes:
            # 多态：每个图形调用自己的calculate_area方法
            total_area += shape.calculate_area()
        return total_area
    
    def calculate_total_perimeter(self) -> float:
        """计算所有图形的总周长 - 多态应用"""
        total_perimeter = 0
        for shape in self.shapes:
            # 多态：每个图形调用自己的calculate_perimeter方法
            total_perimeter += shape.calculate_perimeter()
        return total_perimeter
    
    def find_shapes_by_color(self, color: str) -> List[Shape]:
        """根据颜色查找图形"""
        return [shape for shape in self.shapes if shape.color == color]
    
    def find_shapes_by_type(self, shape_type: type) -> List[Shape]:
        """根据类型查找图形"""
        return [shape for shape in self.shapes if isinstance(shape, shape_type)]
    
    def get_largest_shape(self) -> Shape:
        """获取面积最大的图形"""
        if not self.shapes:
            return None
        return max(self.shapes, key=lambda shape: shape.calculate_area())
    
    def move_all_shapes(self, dx: float, dy: float):
        """移动所有图形 - 多态应用"""
        print(f"\n📍 移动所有图形 ({dx}, {dy}):")
        for shape in self.shapes:
            # 多态：每个图形调用自己的move方法
            shape.move(dx, dy)
    
    def set_all_colors(self, color: str):
        """设置所有图形的颜色 - 多态应用"""
        print(f"\n🎨 将所有图形设置为 {color}:")
        for shape in self.shapes:
            # 多态：每个图形调用自己的set_color方法
            shape.set_color(color)
    
    def get_canvas_statistics(self) -> str:
        """获取画布统计信息"""
        if not self.shapes:
            return f"📊 {self.name} 统计: 暂无图形"
        
        total_shapes = len(self.shapes)
        total_area = self.calculate_total_area()
        total_perimeter = self.calculate_total_perimeter()
        
        # 按类型统计
        type_counts = {}
        for shape in self.shapes:
            shape_type = type(shape).__name__
            type_counts[shape_type] = type_counts.get(shape_type, 0) + 1
        
        # 按颜色统计
        color_counts = {}
        for shape in self.shapes:
            color_counts[shape.color] = color_counts.get(shape.color, 0) + 1
        
        largest_shape = self.get_largest_shape()
        
        stats = [
            f"📊 {self.name} 统计信息:",
            f"   画布尺寸: {self.width}x{self.height}",
            f"   图形总数: {total_shapes}个",
            f"   总面积: {total_area:.2f}",
            f"   总周长: {total_perimeter:.2f}",
            f"   最大图形: {largest_shape} (面积: {largest_shape.calculate_area():.2f})",
            "",
            "🎨 图形类型分布:"
        ]
        
        for shape_type, count in type_counts.items():
            percentage = count / total_shapes * 100
            stats.append(f"   {shape_type}: {count}个 ({percentage:.1f}%)")
        
        stats.append("\n🌈 颜色分布:")
        for color, count in color_counts.items():
            percentage = count / total_shapes * 100
            stats.append(f"   {color}: {count}个 ({percentage:.1f}%)")
        
        return "\n".join(stats)
    
    def list_all_shapes(self):
        """列出所有图形详细信息"""
        if not self.shapes:
            print(f"📝 {self.name} 暂无图形")
            return
        
        print(f"\n📋 {self.name} 图形列表:")
        print("=" * 60)
        
        for i, shape in enumerate(self.shapes, 1):
            print(f"\n{i}. {shape.get_info()}")
        
        print("=" * 60)


# ==================== 图形工厂 ====================
class ShapeFactory:
    """图形工厂 - 演示工厂模式与多态的结合"""
    
    @staticmethod
    def create_shape(shape_type: str, *args, **kwargs) -> Shape:
        """
        创建图形对象
        
        参数:
            shape_type: 图形类型
            *args: 位置参数
            **kwargs: 关键字参数
            
        返回:
            Shape对象
        """
        shape_classes = {
            "circle": Circle,
            "rectangle": Rectangle,
            "triangle": Triangle,
            "polygon": Polygon
        }
        
        shape_type = shape_type.lower()
        if shape_type not in shape_classes:
            raise ValueError(f"不支持的图形类型: {shape_type}")
        
        shape_class = shape_classes[shape_type]
        return shape_class(*args, **kwargs)
    
    @staticmethod
    def create_random_shapes(count: int, canvas_width: float, canvas_height: float) -> List[Shape]:
        """创建随机图形"""
        import random
        
        shapes = []
        shape_types = ["circle", "rectangle", "triangle"]
        colors = ["红色", "蓝色", "绿色", "黄色", "紫色", "橙色"]
        
        for _ in range(count):
            shape_type = random.choice(shape_types)
            x = random.uniform(0, canvas_width)
            y = random.uniform(0, canvas_height)
            color = random.choice(colors)
            
            if shape_type == "circle":
                radius = random.uniform(10, 50)
                shape = Circle(x, y, radius, color)
            elif shape_type == "rectangle":
                width = random.uniform(20, 80)
                height = random.uniform(20, 80)
                shape = Rectangle(x, y, width, height, color)
            else:  # triangle
                base = random.uniform(20, 60)
                height = random.uniform(20, 60)
                shape = Triangle(x, y, base, height, color)
            
            shapes.append(shape)
        
        return shapes


# ==================== 演示函数 ====================
def demo_polymorphism():
    """多态性演示"""
    print("=" * 80)
    print("🎨 面向对象多态性演示")
    print("=" * 80)
    
    # 创建画布
    canvas = Canvas(800, 600, "多态演示画布")
    
    print(f"\n{'='*20} 创建各种图形 {'='*20}")
    
    # 创建不同类型的图形
    circle = Circle(100, 100, 50, "红色")
    circle.set_fill(True)
    
    rectangle = Rectangle(200, 150, 80, 60, "蓝色")
    rectangle.set_fill(False)
    
    triangle = Triangle(350, 200, 70, 80, "绿色")
    triangle.set_fill(True)
    
    # 创建多边形（正六边形）
    hex_vertices = []
    for i in range(6):
        angle = i * math.pi / 3
        x = 40 * math.cos(angle)
        y = 40 * math.sin(angle)
        hex_vertices.append((x, y))
    
    polygon = Polygon(500, 250, hex_vertices, "紫色")
    polygon.set_fill(False)
    
    # 添加图形到画布
    shapes = [circle, rectangle, triangle, polygon]
    for shape in shapes:
        canvas.add_shape(shape)
    
    print(f"\n{'='*20} 多态性演示 {'='*20}")
    
    # 多态演示：统一接口处理不同类型的对象
    print(f"\n🎨 多态绘制演示:")
    canvas.draw_all()
    
    print(f"\n📐 多态计算演示:")
    print(f"   总面积: {canvas.calculate_total_area():.2f}")
    print(f"   总周长: {canvas.calculate_total_perimeter():.2f}")
    
    print(f"\n📊 各图形面积和周长:")
    for shape in canvas.shapes:
        print(f"   {shape}: 面积={shape.calculate_area():.2f}, 周长={shape.calculate_perimeter():.2f}")
    
    print(f"\n{'='*20} 动态方法调用 {'='*20}")
    
    # 演示动态方法调用
    print(f"\n🎯 动态方法调用演示:")
    for shape in canvas.shapes:
        # 根据对象的实际类型调用相应的方法
        if isinstance(shape, Circle):
            print(f"   圆形直径: {shape.get_diameter():.2f}")
        elif isinstance(shape, Rectangle):
            print(f"   矩形是否为正方形: {shape.is_square()}")
        elif isinstance(shape, Triangle):
            print(f"   三角形边长: {shape.get_side_length():.2f}")
        elif isinstance(shape, Polygon):
            print(f"   多边形边数: {shape.sides}")
    
    print(f"\n{'='*20} 统一操作演示 {'='*20}")
    
    # 统一操作：移动所有图形
    canvas.move_all_shapes(10, 10)
    
    # 统一操作：改变所有图形颜色
    canvas.set_all_colors("金色")
    
    print(f"\n{'='*20} 查找和筛选 {'='*20}")
    
    # 按类型查找
    circles = canvas.find_shapes_by_type(Circle)
    rectangles = canvas.find_shapes_by_type(Rectangle)
    print(f"\n🔍 图形类型筛选:")
    print(f"   圆形: {len(circles)}个")
    print(f"   矩形: {len(rectangles)}个")
    
    # 按颜色查找
    gold_shapes = canvas.find_shapes_by_color("金色")
    print(f"   金色图形: {len(gold_shapes)}个")
    
    print(f"\n{'='*20} 工厂模式结合 {'='*20}")
    
    # 使用工厂创建图形
    print(f"\n🏭 使用工厂创建图形:")
    factory_circle = ShapeFactory.create_shape("circle", 600, 300, 30, "银色")
    factory_rectangle = ShapeFactory.create_shape("rectangle", 650, 350, 50, 40, "铜色")
    
    canvas.add_shape(factory_circle)
    canvas.add_shape(factory_rectangle)
    
    # 创建随机图形
    print(f"\n🎲 创建随机图形:")
    random_shapes = ShapeFactory.create_random_shapes(3, canvas.width, canvas.height)
    for shape in random_shapes:
        canvas.add_shape(shape)
    
    print(f"\n{'='*20} 最终状态 {'='*20}")
    
    # 最终绘制
    canvas.draw_all()
    
    # 统计信息
    print(f"\n{canvas.get_canvas_statistics()}")
    
    # 详细信息
    canvas.list_all_shapes()
    
    print("\n" + "=" * 80)
    print("🎉 多态性演示完成!")
    print("💡 关键点:")
    print("   - 多态允许使用统一接口处理不同类型的对象")
    print("   - 运行时根据对象实际类型调用相应方法")
    print("   - 多态提高了代码的灵活性和可扩展性")
    print("   - 接口设计是多态成功应用的关键")
    print("=" * 80)


if __name__ == "__main__":
    demo_polymorphism()
