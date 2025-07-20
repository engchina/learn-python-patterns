#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成器与迭代器的对比

本模块演示了生成器和迭代器的区别与联系，包括：
1. 生成器函数的使用 - yield关键字
2. 生成器表达式 - 简洁的语法
3. 性能和内存对比 - 实际测试
4. 何时选择生成器vs迭代器 - 决策指南

作者: Assistant
日期: 2024-01-20
"""

import sys
import time
import memory_profiler
from typing import Iterator, Generator, List
from functools import wraps


class FibonacciIterator:
    """传统迭代器实现斐波那契数列"""
    
    def __init__(self, max_count: int = None):
        self.max_count = max_count
        self.count = 0
        self.current = 0
        self.next_val = 1
    
    def __iter__(self) -> 'FibonacciIterator':
        return self
    
    def __next__(self) -> int:
        if self.max_count and self.count >= self.max_count:
            raise StopIteration
        
        result = self.current
        self.current, self.next_val = self.next_val, self.current + self.next_val
        self.count += 1
        return result
    
    def reset(self) -> None:
        """重置迭代器状态"""
        self.count = 0
        self.current = 0
        self.next_val = 1


def fibonacci_generator(max_count: int = None) -> Generator[int, None, None]:
    """生成器函数实现斐波那契数列"""
    count = 0
    current, next_val = 0, 1
    
    while max_count is None or count < max_count:
        yield current
        current, next_val = next_val, current + next_val
        count += 1


class NumberRangeIterator:
    """传统迭代器实现数字范围"""
    
    def __init__(self, start: int, end: int, step: int = 1):
        self.start = start
        self.end = end
        self.step = step
        self.current = start
    
    def __iter__(self) -> 'NumberRangeIterator':
        self.current = self.start
        return self
    
    def __next__(self) -> int:
        if self.current >= self.end:
            raise StopIteration
        
        result = self.current
        self.current += self.step
        return result


def number_range_generator(start: int, end: int, step: int = 1) -> Generator[int, None, None]:
    """生成器函数实现数字范围"""
    current = start
    while current < end:
        yield current
        current += step


class DataProcessorIterator:
    """传统迭代器实现数据处理"""
    
    def __init__(self, data: List[int]):
        self.data = data
        self.index = 0
    
    def __iter__(self) -> 'DataProcessorIterator':
        self.index = 0
        return self
    
    def __next__(self) -> dict:
        if self.index >= len(self.data):
            raise StopIteration
        
        value = self.data[self.index]
        result = {
            'original': value,
            'squared': value ** 2,
            'is_even': value % 2 == 0,
            'category': 'small' if value < 10 else 'large'
        }
        self.index += 1
        return result


def data_processor_generator(data: List[int]) -> Generator[dict, None, None]:
    """生成器函数实现数据处理"""
    for value in data:
        yield {
            'original': value,
            'squared': value ** 2,
            'is_even': value % 2 == 0,
            'category': 'small' if value < 10 else 'large'
        }


def timing_decorator(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️ {func.__name__} 执行时间: {end_time - start_time:.6f} 秒")
        return result
    return wrapper


def memory_usage_decorator(func):
    """内存使用装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 获取执行前的内存使用
        start_memory = memory_profiler.memory_usage()[0]
        result = func(*args, **kwargs)
        # 获取执行后的内存使用
        end_memory = memory_profiler.memory_usage()[0]
        memory_diff = end_memory - start_memory
        print(f"💾 {func.__name__} 内存使用: {memory_diff:.2f} MB")
        return result
    return wrapper


@timing_decorator
def test_iterator_performance(count: int) -> int:
    """测试传统迭代器性能"""
    fib_iter = FibonacciIterator(count)
    total = 0
    for num in fib_iter:
        total += num
    return total


@timing_decorator
def test_generator_performance(count: int) -> int:
    """测试生成器性能"""
    fib_gen = fibonacci_generator(count)
    total = 0
    for num in fib_gen:
        total += num
    return total


