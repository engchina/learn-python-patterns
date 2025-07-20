#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
过滤和转换迭代器

本模块演示了迭代器的过滤和转换功能，包括：
1. 条件过滤迭代器 - 根据条件筛选数据
2. 数据转换迭代器 - 对数据进行转换处理
3. 链式操作迭代器 - 多个迭代器的组合使用
4. 管道式数据处理 - 函数式编程风格

作者: Assistant
日期: 2024-01-20
"""

from typing import Any, Callable, Iterator, Iterable, TypeVar, Generic
from functools import reduce
import re

T = TypeVar('T')
U = TypeVar('U')


class FilterIterator(Generic[T]):
    """条件过滤迭代器"""
    
    def __init__(self, iterable: Iterable[T], predicate: Callable[[T], bool]):
        self.iterator = iter(iterable)
        self.predicate = predicate
        self.filtered_count = 0
        self.total_count = 0
    
    def __iter__(self) -> 'FilterIterator[T]':
        return self
    
    def __next__(self) -> T:
        while True:
            try:
                item = next(self.iterator)
                self.total_count += 1
                
                if self.predicate(item):
                    self.filtered_count += 1
                    return item
                # 如果不满足条件，继续下一个
            except StopIteration:
                print(f"🔍 过滤完成: {self.filtered_count}/{self.total_count} 项通过过滤")
                raise
    
    def get_stats(self) -> dict:
        """获取过滤统计信息"""
        return {
            'filtered': self.filtered_count,
            'total': self.total_count,
            'filter_rate': self.filtered_count / self.total_count if self.total_count > 0 else 0
        }


class TransformIterator(Generic[T, U]):
    """数据转换迭代器"""
    
    def __init__(self, iterable: Iterable[T], transform_func: Callable[[T], U]):
        self.iterator = iter(iterable)
        self.transform_func = transform_func
        self.transform_count = 0
    
    def __iter__(self) -> 'TransformIterator[T, U]':
        return self
    
    def __next__(self) -> U:
        try:
            item = next(self.iterator)
            self.transform_count += 1
            transformed = self.transform_func(item)
            return transformed
        except StopIteration:
            print(f"🔄 转换完成: 共转换 {self.transform_count} 项")
            raise


class ChainIterator:
    """链式迭代器 - 连接多个迭代器"""
    
    def __init__(self, *iterables):
        self.iterables = iterables
        self.current_iterator = None
        self.iterator_index = 0
        self.total_items = 0
    
    def __iter__(self) -> 'ChainIterator':
        self.iterator_index = 0
        self.total_items = 0
        if self.iterables:
            self.current_iterator = iter(self.iterables[0])
        return self
    
    def __next__(self) -> Any:
        while self.iterator_index < len(self.iterables):
            try:
                if self.current_iterator is None:
                    self.current_iterator = iter(self.iterables[self.iterator_index])
                
                item = next(self.current_iterator)
                self.total_items += 1
                return item
            except StopIteration:
                # 当前迭代器耗尽，切换到下一个
                self.iterator_index += 1
                self.current_iterator = None
        
        print(f"🔗 链式迭代完成: 共处理 {self.total_items} 项")
        raise StopIteration


class BatchIterator(Generic[T]):
    """批处理迭代器 - 将数据分批处理"""
    
    def __init__(self, iterable: Iterable[T], batch_size: int):
        self.iterator = iter(iterable)
        self.batch_size = batch_size
        self.batch_count = 0
    
    def __iter__(self) -> 'BatchIterator[T]':
        return self
    
    def __next__(self) -> list[T]:
        batch = []
        try:
            for _ in range(self.batch_size):
                item = next(self.iterator)
                batch.append(item)
        except StopIteration:
            if batch:
                self.batch_count += 1
                print(f"📦 最后一批: {len(batch)} 项 (第{self.batch_count}批)")
                return batch
            else:
                print(f"📦 批处理完成: 共 {self.batch_count} 批")
                raise
        
        self.batch_count += 1
        return batch


class DataPipeline:
    """数据处理管道 - 组合多种操作"""
    
    def __init__(self, data: Iterable[Any]):
        self.data = data
        self.operations = []
    
    def filter(self, predicate: Callable[[Any], bool]) -> 'DataPipeline':
        """添加过滤操作"""
        self.operations.append(('filter', predicate))
        return self
    
    def map(self, transform_func: Callable[[Any], Any]) -> 'DataPipeline':
        """添加转换操作"""
        self.operations.append(('map', transform_func))
        return self
    
    def batch(self, size: int) -> 'DataPipeline':
        """添加批处理操作"""
        self.operations.append(('batch', size))
        return self
    
    def execute(self) -> Iterator[Any]:
        """执行管道操作"""
        result = iter(self.data)
        
        for operation, param in self.operations:
            if operation == 'filter':
                result = FilterIterator(result, param)
            elif operation == 'map':
                result = TransformIterator(result, param)
            elif operation == 'batch':
                result = BatchIterator(result, param)
        
        return result


class TextProcessor:
    """文本处理器 - 演示复杂的过滤和转换"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """清理文本"""
        # 移除多余空格和换行
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    @staticmethod
    def extract_words(text: str) -> list[str]:
        """提取单词"""
        return re.findall(r'\b\w+\b', text.lower())
    
    @staticmethod
    def is_valid_word(word: str) -> bool:
        """判断是否为有效单词"""
        return len(word) >= 2 and word.isalpha()
    
    @staticmethod
    def word_length_category(word: str) -> str:
        """单词长度分类"""
        length = len(word)
        if length <= 3:
            return "短词"
        elif length <= 6:
            return "中词"
        else:
            return "长词"


def demo_filter_iterator():
    """演示过滤迭代器"""
    print("=" * 50)
    print("🔍 过滤迭代器演示")
    print("=" * 50)
    
    # 数字过滤示例
    numbers = range(1, 21)
    print(f"原始数据: {list(numbers)}")
    
    # 过滤偶数
    even_filter = FilterIterator(numbers, lambda x: x % 2 == 0)
    even_numbers = list(even_filter)
    print(f"偶数: {even_numbers}")
    print(f"过滤统计: {even_filter.get_stats()}")
    
    # 过滤质数
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    prime_filter = FilterIterator(range(1, 21), is_prime)
    prime_numbers = list(prime_filter)
    print(f"质数: {prime_numbers}")
    print(f"过滤统计: {prime_filter.get_stats()}")


def demo_transform_iterator():
    """演示转换迭代器"""
    print("\n" + "=" * 50)
    print("🔄 转换迭代器演示")
    print("=" * 50)
    
    # 数字转换示例
    numbers = [1, 2, 3, 4, 5]
    print(f"原始数据: {numbers}")
    
    # 平方转换
    square_transform = TransformIterator(numbers, lambda x: x ** 2)
    squares = list(square_transform)
    print(f"平方: {squares}")
    
    # 字符串转换
    words = ["hello", "world", "python", "iterator"]
    print(f"\n原始单词: {words}")
    
    # 转换为大写并添加长度信息
    word_transform = TransformIterator(
        words, 
        lambda w: f"{w.upper()}({len(w)})"
    )
    transformed_words = list(word_transform)
    print(f"转换后: {transformed_words}")


def demo_chain_iterator():
    """演示链式迭代器"""
    print("\n" + "=" * 50)
    print("🔗 链式迭代器演示")
    print("=" * 50)
    
    # 连接多个数据源
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    list3 = [10, 20, 30]
    
    print(f"列表1: {list1}")
    print(f"列表2: {list2}")
    print(f"列表3: {list3}")
    
    # 链式连接
    chain_iter = ChainIterator(list1, list2, list3)
    chained_data = list(chain_iter)
    print(f"链式结果: {chained_data}")


def demo_batch_iterator():
    """演示批处理迭代器"""
    print("\n" + "=" * 50)
    print("📦 批处理迭代器演示")
    print("=" * 50)
    
    # 大数据集分批处理
    large_dataset = range(1, 26)  # 1到25
    print(f"数据集大小: {len(list(large_dataset))}")
    
    # 分批处理，每批5个
    batch_iter = BatchIterator(large_dataset, batch_size=5)
    
    print("分批处理结果:")
    for batch_num, batch in enumerate(batch_iter, 1):
        print(f"  第{batch_num}批: {batch}")


def demo_data_pipeline():
    """演示数据处理管道"""
    print("\n" + "=" * 50)
    print("🚰 数据处理管道演示")
    print("=" * 50)
    
    # 原始数据
    data = range(1, 21)
    print(f"原始数据: {list(data)}")
    
    # 构建处理管道
    pipeline = (DataPipeline(data)
                .filter(lambda x: x % 2 == 0)  # 过滤偶数
                .map(lambda x: x ** 2)          # 平方
                .batch(3))                      # 分批，每批3个
    
    print("管道处理结果:")
    for batch in pipeline.execute():
        print(f"  批次: {batch}")


def demo_text_processing():
    """演示文本处理"""
    print("\n" + "=" * 50)
    print("📝 文本处理演示")
    print("=" * 50)
    
    # 示例文本
    texts = [
        "Hello World! This is a sample text.",
        "Python is great for data processing.",
        "Iterator pattern provides efficient data traversal.",
        "   Extra   spaces   should   be   cleaned   ",
        "Short words: a, I, to, be, or, not"
    ]
    
    print("原始文本:")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text}")
    
    # 文本清理管道
    processor = TextProcessor()
    
    # 清理文本
    cleaned_texts = list(TransformIterator(texts, processor.clean_text))
    print("\n清理后的文本:")
    for i, text in enumerate(cleaned_texts, 1):
        print(f"  {i}. {text}")
    
    # 提取所有单词
    all_words = []
    for text in cleaned_texts:
        all_words.extend(processor.extract_words(text))
    
    print(f"\n提取的所有单词 ({len(all_words)} 个):")
    print(f"  {all_words}")
    
    # 过滤有效单词
    valid_words = list(FilterIterator(all_words, processor.is_valid_word))
    print(f"\n有效单词 ({len(valid_words)} 个):")
    print(f"  {valid_words}")
    
    # 单词分类
    word_categories = list(TransformIterator(
        valid_words, 
        lambda w: f"{w}({processor.word_length_category(w)})"
    ))
    print(f"\n单词分类:")
    print(f"  {word_categories}")


if __name__ == "__main__":
    print("🎯 过滤和转换迭代器演示")
    
    # 运行所有演示
    demo_filter_iterator()
    demo_transform_iterator()
    demo_chain_iterator()
    demo_batch_iterator()
    demo_data_pipeline()
    demo_text_processing()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 这些迭代器可以组合使用，构建强大的数据处理管道")
    print("=" * 50)
