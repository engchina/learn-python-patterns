"""
01_basic_factory.py - 简单工厂模式基础实现

图形工厂示例
这个示例展示了简单工厂模式的核心概念。
我们有不同类型的图形（圆形、矩形、三角形），通过一个图形工厂来创建这些图形对象。
客户端只需要指定图形类型和参数，无需了解具体的创建过程。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import math


# ==================== 抽象产品 ====================
class Shape(ABC):
    """图形抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def draw(self) -> str:
        """绘制图形"""
        pass
    
    @abstractmethod
    def get_area(self) -> float:
        """计算面积"""
        pass
    
    @abstractmethod
    def get_perimeter(self) -> float:
        """计算周长"""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """获取图形信息"""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "area": round(self.get_area(), 2),
            "perimeter": round(self.get_perimeter(), 2)
        }


# ==================== 具体产品 ====================
class Circle(Shape):
    """圆形"""
    
    def __init__(self, radius: float):
        super().__init__("圆形")
        if radius <= 0:
            raise ValueError("半径必须大于0")
        self.radius = radius
    
    def draw(self) -> str:
        return f"""
    ⭕ 绘制圆形
    半径: {self.radius}
    直径: {self.radius * 2}
    """
    
    def get_area(self) -> float:
        return math.pi * self.radius ** 2
    
    def get_perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    """矩形"""
    
    def __init__(self, width: float, height: float):
        super().__init__("矩形")
        if width <= 0 or height <= 0:
            raise ValueError("宽度和高度必须大于0")
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"""
    ⬜ 绘制矩形
    宽度: {self.width}
    高度: {self.height}
    """
    
    def get_area(self) -> float:
        return self.width * self.height
    
    def get_perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    """三角形"""
    
    def __init__(self, side_a: float, side_b: float, side_c: float):
        super().__init__("三角形")
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise ValueError("边长必须大于0")
        
        # 检查三角形的有效性
        if (side_a + side_b <= side_c or 
            side_a + side_c <= side_b or 
            side_b + side_c <= side_a):
            raise ValueError("无效的三角形边长")
        
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
    
    def draw(self) -> str:
        return f"""
    🔺 绘制三角形
    边长A: {self.side_a}
    边长B: {self.side_b}
    边长C: {self.side_c}
    """
    
    def get_area(self) -> float:
        # 使用海伦公式计算面积
        s = self.get_perimeter() / 2
        return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))
    
    def get_perimeter(self) -> float:
        return self.side_a + self.side_b + self.side_c


class Square(Rectangle):
    """正方形（继承自矩形）"""
    
    def __init__(self, side: float):
        super().__init__(side, side)
        self.name = "正方形"
        self.side = side
    
    def draw(self) -> str:
        return f"""
    ⬛ 绘制正方形
    边长: {self.side}
    """


# ==================== 简单工厂 ====================
class ShapeFactory:
    """图形工厂类"""
    
    # 支持的图形类型
    SUPPORTED_SHAPES = {
        "circle": "圆形",
        "rectangle": "矩形", 
        "triangle": "三角形",
        "square": "正方形"
    }
    
    @staticmethod
    def create_shape(shape_type: str, **kwargs) -> Shape:
        """
        创建图形对象
        
        Args:
            shape_type: 图形类型 (circle, rectangle, triangle, square)
            **kwargs: 图形参数
                - circle: radius
                - rectangle: width, height
                - triangle: side_a, side_b, side_c
                - square: side
        
        Returns:
            Shape: 创建的图形对象
        
        Raises:
            ValueError: 不支持的图形类型或参数错误
        """
        shape_type = shape_type.lower().strip()
        
        print(f"🏭 图形工厂正在创建 {ShapeFactory.SUPPORTED_SHAPES.get(shape_type, '未知')} 图形...")
        
        try:
            if shape_type == "circle":
                radius = kwargs.get("radius")
                if radius is None:
                    raise ValueError("圆形需要 radius 参数")
                return Circle(radius)
            
            elif shape_type == "rectangle":
                width = kwargs.get("width")
                height = kwargs.get("height")
                if width is None or height is None:
                    raise ValueError("矩形需要 width 和 height 参数")
                return Rectangle(width, height)
            
            elif shape_type == "triangle":
                side_a = kwargs.get("side_a")
                side_b = kwargs.get("side_b")
                side_c = kwargs.get("side_c")
                if side_a is None or side_b is None or side_c is None:
                    raise ValueError("三角形需要 side_a, side_b, side_c 参数")
                return Triangle(side_a, side_b, side_c)
            
            elif shape_type == "square":
                side = kwargs.get("side")
                if side is None:
                    raise ValueError("正方形需要 side 参数")
                return Square(side)
            
            else:
                supported = ", ".join(ShapeFactory.SUPPORTED_SHAPES.keys())
                raise ValueError(f"不支持的图形类型: {shape_type}。支持的类型: {supported}")
        
        except Exception as e:
            print(f"❌ 创建图形失败: {e}")
            raise
    
    @staticmethod
    def get_supported_shapes() -> Dict[str, str]:
        """获取支持的图形类型"""
        return ShapeFactory.SUPPORTED_SHAPES.copy()
    
    @staticmethod
    def create_shape_from_config(config: Dict[str, Any]) -> Shape:
        """从配置字典创建图形"""
        shape_type = config.get("type")
        if not shape_type:
            raise ValueError("配置中缺少 type 字段")
        
        # 提取参数（排除 type 字段）
        params = {k: v for k, v in config.items() if k != "type"}
        
        return ShapeFactory.create_shape(shape_type, **params)


