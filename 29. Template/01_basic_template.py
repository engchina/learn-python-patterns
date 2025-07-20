"""
01_basic_template.py - 模板方法模式基础实现

这个示例展示了模板方法模式的核心概念：
- 在抽象类中定义算法的骨架
- 将具体步骤的实现延迟到子类
- 使用钩子方法提供可选的扩展点
"""

from abc import ABC, abstractmethod
import time


# ==================== 抽象模板类 ====================
class DataProcessor(ABC):
    """数据处理模板类
    
    定义了数据处理的标准流程：
    1. 验证数据
    2. 预处理数据  
    3. 核心处理
    4. 后处理（可选）
    5. 保存结果
    """
    
    def process(self, data):
        """模板方法 - 定义数据处理的完整流程"""
        print(f"开始处理数据: {type(self).__name__}")
        print("-" * 50)
        
        # 1. 验证数据
        print("步骤1: 验证数据")
        if not self.validate_data(data):
            print("❌ 数据验证失败")
            return None
        print("✅ 数据验证通过")
        
        # 2. 预处理数据
        print("\n步骤2: 预处理数据")
        processed_data = self.preprocess_data(data)
        print(f"预处理完成，数据量: {len(processed_data) if hasattr(processed_data, '__len__') else '未知'}")
        
        # 3. 核心处理逻辑
        print("\n步骤3: 核心处理")
        result = self.process_core(processed_data)
        print(f"核心处理完成，结果: {result}")
        
        # 4. 后处理（可选）
        if self.should_postprocess():
            print("\n步骤4: 后处理数据")
            result = self.postprocess_data(result)
            print(f"后处理完成，最终结果: {result}")
        else:
            print("\n步骤4: 跳过后处理")
            
        # 5. 保存结果
        print("\n步骤5: 保存结果")
        self.save_result(result)
        
        print("-" * 50)
        print("✅ 数据处理完成\n")
        return result
    
    # 抽象方法 - 子类必须实现
    @abstractmethod
    def validate_data(self, data) -> bool:
        """验证数据 - 子类必须实现"""
        pass
    
    @abstractmethod
    def process_core(self, data):
        """核心处理逻辑 - 子类必须实现"""
        pass
    
    # 具体方法 - 提供默认实现
    def preprocess_data(self, data):
        """预处理数据 - 默认实现"""
        print("执行默认预处理...")
        return data
    
    def postprocess_data(self, data):
        """后处理数据 - 默认实现"""
        print("执行默认后处理...")
        return data
    
    def save_result(self, result):
        """保存结果 - 默认实现"""
        print(f"保存结果到默认位置: {result}")
    
    # 钩子方法 - 子类可选择重写
    def should_postprocess(self) -> bool:
        """是否需要后处理 - 钩子方法"""
        return True


# ==================== 具体实现类 ====================
class NumberProcessor(DataProcessor):
    """数字处理器 - 计算数字列表的统计信息"""
    
    def validate_data(self, data) -> bool:
        """验证数据是否为数字列表"""
        if not isinstance(data, (list, tuple)):
            print("数据必须是列表或元组")
            return False
        
        if not data:
            print("数据不能为空")
            return False
            
        if not all(isinstance(x, (int, float)) for x in data):
            print("所有元素必须是数字")
            return False
            
        return True
    
    def preprocess_data(self, data):
        """预处理：过滤掉负数"""
        print("过滤负数...")
        filtered_data = [x for x in data if x >= 0]
        print(f"过滤前: {len(data)} 个数字，过滤后: {len(filtered_data)} 个数字")
        return filtered_data
    
    def process_core(self, data):
        """核心处理：计算平均值"""
        if not data:
            return 0
        average = sum(data) / len(data)
        print(f"计算 {len(data)} 个数字的平均值")
        return round(average, 2)
    
    def should_postprocess(self) -> bool:
        """数字处理不需要后处理"""
        return False


