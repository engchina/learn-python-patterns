#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据处理中的迭代器应用

本模块演示了迭代器在实际数据处理中的应用，包括：
1. 文件行迭代器 - 内存友好的大文件处理
2. CSV数据迭代器 - 结构化数据的逐行处理
3. 分页数据迭代器 - 模拟API分页数据获取
4. 数据库结果集迭代器 - 模拟数据库查询结果

作者: Assistant
日期: 2024-01-20
"""

import csv
import io
import json
import time
from typing import Dict, List, Any, Optional, Iterator
from contextlib import contextmanager


class FileLineIterator:
    """文件行迭代器 - 逐行读取大文件"""
    
    def __init__(self, filename: str, encoding: str = 'utf-8'):
        self.filename = filename
        self.encoding = encoding
        self.file = None
        self.line_count = 0
    
    def __iter__(self) -> 'FileLineIterator':
        """打开文件并返回自身"""
        try:
            self.file = open(self.filename, 'r', encoding=self.encoding)
            self.line_count = 0
            return self
        except FileNotFoundError:
            print(f"❌ 文件不存在: {self.filename}")
            raise
        except Exception as e:
            print(f"❌ 打开文件失败: {e}")
            raise
    
    def __next__(self) -> str:
        """返回下一行"""
        if self.file is None:
            raise StopIteration
        
        line = self.file.readline()
        if line:
            self.line_count += 1
            return line.rstrip('\n\r')
        else:
            self.close()
            raise StopIteration
    
    def close(self) -> None:
        """关闭文件"""
        if self.file:
            self.file.close()
            self.file = None
            print(f"📁 文件已关闭，共读取 {self.line_count} 行")
    
    def __enter__(self):
        """上下文管理器支持"""
        return self.__iter__()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器支持"""
        self.close()


class CSVDataIterator:
    """CSV数据迭代器 - 逐行解析CSV数据"""
    
    def __init__(self, csv_content: str, has_header: bool = True):
        self.csv_content = csv_content
        self.has_header = has_header
        self.reader = None
        self.headers = None
        self.row_count = 0
    
    def __iter__(self) -> 'CSVDataIterator':
        """初始化CSV读取器"""
        csv_file = io.StringIO(self.csv_content)
        self.reader = csv.reader(csv_file)
        self.row_count = 0
        
        # 如果有标题行，先读取标题
        if self.has_header:
            try:
                self.headers = next(self.reader)
                print(f"📋 CSV标题: {self.headers}")
            except StopIteration:
                self.headers = None
        
        return self
    
    def __next__(self) -> Dict[str, str]:
        """返回下一行数据"""
        if self.reader is None:
            raise StopIteration
        
        try:
            row = next(self.reader)
            self.row_count += 1
            
            # 如果有标题，返回字典；否则返回列表
            if self.headers:
                return dict(zip(self.headers, row))
            else:
                return {f"column_{i}": value for i, value in enumerate(row)}
        except StopIteration:
            print(f"📊 CSV处理完成，共处理 {self.row_count} 行数据")
            raise


class PaginatedDataIterator:
    """分页数据迭代器 - 模拟API分页数据获取"""
    
    def __init__(self, total_items: int, page_size: int = 10):
        self.total_items = total_items
        self.page_size = page_size
        self.current_page = 0
        self.current_item = 0
    
    def __iter__(self) -> 'PaginatedDataIterator':
        """重置迭代器状态"""
        self.current_page = 0
        self.current_item = 0
        return self
    
    def __next__(self) -> Dict[str, Any]:
        """返回下一个数据项"""
        if self.current_item >= self.total_items:
            print(f"📄 分页数据获取完成，共 {self.current_page} 页")
            raise StopIteration
        
        # 模拟分页加载
        if self.current_item % self.page_size == 0:
            self.current_page += 1
            print(f"🔄 正在加载第 {self.current_page} 页...")
            time.sleep(0.1)  # 模拟网络延迟
        
        # 生成模拟数据
        item = {
            'id': self.current_item + 1,
            'name': f'用户_{self.current_item + 1}',
            'email': f'user{self.current_item + 1}@example.com',
            'page': self.current_page
        }
        
        self.current_item += 1
        return item