# ==================== 图形管理器 ====================
class ShapeManager:
    """图形管理器 - 演示工厂的使用"""
    
    def __init__(self):
        self.shapes = []
    
    def add_shape(self, shape_type: str, **kwargs):
        """添加图形"""
        try:
            shape = ShapeFactory.create_shape(shape_type, **kwargs)
            self.shapes.append(shape)
            print(f"✅ 成功添加 {shape.name}")
            return shape
        except Exception as e:
            print(f"❌ 添加图形失败: {e}")
            return None
    
    def add_shapes_from_config(self, configs: list):
        """从配置列表批量添加图形"""
        print(f"📋 开始批量添加 {len(configs)} 个图形...")
        
        for i, config in enumerate(configs, 1):
            print(f"\n--- 添加第 {i} 个图形 ---")
            try:
                shape = ShapeFactory.create_shape_from_config(config)
                self.shapes.append(shape)
                print(f"✅ 成功添加 {shape.name}")
            except Exception as e:
                print(f"❌ 添加失败: {e}")
    
    def display_all_shapes(self):
        """显示所有图形"""
        if not self.shapes:
            print("📭 没有图形可显示")
            return
        
        print(f"\n🎨 图形展示厅 - 共有 {len(self.shapes)} 个图形")
        print("=" * 60)
        
        for i, shape in enumerate(self.shapes, 1):
            print(f"\n图形 {i}:")
            print(shape.draw())
            
            info = shape.get_info()
            print(f"📊 图形信息:")
            print(f"   类型: {info['type']}")
            print(f"   面积: {info['area']}")
            print(f"   周长: {info['perimeter']}")
    
    def get_statistics(self):
        """获取统计信息"""
        if not self.shapes:
            return {"total": 0}
        
        total_area = sum(shape.get_area() for shape in self.shapes)
        total_perimeter = sum(shape.get_perimeter() for shape in self.shapes)
        
        shape_counts = {}
        for shape in self.shapes:
            shape_type = shape.__class__.__name__
            shape_counts[shape_type] = shape_counts.get(shape_type, 0) + 1
        
        return {
            "total": len(self.shapes),
            "total_area": round(total_area, 2),
            "total_perimeter": round(total_perimeter, 2),
            "shape_counts": shape_counts
        }


# ==================== 演示函数 ====================
def demo_basic_factory():
    """演示基本的简单工厂使用"""
    print("=== 简单工厂模式演示 ===\n")
    
    manager = ShapeManager()
    
    # 创建不同类型的图形
    print("1. 创建各种图形:")
    manager.add_shape("circle", radius=5.0)
    manager.add_shape("rectangle", width=4.0, height=6.0)
    manager.add_shape("triangle", side_a=3.0, side_b=4.0, side_c=5.0)
    manager.add_shape("square", side=3.0)
    
    # 显示所有图形
    manager.display_all_shapes()
    
    # 显示统计信息
    stats = manager.get_statistics()
    print(f"\n📈 统计信息:")
    print(f"   图形总数: {stats['total']}")
    print(f"   总面积: {stats['total_area']}")
    print(f"   总周长: {stats['total_perimeter']}")
    print(f"   图形分布: {stats['shape_counts']}")


def demo_config_driven():
    """演示配置驱动的图形创建"""
    print("\n" + "=" * 60)
    print("配置驱动的图形创建演示")
    print("=" * 60)
    
    # 配置数据（可以来自文件、数据库等）
    shape_configs = [
        {"type": "circle", "radius": 3.0},
        {"type": "rectangle", "width": 5.0, "height": 3.0},
        {"type": "square", "side": 4.0},
        {"type": "triangle", "side_a": 6.0, "side_b": 8.0, "side_c": 10.0}
    ]
    
    manager = ShapeManager()
    manager.add_shapes_from_config(shape_configs)
    manager.display_all_shapes()


def demo_error_handling():
    """演示错误处理"""
    print("\n" + "=" * 60)
    print("错误处理演示")
    print("=" * 60)
    
    manager = ShapeManager()
    
    # 测试各种错误情况
    print("1. 测试不支持的图形类型:")
    manager.add_shape("hexagon", side=5.0)
    
    print("\n2. 测试缺少参数:")
    manager.add_shape("circle")
    
    print("\n3. 测试无效参数:")
    manager.add_shape("circle", radius=-5.0)
    
    print("\n4. 测试无效三角形:")
    manager.add_shape("triangle", side_a=1.0, side_b=2.0, side_c=10.0)


def main():
    """主函数"""
    demo_basic_factory()
    demo_config_driven()
    demo_error_handling()
    
    print("\n" + "=" * 60)
    print("简单工厂模式的优势:")
    print("1. 封装创建逻辑：客户端无需了解具体的创建过程")
    print("2. 统一创建接口：所有图形都通过同一个工厂创建")
    print("3. 参数验证：工厂可以验证参数的有效性")
    print("4. 错误处理：集中处理创建过程中的错误")
    print("5. 配置驱动：支持从配置数据创建对象")
    print("=" * 60)


if __name__ == "__main__":
    main()
