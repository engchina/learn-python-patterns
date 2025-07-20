"""
组合模式基础实现 - 图形绘制系统

这个示例展示了组合模式的基本概念，通过一个图形绘制系统来演示
如何统一处理单个图形和图形组合。

作者: Composite Pattern Demo
日期: 2024
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import math


class Graphic(ABC):
    """图形组件抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def draw(self, indent: int = 0) -> str:
        """绘制图形"""
        pass
    
    @abstractmethod
    def get_area(self) -> float:
        """计算面积"""
        pass
    
    def add(self, graphic: 'Graphic') -> None:
        """添加子图形（默认实现，叶子节点不支持）"""
        raise NotImplementedError("叶子图形不支持添加操作")
    
    def remove(self, graphic: 'Graphic') -> None:
        """移除子图形（默认实现，叶子节点不支持）"""
        raise NotImplementedError("叶子图形不支持移除操作")
    
    def get_children(self) -> List['Graphic']:
        """获取子图形列表（默认实现，叶子节点返回空列表）"""
        return []


class Circle(Graphic):
    """圆形 - 叶子组件"""
    
    def __init__(self, name: str, radius: float):
        super().__init__(name)
        self.radius = radius
    
    def draw(self, indent: int = 0) -> str:
        """绘制圆形"""
        prefix = "  " * indent
        return f"{prefix}🔵 圆形 '{self.name}' (半径: {self.radius}, 面积: {self.get_area():.2f})"
    
    def get_area(self) -> float:
        """计算圆形面积"""
        return math.pi * self.radius ** 2


class Rectangle(Graphic):
    """矩形 - 叶子组件"""
    
    def __init__(self, name: str, width: float, height: float):
        super().__init__(name)
        self.width = width
        self.height = height
    
    def draw(self, indent: int = 0) -> str:
        """绘制矩形"""
        prefix = "  " * indent
        return f"{prefix}🟦 矩形 '{self.name}' ({self.width}x{self.height}, 面积: {self.get_area():.2f})"
    
    def get_area(self) -> float:
        """计算矩形面积"""
        return self.width * self.height


class Triangle(Graphic):
    """三角形 - 叶子组件"""
    
    def __init__(self, name: str, base: float, height: float):
        super().__init__(name)
        self.base = base
        self.height = height
    
    def draw(self, indent: int = 0) -> str:
        """绘制三角形"""
        prefix = "  " * indent
        return f"{prefix}🔺 三角形 '{self.name}' (底: {self.base}, 高: {self.height}, 面积: {self.get_area():.2f})"
    
    def get_area(self) -> float:
        """计算三角形面积"""
        return 0.5 * self.base * self.height


class GraphicGroup(Graphic):
    """图形组合 - 组合组件"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[Graphic] = []
    
    def draw(self, indent: int = 0) -> str:
        """绘制图形组合"""
        prefix = "  " * indent
        result = [f"{prefix}📁 图形组合 '{self.name}' (总面积: {self.get_area():.2f})"]
        
        for child in self._children:
            result.append(child.draw(indent + 1))
        
        return "\n".join(result)
    
    def get_area(self) -> float:
        """计算组合的总面积"""
        return sum(child.get_area() for child in self._children)
    
    def add(self, graphic: Graphic) -> None:
        """添加子图形"""
        if graphic not in self._children:
            self._children.append(graphic)
            print(f"✅ 已将 '{graphic.name}' 添加到组合 '{self.name}'")
        else:
            print(f"⚠️  '{graphic.name}' 已存在于组合 '{self.name}' 中")
    
    def remove(self, graphic: Graphic) -> None:
        """移除子图形"""
        if graphic in self._children:
            self._children.remove(graphic)
            print(f"❌ 已从组合 '{self.name}' 中移除 '{graphic.name}'")
        else:
            print(f"⚠️  '{graphic.name}' 不存在于组合 '{self.name}' 中")
    
    def get_children(self) -> List[Graphic]:
        """获取子图形列表"""
        return self._children.copy()
    
    def find_graphic(self, name: str) -> Optional[Graphic]:
        """查找指定名称的图形"""
        if self.name == name:
            return self
        
        for child in self._children:
            if child.name == name:
                return child
            if isinstance(child, GraphicGroup):
                found = child.find_graphic(name)
                if found:
                    return found
        return None


def demo_basic_composite():
    """基础组合模式演示"""
    print("=" * 50)
    print("🎨 图形绘制系统 - 组合模式演示")
    print("=" * 50)
    
    # 创建基本图形（叶子组件）
    circle1 = Circle("小圆", 3.0)
    circle2 = Circle("大圆", 5.0)
    rect1 = Rectangle("矩形1", 4.0, 6.0)
    rect2 = Rectangle("矩形2", 3.0, 3.0)
    triangle1 = Triangle("三角形1", 4.0, 3.0)
    
    # 创建图形组合（组合组件）
    basic_shapes = GraphicGroup("基础图形")
    complex_shapes = GraphicGroup("复杂图形")
    all_graphics = GraphicGroup("所有图形")
    
    # 构建图形层次结构
    print("\n📝 构建图形层次结构:")
    basic_shapes.add(circle1)
    basic_shapes.add(rect1)
    basic_shapes.add(triangle1)
    
    complex_shapes.add(circle2)
    complex_shapes.add(rect2)
    
    all_graphics.add(basic_shapes)
    all_graphics.add(complex_shapes)
    
    # 绘制整个图形结构
    print(f"\n🖼️  绘制结果:")
    print(all_graphics.draw())
    
    # 演示统一接口的使用
    print(f"\n📊 面积统计:")
    graphics_to_check = [circle1, basic_shapes, all_graphics]
    
    for graphic in graphics_to_check:
        print(f"  • {graphic.name}: {graphic.get_area():.2f} 平方单位")
    
    # 演示查找功能
    print(f"\n🔍 查找图形:")
    search_names = ["小圆", "基础图形", "不存在的图形"]
    
    for name in search_names:
        found = all_graphics.find_graphic(name)
        if found:
            print(f"  ✅ 找到: {found.name} (类型: {type(found).__name__})")
        else:
            print(f"  ❌ 未找到: {name}")
    
    # 演示动态修改
    print(f"\n🔄 动态修改结构:")
    new_circle = Circle("新圆", 2.0)
    basic_shapes.add(new_circle)
    
    print(f"\n🖼️  修改后的结构:")
    print(all_graphics.draw())


def demo_client_transparency():
    """演示客户端透明性"""
    print("\n" + "=" * 50)
    print("🔄 客户端透明性演示")
    print("=" * 50)
    
    # 创建不同类型的图形对象
    single_circle = Circle("独立圆", 4.0)
    
    group = GraphicGroup("图形组")
    group.add(Rectangle("矩形", 5.0, 3.0))
    group.add(Triangle("三角形", 6.0, 4.0))
    
    # 客户端代码统一处理不同类型的图形
    graphics = [single_circle, group]
    
    print("📋 统一处理不同类型的图形:")
    for i, graphic in enumerate(graphics, 1):
        print(f"\n{i}. 处理图形: {graphic.name}")
        print(f"   类型: {type(graphic).__name__}")
        print(f"   面积: {graphic.get_area():.2f}")
        print(f"   绘制结果:")
        print(graphic.draw())


if __name__ == "__main__":
    demo_basic_composite()
    demo_client_transparency()