class DatabaseResultIterator:
    """数据库结果集迭代器 - 模拟数据库查询结果"""
    
    def __init__(self, query: str, batch_size: int = 100):
        self.query = query
        self.batch_size = batch_size
        self.current_batch = 0
        self.batch_data = []
        self.batch_index = 0
        self.total_fetched = 0
        
        # 模拟数据库连接
        self.connection = self._mock_database_connection()
    
    def _mock_database_connection(self) -> Dict[str, Any]:
        """模拟数据库连接"""
        return {
            'connected': True,
            'total_records': 250,  # 模拟总记录数
            'fetched': 0
        }
    
    def _fetch_batch(self) -> List[Dict[str, Any]]:
        """获取一批数据"""
        if not self.connection['connected']:
            return []
        
        start_id = self.connection['fetched'] + 1
        remaining = self.connection['total_records'] - self.connection['fetched']
        batch_size = min(self.batch_size, remaining)
        
        if batch_size <= 0:
            return []
        
        # 模拟数据库查询延迟
        time.sleep(0.05)
        
        batch = []
        for i in range(batch_size):
            record_id = start_id + i
            batch.append({
                'id': record_id,
                'name': f'记录_{record_id}',
                'value': record_id * 10,
                'category': f'类别_{record_id % 5}'
            })
        
        self.connection['fetched'] += batch_size
        self.current_batch += 1
        print(f"🗄️ 获取第 {self.current_batch} 批数据，{batch_size} 条记录")
        
        return batch
    
    def __iter__(self) -> 'DatabaseResultIterator':
        """重置迭代器状态"""
        self.current_batch = 0
        self.batch_data = []
        self.batch_index = 0
        self.total_fetched = 0
        self.connection['fetched'] = 0
        return self
    
    def __next__(self) -> Dict[str, Any]:
        """返回下一条记录"""
        # 如果当前批次数据已用完，获取下一批
        if self.batch_index >= len(self.batch_data):
            self.batch_data = self._fetch_batch()
            self.batch_index = 0
            
            if not self.batch_data:
                print(f"📊 数据库查询完成，共获取 {self.total_fetched} 条记录")
                raise StopIteration
        
        # 返回当前记录
        record = self.batch_data[self.batch_index]
        self.batch_index += 1
        self.total_fetched += 1
        
        return record
    
    def close(self) -> None:
        """关闭数据库连接"""
        self.connection['connected'] = False
        print("🔌 数据库连接已关闭")


def create_sample_file():
    """创建示例文件用于演示"""
    sample_content = """这是第一行文本
这是第二行文本
这是第三行文本
包含中文的第四行
最后一行文本"""
    
    with open('23. Iterator/sample.txt', 'w', encoding='utf-8') as f:
        f.write(sample_content)
    print("📝 已创建示例文件: sample.txt")


def demo_file_iterator():
    """演示文件行迭代器"""
    print("=" * 50)
    print("📁 文件行迭代器演示")
    print("=" * 50)
    
    # 创建示例文件
    create_sample_file()
    
    # 使用上下文管理器
    print("\n使用上下文管理器读取文件:")
    try:
        with FileLineIterator('23. Iterator/sample.txt') as file_iter:
            for line_num, line in enumerate(file_iter, 1):
                print(f"  第{line_num}行: {line}")
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
    
    # 手动管理文件
    print("\n手动管理文件读取:")
    file_iter = FileLineIterator('23. Iterator/sample.txt')
    try:
        for line in file_iter:
            print(f"  内容: {line}")
    except Exception as e:
        print(f"❌ 读取失败: {e}")


def demo_csv_iterator():
    """演示CSV数据迭代器"""
    print("\n" + "=" * 50)
    print("📊 CSV数据迭代器演示")
    print("=" * 50)
    
    # 创建示例CSV数据
    csv_data = """姓名,年龄,城市,职业
张三,25,北京,工程师
李四,30,上海,设计师
王五,28,广州,产品经理
赵六,35,深圳,架构师
钱七,22,杭州,前端开发"""
    
    print("CSV数据预览:")
    print(csv_data[:100] + "...")
    
    print("\n逐行处理CSV数据:")
    csv_iter = CSVDataIterator(csv_data)
    for row_num, row_data in enumerate(csv_iter, 1):
        print(f"  第{row_num}行: {row_data}")


def demo_paginated_iterator():
    """演示分页数据迭代器"""
    print("\n" + "=" * 50)
    print("📄 分页数据迭代器演示")
    print("=" * 50)
    
    # 创建分页迭代器
    paginated_data = PaginatedDataIterator(total_items=25, page_size=8)
    
    print("模拟分页API数据获取:")
    for item in paginated_data:
        print(f"  {item}")
        
        # 只显示前几条，避免输出过多
        if item['id'] >= 15:
            print("  ... (省略剩余数据)")
            break


def demo_database_iterator():
    """演示数据库结果集迭代器"""
    print("\n" + "=" * 50)
    print("🗄️ 数据库结果集迭代器演示")
    print("=" * 50)
    
    # 创建数据库迭代器
    db_iter = DatabaseResultIterator("SELECT * FROM users", batch_size=20)
    
    print("模拟数据库查询结果:")
    count = 0
    for record in db_iter:
        count += 1
        print(f"  {record}")
        
        # 只显示前几条记录
        if count >= 10:
            print("  ... (省略剩余记录)")
            break
    
    db_iter.close()


if __name__ == "__main__":
    print("🎯 数据处理迭代器演示")
    
    # 运行所有演示
    demo_file_iterator()
    demo_csv_iterator()
    demo_paginated_iterator()
    demo_database_iterator()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("💡 提示: 这些迭代器都采用惰性求值，内存使用效率很高")
    print("=" * 50)
