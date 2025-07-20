"""
类装饰器实用示例
展示如何使用装饰器增强类的功能
"""

import time
from typing import Any, Dict
from dataclasses import dataclass

# 1. 单例装饰器
def singleton(cls):
    """单例模式装饰器"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
            print(f"🏗️ 创建新的 {cls.__name__} 实例")
        else:
            print(f"♻️ 返回已存在的 {cls.__name__} 实例")
        return instances[cls]

    return get_instance

# 2. 自动属性装饰器
def auto_property(cls):
    """自动为类添加属性访问方法的装饰器"""

    def add_getter_setter(attr_name):
        """为属性添加getter和setter"""
        private_name = f"_{attr_name}"

        def getter(self):
            return getattr(self, private_name, None)

        def setter(self, value):
            print(f"📝 设置 {attr_name} = {value}")
            setattr(self, private_name, value)

        setattr(cls, f"get_{attr_name}", getter)
        setattr(cls, f"set_{attr_name}", setter)

    # 为所有非私有属性添加getter/setter
    for attr_name in dir(cls):
        if not attr_name.startswith('_') and not callable(getattr(cls, attr_name)):
            add_getter_setter(attr_name)

    return cls

# 3. 方法计时装饰器
def time_methods(cls):
    """为类的所有方法添加计时功能"""

    def time_method(method):
        """为单个方法添加计时"""
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            result = method(self, *args, **kwargs)
            end_time = time.time()
            print(f"⏱️ {cls.__name__}.{method.__name__} 执行时间: {end_time - start_time:.4f}秒")
            return result
        return wrapper

    # 为所有方法添加计时
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and not attr_name.startswith('_'):
            setattr(cls, attr_name, time_method(attr))

    return cls

# 4. 验证装饰器
def validate_types(**type_hints):
    """类型验证装饰器"""
    def decorator(cls):
        original_setattr = cls.__setattr__

        def new_setattr(self, name, value):
            if name in type_hints:
                expected_type = type_hints[name]
                if not isinstance(value, expected_type):
                    raise TypeError(f"❌ {name} 必须是 {expected_type.__name__} 类型，得到 {type(value).__name__}")
                print(f"✅ {name} 类型验证通过")
            original_setattr(self, name, value)

        cls.__setattr__ = new_setattr
        return cls

    return decorator

# 使用装饰器的示例类
@singleton
class DatabaseConnection:
    """数据库连接类（单例模式）"""

    def __init__(self, host: str = "localhost", port: int = 5432):
        self.host = host
        self.port = port
        self.connected = False
        print(f"🔌 初始化数据库连接: {host}:{port}")

    def connect(self):
        """连接数据库"""
        self.connected = True
        print(f"✅ 已连接到数据库 {self.host}:{self.port}")

    def disconnect(self):
        """断开数据库连接"""
        self.connected = False
        print(f"❌ 已断开数据库连接")

@auto_property
class Product:
    """产品类（自动属性访问）"""
    name = ""
    price = 0.0
    category = ""

    def __init__(self, name: str, price: float, category: str = "通用"):
        self.name = name
        self.price = price
        self.category = category

    def get_info(self):
        """获取产品信息"""
        return f"产品: {self.name}, 价格: ¥{self.price}, 分类: {self.category}"

@validate_types(name=str, age=int, salary=float)
class Employee:
    """员工类（带类型验证）"""

    def __init__(self, name: str, age: int, salary: float):
        self.name = name
        self.age = age
        self.salary = salary

    def get_info(self):
        """获取员工信息"""
        return f"员工: {self.name}, 年龄: {self.age}, 薪资: ¥{self.salary}"

    def give_raise(self, amount: float):
        """加薪"""
        self.salary += amount
        print(f"💰 {self.name} 加薪 ¥{amount}")

@time_methods
class Calculator:
    """计算器类（所有方法都有计时功能）"""

    def add(self, a: float, b: float) -> float:
        """加法"""
        time.sleep(0.1)  # 模拟计算时间
        return a + b

    def multiply(self, a: float, b: float) -> float:
        """乘法"""
        time.sleep(0.2)  # 模拟计算时间
        return a * b

    def factorial(self, n: int) -> int:
        """阶乘"""
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)

# 使用dataclass装饰器的现代化员工类
@dataclass
class ModernEmployee:
    """现代化员工类（使用dataclass）"""
    name: str
    age: int
    department: str
    salary: float = 5000.0

    def get_annual_salary(self) -> float:
        """获取年薪"""
        return self.salary * 12

    def __str__(self) -> str:
        return f"{self.name} ({self.age}岁) - {self.department}部门"

def main():
    """演示类装饰器的使用"""
    print("=== 类装饰器演示 ===\n")

    # 1. 单例装饰器
    print("1. 单例装饰器:")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")  # True
    db1.connect()
    print()

    # 2. 自动属性装饰器
    print("2. 自动属性装饰器:")
    product = Product("笔记本电脑", 5999.0, "电子产品")
    print(product.get_info())

    # 使用自动生成的getter/setter方法
    product.set_name("游戏笔记本")
    product.set_price(7999.0)
    print(f"更新后名称: {product.get_name()}")
    print(f"更新后价格: ¥{product.get_price()}")
    print(product.get_info())
    print()

    # 3. 类型验证装饰器
    print("3. 类型验证装饰器:")
    emp = Employee("张三", 30, 8000.0)
    print(emp.get_info())

    try:
        emp.age = "三十"  # 这会引发类型错误
    except TypeError as e:
        print(e)

    emp.give_raise(1000.0)
    print(emp.get_info())
    print()

    # 4. 方法计时装饰器
    print("4. 方法计时装饰器:")
    calc = Calculator()
    result1 = calc.add(10, 20)
    print(f"加法结果: {result1}")

    result2 = calc.multiply(5, 6)
    print(f"乘法结果: {result2}")

    result3 = calc.factorial(5)
    print(f"阶乘结果: {result3}")
    print()

    # 5. dataclass装饰器
    print("5. dataclass装饰器:")
    emp1 = ModernEmployee("李四", 25, "技术")
    emp2 = ModernEmployee("王五", 28, "销售", 6000.0)

    print(emp1)
    print(f"年薪: ¥{emp1.get_annual_salary()}")
    print(emp2)
    print(f"年薪: ¥{emp2.get_annual_salary()}")

if __name__ == "__main__":
    main()