@memory_usage_decorator
def test_iterator_memory(count: int) -> List[int]:
    """测试传统迭代器内存使用"""
    fib_iter = FibonacciIterator(count)
    return list(fib_iter)


@memory_usage_decorator
def test_generator_memory(count: int) -> List[int]:
    """测试生成器内存使用"""
    fib_gen = fibonacci_generator(count)
    return list(fib_gen)


def demo_basic_comparison():
    """演示基本对比"""
    print("=" * 50)
    print("🔄 生成器与迭代器基本对比")
    print("=" * 50)
    
    count = 10
    
    # 传统迭代器
    print("传统迭代器实现:")
    fib_iter = FibonacciIterator(count)
    iter_result = list(fib_iter)
    print(f"  结果: {iter_result}")
    print(f"  类型: {type(fib_iter)}")
    print(f"  大小: {sys.getsizeof(fib_iter)} bytes")
    
    # 生成器函数
    print("\n生成器函数实现:")
    fib_gen = fibonacci_generator(count)
    gen_result = list(fib_gen)
    print(f"  结果: {gen_result}")
    print(f"  类型: {type(fib_gen)}")
    print(f"  大小: {sys.getsizeof(fib_gen)} bytes")
    
    # 生成器表达式
    print("\n生成器表达式实现:")
    gen_expr = (x**2 for x in range(count))
    expr_result = list(gen_expr)
    print(f"  结果: {expr_result}")
    print(f"  类型: {type(gen_expr)}")
    print(f"  大小: {sys.getsizeof(gen_expr)} bytes")


def demo_syntax_comparison():
    """演示语法对比"""
    print("\n" + "=" * 50)
    print("📝 语法对比")
    print("=" * 50)
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("原始数据:", data)
    
    # 传统迭代器 - 需要完整的类定义
    print("\n传统迭代器 (类定义):")
    print("```python")
    print("class DataProcessorIterator:")
    print("    def __init__(self, data): ...")
    print("    def __iter__(self): ...")
    print("    def __next__(self): ...")
    print("```")
    
    processor_iter = DataProcessorIterator(data[:3])
    iter_results = list(processor_iter)
    print("结果示例:", iter_results[0])
    
    # 生成器函数 - 简洁的函数定义
    print("\n生成器函数 (函数定义):")
    print("```python")
    print("def data_processor_generator(data):")
    print("    for value in data:")
    print("        yield {...}")
    print("```")
    
    processor_gen = data_processor_generator(data[:3])
    gen_results = list(processor_gen)
    print("结果示例:", gen_results[0])
    
    # 生成器表达式 - 最简洁
    print("\n生成器表达式 (一行代码):")
    print("```python")
    print("(x**2 for x in data if x % 2 == 0)")
    print("```")
    
    expr_gen = (x**2 for x in data if x % 2 == 0)
    expr_results = list(expr_gen)
    print("结果:", expr_results)


def demo_performance_comparison():
    """演示性能对比"""
    print("\n" + "=" * 50)
    print("⚡ 性能对比")
    print("=" * 50)
    
    test_counts = [1000, 5000, 10000]
    
    for count in test_counts:
        print(f"\n测试规模: {count} 个斐波那契数")
        
        # 性能测试
        iter_total = test_iterator_performance(count)
        gen_total = test_generator_performance(count)
        
        print(f"  迭代器总和: {iter_total}")
        print(f"  生成器总和: {gen_total}")
        print(f"  结果一致: {'✅' if iter_total == gen_total else '❌'}")


def demo_memory_comparison():
    """演示内存对比"""
    print("\n" + "=" * 50)
    print("💾 内存使用对比")
    print("=" * 50)
    
    test_count = 1000
    print(f"测试规模: {test_count} 个斐波那契数")
    
    # 内存测试
    iter_result = test_iterator_memory(test_count)
    gen_result = test_generator_memory(test_count)
    
    print(f"结果长度一致: {'✅' if len(iter_result) == len(gen_result) else '❌'}")


