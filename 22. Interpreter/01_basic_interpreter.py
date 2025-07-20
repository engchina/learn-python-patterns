"""
01_basic_interpreter.py - 解释器模式基础实现

数学表达式解释器示例
这个示例展示了解释器模式的基本概念和实现方式。
通过数学表达式的解释，我们可以看到如何将语法规则转换为类，
并通过递归调用来解释复杂的表达式。
"""

from abc import ABC, abstractmethod
from typing import Dict, Union


# ==================== 上下文类 ====================
class Context:
    """解释器上下文 - 存储变量和状态信息"""
    
    def __init__(self):
        self._variables: Dict[str, Union[int, float]] = {}
        self._functions: Dict[str, callable] = {}
        self._debug = False
    
    def set_variable(self, name: str, value: Union[int, float]):
        """设置变量值"""
        self._variables[name] = value
        if self._debug:
            print(f"设置变量: {name} = {value}")
    
    def get_variable(self, name: str) -> Union[int, float]:
        """获取变量值"""
        value = self._variables.get(name, 0)
        if self._debug:
            print(f"获取变量: {name} = {value}")
        return value
    
    def has_variable(self, name: str) -> bool:
        """检查变量是否存在"""
        return name in self._variables
    
    def set_function(self, name: str, func: callable):
        """设置函数"""
        self._functions[name] = func
    
    def get_function(self, name: str) -> callable:
        """获取函数"""
        return self._functions.get(name)
    
    def set_debug(self, debug: bool):
        """设置调试模式"""
        self._debug = debug
    
    def get_all_variables(self) -> Dict[str, Union[int, float]]:
        """获取所有变量"""
        return self._variables.copy()
    
    def clear(self):
        """清空上下文"""
        self._variables.clear()
        self._functions.clear()
    
    def __str__(self):
        return f"Context(variables={self._variables})"


# ==================== 抽象表达式 ====================
class AbstractExpression(ABC):
    """抽象表达式基类"""
    
    @abstractmethod
    def interpret(self, context: Context) -> Union[int, float]:
        """解释表达式"""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """返回表达式的字符串表示"""
        pass


# ==================== 终结符表达式 ====================
class NumberExpression(AbstractExpression):
    """数字表达式（终结符）"""
    
    def __init__(self, value: Union[int, float]):
        self.value = value
    
    def interpret(self, context: Context) -> Union[int, float]:
        """解释数字"""
        if context._debug:
            print(f"解释数字: {self.value}")
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


class VariableExpression(AbstractExpression):
    """变量表达式（终结符）"""
    
    def __init__(self, name: str):
        self.name = name
    
    def interpret(self, context: Context) -> Union[int, float]:
        """解释变量"""
        if not context.has_variable(self.name):
            raise ValueError(f"未定义的变量: {self.name}")
        
        value = context.get_variable(self.name)
        if context._debug:
            print(f"解释变量: {self.name} = {value}")
        return value
    
    def __str__(self) -> str:
        return self.name


# ==================== 非终结符表达式 ====================
class BinaryExpression(AbstractExpression):
    """二元表达式基类"""
    
    def __init__(self, left: AbstractExpression, right: AbstractExpression):
        self.left = left
        self.right = right
    
    @abstractmethod
    def operate(self, left_value: Union[int, float], right_value: Union[int, float]) -> Union[int, float]:
        """执行具体的运算"""
        pass
    
    @abstractmethod
    def get_operator_symbol(self) -> str:
        """获取运算符符号"""
        pass
    
    def interpret(self, context: Context) -> Union[int, float]:
        """解释二元表达式"""
        left_value = self.left.interpret(context)
        right_value = self.right.interpret(context)
        result = self.operate(left_value, right_value)
        
        if context._debug:
            print(f"解释{self.get_operator_symbol()}运算: {left_value} {self.get_operator_symbol()} {right_value} = {result}")
        
        return result
    
    def __str__(self) -> str:
        return f"({self.left} {self.get_operator_symbol()} {self.right})"


class AddExpression(BinaryExpression):
    """加法表达式"""
    
    def operate(self, left_value: Union[int, float], right_value: Union[int, float]) -> Union[int, float]:
        return left_value + right_value
    
    def get_operator_symbol(self) -> str:
        return "+"


class SubtractExpression(BinaryExpression):
    """减法表达式"""
    
    def operate(self, left_value: Union[int, float], right_value: Union[int, float]) -> Union[int, float]:
        return left_value - right_value
    
    def get_operator_symbol(self) -> str:
        return "-"


