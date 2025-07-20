"""
02_calculator_factory.py - 计算器工厂简单工厂模式

计算器工厂示例
这个示例展示了简单工厂模式在计算器系统中的应用。
我们有不同类型的运算器（加法、减法、乘法、除法等），通过一个计算器工厂来创建这些运算器。
体现了简单工厂模式与策略模式的结合使用。
"""

from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any
import math


# ==================== 抽象产品 ====================
class Calculator(ABC):
    """计算器抽象基类"""
    
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
    
    @abstractmethod
    def calculate(self, a: float, b: float = None) -> float:
        """执行计算"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """获取计算器描述"""
        pass
    
    def validate_inputs(self, a: float, b: float = None) -> bool:
        """验证输入参数"""
        if not isinstance(a, (int, float)):
            raise TypeError("第一个参数必须是数字")
        if b is not None and not isinstance(b, (int, float)):
            raise TypeError("第二个参数必须是数字")
        return True


# ==================== 具体产品 ====================
class AddCalculator(Calculator):
    """加法计算器"""
    
    def __init__(self):
        super().__init__("加法计算器", "+")
    
    def calculate(self, a: float, b: float = None) -> float:
        self.validate_inputs(a, b)
        if b is None:
            raise ValueError("加法运算需要两个操作数")
        result = a + b
        print(f"🔢 {a} {self.symbol} {b} = {result}")
        return result
    
    def get_description(self) -> str:
        return "执行两个数的加法运算"


class SubtractCalculator(Calculator):
    """减法计算器"""
    
    def __init__(self):
        super().__init__("减法计算器", "-")
    
    def calculate(self, a: float, b: float = None) -> float:
        self.validate_inputs(a, b)
        if b is None:
            raise ValueError("减法运算需要两个操作数")
        result = a - b
        print(f"🔢 {a} {self.symbol} {b} = {result}")
        return result
    
    def get_description(self) -> str:
        return "执行两个数的减法运算"


class MultiplyCalculator(Calculator):
    """乘法计算器"""
    
    def __init__(self):
        super().__init__("乘法计算器", "*")
    
    def calculate(self, a: float, b: float = None) -> float:
        self.validate_inputs(a, b)
        if b is None:
            raise ValueError("乘法运算需要两个操作数")
        result = a * b
        print(f"🔢 {a} {self.symbol} {b} = {result}")
        return result
    
    def get_description(self) -> str:
        return "执行两个数的乘法运算"


class DivideCalculator(Calculator):
    """除法计算器"""
    
    def __init__(self):
        super().__init__("除法计算器", "/")
    
    def calculate(self, a: float, b: float = None) -> float:
        self.validate_inputs(a, b)
        if b is None:
            raise ValueError("除法运算需要两个操作数")
        if b == 0:
            raise ValueError("除数不能为零")
        result = a / b
        print(f"🔢 {a} {self.symbol} {b} = {result}")
        return result
    
    def get_description(self) -> str:
        return "执行两个数的除法运算（除数不能为零）"


class PowerCalculator(Calculator):
    """幂运算计算器"""
    
    def __init__(self):
        super().__init__("幂运算计算器", "^")
    
    def calculate(self, a: float, b: float = None) -> float:
        self.validate_inputs(a, b)
        if b is None:
            raise ValueError("幂运算需要两个操作数")
        result = a ** b
        print(f"🔢 {a} {self.symbol} {b} = {result}")
        return result
    
    def get_description(self) -> str:
        return "执行幂运算（a的b次方）"


class SquareRootCalculator(Calculator):
    """平方根计算器"""
    
    def __init__(self):
        super().__init__("平方根计算器", "√")
    
    def calculate(self, a: float, b: float = None) -> float:
        self.validate_inputs(a, b)
        if a < 0:
            raise ValueError("不能计算负数的平方根")
        result = math.sqrt(a)
        print(f"🔢 {self.symbol}{a} = {result}")
        return result
    
    def get_description(self) -> str:
        return "计算数字的平方根（只需要一个操作数）"


class LogarithmCalculator(Calculator):
    """对数计算器"""
    
    def __init__(self):
        super().__init__("对数计算器", "log")
    
    def calculate(self, a: float, b: float = None) -> float:
        self.validate_inputs(a, b)
        if a <= 0:
            raise ValueError("对数的真数必须大于0")
        
        if b is None:
            # 自然对数
            result = math.log(a)
            print(f"🔢 ln({a}) = {result}")
        else:
            if b <= 0 or b == 1:
                raise ValueError("对数的底数必须大于0且不等于1")
            result = math.log(a, b)
            print(f"🔢 log_{b}({a}) = {result}")
        
        return result
    
    def get_description(self) -> str:
        return "计算对数（一个参数为自然对数，两个参数为指定底数的对数）"


# ==================== 简单工厂 ====================
class CalculatorFactory:
    """计算器工厂类"""
    
    # 支持的计算器类型
    SUPPORTED_CALCULATORS = {
        "add": ("加法", AddCalculator),
        "subtract": ("减法", SubtractCalculator),
        "multiply": ("乘法", MultiplyCalculator),
        "divide": ("除法", DivideCalculator),
        "power": ("幂运算", PowerCalculator),
        "sqrt": ("平方根", SquareRootCalculator),
        "log": ("对数", LogarithmCalculator),
        # 别名支持
        "+": ("加法", AddCalculator),
        "-": ("减法", SubtractCalculator),
        "*": ("乘法", MultiplyCalculator),
        "/": ("除法", DivideCalculator),
        "^": ("幂运算", PowerCalculator),
        "**": ("幂运算", PowerCalculator),
    }
    
    @staticmethod
    def create_calculator(calc_type: str) -> Calculator:
        """
        创建计算器对象
        
        Args:
            calc_type: 计算器类型
        
        Returns:
            Calculator: 创建的计算器对象
        
        Raises:
            ValueError: 不支持的计算器类型
        """
        calc_type = calc_type.lower().strip()
        
        if calc_type in CalculatorFactory.SUPPORTED_CALCULATORS:
            calc_name, calc_class = CalculatorFactory.SUPPORTED_CALCULATORS[calc_type]
            print(f"🏭 计算器工厂正在创建 {calc_name} 计算器...")
            calculator = calc_class()
            print(f"✅ {calculator.name} 创建成功")
            return calculator
        else:
            supported = list(set([name for name, _ in CalculatorFactory.SUPPORTED_CALCULATORS.values()]))
            raise ValueError(f"不支持的计算器类型: {calc_type}。支持的类型: {supported}")
    
    @staticmethod
    def get_supported_calculators() -> Dict[str, str]:
        """获取支持的计算器类型"""
        result = {}
        for key, (name, _) in CalculatorFactory.SUPPORTED_CALCULATORS.items():
            if key not in result.values():  # 避免重复
                result[key] = name
        return result
    
    @staticmethod
    def calculate(calc_type: str, a: float, b: float = None) -> float:
        """
        便捷方法：直接执行计算
        
        Args:
            calc_type: 计算器类型
            a: 第一个操作数
            b: 第二个操作数（可选）
        
        Returns:
            float: 计算结果
        """
        calculator = CalculatorFactory.create_calculator(calc_type)
        return calculator.calculate(a, b)


# ==================== 计算器管理器 ====================
class CalculatorManager:
    """计算器管理器 - 演示工厂的使用"""
    
    def __init__(self):
        self.history = []  # 计算历史
    
    def calculate(self, calc_type: str, a: float, b: float = None) -> float:
        """执行计算并记录历史"""
        try:
            calculator = CalculatorFactory.create_calculator(calc_type)
            result = calculator.calculate(a, b)
            
            # 记录历史
            self.history.append({
                "calculator": calculator.name,
                "operation": f"{a} {calculator.symbol} {b if b is not None else ''}".strip(),
                "result": result
            })
            
            return result
        except Exception as e:
            print(f"❌ 计算失败: {e}")
            raise
    
    def batch_calculate(self, operations: List[Dict[str, Any]]):
        """批量计算"""
        print(f"📊 开始批量计算 {len(operations)} 个表达式...")
        
        for i, op in enumerate(operations, 1):
            print(f"\n--- 计算第 {i} 个表达式 ---")
            try:
                calc_type = op["type"]
                a = op["a"]
                b = op.get("b")
                
                result = self.calculate(calc_type, a, b)
                print(f"✅ 计算成功，结果: {result}")
                
            except Exception as e:
                print(f"❌ 计算失败: {e}")
    
    def show_history(self):
        """显示计算历史"""
        if not self.history:
            print("📭 没有计算历史")
            return
        
        print(f"\n📜 计算历史 - 共 {len(self.history)} 条记录")
        print("=" * 50)
        
        for i, record in enumerate(self.history, 1):
            print(f"{i:2d}. {record['calculator']}: {record['operation']} = {record['result']}")
    
    def clear_history(self):
        """清空历史"""
        self.history.clear()
        print("🗑️  计算历史已清空")
    
    def get_statistics(self):
        """获取统计信息"""
        if not self.history:
            return {"total": 0}
        
        calc_counts = {}
        for record in self.history:
            calc_name = record["calculator"]
            calc_counts[calc_name] = calc_counts.get(calc_name, 0) + 1
        
        return {
            "total": len(self.history),
            "calculator_usage": calc_counts
        }


# ==================== 演示函数 ====================
def demo_basic_calculations():
    """演示基本计算功能"""
    print("=== 计算器工厂演示 ===\n")
    
    manager = CalculatorManager()
    
    print("1. 基本四则运算:")
    manager.calculate("add", 10, 5)
    manager.calculate("subtract", 10, 3)
    manager.calculate("multiply", 4, 6)
    manager.calculate("divide", 15, 3)
    
    print("\n2. 高级运算:")
    manager.calculate("power", 2, 8)
    manager.calculate("sqrt", 16)
    manager.calculate("log", 100, 10)
    
    # 显示历史
    manager.show_history()


def demo_batch_calculations():
    """演示批量计算"""
    print("\n" + "=" * 60)
    print("批量计算演示")
    print("=" * 60)
    
    # 批量计算配置
    operations = [
        {"type": "add", "a": 5, "b": 3},
        {"type": "*", "a": 4, "b": 7},
        {"type": "sqrt", "a": 25},
        {"type": "power", "a": 3, "b": 4},
        {"type": "log", "a": 8, "b": 2},
        {"type": "divide", "a": 20, "b": 4}
    ]
    
    manager = CalculatorManager()
    manager.batch_calculate(operations)
    
    # 显示统计信息
    stats = manager.get_statistics()
    print(f"\n📈 统计信息:")
    print(f"   总计算次数: {stats['total']}")
    print(f"   计算器使用情况: {stats['calculator_usage']}")


def demo_error_handling():
    """演示错误处理"""
    print("\n" + "=" * 60)
    print("错误处理演示")
    print("=" * 60)
    
    manager = CalculatorManager()
    
    print("1. 测试不支持的计算器类型:")
    try:
        manager.calculate("modulo", 10, 3)
    except Exception as e:
        print(f"捕获异常: {e}")
    
    print("\n2. 测试除零错误:")
    try:
        manager.calculate("divide", 10, 0)
    except Exception as e:
        print(f"捕获异常: {e}")
    
    print("\n3. 测试负数平方根:")
    try:
        manager.calculate("sqrt", -4)
    except Exception as e:
        print(f"捕获异常: {e}")
    
    print("\n4. 测试无效对数:")
    try:
        manager.calculate("log", -5)
    except Exception as e:
        print(f"捕获异常: {e}")


def demo_calculator_info():
    """演示计算器信息"""
    print("\n" + "=" * 60)
    print("计算器信息演示")
    print("=" * 60)
    
    # 显示所有支持的计算器
    supported = CalculatorFactory.get_supported_calculators()
    print("🔧 支持的计算器类型:")
    for key, name in supported.items():
        if len(key) <= 3:  # 只显示主要的键
            try:
                calc = CalculatorFactory.create_calculator(key)
                print(f"   {key:8} - {name}: {calc.get_description()}")
            except:
                pass


def main():
    """主函数"""
    demo_basic_calculations()
    demo_batch_calculations()
    demo_error_handling()
    demo_calculator_info()
    
    print("\n" + "=" * 60)
    print("简单工厂模式在计算器中的优势:")
    print("1. 统一创建接口：所有计算器都通过同一个工厂创建")
    print("2. 类型安全：工厂验证计算器类型的有效性")
    print("3. 易于扩展：添加新的计算器类型很简单")
    print("4. 别名支持：支持多种方式指定计算器类型")
    print("5. 错误处理：集中处理创建和计算过程中的错误")
    print("=" * 60)


if __name__ == "__main__":
    main()