def demo_lazy_evaluation():
    """演示惰性求值"""
    print("\n" + "=" * 50)
    print("🦥 惰性求值演示")
    print("=" * 50)
    
    print("创建大型生成器 (不会立即计算):")
    large_gen = fibonacci_generator(1000000)  # 100万个数
    print(f"  生成器大小: {sys.getsizeof(large_gen)} bytes")
    print("  ✅ 创建完成，内存使用很少")
    
    print("\n只取前5个值:")
    for i, value in enumerate(large_gen):
        if i >= 5:
            break
        print(f"  第{i+1}个: {value}")
    
    print("\n对比：创建相同大小的列表:")
    try:
        # 这会消耗大量内存
        print("  ⚠️ 创建大列表会消耗大量内存，这里跳过演示")
        # large_list = list(range(1000000))
    except MemoryError:
        print("  ❌ 内存不足")


def demo_generator_expressions():
    """演示生成器表达式"""
    print("\n" + "=" * 50)
    print("🎭 生成器表达式演示")
    print("=" * 50)
    
    data = range(1, 21)
    print(f"原始数据: {list(data)}")
    
    # 基本生成器表达式
    squares = (x**2 for x in data)
    print(f"\n平方数生成器: {type(squares)}")
    print(f"前5个平方数: {[next(squares) for _ in range(5)]}")
    
    # 带条件的生成器表达式
    even_squares = (x**2 for x in data if x % 2 == 0)
    print(f"\n偶数平方数: {list(even_squares)}")
    
    # 嵌套生成器表达式
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = (item for row in matrix for item in row)
    print(f"\n矩阵扁平化: {list(flattened)}")
    
    # 生成器表达式的组合
    data_pipeline = (
        str(x) + "!" 
        for x in (x**2 for x in range(1, 11) if x % 2 == 0)
        if x > 10
    )
    print(f"\n管道处理结果: {list(data_pipeline)}")


def demo_when_to_use():
    """演示何时使用生成器vs迭代器"""
    print("\n" + "=" * 50)
    print("🤔 何时使用生成器 vs 迭代器")
    print("=" * 50)
    
    print("✅ 使用生成器的场景:")
    print("  1. 简单的数据转换和过滤")
    print("  2. 一次性遍历的数据序列")
    print("  3. 内存敏感的大数据处理")
    print("  4. 函数式编程风格")
    print("  5. 快速原型开发")
    
    print("\n✅ 使用传统迭代器的场景:")
    print("  1. 需要复杂状态管理")
    print("  2. 需要重置和重用迭代器")
    print("  3. 需要多种遍历方式")
    print("  4. 面向对象设计")
    print("  5. 需要额外的方法和属性")
    
    print("\n📊 特性对比:")
    comparison_table = [
        ["特性", "生成器", "传统迭代器"],
        ["代码简洁性", "⭐⭐⭐⭐⭐", "⭐⭐⭐"],
        ["内存效率", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐"],
        ["执行性能", "⭐⭐⭐⭐", "⭐⭐⭐⭐"],
        ["状态管理", "⭐⭐", "⭐⭐⭐⭐⭐"],
        ["可重用性", "⭐⭐", "⭐⭐⭐⭐⭐"],
        ["灵活性", "⭐⭐⭐", "⭐⭐⭐⭐⭐"],
    ]
    
    for row in comparison_table:
        print(f"  {row[0]:<12} | {row[1]:<15} | {row[2]}")


if __name__ == "__main__":
    print("🎯 生成器与迭代器对比演示")
    
    # 运行所有演示
    demo_basic_comparison()
    demo_syntax_comparison()
    demo_performance_comparison()
    demo_memory_comparison()
    demo_lazy_evaluation()
    demo_generator_expressions()
    demo_when_to_use()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 在大多数情况下，生成器是更好的选择")
    print("=" * 50)