class MultiplyExpression(BinaryExpression):
    """乘法表达式"""
    
    def operate(self, left_value: Union[int, float], right_value: Union[int, float]) -> Union[int, float]:
        return left_value * right_value
    
    def get_operator_symbol(self) -> str:
        return "*"


class DivideExpression(BinaryExpression):
    """除法表达式"""
    
    def operate(self, left_value: Union[int, float], right_value: Union[int, float]) -> Union[int, float]:
        if right_value == 0:
            raise ValueError("除零错误")
        return left_value / right_value
    
    def get_operator_symbol(self) -> str:
        return "/"


class PowerExpression(BinaryExpression):
    """幂运算表达式"""
    
    def operate(self, left_value: Union[int, float], right_value: Union[int, float]) -> Union[int, float]:
        return left_value ** right_value
    
    def get_operator_symbol(self) -> str:
        return "^"


# ==================== 一元表达式 ====================
class UnaryExpression(AbstractExpression):
    """一元表达式基类"""
    
    def __init__(self, expression: AbstractExpression):
        self.expression = expression
    
    @abstractmethod
    def operate(self, value: Union[int, float]) -> Union[int, float]:
        """执行一元运算"""
        pass
    
    @abstractmethod
    def get_operator_symbol(self) -> str:
        """获取运算符符号"""
        pass
    
    def interpret(self, context: Context) -> Union[int, float]:
        """解释一元表达式"""
        value = self.expression.interpret(context)
        result = self.operate(value)
        
        if context._debug:
            print(f"解释{self.get_operator_symbol()}运算: {self.get_operator_symbol()}{value} = {result}")
        
        return result
    
    def __str__(self) -> str:
        return f"{self.get_operator_symbol()}{self.expression}"


class NegateExpression(UnaryExpression):
    """取负表达式"""
    
    def operate(self, value: Union[int, float]) -> Union[int, float]:
        return -value
    
    def get_operator_symbol(self) -> str:
        return "-"


# ==================== 函数表达式 ====================
class FunctionExpression(AbstractExpression):
    """函数调用表达式"""
    
    def __init__(self, name: str, *args: AbstractExpression):
        self.name = name
        self.args = args
    
    def interpret(self, context: Context) -> Union[int, float]:
        """解释函数调用"""
        func = context.get_function(self.name)
        if func is None:
            raise ValueError(f"未定义的函数: {self.name}")
        
        # 解释所有参数
        arg_values = [arg.interpret(context) for arg in self.args]
        
        try:
            result = func(*arg_values)
            if context._debug:
                print(f"调用函数: {self.name}({', '.join(map(str, arg_values))}) = {result}")
            return result
        except Exception as e:
            raise ValueError(f"函数 {self.name} 执行错误: {str(e)}")
    
    def __str__(self) -> str:
        args_str = ', '.join(str(arg) for arg in self.args)
        return f"{self.name}({args_str})"


# ==================== 表达式构建器 ====================
class ExpressionBuilder:
    """表达式构建器 - 帮助构建复杂表达式"""
    
    @staticmethod
    def number(value: Union[int, float]) -> NumberExpression:
        """创建数字表达式"""
        return NumberExpression(value)
    
    @staticmethod
    def variable(name: str) -> VariableExpression:
        """创建变量表达式"""
        return VariableExpression(name)
    
    @staticmethod
    def add(left: AbstractExpression, right: AbstractExpression) -> AddExpression:
        """创建加法表达式"""
        return AddExpression(left, right)
    
    @staticmethod
    def subtract(left: AbstractExpression, right: AbstractExpression) -> SubtractExpression:
        """创建减法表达式"""
        return SubtractExpression(left, right)
    
    @staticmethod
    def multiply(left: AbstractExpression, right: AbstractExpression) -> MultiplyExpression:
        """创建乘法表达式"""
        return MultiplyExpression(left, right)
    
    @staticmethod
    def divide(left: AbstractExpression, right: AbstractExpression) -> DivideExpression:
        """创建除法表达式"""
        return DivideExpression(left, right)
    
    @staticmethod
    def power(left: AbstractExpression, right: AbstractExpression) -> PowerExpression:
        """创建幂运算表达式"""
        return PowerExpression(left, right)
    
    @staticmethod
    def negate(expression: AbstractExpression) -> NegateExpression:
        """创建取负表达式"""
        return NegateExpression(expression)
    
    @staticmethod
    def function(name: str, *args: AbstractExpression) -> FunctionExpression:
        """创建函数调用表达式"""
        return FunctionExpression(name, *args)