class TextProcessor(DataProcessor):
    """文本处理器 - 处理文本列表"""
    
    def validate_data(self, data) -> bool:
        """验证数据是否为字符串列表"""
        if not isinstance(data, (list, tuple)):
            print("数据必须是列表或元组")
            return False
            
        if not all(isinstance(x, str) for x in data):
            print("所有元素必须是字符串")
            return False
            
        return True
    
    def preprocess_data(self, data):
        """预处理：去除空字符串和前后空格"""
        print("清理文本数据...")
        cleaned_data = [text.strip() for text in data if text.strip()]
        print(f"清理前: {len(data)} 个文本，清理后: {len(cleaned_data)} 个文本")
        return cleaned_data
    
    def process_core(self, data):
        """核心处理：统计词频"""
        word_count = {}
        total_words = 0
        
        for text in data:
            words = text.lower().split()
            total_words += len(words)
            for word in words:
                word_count[word] = word_count.get(word, 0) + 1
        
        print(f"处理了 {len(data)} 个文本，总共 {total_words} 个单词")
        return word_count
    
    def postprocess_data(self, data):
        """后处理：只保留出现次数大于1的词"""
        print("过滤低频词...")
        filtered_words = {word: count for word, count in data.items() if count > 1}
        print(f"过滤前: {len(data)} 个词，过滤后: {len(filtered_words)} 个词")
        return filtered_words
    
    def save_result(self, result):
        """保存到文本文件"""
        print("保存词频统计到 word_frequency.txt")
        # 这里只是模拟保存过程
        print(f"前5个高频词: {dict(list(sorted(result.items(), key=lambda x: x[1], reverse=True))[:5])}")


class FileProcessor(DataProcessor):
    """文件处理器 - 处理文件路径列表"""
    
    def __init__(self):
        self.processed_files = []
    
    def validate_data(self, data) -> bool:
        """验证数据是否为文件路径列表"""
        if not isinstance(data, (list, tuple)):
            print("数据必须是列表或元组")
            return False
            
        if not all(isinstance(x, str) for x in data):
            print("所有元素必须是字符串（文件路径）")
            return False
            
        return True
    
    def preprocess_data(self, data):
        """预处理：过滤有效的文件扩展名"""
        print("过滤有效文件...")
        valid_extensions = ['.txt', '.py', '.md', '.json']
        valid_files = []
        
        for file_path in data:
            if any(file_path.endswith(ext) for ext in valid_extensions):
                valid_files.append(file_path)
        
        print(f"过滤前: {len(data)} 个文件，过滤后: {len(valid_files)} 个有效文件")
        return valid_files
    
    def process_core(self, data):
        """核心处理：统计文件信息"""
        file_stats = {
            'total_files': len(data),
            'file_types': {},
            'processed_files': []
        }
        
        for file_path in data:
            # 模拟文件处理
            extension = file_path.split('.')[-1] if '.' in file_path else 'unknown'
            file_stats['file_types'][extension] = file_stats['file_types'].get(extension, 0) + 1
            file_stats['processed_files'].append(file_path)
            
        print(f"处理了 {len(data)} 个文件")
        return file_stats
    
    def postprocess_data(self, data):
        """后处理：生成处理报告"""
        print("生成处理报告...")
        report = {
            'summary': f"总共处理了 {data['total_files']} 个文件",
            'file_types': data['file_types'],
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return report
    
    def save_result(self, result):
        """保存处理报告"""
        print("保存处理报告到 file_report.json")
        print(f"报告摘要: {result['summary']}")
        print(f"文件类型分布: {result['file_types']}")


# ==================== 演示函数 ====================
def demo_basic_template():
    """基础模板方法演示"""
    print("=" * 60)
    print("模板方法模式基础演示")
    print("=" * 60)
    
    # 测试数据
    number_data = [1, 2, -3, 4, 5, -6, 7, 8, 9, 10]
    text_data = ["hello world", "python programming", "template method", "design pattern", "hello python"]
    file_data = ["document.txt", "script.py", "readme.md", "data.json", "image.jpg", "config.xml"]
    
    # 创建处理器实例
    processors = [
        ("数字处理器", NumberProcessor(), number_data),
        ("文本处理器", TextProcessor(), text_data),
        ("文件处理器", FileProcessor(), file_data)
    ]
    
    # 执行处理
    for name, processor, data in processors:
        print(f"\n{'='*20} {name} {'='*20}")
        print(f"输入数据: {data}")
        result = processor.process(data)
        print(f"处理结果: {result}")
        time.sleep(1)  # 模拟处理时间


if __name__ == "__main__":
    demo_basic_template()
