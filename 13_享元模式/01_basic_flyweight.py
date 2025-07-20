"""
01_basic_flyweight.py - 享元模式基础实现

这个示例展示了享元模式的基本概念和实现方式。
通过分离内在状态和外在状态，实现对象的共享和内存优化。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


# ==================== 抽象享元接口 ====================
class Flyweight(ABC):
    """抽象享元接口"""
    
    @abstractmethod
    def operation(self, extrinsic_state: Any) -> str:
        """执行操作，接受外在状态作为参数"""
        pass


# ==================== 具体享元实现 ====================
class ConcreteFlyweight(Flyweight):
    """具体享元实现"""
    
    def __init__(self, intrinsic_state: str):
        """
        初始化享元对象
        
        Args:
            intrinsic_state: 内在状态（可共享的状态）
        """
        self._intrinsic_state = intrinsic_state
        print(f"创建享元对象: {intrinsic_state}")
    
    def operation(self, extrinsic_state: Any) -> str:
        """
        执行操作
        
        Args:
            extrinsic_state: 外在状态（不可共享的状态）
            
        Returns:
            操作结果字符串
        """
        return f"享元[{self._intrinsic_state}] 处理外在状态: {extrinsic_state}"
    
    def get_intrinsic_state(self) -> str:
        """获取内在状态"""
        return self._intrinsic_state


# ==================== 享元工厂 ====================
class FlyweightFactory:
    """享元工厂 - 负责创建和管理享元对象"""
    
    def __init__(self):
        self._flyweights: Dict[str, Flyweight] = {}
        self._creation_count = 0
        self._access_count = 0
    
    def get_flyweight(self, key: str) -> Flyweight:
        """
        获取享元对象
        
        Args:
            key: 享元对象的标识键
            
        Returns:
            享元对象
        """
        self._access_count += 1
        
        if key not in self._flyweights:
            self._flyweights[key] = ConcreteFlyweight(key)
            self._creation_count += 1
            print(f"✓ 创建新享元: {key}")
        else:
            print(f"♻️ 复用现有享元: {key}")
        
        return self._flyweights[key]
    
    def get_flyweight_count(self) -> int:
        """获取享元对象数量"""
        return len(self._flyweights)
    
    def get_statistics(self) -> Dict[str, int]:
        """获取统计信息"""
        return {
            "flyweight_count": len(self._flyweights),
            "creation_count": self._creation_count,
            "access_count": self._access_count,
            "reuse_rate": round((self._access_count - self._creation_count) / self._access_count * 100, 1) if self._access_count > 0 else 0
        }
    
    def list_flyweights(self):
        """列出所有享元对象"""
        print(f"\n📋 享元工厂包含 {len(self._flyweights)} 个享元对象:")
        for key, flyweight in self._flyweights.items():
            print(f"  • {key}: {flyweight}")


# ==================== 上下文类 ====================
class Context:
    """上下文类 - 维护外在状态并使用享元对象"""
    
    def __init__(self, factory: FlyweightFactory, intrinsic_state: str, extrinsic_state: Any):
        """
        初始化上下文
        
        Args:
            factory: 享元工厂
            intrinsic_state: 内在状态（用于获取享元对象）
            extrinsic_state: 外在状态
        """
        self._flyweight = factory.get_flyweight(intrinsic_state)
        self._extrinsic_state = extrinsic_state
        self._intrinsic_state = intrinsic_state
    
    def operation(self) -> str:
        """执行操作"""
        return self._flyweight.operation(self._extrinsic_state)
    
    def get_states(self) -> Dict[str, Any]:
        """获取状态信息"""
        return {
            "intrinsic_state": self._intrinsic_state,
            "extrinsic_state": self._extrinsic_state
        }


# ==================== 使用示例 ====================
def demo_basic_flyweight():
    """基础享元模式演示"""
    print("=" * 60)
    print("🎯 享元模式基础演示")
    print("=" * 60)
    
    # 创建享元工厂
    factory = FlyweightFactory()
    
    print("\n📝 创建多个上下文对象...")
    
    # 创建多个上下文对象，观察享元对象的复用
    contexts = [
        Context(factory, "类型A", "外在状态1"),
        Context(factory, "类型B", "外在状态2"),
        Context(factory, "类型A", "外在状态3"),  # 复用类型A的享元
        Context(factory, "类型C", "外在状态4"),
        Context(factory, "类型B", "外在状态5"),  # 复用类型B的享元
        Context(factory, "类型A", "外在状态6"),  # 再次复用类型A的享元
        Context(factory, "类型D", "外在状态7"),
        Context(factory, "类型C", "外在状态8"),  # 复用类型C的享元
    ]
    
    print(f"\n🔄 执行操作...")
    for i, context in enumerate(contexts, 1):
        result = context.operation()
        states = context.get_states()
        print(f"  {i}. {result}")
        print(f"     状态: 内在={states['intrinsic_state']}, 外在={states['extrinsic_state']}")
    
    # 显示统计信息
    print(f"\n📊 享元统计信息:")
    stats = factory.get_statistics()
    print(f"  • 享元对象数量: {stats['flyweight_count']}")
    print(f"  • 对象创建次数: {stats['creation_count']}")
    print(f"  • 对象访问次数: {stats['access_count']}")
    print(f"  • 对象复用率: {stats['reuse_rate']}%")
    print(f"  • 上下文对象数量: {len(contexts)}")
    
    memory_saved = len(contexts) - stats['flyweight_count']
    memory_save_rate = (memory_saved / len(contexts)) * 100
    print(f"  • 节省对象数量: {memory_saved}")
    print(f"  • 内存节省率: {memory_save_rate:.1f}%")
    
    # 列出所有享元对象
    factory.list_flyweights()


def demo_shape_flyweight():
    """图形享元演示"""
    print("\n" + "=" * 60)
    print("🎨 图形享元演示")
    print("=" * 60)
    
    # 图形享元类
    class Shape(Flyweight):
        """图形享元"""
        
        def __init__(self, shape_type: str, color: str):
            self.shape_type = shape_type  # 内在状态
            self.color = color           # 内在状态
            print(f"创建图形享元: {shape_type}-{color}")
        
        def operation(self, extrinsic_state: Any) -> str:
            """绘制图形"""
            x, y, size = extrinsic_state
            return f"绘制{self.color}{self.shape_type} 位置:({x},{y}) 大小:{size}"
    
    # 图形工厂
    class ShapeFactory:
        """图形工厂"""
        
        def __init__(self):
            self._shapes: Dict[str, Shape] = {}
        
        def get_shape(self, shape_type: str, color: str) -> Shape:
            """获取图形享元"""
            key = f"{shape_type}-{color}"
            
            if key not in self._shapes:
                self._shapes[key] = Shape(shape_type, color)
                print(f"✓ 创建新图形: {key}")
            else:
                print(f"♻️ 复用现有图形: {key}")
            
            return self._shapes[key]
        
        def get_shape_count(self) -> int:
            """获取图形类型数量"""
            return len(self._shapes)
    
    # 图形上下文
    class ShapeContext:
        """图形上下文"""
        
        def __init__(self, factory: ShapeFactory, shape_type: str, color: str, 
                     x: int, y: int, size: int):
            self.shape = factory.get_shape(shape_type, color)
            self.x = x        # 外在状态
            self.y = y        # 外在状态
            self.size = size  # 外在状态
        
        def draw(self) -> str:
            """绘制图形"""
            return self.shape.operation((self.x, self.y, self.size))
    
    # 创建图形工厂
    shape_factory = ShapeFactory()
    
    print("\n🎨 创建多个图形...")
    
    # 创建多个图形上下文
    shapes = [
        ShapeContext(shape_factory, "圆形", "红色", 10, 20, 5),
        ShapeContext(shape_factory, "矩形", "蓝色", 30, 40, 8),
        ShapeContext(shape_factory, "圆形", "红色", 50, 60, 3),  # 复用红色圆形
        ShapeContext(shape_factory, "三角形", "绿色", 70, 80, 6),
        ShapeContext(shape_factory, "矩形", "蓝色", 90, 100, 4), # 复用蓝色矩形
        ShapeContext(shape_factory, "圆形", "黄色", 110, 120, 7),
        ShapeContext(shape_factory, "圆形", "红色", 130, 140, 2), # 再次复用红色圆形
        ShapeContext(shape_factory, "矩形", "绿色", 150, 160, 5),
    ]
    
    print(f"\n🖼️ 绘制所有图形...")
    for i, shape_context in enumerate(shapes, 1):
        result = shape_context.draw()
        print(f"  {i}. {result}")
    
    print(f"\n📊 图形统计信息:")
    print(f"  • 图形享元数量: {shape_factory.get_shape_count()}")
    print(f"  • 图形实例数量: {len(shapes)}")
    
    memory_saved = len(shapes) - shape_factory.get_shape_count()
    memory_save_rate = (memory_saved / len(shapes)) * 100
    print(f"  • 节省对象数量: {memory_saved}")
    print(f"  • 内存节省率: {memory_save_rate:.1f}%")


def main():
    """主演示函数"""
    demo_basic_flyweight()
    demo_shape_flyweight()
    
    print("\n" + "=" * 60)
    print("🎉 享元模式基础演示完成！")
    print("💡 关键要点:")
    print("   • 享元模式通过共享内在状态来减少对象数量")
    print("   • 外在状态由上下文维护，不被共享")
    print("   • 享元工厂负责管理和复用享元对象")
    print("   • 适用于需要大量相似对象的场景")
    print("=" * 60)


if __name__ == "__main__":
    main()