# ==================== 演示函数 ====================
def demonstrate_basic_interpreter():
    """演示基础解释器功能"""
    print("=" * 60)
    print("基础数学表达式解释器演示")
    print("=" * 60)
    
    # 创建上下文
    context = Context()
    context.set_debug(True)
    
    # 设置变量
    context.set_variable("x", 10)
    context.set_variable("y", 5)
    context.set_variable("z", 2)
    
    print(f"初始上下文: {context}")
    
    # 使用构建器创建表达式
    builder = ExpressionBuilder
    
    print("\n1. 简单算术表达式:")
    
    # 表达式: x + y
    expr1 = builder.add(builder.variable("x"), builder.variable("y"))
    print(f"表达式: {expr1}")
    result1 = expr1.interpret(context)
    print(f"结果: {result1}\n")
    
    # 表达式: (x + y) * z
    expr2 = builder.multiply(
        builder.add(builder.variable("x"), builder.variable("y")),
        builder.variable("z")
    )
    print(f"表达式: {expr2}")
    result2 = expr2.interpret(context)
    print(f"结果: {result2}\n")
    
    # 表达式: x^2 + y^2
    expr3 = builder.add(
        builder.power(builder.variable("x"), builder.number(2)),
        builder.power(builder.variable("y"), builder.number(2))
    )
    print(f"表达式: {expr3}")
    result3 = expr3.interpret(context)
    print(f"结果: {result3}\n")
    
    print("2. 包含函数的表达式:")
    
    # 添加数学函数
    import math
    context.set_function("sqrt", math.sqrt)
    context.set_function("sin", math.sin)
    context.set_function("cos", math.cos)
    context.set_function("max", max)
    context.set_function("min", min)
    
    # 表达式: sqrt(x^2 + y^2)
    expr4 = builder.function("sqrt",
        builder.add(
            builder.power(builder.variable("x"), builder.number(2)),
            builder.power(builder.variable("y"), builder.number(2))
        )
    )
    print(f"表达式: {expr4}")
    result4 = expr4.interpret(context)
    print(f"结果: {result4:.2f}\n")
    
    # 表达式: max(x, y, z)
    expr5 = builder.function("max",
        builder.variable("x"),
        builder.variable("y"),
        builder.variable("z")
    )
    print(f"表达式: {expr5}")
    result5 = expr5.interpret(context)
    print(f"结果: {result5}\n")


def demonstrate_complex_expressions():
    """演示复杂表达式"""
    print("=" * 60)
    print("复杂表达式演示")
    print("=" * 60)
    
    context = Context()
    context.set_variable("a", 3)
    context.set_variable("b", 4)
    context.set_variable("c", 5)
    
    builder = ExpressionBuilder
    
    print("变量值: a=3, b=4, c=5\n")
    
    # 二次方程求解: (-b + sqrt(b^2 - 4*a*c)) / (2*a)
    # 这里假设 a=1, b=-5, c=6，方程为 x^2 - 5x + 6 = 0
    context.set_variable("a", 1)
    context.set_variable("b", -5)
    context.set_variable("c", 6)
    
    import math
    context.set_function("sqrt", math.sqrt)
    
    print("求解二次方程 x^2 - 5x + 6 = 0:")
    print("使用公式: (-b + sqrt(b^2 - 4*a*c)) / (2*a)")
    
    # 判别式: b^2 - 4*a*c
    discriminant = builder.subtract(
        builder.power(builder.variable("b"), builder.number(2)),
        builder.multiply(
            builder.multiply(builder.number(4), builder.variable("a")),
            builder.variable("c")
        )
    )
    
    # 解1: (-b + sqrt(discriminant)) / (2*a)
    solution1 = builder.divide(
        builder.add(
            builder.negate(builder.variable("b")),
            builder.function("sqrt", discriminant)
        ),
        builder.multiply(builder.number(2), builder.variable("a"))
    )
    
    print(f"判别式: {discriminant}")
    print(f"判别式值: {discriminant.interpret(context)}")
    print(f"解1: {solution1}")
    print(f"解1值: {solution1.interpret(context)}")
    
    # 解2: (-b - sqrt(discriminant)) / (2*a)
    solution2 = builder.divide(
        builder.subtract(
            builder.negate(builder.variable("b")),
            builder.function("sqrt", discriminant)
        ),
        builder.multiply(builder.number(2), builder.variable("a"))
    )
    
    print(f"解2: {solution2}")
    print(f"解2值: {solution2.interpret(context)}")


if __name__ == "__main__":
    demonstrate_basic_interpreter()
    demonstrate_complex_expressions()
