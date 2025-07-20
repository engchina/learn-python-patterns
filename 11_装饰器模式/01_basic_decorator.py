"""
基础装饰器模式演示
展示装饰器模式的核心概念和基本实现
"""

from abc import ABC, abstractmethod

# 抽象组件接口
class Beverage(ABC):
    """饮料抽象基类"""
    
    @abstractmethod
    def get_description(self) -> str:
        """获取饮料描述"""
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        """获取饮料价格"""
        pass

# 具体组件 - 基础饮料
class Coffee(Beverage):
    """咖啡类"""
    
    def get_description(self) -> str:
        return "咖啡"
    
    def get_cost(self) -> float:
        return 15.0

class Tea(Beverage):
    """茶类"""
    
    def get_description(self) -> str:
        return "茶"
    
    def get_cost(self) -> float:
        return 10.0

# 抽象装饰器
class BeverageDecorator(Beverage):
    """饮料装饰器基类"""
    
    def __init__(self, beverage: Beverage):
        self._beverage = beverage
    
    def get_description(self) -> str:
        return self._beverage.get_description()
    
    def get_cost(self) -> float:
        return self._beverage.get_cost()

# 具体装饰器
class MilkDecorator(BeverageDecorator):
    """牛奶装饰器"""
    
    def get_description(self) -> str:
        return f"{self._beverage.get_description()} + 牛奶"
    
    def get_cost(self) -> float:
        return self._beverage.get_cost() + 3.0

class SugarDecorator(BeverageDecorator):
    """糖装饰器"""
    
    def get_description(self) -> str:
        return f"{self._beverage.get_description()} + 糖"
    
    def get_cost(self) -> float:
        return self._beverage.get_cost() + 1.0

class WhipDecorator(BeverageDecorator):
    """奶泡装饰器"""
    
    def get_description(self) -> str:
        return f"{self._beverage.get_description()} + 奶泡"
    
    def get_cost(self) -> float:
        return self._beverage.get_cost() + 4.0

def main():
    """演示装饰器模式的使用"""
    print("=== 装饰器模式演示 ===\n")
    
    # 基础饮料
    coffee = Coffee()
    print(f"基础咖啡: {coffee.get_description()}, 价格: ¥{coffee.get_cost()}")
    
    # 添加牛奶
    coffee_with_milk = MilkDecorator(coffee)
    print(f"加牛奶: {coffee_with_milk.get_description()}, 价格: ¥{coffee_with_milk.get_cost()}")
    
    # 添加糖和奶泡
    fancy_coffee = WhipDecorator(SugarDecorator(coffee_with_milk))
    print(f"豪华咖啡: {fancy_coffee.get_description()}, 价格: ¥{fancy_coffee.get_cost()}")
    
    print("\n" + "="*50 + "\n")
    
    # 茶的例子
    tea = Tea()
    print(f"基础茶: {tea.get_description()}, 价格: ¥{tea.get_cost()}")
    
    # 奶茶
    milk_tea = MilkDecorator(SugarDecorator(tea))
    print(f"奶茶: {milk_tea.get_description()}, 价格: ¥{milk_tea.get_cost()}")

if __name__ == "__main__":
    main()