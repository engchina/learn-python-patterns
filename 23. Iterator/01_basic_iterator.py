#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
迭代器模式基础实现

本模块演示了迭代器模式的基本概念和实现方式，包括：
1. 自定义集合类和迭代器
2. Python迭代器协议的实现
3. 迭代器与可迭代对象的区别
4. 基本的遍历操作

作者: Assistant
日期: 2024-01-20
"""

from abc import ABC, abstractmethod
from typing import Any, Iterator, List


class BookCollection:
    """图书集合类 - 可迭代对象"""
    
    def __init__(self):
        self._books: List[str] = []
    
    def add_book(self, book: str) -> None:
        """添加图书"""
        self._books.append(book)
        print(f"📚 已添加图书: {book}")
    
    def remove_book(self, book: str) -> bool:
        """移除图书"""
        if book in self._books:
            self._books.remove(book)
            print(f"🗑️ 已移除图书: {book}")
            return True
        return False
    
    def get_count(self) -> int:
        """获取图书数量"""
        return len(self._books)
    
    def __iter__(self) -> 'BookIterator':
        """返回迭代器"""
        return BookIterator(self._books)
    
    def reverse_iterator(self) -> 'ReverseBookIterator':
        """返回反向迭代器"""
        return ReverseBookIterator(self._books)


class BookIterator:
    """图书迭代器 - 正向遍历"""
    
    def __init__(self, books: List[str]):
        self._books = books
        self._index = 0
    
    def __iter__(self) -> 'BookIterator':
        """返回自身"""
        return self
    
    def __next__(self) -> str:
        """返回下一个元素"""
        if self._index < len(self._books):
            book = self._books[self._index]
            self._index += 1
            return book
        else:
            raise StopIteration


class ReverseBookIterator:
    """反向图书迭代器"""
    
    def __init__(self, books: List[str]):
        self._books = books
        self._index = len(books) - 1
    
    def __iter__(self) -> 'ReverseBookIterator':
        return self
    
    def __next__(self) -> str:
        if self._index >= 0:
            book = self._books[self._index]
            self._index -= 1
            return book
        else:
            raise StopIteration


class NumberRange:
    """数字范围类 - 演示可重复迭代"""
    
    def __init__(self, start: int, end: int, step: int = 1):
        self.start = start
        self.end = end
        self.step = step
    
    def __iter__(self) -> 'NumberRangeIterator':
        """每次调用都返回新的迭代器实例"""
        return NumberRangeIterator(self.start, self.end, self.step)


class NumberRangeIterator:
    """数字范围迭代器"""
    
    def __init__(self, start: int, end: int, step: int):
        self.current = start
        self.end = end
        self.step = step
    
    def __iter__(self) -> 'NumberRangeIterator':
        return self
    
    def __next__(self) -> int:
        if self.current < self.end:
            value = self.current
            self.current += self.step
            return value
        else:
            raise StopIteration


class FibonacciIterator:
    """斐波那契数列迭代器 - 演示无限序列"""
    
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
        print("🔄 斐波那契迭代器已重置")


def demo_book_collection():
    """演示图书集合的迭代"""
    print("=" * 50)
    print("📖 图书集合迭代演示")
    print("=" * 50)
    
    # 创建图书集合
    library = BookCollection()
    library.add_book("Python编程从入门到实践")
    library.add_book("设计模式：可复用面向对象软件的基础")
    library.add_book("代码大全")
    library.add_book("重构：改善既有代码的设计")
    
    print(f"\n📊 图书总数: {library.get_count()}")
    
    # 正向遍历
    print("\n🔄 正向遍历:")
    for i, book in enumerate(library, 1):
        print(f"  {i}. {book}")
    
    # 反向遍历
    print("\n🔄 反向遍历:")
    for i, book in enumerate(library.reverse_iterator(), 1):
        print(f"  {i}. {book}")
    
    # 演示迭代器的一次性特性
    print("\n🔍 演示迭代器的一次性特性:")
    iterator = iter(library)
    print("第一次遍历:")
    for book in iterator:
        print(f"  - {book}")
        break  # 只取第一个
    
    print("继续遍历同一个迭代器:")
    for book in iterator:
        print(f"  - {book}")


def demo_number_range():
    """演示数字范围迭代"""
    print("\n" + "=" * 50)
    print("🔢 数字范围迭代演示")
    print("=" * 50)
    
    # 创建数字范围
    numbers = NumberRange(1, 10, 2)
    
    print("第一次遍历:")
    for num in numbers:
        print(f"  {num}", end=" ")
    print()
    
    print("第二次遍历 (可重复):")
    for num in numbers:
        print(f"  {num}", end=" ")
    print()
    
    # 手动使用迭代器
    print("\n手动迭代:")
    iterator = iter(numbers)
    try:
        while True:
            value = next(iterator)
            print(f"  下一个值: {value}")
    except StopIteration:
        print("  ✅ 迭代完成")


def demo_fibonacci():
    """演示斐波那契迭代器"""
    print("\n" + "=" * 50)
    print("🌀 斐波那契数列迭代演示")
    print("=" * 50)
    
    # 有限斐波那契数列
    print("前10个斐波那契数:")
    fib = FibonacciIterator(10)
    for num in fib:
        print(f"  {num}", end=" ")
    print()
    
    # 重置并再次使用
    fib.reset()
    print("\n重置后前5个数:")
    for i, num in enumerate(fib):
        if i >= 5:
            break
        print(f"  {num}", end=" ")
    print()
    
    # 无限斐波那契数列（手动控制）
    print("\n无限斐波那契数列（前15个）:")
    infinite_fib = FibonacciIterator()
    for i, num in enumerate(infinite_fib):
        if i >= 15:
            break
        print(f"  {num}", end=" ")
    print()


def demo_iterator_protocol():
    """演示迭代器协议的细节"""
    print("\n" + "=" * 50)
    print("🔧 迭代器协议演示")
    print("=" * 50)
    
    # 创建一个简单列表
    data = [1, 2, 3, 4, 5]
    
    print("原始数据:", data)
    
    # 获取迭代器
    iterator = iter(data)
    print(f"迭代器类型: {type(iterator)}")
    print(f"迭代器是否等于自身: {iterator is iter(iterator)}")
    
    # 手动迭代
    print("\n手动迭代过程:")
    try:
        while True:
            value = next(iterator)
            print(f"  获取到值: {value}")
    except StopIteration:
        print("  ✅ 迭代器耗尽")
    
    # 尝试再次迭代已耗尽的迭代器
    print("\n尝试再次迭代已耗尽的迭代器:")
    try:
        value = next(iterator)
        print(f"  获取到值: {value}")
    except StopIteration:
        print("  ❌ 迭代器已耗尽，无法获取更多值")


if __name__ == "__main__":
    print("🎯 迭代器模式基础实现演示")
    
    # 运行所有演示
    demo_book_collection()
    demo_number_range()
    demo_fibonacci()
    demo_iterator_protocol()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("=" * 50)
